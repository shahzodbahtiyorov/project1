from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.wallet.serializers import TransferSerializer, ConfirmTransferSerializer, W2WSerializer, OtpCheckSerializer
from api.wallet.utils.balance import get_wallet_balance
from api.wallet.utils.transfer import transfer_service, confirm_transfer_service, w2w_step_one, w2w_step_two
from apps.accounts.models import Account
from apps.accounts.utils import create_wallet_util
from apps.wallet.models import WalletModel, TransactionsModel, TransferW2WModel


@swagger_auto_schema(method="get", tags=["wallet"])
@api_view(["GET", ])
@permission_classes([IsAuthenticated])
def get_wallet_balance_view(request):
    user = request.user
    try:
        wallet = WalletModel.objects.get(owner=user)
    except:
        data = create_wallet_util(user.phone_number)
        if data:
            card_number = data['result']['card_number']
            expire = data['result']['expire']

            wallet = WalletModel.objects.create(
                owner=user,
                card_number=card_number,
                expire=expire,
                # type=False
            )
        else:
            return Response(status=400)
    balance = get_wallet_balance(wallet)
    if balance:
        return Response(balance)
    else:
        return Response(status=400)


@swagger_auto_schema(method="post", tags=["wallet"], request_body=TransferSerializer)
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def transfer_to_wallet(request):
    account: Account = request.user
    try:
        wallet = WalletModel.objects.get(owner=request.user)
    except WalletModel.DoesNotExist:
        data = create_wallet_util(account.phone_number)

        card_number = data['result']['card_number']
        expire = data['result']['expire']

        WalletModel.objects.create(
            owner=account,
            card_number=card_number,
            expire=expire,
        )
        wallet = WalletModel.objects.get(owner=request.user)

    if request.method == 'POST':
        serializer = TransferSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.data

            # if data['is_saved_card']:
            #     try:
            #         saved_card = CardModel.objects.get(card_uuid=data['number'])
            #     except CardModel.DoesNotExist:
            #         return Response(
            #             {'message': f"Card with UUID: {data['number']} does not exist!",
            #              'status': False},
            #             status=status.HTTP_404_NOT_FOUND
            #         )
            #     data['number'] = str(saved_card.card_number)
            #     print(f"*************{data}")
            data['amount'] = data['amount'] * 100

            return transfer_service(wallet, data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method="post", tags=["wallet"], request_body=ConfirmTransferSerializer)
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def confirm_transfer_to_wallet(request):
    if request.method == 'POST':
        serializers = ConfirmTransferSerializer(data=request.data)

        if serializers.is_valid():
            data = serializers.data
            return confirm_transfer_service(data)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method="post", tags=["wallet"], request_body=W2WSerializer)
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_wallet_to_wallet(request):
    user_wallet = request.user.wallet
    data = request.data
    serializer = W2WSerializer(data=data)
    if serializer.is_valid():
        receiver = WalletModel.objects.get(card_number=data["receiver"])
        otp_token = w2w_step_one(user_wallet, receiver, data["amount"])
        return Response({"otp_token": otp_token})
    return Response(serializer.errors)


@swagger_auto_schema(method="post", tags=["wallet"], request_body=OtpCheckSerializer)
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def confirm_wallet_to_wallet(request):
    data = request.data
    serializer = OtpCheckSerializer(data=data)
    if serializer.is_valid():
        return w2w_step_two(request.user, data["otp"], data["otp_token"])
    return Response(serializer.errors)


@swagger_auto_schema(method="get", tags=["wallet"], )
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def wallet_history(request):
    wallet_number = request.user.wallet.card_number
    wallet = request.user.wallet
    response = []

    transactions = TransactionsModel.objects.filter(
        Q(sender=wallet_number) | Q(receiver=wallet_number) & Q(option__in=["WalletToCard", "CardToWallet"])).values(
        "created_at", "sender", "receiver", "amount")
    w2w_transactions = TransferW2WModel.objects.filter(Q(sender=wallet) | Q(receiver=wallet)).values(
        "created_at", "sender__card_number", "receiver__card_number", "amount")

    for i in transactions:
        response.append(i)
    for i in w2w_transactions:
        one_dict = {}
        one_dict["created_at"] = i["created_at"]
        one_dict["sender"] = i["sender__card_number"]
        one_dict["receiver"] = i["receiver__card_number"]
        one_dict["amount"] = i["amount"]
        response.append(one_dict)
    response.sort(key=lambda x: x["created_at"], reverse=True)
    return Response(response)
