"""
Django API for Wallet Management
=================================

This module handles all operations related to wallet management, card transfers, and transaction
history. It includes endpoints for adding new cards, transferring funds between cards, confirming
card transfers, and viewing transaction histories. The API uses Django REST framework for
serialization and validation.

Requirements:
-------------
- Django REST Framework
- A configured logger for request tracking
- Custom services for card information retrieval and transactions

Usage:
------
- Integrate this module into a Django project
- Configure the necessary settings and environment variables

Note:
-----
Ensure proper handling of sensitive information such as card details and OTP tokens.

Author: [Isroilov Sukhrob]

"""
import uuid
from rest_framework import status
from rest_framework.response import Response
from api.wallet.serializers import (CardInfoSerializer, P2PCardSerializer,
                                    TransferCofirmeSerializer,
                                    CardDetailsSerializer, CardModelSerializer,
                                    UzcardInfoSerializer, TransferSerializers,
                                    CardTransferSerializer, HumoInfoSerializer,
                                    CommissionCardSerializer, CardBlockedSerializers, CardModelBalanceSerializer,
                                    CardNameSerializer)
from apps.accounts.models import OtpModel
from apps.wallet.card_info.helper import get_card_info
from services.card_background.background import get_background, get_logo
from services.unigate import methods as Gwmethods
from apps.wallet.models import TransactionsModel, CardModel, Commission
from services.unigate.dragon import send_sms
from services.unigate.helper import expire_date_format, transform_date_format
from fernet.fernet_helper import decrypt_message, encrypt_message
from services.unigate.message_error import MESSAGE

from services.unigate import card_helper as Gwcard_helper
import random

"""
    Card create
"""


def card_create(request):
    """Card add"""
    data = request.data
    serializers = CardDetailsSerializer(data=data)

    try:
        if serializers.is_valid():
            card_model = CardModel.objects.filter(
                card_number=data['card_number'],
                owner=request.user.phone_number
            ).first()

            if card_model:
                return Response({"success": MESSAGE['CardAdd']})

            card_info = Gwmethods.card_info(number=data['card_number'])

            if 'result' in card_info:
                if card_info['result']['pc_type'] == 3:
                    card_about = Gwmethods.humo_register(
                        number=data['card_number'],
                        expire=expire_date_format(data['expire'])
                    )

                    if 'result' in card_about:
                        card = card_about['result']['phone']

                        if card[1:] in request.user.phone_number:
                            code = random.randint(100000, 999999)
                            encryptions = encrypt_message(message=str(code))
                            send_message = send_sms(
                                phone=card_about['result']['phone'],
                                text=f"DIQQAT! Ushbu kodni hech kimga bermang!!!Sizning registratsiya qilish uchun tasdiqlash kodi {code}"
                            )

                            otp = OtpModel.objects.create(
                                user=request.user,
                                phone_number=card_about['result']['phone'],
                                otp_token=encryptions,
                            )
                            otp.save()

                            return Response(
                                {
                                    "message": 'sent sms humo ',
                                    'otp_token': otp.otp_token,
                                    'number': data['card_number'],
                                    'expire': transform_date_format(data['expire']),
                                    'card_name': data['card_name'],
                                    'card_number': f"********{card_about['result']['phone'][-4:]}",
                                    'count':6
                                },
                                status=status.HTTP_200_OK
                            )

                        return Response({'message': MESSAGE['PhoneError']},
                                        status=status.HTTP_400_BAD_REQUEST)
                    return Response(card_about['error'], status=status.HTTP_400_BAD_REQUEST)

                elif card_info['result']['pc_type'] == 1:
                    card_about = Gwmethods.card_create(
                        number=data['card_number'],
                        expire=expire_date_format(data['expire'])
                    )

                    if 'result' in card_about:
                        otp = OtpModel.objects.create(
                            user=request.user,
                            phone_number=card_about['result']['phoneMask'],
                            otp_token=card_about['result']['ext_id'],
                        )
                        otp.save()

                        return Response({
                            "success": "Sms sent to uzcard",
                            "ext_id": str(card_about['result']['ext_id']),
                            "card_number": card_about['result']['phoneMask'],
                            "number": data['card_number'],
                            'expire': transform_date_format(data['expire']),
                            'card_name': data['card_name'],
                            'count': 6
                        })

            return Response(card_info['error'], status=status.HTTP_400_BAD_REQUEST)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



"""Humo card sms confirmation"""


def card_sms_humo_confirm(request):
    data = request.data
    serializers = HumoInfoSerializer(data=data)

    try:
        if serializers.is_valid():
            otp = OtpModel.objects.filter(otp_token=f"b'{data['otp_code']}'").first()

            if not otp:
                return Response({"message": "OTP Token not found"}, status=status.HTTP_400_BAD_REQUEST)

            decryptions = decrypt_message(encrypted_message=otp.otp_token)

            if int(data['code']) != int(decryptions):
                otp.tried += 1  # Increment the tried count
                otp.save()
                if otp.tried >= 3:  # Change to >= to include the third attempt
                    otp.expire = True
                    otp.save()
                return Response({"message": "OTP Code wrong"}, status=status.HTTP_400_BAD_REQUEST)

            if otp.is_expired(expiration_time=60):
                otp.expire = True
                otp.save()  # Mark as expired after 60 seconds
                return Response({"message": "OTP Token expired"}, status=status.HTTP_400_BAD_REQUEST)

            if otp.expire:
                return Response({"message": "OTP Token expired"}, status=status.HTTP_400_BAD_REQUEST)

            # Correct OTP case
            otp.expire = True
            otp.save()

            card = Gwmethods.humo_register(number=data['number'], expire=data['expire'])

            if not card['result']:
                return Response({"message": MESSAGE['CardFoundnot']}, status=status.HTTP_400_BAD_REQUEST)

            cards = CardModel.objects.create(
                owner=request.user,
                card_number=card['result']['card_number'],
                expire=data['expire'],
                active=True,
                balance=card['result']['balance'],
                mask=card['result']['mask'],
                bank=card['result']['bank'],
                card_owner_name=card['result']['owner'],
                pc_type=card['result']['pc_type'],
                card_name=data['card_name'],
            )
            cards.save()

            card_model = CardModel.objects.filter(owner=request.user)
            serializers = CardModelSerializer(card_model, many=True)

            return Response({'message': MESSAGE['CardAdd'], 'result': serializers.data})

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



"""Uzcard card sms confirmation"""


def card_uzcard(request):
    data = request.data
    serializers = UzcardInfoSerializer(data=data)

    try:
        if serializers.is_valid():
            card_info = Gwmethods.uzcard_verify(code=int(data['code']), ext_id=data['ext_id'])

            if 'result' in card_info:
                card_register = Gwmethods.humo_register(number=data['number'], expire=data['expire'])

                otp = OtpModel.objects.filter(otp_token=data['ext_id']).first()
                if not otp:
                    return Response({"message": "OTP Token not found"}, status=status.HTTP_400_BAD_REQUEST)

                otp.phone_number = card_info['result']['phone']
                otp.save()

                if 'result' in card_register:
                    if card_register['result']['phone'] in request.user.phone_number:
                        card = Gwmethods.card_info(number=data['number'])

                        if 'result' in card:
                            card_model = CardModel.objects.create(
                                owner=request.user,
                                expire=data.get('expire'),
                                card_number=card_register['result']['card_number'],
                                active=True,
                                balance=card_register['result']['balance'],
                                mask=card_register['result']['mask'],
                                card_owner_name=card_register['result']['owner'],
                                bank=card['result']['bank'],
                                pc_type=card['result']['pc_type'],
                                card_name=data['card_name']
                            )
                            card_model.save()

                            cards = CardModel.objects.filter(owner=request.user)
                            serializers = CardModelSerializer(cards, many=True)

                            return Response({
                                "success": "Card Add",
                                "result": serializers.data
                            }, status=status.HTTP_200_OK)

                    return Response({"message": MESSAGE['PhoneError']}, status=status.HTTP_400_BAD_REQUEST)

                return Response(card_register.get('error', 'Unknown error occurred'),
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""
    User cards bring balance
"""


def cards_all_balance(request):
    try:
        cards = CardModel.objects.filter(owner=request.user).select_related('owner')

        for card in cards:
            if card.pc_type == 2:
                continue

            if card.pc_type in [1, 3]:
                card_info = get_card_info(card_number=card.card_number, expire=card.expire)

                if card_info is None or 'result' not in card_info:
                    card.balance = 0
                    card.blocked = True
                    card.save()

                    if card.pc_type == 1:
                        return Response({
                            "message": MESSAGE['UzcardError']
                        }, status=status.HTTP_400_BAD_REQUEST)
                    elif card.pc_type == 3:
                        return Response({
                            "message": MESSAGE['HumoError']
                        }, status=status.HTTP_400_BAD_REQUEST)

                if card_info['result']['balance'] != card.balance:
                    card.balance = card_info['result']['balance']
                    card.save()

        total_balance = sum(card.balance for card in cards) / 100

        card_serializers = CardModelBalanceSerializer(cards, many=True, context={'request': request})

        return Response({
            "total_balance": total_balance,
            "cards": card_serializers.data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


######################
# Card about info ####
######################
def card_info_about(request):
    """Card about info"""
    try:
        data = request.data
        receiver = data.get("receiver", None)

        if not receiver:
            return Response({"error": "Receiver field is missing"}, status=status.HTTP_400_BAD_REQUEST)

        card_about = Gwmethods.card_info(number=receiver)
        card_background = get_background(receiver)
        card_icon = get_logo(receiver)

        if 'result' in card_about:
            return Response({
                'result': card_about['result'],
                'image_back': card_background,
                'image_icon': card_icon
            }, status=status.HTTP_200_OK)

        return Response({'message': MESSAGE['CardNotFound']}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#################
# Card transfer #
#################


def handle_payment_creation(epos, card_info_sender, balance, sender_ext_id, receiver_id=1):
    return Gwmethods.payment_create(
        number=card_info_sender.card_number,
        expire=card_info_sender.expire,
        amount=balance,
        merchant_id=epos.in_merchant,
        terminal_id=epos.in_terminal,
        ext_id=sender_ext_id, receiver_id=receiver_id
    )


def handle_transfer_creation(receiver_ext_id, data, balance, epos):
    return Gwmethods.transfer_create(
        ext_id=receiver_ext_id,
        number=data['receiver'],
        amount=balance,
        merchant_id=epos.out_merchant,
        terminal_id=epos.out_terminal,
    )


#########################
# Card transfer       ###
#########################
def card_transfer(request):
    """Card transfer"""
    try:
        data = request.data
        serializer = CardTransferSerializer(data=data)

        if serializer.is_valid():
            card_info_sender = CardModel.objects.filter(card_uuid=data['ext_id']).first()

            if not card_info_sender:
                return Response({"error": "Card info sender not found"},
                                status=status.HTTP_400_BAD_REQUEST)

            card_info_receiver = Gwmethods.bin_check(data['receiver'])

            balance = data['amount']
            sender_ext_id = str(uuid.uuid4())
            receiver_ext_id = str(uuid.uuid4())

            transfer = TransactionsModel.objects.filter(sender_ext_id=sender_ext_id).first()
            if transfer:
                return Response({"message": "Ext_Id already in use"},
                                status=status.HTTP_400_BAD_REQUEST)

            epos = {}
            card_to_card_type = None

            # Determine commission and card type
            if card_info_sender.pc_type == 3 and card_info_receiver['result']['pc_type'] == 1:
                epos = Commission.objects.filter(name='HUMO_TO_UZCARD').first()
                card_to_card_type = Gwcard_helper.HUMO_TO_UZCARD
            elif card_info_sender.pc_type == 1 and card_info_receiver['result']['pc_type'] == 3:
                epos = Commission.objects.filter(name='UZCARD_TO_HUMO').first()
                card_to_card_type = Gwcard_helper.UZCARD_TO_HUMO
            elif card_info_sender.pc_type == 3 and card_info_receiver['result']['pc_type'] == 3:
                epos = Commission.objects.filter(name='HUMO_TO_HUMO').first()
                card_to_card_type = Gwcard_helper.HUMO_TO_HUMO
            elif card_info_sender.pc_type == 1 and card_info_receiver['result']['pc_type'] == 1:
                epos = Commission.objects.filter(name='UZCARD_TO_UZCARD').first()
                card_to_card_type = Gwcard_helper.UZCARD_TO_UZCARD
            else:
                return Response({"error": "Invalid card type combination"},
                                status=status.HTTP_400_BAD_REQUEST)

            # Handle payment creation
            payment_created = handle_payment_creation(epos, card_info_sender, balance, sender_ext_id)

            if 'error' in payment_created:
                return Response({"error": payment_created['error']}, status=status.HTTP_400_BAD_REQUEST)

            if 'result' in payment_created:
                transfer = TransactionsModel.objects.create(
                    sender=card_info_sender.card_number,
                    sender_ext_id=payment_created['result']['ext_id'],
                    expire=card_info_sender.expire,
                    db_amount=payment_created['result']['amount'],
                    db_rrn=payment_created['result']['payment']['ref_num'],
                    db_state=payment_created['result']['state'],
                    db_description=payment_created['result']['description'],
                    sender_owner=request.user,
                    commision=payment_created['result']['commission'],
                    debit_currency=int(payment_created['result']['currency']),
                    db_currency=int(payment_created['result']['currency']),
                    card_to_card=card_to_card_type,
                    payment_type=card_to_card_type
                )
                transfer.save()

                monitoring = TransactionsModel.objects.filter(sender_ext_id=payment_created['result']['ext_id']).first()

                if not monitoring:
                    return Response({"error": "EXT_ID not found"}, status=status.HTTP_400_BAD_REQUEST)

                # Handle transfer creation
                transfer_created = handle_transfer_creation(receiver_ext_id, data, balance, epos)

                if 'error' in transfer_created:
                    return Response({"error": transfer_created['error']}, status=status.HTTP_400_BAD_REQUEST)

                if 'result' in transfer_created:
                    monitoring.receiver = transfer_created['result']['number']
                    monitoring.receiver_owner = transfer_created['result']['account'][1]['value']
                    monitoring.cr_rrn = transfer_created['result']['payment']['ref_num']
                    monitoring.cr_state = transfer_created['result']['state']
                    monitoring.cr_description = transfer_created['result']['description']
                    monitoring.cr_ext_id = transfer_created['result']['ext_id']
                    monitoring.cr_amount = transfer_created['result']['amount']
                    monitoring.cr_currency = int(transfer_created['result']['currency'])
                    monitoring.card_to_card = card_to_card_type
                    monitoring.save()

                    return Response({
                        "message": "Sms otp",
                        'sender_ext_id': payment_created['result']['ext_id'],
                        'receiver_ext_id': transfer_created['result']['ext_id'],
                        'count': 6
                    })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



##################
#   Card confirm #
##################
def card_confirm(request):
    """Card confirm"""
    try:
        data = request.data
        serializers = P2PCardSerializer(data=data)

        if not serializers.is_valid():
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

        sender_transfer = TransactionsModel.objects.filter(sender_ext_id=data['sender_ext_id']).first()

        if not sender_transfer:
            return Response({'message': 'Sender external ID not found'}, status=status.HTTP_404_NOT_FOUND)

        payment_confirm = Gwmethods.payment_confirm(ext_id=data['sender_ext_id'], code=data['code'])

        if 'result' in payment_confirm:
            sender_transfer.db_state = payment_confirm['result']['state']
            sender_transfer.db_description = payment_confirm['result']['description']
            sender_transfer.save()

            receiver_transfer = TransactionsModel.objects.filter(cr_ext_id=data['receiver_ext_id']).first()

            if not receiver_transfer:
                return Response({'message': 'Receiver external ID not found'}, status=status.HTTP_404_NOT_FOUND)

            transfer_confirm = Gwmethods.transfer_confirm(ext_id=data['receiver_ext_id'])

            if 'result' in transfer_confirm:
                receiver_transfer.cr_state = transfer_confirm['result']['state']
                receiver_transfer.cr_description = transfer_confirm['result']['description']
                receiver_transfer.save()

                return Response({
                    'success': MESSAGE['PaymentSuccess'],
                      'ext_id': data['sender_ext_id'],})

        return Response({'error': payment_confirm.get('error', 'Unknown error')}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



def epos_add(request):
    data = request.data
    serializers = CommissionCardSerializer(data=data)
    if serializers.is_valid():
        epos = Commission.objects.filter(name=data['name']).first()
        if epos:
            return Response({'message': 'this epic exists '})
        epos = Commission.objects.create(
            name=data['name'],
            in_merchant=data['in_merchant'],
            in_terminal=data['in_terminal'],
            out_terminal=data['out_terminal'],
            out_merchant=data['out_merchant'], )
        epos.save()
        return Response({'message': 'epos created'})
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


"""Card blocked"""


def card_blocked(request):
    data = request.data
    serializers = CardBlockedSerializers(data=data)
    if serializers.is_valid():
        user = request.user
        card = CardModel.objects.filter(id=data['card_id'], owner=user).first()
        if not card:
            return Response({'message': 'card not found'})
        if data['is_blocked'] == 0:
            card.active = data['is_blocked']
            card.save()
            return Response({'message': 'card blocked'})
        elif data['is_blocked'] == 1:
            card.active = data['is_blocked']
            card.save()
            return Response({'message': 'card is active '})

    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


"""Card name update"""


def card_name_update(request):
    data = request.data
    serializers = CardNameSerializer(data=data)
    if serializers.is_valid():
        card = CardModel.objects.filter(id=data['card_id'], owner=request.user).first()
        if not card:
            return Response({'message': 'card not found'}, status=status.HTTP_400_BAD_REQUEST)
        card.card_name = data['name']
        card.save()
        return Response({'message': 'card name updated'})

    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

