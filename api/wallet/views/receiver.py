from amqp.spec import method
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from api.wallet.modules.receiver import create_receiver_card, get_receiver_card
from api.wallet.serializers import ReceiverSerializer


@swagger_auto_schema(method="POST", tags=["ReceiverCard"],request_body=ReceiverSerializer)
@api_view(["POST", ])
@permission_classes([IsAuthenticated])
def receiver_create(request):
    return create_receiver_card(request)
@swagger_auto_schema(method = "GET",tags=["ReceiverCard"])
@api_view(["GET", ])
@permission_classes([IsAuthenticated])
def get_receiver_cards(request):
    return get_receiver_card(request)