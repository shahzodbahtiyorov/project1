# monitoring.py

"""
This module provides functions to monitor and retrieve transaction data
for user cards in the super app application.
"""

from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from xhtml2pdf import pisa
from api.wallet.serializers.monitoring import MonitoringCheckSerializer, TransactionsModelSerializer, \
    TransactionsStateSerializer
from apps.wallet.models import TransactionsModel, CardModel


def get_payment_type_display(payment_type):
    """Get a human-readable display for the payment type."""
    payment_type_map = {
        0: 'UZCARD to UZCARD',
        1: 'UZCARD to HUMO',
        2: 'HUMO to UZCARD',
        3: 'HUMO to HUMO',
        4: 'UZCARD to PAYNET',
        5: 'HUMO to PAYNET',
        6: 'RF to UZB',
        7: 'UZB to RF',
    }

    if isinstance(payment_type, int):
        return payment_type_map.get(payment_type, 'Unknown')
    return 'Invalid type'


def card_monitoring_all(request):
    """
    Retrieve all transactions for the authenticated user's cards.
    """
    user = request.user

    if not user.is_authenticated:
        return Response(
            {'error': 'User not authenticated'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    try:
        user_cards = CardModel.objects.filter(owner=user)

        if not user_cards.exists():
            return Response(
                {'error': 'No cards found for this user'},
                status=status.HTTP_404_NOT_FOUND
            )

        all_transactions = []

        for card in user_cards:
            # Sent transactions
            sent = TransactionsModel.objects.filter(sender=card.card_number).order_by('-created_at')
            for transaction in sent:
                db_amount = transaction.db_amount or 0
                all_transactions.append({
                    "id": transaction.id,
                    "card_number": transaction.sender,
                    "total_amount": db_amount / 100,
                    "transaction_type": 1,
                    "owner_name": get_payment_type_display(transaction.payment_type),
                    "created_at": transaction.created_at.strftime('%Y-%m-%d'),
                    "dated_at": transaction.created_at.strftime('%H:%M'),
                    "currency": transaction.db_currency,
                })

            # Received transactions
            received = TransactionsModel.objects.filter(receiver=card.card_number).order_by('-created_at')
            for transaction in received:
                db_amount = transaction.db_amount or 0
                all_transactions.append({
                    "id": transaction.id,
                    "card_number": transaction.receiver,
                    "total_amount": db_amount / 100,
                    "transaction_type": 2,
                    "owner_name": get_payment_type_display(int(transaction.payment_type)),
                    "created_at": transaction.created_at.strftime('%Y-%m-%d'),
                    "dated_at": transaction.created_at.strftime('%H:%M'),
                    "currency": transaction.cr_currency,
                })

        all_transactions.sort(key=lambda x: x['created_at'], reverse=True)
        return Response({'result': all_transactions}, status=status.HTTP_200_OK)

    except (ValueError, TypeError, KeyError, AttributeError) as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': f'An unexpected error occurred: {str(e)}'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def card_monitoring(request):
    """
    Retrieve transactions based on specified card numbers and date range.
    """
    data = request.data
    user = request.user
    cards = CardModel.objects.filter(owner=user).values_list('card_number', flat=True)

    if not data:
        return Response({'error': 'Data not found'}, status=status.HTTP_400_BAD_REQUEST)

    request_cards = data.get("card_numbers")
    if isinstance(request_cards, str):
        request_cards = [request_cards]

    start_date = data.get("start_date")
    end_date = data.get("end_date")

    try:
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')

        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)

        all_transactions = []

        # Sent transactions
        sender_card = TransactionsModel.objects.filter(sender__in=request_cards or cards)
        if start_date:
            sender_card = sender_card.filter(created_at__gte=start_date)
        if end_date:
            sender_card = sender_card.filter(created_at__lte=end_date)

        sender_card = sender_card.order_by('-pk')
        for transaction in sender_card:
            if transaction.db_amount:
                all_transactions.append({
                    "id": transaction.id,
                    "card_number": transaction.sender,
                    "total_amount": transaction.db_amount / 100,
                    "transaction_type": 1,
                    "owner_name": get_payment_type_display(transaction.payment_type),
                    "created_at": transaction.created_at.strftime('%Y-%m-%d'),
                    "dated_at": transaction.created_at.strftime('%H:%M'),
                    "currency": transaction.db_currency,
                })

        # Received transactions
        received_card = TransactionsModel.objects.filter(receiver__in=request_cards or cards)
        if start_date:
            received_card = received_card.filter(created_at__gte=start_date)
        if end_date:
            received_card = received_card.filter(created_at__lte=end_date)

        received_card = received_card.order_by('-pk')
        for transaction in received_card:
            if transaction.db_amount:
                all_transactions.append({
                    "id": transaction.id,
                    "card_number": transaction.receiver,
                    "total_amount": transaction.db_amount / 100,
                    "transaction_type": 2,
                    "owner_name": get_payment_type_display(transaction.payment_type),
                    "created_at": transaction.created_at.strftime('%Y-%m-%d'),
                    "dated_at": transaction.created_at.strftime('%H:%M'),
                    "currency": transaction.cr_currency,
                })

        all_transactions.sort(key=lambda x: x['created_at'], reverse=True)
        return Response({'result': all_transactions}, status=status.HTTP_200_OK)

    except (ValueError, TypeError) as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": f"An unexpected error occurred: {str(e)}"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def monitoring_check(request):
    """
    Check the details of a specific monitoring transaction.
    """
    try:
        data = request.data
        serializer = MonitoringCheckSerializer(data=data)

        if serializer.is_valid():
            monitoring = TransactionsModel.objects.filter(id=data['id']).first()
            if not monitoring:
                return Response({"error": "No monitoring data"}, status=status.HTTP_400_BAD_REQUEST)

            serialized_data = TransactionsModelSerializer(monitoring)
            return Response(serialized_data.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def transfer_check(request):
    """
    Check the status of a specific transfer based on the external ID.
    """
    data = request.data
    serializer = TransactionsStateSerializer(data=data)

    if serializer.is_valid():
        transaction = TransactionsModel.objects.filter(sender_ext_id=data['ext_id']).first()

        if not transaction:
            return Response({"message": "Transactions not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TransactionsModelSerializer(transaction)
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def render_to_pdf(template_src, context_dict=None):
    """
    Render a template to PDF.
    """
    if context_dict is None:
        context_dict = {}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    template = get_template(template_src)
    html = template.render(context_dict)

    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)

    if pisa_status.err:
        return HttpResponse(f'We had some errors <pre>{html}</pre>')

    return response


def link_callback(uri, rel):
    """
    Fix for links inside the PDF (external links, images).
    """
    return uri



def get_transaction_pdf(request):
    """
    Generate a PDF for a transaction based on the transaction ID.
    """
    transaction_id = request.data.get('id')

    if not transaction_id:
        return JsonResponse({'error': ' ID is required'}, status=400)

    try:
        transaction = TransactionsModel.objects.get(id=transaction_id)

        context = {
            'debit_tr_id': transaction.debit_tr_id,
            'db_amount': transaction.db_amount / 100.0,
            'created_at': transaction.created_at.strftime('%Y-%m-%d'),
            'sender': transaction.sender,
            'cr_amount': transaction.cr_amount / 100.0,
            'db_state': transaction.db_state,
        }

        return render_to_pdf('transaction_details.html', context)

    except TransactionsModel.DoesNotExist:
        return JsonResponse({'error': 'Transaction not found'}, status=404)
