from django.dispatch import receiver
from rest_framework import status
from rest_framework.response import Response
from apps.wallet.models import ReceiverCardModel
from  services.unigate import  methods as Gwmethod
from services.unigate.message_error import MESSAGE
from api.wallet.serializers.receiver import ReceiverSerializer, ReceiverModelSerializer
from services.unigate.helper import mask_card_number


def create_receiver_card(request):
    data = request.data
    user = request.user
    serializer = ReceiverSerializer(data=data)
    if serializer.is_valid():
        card = ReceiverCardModel.objects.filter(card_number=data['card_number'],owner=user).first()
        if card:
            return Response({"message":MESSAGE['CardAdd']})
        card_info = Gwmethod.card_info(data['card_number'])
        if 'result' in card_info:
            card = ReceiverCardModel.objects.create(
                card_number=card_info['result']['card_number'],
                card_name=card_info['result']['owner'],
                card_mask=mask_card_number(card_info['result']['card_number']),
                pc_type=card_info['result']['pc_type'],
                owner=user,
                type=data['type']
            )
            card.save()
            return Response({"message":MESSAGE['CardAdd']})
        return Response(card_info)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_receiver_card(request):
    data = request.data
    user = request.user
    receiver = ReceiverCardModel.objects.filter(owner=user)
    if not receiver:
        return Response({})
    serializers = ReceiverModelSerializer(receiver, many=True)
    return Response(serializers.data)

