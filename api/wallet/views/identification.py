from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from api.wallet.modules.identification import identification, my_id_user_info, notification
from api.wallet.serializers.identification import IdentificationSerializer


@swagger_auto_schema(method="POST", tags=['Identification'], request_body=IdentificationSerializer)
@api_view(["POST", ])
@permission_classes([IsAuthenticated])
def identification_id(request):
    return identification(request)


@swagger_auto_schema(method="GET", tags=['Identification'])
@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def my_id_info(request):
    return my_id_user_info(request)


@swagger_auto_schema(method="GET", tags=['Identification'])
@api_view(['GET', ])
def user_notification(request):
    return notification(request)
