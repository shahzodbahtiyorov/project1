from rest_framework import status
from rest_framework.response import Response
from services.unigate.message_error import MESSAGE
from apps.wallet.models import CardModel
from services.visa import method as VisaMethod
from api.wallet.serializers.visa import LoginSerializer, CardRegisterSerializer, CardRegisterConfirmSerializer, \
    CardBinCheckSerializer, CardTokenSerializer


def login(request):
    data = request.data
    serializers = LoginSerializer(data=data)
    if serializers.is_valid():
        result = VisaMethod.login(username=data['username'], password=data['password'])
        if 'result' in result:
            return Response(result, status=status.HTTP_200_OK)
        return Response(result)

    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


def card_register(request):
    data = request.data
    serializers = CardRegisterSerializer(data=data)
    if serializers.is_valid():

        result = VisaMethod.card_register(number=data['number'], expire=data['expire'])
        if 'result' in result:
           pass

        return Response(result)
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


def card_confirm(request):
    data = request.data
    serializers = CardRegisterConfirmSerializer(data=data)
    if serializers.is_valid():
        result = VisaMethod.card_confirm(ext_id=data['ext_id'], code=data['code'])
        if 'result' in result:
            return Response(result, status=status.HTTP_200_OK)
        return Response(result)
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


def card_bin(request):
    data = request.data
    serializers = CardBinCheckSerializer(data=data)
    if serializers.is_valid():
        result = VisaMethod.card_bins(card_number=data['number'])
        if 'result' in result:
            return Response(result, status=status.HTTP_200_OK)
        return Response(result)
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


def card_detail(request):
    data = request.data
    serializers = CardTokenSerializer(data=data)
    if serializers.is_valid():
        result = VisaMethod.card_details(card_token=data['token'])
        if 'result' in result:
            return Response(result, status=status.HTTP_200_OK)
        return Response(result)
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
