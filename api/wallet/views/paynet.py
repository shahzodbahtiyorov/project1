import uuid

from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.wallet.modules.paynet_views import categories, providers, services, services_by_category, \
    services_by_search, fetch_and_update_categories, payment_transfers, payment_confirms, \
    services_get_providers, check_receiver
from api.wallet.serializers.paynet import ProvidersSerializer, ServersSerializer, \
    ServerSearchSerializer, CheckReceiverSerializer, PaymentSerializer, PaymentConfirmSerializer

""" Paynet category """


@swagger_auto_schema(method="POST", tags=["Paynet"])
@api_view(["POST", ])
@permission_classes([IsAuthenticated])
def categories_all(request):
    return categories(request)


""" Paynet provider """


@swagger_auto_schema(method="POST", tags=["Paynet"], request_body=ProvidersSerializer)
@api_view(["POST", ])
@permission_classes([IsAuthenticated])
def providers_all(request):
    return providers(request)


"""Paynet services enter the provider id and you can get a list of services """


@swagger_auto_schema(method="POST", tags=["Paynet"], request_body=ServersSerializer)
@api_view(["POST", ])
@permission_classes([IsAuthenticated])
def services_all(request):
    return services(request)


@swagger_auto_schema(method="POST", tags=["Paynet"], request_body=ProvidersSerializer)
@api_view(["POST", ])
@permission_classes([IsAuthenticated])
def service_by_category_filter(request):
    return services_by_category(request)


@swagger_auto_schema(method="POST", tags=["Paynet"], request_body=ServerSearchSerializer)
@api_view(["POST", ])
@permission_classes([IsAuthenticated])
def service_search(request):
    return services_by_search(request)


@swagger_auto_schema(method="POST", tags=["Paynet"], request_body=ServersSerializer)
@api_view(["POST", ])
@permission_classes([IsAuthenticated])
def service_get_providers(request):
    return services_get_providers(request)


@swagger_auto_schema(method="POST", tags=["Paynet"], request_body=CheckReceiverSerializer)
@api_view(["POST", ])
@permission_classes([IsAuthenticated])
def checks_receiver(request):
    return check_receiver(request)


@swagger_auto_schema(method="POST", tags=["Paynet"],request_body=PaymentSerializer)
@api_view(["POST", ])
@permission_classes([IsAuthenticated])
def payment_transfer(request):
    return payment_transfers(request)


@swagger_auto_schema(method="POST", tags=["Paynet"],request_body=PaymentConfirmSerializer)
@api_view(["POST", ])
@permission_classes([IsAuthenticated])
def payment_confirm(request):
    return payment_confirms(request)
