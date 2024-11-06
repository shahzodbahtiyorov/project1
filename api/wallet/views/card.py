import uuidfrom amqp.spec import methodfrom drf_yasg.utils import swagger_auto_schemafrom rest_framework.decorators import api_view, permission_classesfrom rest_framework.permissions import IsAuthenticatedfrom rest_framework.response import Responsefrom api.wallet.modules.views import card_info_about, card_transfer, card_confirm, card_create, \    card_uzcard, cards_all_balance, card_sms_humo_confirm, epos_add, card_blocked, card_name_updatefrom api.wallet.serializers import (CardDetailsSerializer, OtpCheckSerializer, CardModelSerializer, \                                    CardInfoSerializer, P2PCardSerializer,                                    TransferCofirmeSerializer, HumoInfoSerializer,                                    UzcardInfoSerializer, \                                    CardAboutSerializers, CardToken, CardTransferSerializer,                                    CommissionCardSerializer, CardDeleteSerializers,                                    CardBlockedSerializers, CardNameSerializer)from apps.accounts.models import OtpModelfrom apps.wallet.models import CardModel@swagger_auto_schema(method="post", tags=["card"], request_body=CardDetailsSerializer)@api_view(["POST", ])@permission_classes([IsAuthenticated])def card_add_step_one(request):    data = request.data    serializer = CardDetailsSerializer(data=data)    if serializer.is_valid():        # karta egasi topilsin va unga sms jo'natilsin!        otp_token = str(uuid.uuid4())        otp = 1234        card = CardModel.objects.create(owner=request.user, expire=data["expire"],                                        card_number=data["card_number"])        otp = OtpModel.objects.create(otp=otp, otp_token=otp_token, comment="card_add",                                      user=request.user,                                      object_id=card.id)        return Response({"status": True, "otp_token": otp_token})    return Response(serializer.errors)@swagger_auto_schema(method="post", tags=["card"], request_body=OtpCheckSerializer)@api_view(["POST", ])@permission_classes([IsAuthenticated])def card_add_step_two(request):    data = request.data    serializer = OtpCheckSerializer(data=data)    if serializer.is_valid():        try:            otp = OtpModel.objects.get(otp=data["otp"], otp_token=data["otp_token"],                                       comment="card_add",                                       user=request.user)        except:            return Response({"status": False, "message": "Wrong OTP"})        if not otp.is_active:            return Response({"status": False, "message": "OTP expired"})        card = CardModel.objects.get(pk=otp.object_id)        card.active = True        card.save(update_fields=["active"])        return Response({"status": True})@swagger_auto_schema(method="get", tags=["card"])@api_view(["GET", ])@permission_classes([IsAuthenticated])def get_cards(request):    """get card"""    user = request.user    cards = CardModel.objects.filter(active=True, owner=user)    serializer = CardModelSerializer(cards, many=True)    return Response(serializer.data)@swagger_auto_schema(method="POST", tags=["card"], request_body=CardDeleteSerializers)@api_view(["POST", ])@permission_classes([IsAuthenticated])def delete_card(request):    """Delete a card """    data = request.data    serializer = CardDeleteSerializers(data=request.data)    if serializer.is_valid():        user = request.user        card = CardModel.objects.filter(id=data['card_id'], owner=user).first()        if not card:            return Response({"status": False, "message": "card not found"})        card.delete()        return Response(status=200)    return Response(serializer.errors)###p2p card transfer@swagger_auto_schema(    method="post",    operation_description="Add Cards",    tags=["card"],    request_body=CardDetailsSerializer)@api_view(["POST", ])@permission_classes([IsAuthenticated])def card_create_add(request):    """add cards"""    return card_create(request)@swagger_auto_schema(method="post", tags=["card"], request_body=UzcardInfoSerializer)@api_view(["POST", ])@permission_classes([IsAuthenticated])def card_uzcard_info(request):    return card_uzcard(request)@swagger_auto_schema(method='post', tags=['card'], request_body=HumoInfoSerializer)@api_view(["POST", ])@permission_classes([IsAuthenticated])def card_humo_add(request):    return card_sms_humo_confirm(request)@swagger_auto_schema(method="post", tags=["card"], request_body=CardAboutSerializers)@api_view(["POST", ])@permission_classes([IsAuthenticated])def card_info(request):    """ information about cards """    return card_info_about(request)@swagger_auto_schema(method="post", tags=["card"], request_body=CardTransferSerializer)@api_view(["POST", ])@permission_classes([IsAuthenticated])def card_p2p_transfer(request):    return card_transfer(request)@swagger_auto_schema(method="post", tags=["card"], request_body=P2PCardSerializer)@api_view(["POST", ])@permission_classes([IsAuthenticated])def transfer_otp_confirme(request):    return card_confirm(request)@swagger_auto_schema(method="get", tags=["card"])@api_view(["GET", ])@permission_classes([IsAuthenticated])def cards_user_get(request):    return cards_all_balance(request)@swagger_auto_schema(method='post', tags=["card"], request_body=CommissionCardSerializer)@api_view(["POST", ])@permission_classes([IsAuthenticated])def create_epos(request):    return epos_add(request)@swagger_auto_schema(method='POST', tags=['card'], request_body=CardBlockedSerializers)@api_view(["POST", ])@permission_classes([IsAuthenticated])def cards_blocked(request):    return card_blocked(request)@swagger_auto_schema(    method='POST',    tags=['card'],    request_body=CardNameSerializer)@api_view(["POST", ])@permission_classes([IsAuthenticated])def card_update_name(request):    return card_name_update(request)