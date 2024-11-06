from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from api.wallet.modules.visa import login, card_confirm, card_register, card_bin, card_detail
from api.wallet.serializers import (LoginSerializer, CardRegisterSerializer, CardRegisterConfirmSerializer,
                                    CardBinCheckSerializer, CardTokenSerializer)


@swagger_auto_schema(method='POST', tags=['Visa'],request_body=LoginSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def visa_login(request):
    return login(request)
@swagger_auto_schema(method='POST', tags=['Visa'],request_body=CardRegisterSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def visa_register_card(request):
    return card_register(request)
@swagger_auto_schema(method='POST', tags=['Visa'],request_body=CardRegisterConfirmSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def visa_card_confirm(request):
    return card_confirm(request)
@swagger_auto_schema(method='POST', tags=['Visa'],request_body=CardBinCheckSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def visa_card_bin_check(request):
    return card_bin(request)
@swagger_auto_schema(method="POST", tags=["Visa"],request_body=CardTokenSerializer)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def visa_card_token(request):
    return card_detail(request)

