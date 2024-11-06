from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from api.wallet.serializers.monitoring import MonitoringCheckSerializer, TransactionsStateSerializer, \
    TransactionsModelSerializer
from api.wallet.modules.monitoring import card_monitoring, card_monitoring_all, monitoring_check, transfer_check, \
    get_transaction_pdf


@swagger_auto_schema(method='POST', tags=['Monitoring'])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def card_monitor(request):
    return card_monitoring_all(request)


@swagger_auto_schema(method='POST', tags=['Monitoring'])
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def card_all_monitoring(request):
    return card_monitoring(request)
@swagger_auto_schema(method='POST', tags=['Monitoring'],request_body=MonitoringCheckSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_monitoring(request):
    return monitoring_check(request)
@swagger_auto_schema(method='POST', tags=['Monitoring'],request_body=TransactionsStateSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def state_transactions(request):
    return transfer_check(request)
@swagger_auto_schema(method='POST', tags=['Monitoring'],request_body=MonitoringCheckSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer_pdf(request):
    return get_transaction_pdf(request)