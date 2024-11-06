from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from api.wallet.modules.tcb import service_infos, register_card, transfer_receiver_info, transfer_create, \
    transfer_callback, register_card_state, transfer_sender_info, transfer_rf_confirm, transfer_rf_create
from api.wallet.serializers import TransferReceiverInfo, TransferCreateSerializer, ReceiverInfoCard, TransferCreateRF, \
    TransferStateSerializer


"""RF --->UZ"""
@swagger_auto_schema(method='POST', tags=['TCB'])
@api_view(['POST'])
def services_info(request):
    return service_infos(request)


@swagger_auto_schema(method='POST', tags=['TCB'])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cards_register(request):
    return register_card(request)


@swagger_auto_schema(method='POST', tags=['TCB'])
@api_view(['POST'])
def card_state_register(request):
    print({"callback": request.data})
    return register_card_state(request)


@swagger_auto_schema(method='POST', tags=['TCB'], request_body=TransferReceiverInfo)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer_receivers_info(request):
    return transfer_receiver_info(request)


@swagger_auto_schema(method='POST', tags=['TCB'], request_body=TransferCreateSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_transfer(request):
    return transfer_create(request)


@swagger_auto_schema(method='POST', tags=['TCB'])
@api_view(['POST'])
def transfer_tcb_callback(request):
    return transfer_callback(request)
"""UZ --->RF"""

@swagger_auto_schema(method='POST', tags=['TCB-UZ-RF'],request_body=ReceiverInfoCard)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer_rf_sender_check(request):
    return transfer_sender_info(request)
@swagger_auto_schema(method='POST',tags=['TCB-UZ-RF'],request_body=TransferCreateRF)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer_create_rf(request):
    return transfer_rf_create(request)
@swagger_auto_schema(method='POST',tags=['TCB-UZ-RF'],request_body=TransferStateSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer_confirm_rf(request):
    return transfer_rf_confirm(request)