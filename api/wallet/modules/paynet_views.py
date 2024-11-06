import uuid
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from api.wallet.serializers.paynet import ProvidersSerializer, ServersSerializer, \
    ServerSearchSerializer, CategoriesSerializer, ProviderSerializer, CheckReceiverSerializer, \
    PaymentSerializer, PaymentConfirmSerializer
from apps.wallet.models import CardModel, TransactionsModel, Commission
from apps.wallet.models.paynet import Category, Providers
from services.unigate.message_error import MESSAGE
from services.unigate import paynet_methods as Gwmethods
from services.unigate import methods as Gwmethod
from services.unigate.paynet_methods import get_cached_services, \
    get_cached_services_filter_by_category
from services.unigate import card_helper as Gwcard_helper
from django.core.cache import cache


def categories(request):
    """Check if Paynet categories exist in the database, update if not."""

    cache_key = 'paynet_categories'
    cached_categories = cache.get(cache_key)

    if cached_categories:
        return Response({'categories': cached_categories}, status=status.HTTP_200_OK)

    ctg = Category.objects.all()

    if not ctg.exists():

        category_response = Gwmethods.categories()

        if 'result' in category_response and isinstance(category_response['result'], list):
            new_categories = []
            for category in category_response['result']:
                new_categories.append(Category(
                    title_ru=category['title_ru'],
                    title_uz=category['title_uz'],
                    is_subcategory=category['is_subcategory'],
                    category_id=category['id']
                ))

            Category.objects.bulk_create(new_categories)
            ctg = Category.objects.all()

    serializers = CategoriesSerializer(ctg, context={'request': request}, many=True)
    serialized_data = serializers.data

    cache.set(cache_key, serialized_data, timeout=3600)

    return Response({'categories': serialized_data}, status=status.HTTP_200_OK)


def providers(request):
    data = request.data

    serializer = ProvidersSerializer(data=data, context={'request': request})

    if serializer.is_valid():

        cache_key = f'providers_{data["category_id"]}'
        cached_providers = cache.get(cache_key)

        if cached_providers:
            return Response({'providers': cached_providers}, status=status.HTTP_200_OK)

        provider = Providers.objects.filter(category_id=data['category_id'])

        if not provider.exists():

            providers_response = Gwmethods.providers(data['category_id'])

            if 'result' in providers_response and isinstance(providers_response['result'], list):
                new_providers = []
                for provider in providers_response['result']:
                    new_providers.append(Providers(
                        title=provider['title'],
                        title_short=provider['title_short'],
                        provider_id=provider['id'],
                        category_id=data['category_id']
                    ))

                Providers.objects.bulk_create(new_providers)

        providers = Providers.objects.filter(category_id=data['category_id'])
        serializers = ProviderSerializer(providers, context={'request': request}, many=True)
        serialized_data = serializers.data

        cache.set(cache_key, serialized_data, timeout=3600)

        return Response({'providers': serialized_data}, status=status.HTTP_200_OK)

    return Response({'message': "Invalid data", 'errors': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST)


def services(request):
    """Retrieve Paynet services for a provider."""
    data = request.data
    serializers = ServersSerializer(data=data)
    if serializers.is_valid():
        services = get_cached_services(data['provider_id'])
        if services['result']:
            return Response(services['result'])
        return Response(services['error'])
    return Response(serializers.errors)


def services_by_category(request):
    """Retrieve Paynet services filtered by category."""
    data = request.data
    serializers = ProvidersSerializer(data=data)
    if serializers.is_valid():
        service = get_cached_services_filter_by_category(data['category_id'])
        if service['result']:
            return Response(service['result'])
    return Response(serializers.errors)


def services_by_search(request):
    """Retrieve Paynet services based on search text."""
    data = request.data
    serializers = ServerSearchSerializer(data=data)

    if serializers.is_valid():
        search_text = data['search_text']

        category = Category.objects.filter(
            Q(title_uz__icontains=search_text) |
            Q(title_ru__icontains=search_text)
        )
        serializers = CategoriesSerializer(category, many=True, context={'request': request})
        return Response(serializers.data)

    return Response(serializers.errors, status=400)


def fetch_and_update_categories(request):
    category = Gwmethods.categories()
    if category['result']:
        categories = category['result']
        category_list = []
        for item in categories:
            category, created = Category.objects.get_or_create(category_id=item['id'], defaults={
                'title_ru': item['title_ru'],
                'title_uz': item['title_uz'],
                'is_subcategory': item['is_subcategory']
            })
            if created:
                category_list.append(category)
        serializer = CategoriesSerializer(category_list, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:

        return Response({"error": "Error"},
                        status=status.HTTP_400_BAD_REQUEST)


def services_get_providers(request):
    data = request.data
    serializer = ServersSerializer(data=data)
    if serializer.is_valid():
        servers = Gwmethods.services(provider_id=data['provider_id'])
        return Response(servers['result'], status=status.HTTP_200_OK)
    return Response({'status': False,
                     "message": {
                         "uz": "Noma'lum xatolik",
                         "ru": "Unknown error",
                         "en": "Неизвестная ошибка"
                     }
                     })


def check_receiver(request):
    data = request.data
    serializers = CheckReceiverSerializer(data=data)
    if serializers.is_valid():
        data = serializers.validated_data
        service_id = data['service_id']
        field_data = data['fields']

        check_receivers = Gwmethods.check_receiver(service_id=service_id, field=field_data)
        return Response(check_receivers, status=status.HTTP_200_OK)

    return Response({
        'status': False,
        "message": {
            "uz": "Noma'lum xatolik",
            "ru": "Unknown error",
            "en": "Unknown error"
        }
    }, status=status.HTTP_400_BAD_REQUEST)


def payment_transfers(request):
    data = request.data

    serializer = PaymentSerializer(data=data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:

        card = CardModel.objects.filter(card_uuid=data.get('card_number')).first()
        if not card:
            return Response({"error": "No card found"}, status=status.HTTP_400_BAD_REQUEST)

        sender_ext_id = str(uuid.uuid4())
        receiver_ext_id = str(uuid.uuid4())

        transfer = TransactionsModel.objects.filter(sender_ext_id=sender_ext_id).first()
        if transfer:
            return Response({"error": "Transaction already exists"}, status=status.HTTP_400_BAD_REQUEST)

        if card.pc_type == 1:
            epos = Commission.objects.filter(name="PAYNET_TO_UZCARD").first()
            card_to_card_type = Gwcard_helper.UZCARD_TO_PAYNET
        elif card.pc_type == 3:
            epos = Commission.objects.filter(name="PAYNET_TO_HUMO").first()
            card_to_card_type = Gwcard_helper.HUMO_TO_PAYNET
        else:
            return Response({"error": "Invalid card type"}, status=status.HTTP_400_BAD_REQUEST)

        if not epos:
            return Response({"error": "No epos found"}, status=status.HTTP_400_BAD_REQUEST)

        paynet_transfer = Gwmethods.create_transaction(ext_id=receiver_ext_id, field=data['fields'],
                                                       service_id=data['service_id'])
        if 'error' in paynet_transfer:
            return Response({"error": paynet_transfer['error']}, status=status.HTTP_400_BAD_REQUEST)

        amount = paynet_transfer['result']['transfer']['receiver']['amount'] * 100

        payment_created = Gwmethod.payment_create(
            ext_id=receiver_ext_id,
            number=card.card_number,
            receiver_id=1,
            expire=card.expire,
            amount=amount,
            merchant_id=epos.in_merchant,
            terminal_id=epos.in_terminal
        )
        if 'error' in payment_created:
            return Response({"error": payment_created['error']}, status=status.HTTP_400_BAD_REQUEST)

        transfer = TransactionsModel.objects.create(
            sender=card.card_number,
            sender_ext_id=payment_created['result']['ext_id'],
            expire=card.expire,
            db_amount=payment_created['result']['amount'],
            db_currency=payment_created['result']['currency'],
            db_rrn=payment_created['result']['payment']['ref_num'],
            db_state=payment_created['result']['state'],
            db_description=payment_created['result']['description'],
            cr_currency=payment_created['result']['currency'],
            sender_owner=request.user,
            receiver=paynet_transfer['result']['transfer']['receiver']['receiver'],
            receiver_owner=paynet_transfer['result']['transfer']['receiver']['provider'],
            cr_ext_id=paynet_transfer['result']['transfer']['ext_id'],
            cr_amount=paynet_transfer['result']['transfer']['receiver']['amount'],
            payment_type=card_to_card_type
        )

        transfer.save()

        return Response({
            "message": "success",
            "sender": payment_created['result']['ext_id'],
            "receiver": paynet_transfer['result']['transfer']['ext_id'],
            'count': 6
        }, status=status.HTTP_200_OK)

    except KeyError as e:

        return Response({"error": f"KeyError: Missing expected field {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:

        return Response({"error": f"An unexpected error occurred: {str(e)}"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def payment_confirms(request):
    data = request.data
    serializer = PaymentConfirmSerializer(data=data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:

        if not data.get('code'):
            return Response({"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)

        transaction = TransactionsModel.objects.filter(sender_ext_id=data['sender_ext'],
                                                       cr_ext_id=data['receiver_ext']).first()
        if not transaction:
            return Response({"error": "Transaction not found"}, status=status.HTTP_400_BAD_REQUEST)

        payment_confirm = Gwmethod.payment_confirm(ext_id=data['sender_ext'], code=data['code'])
        if 'error' in payment_confirm:
            return Response({"error": payment_confirm['error']}, status=status.HTTP_400_BAD_REQUEST)

        transaction.db_state = payment_confirm['result']['state']
        transaction.db_description = payment_confirm['result']['description']
        transaction.save()

        paynet_confirm = Gwmethods.transaction_confirm(ext_id=data['receiver_ext'])
        if 'error' in paynet_confirm:
            return Response({"error": paynet_confirm['error']}, status=status.HTTP_400_BAD_REQUEST)

        if not paynet_confirm['result']['transfer']['is_confirmed']:
            return Response({"error": "Not confirmed"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": MESSAGE['PaymentSuccess']})

    except KeyError as e:

        return Response({"error": f"KeyError: Missing expected field {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:

        return Response({"error": f"An unexpected error occurred: {str(e)}"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
