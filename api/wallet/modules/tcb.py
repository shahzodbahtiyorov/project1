import uuid
import random

from apps.accounts.models import OtpModel
from fernet.fernet_helper import encrypt_message, decrypt_message
from services.unigate.dragon import send_sms
from services.unigate.message_error import MESSAGE
from django.core.cache import cache
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from api.wallet.serializers import TransferReceiverInfo, ReceiverInfoCard, TransferCreateRF, TransferStateSerializer
from apps.wallet.models import Form, CardModel, TransactionsModel
from services.tcb import method as Method
from services.unigate import  card_helper as CardHelper

"""RF--->UZ"""


def register_card(request):
    """
    Registers a new card by generating a unique external ID and calling the card registration method.

    This function creates a new card registration request, saves it to the database,
    and returns the result of the registration process. It handles exceptions and returns
    appropriate error messages when needed.
    """
    ext_id = 'S_A_TCB_CARD_' + f"{uuid.uuid4()}"

    try:

        result = Method.card_register(ext_id=ext_id)

        if 'result' in result:
            forms = Form()
            forms.owner = request.user
            forms.ext_id = ext_id
            forms.status = 0
            forms.save()
            return Response({'message': result['result']})

    except Exception as e:

        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({'message': result.get('error', 'Unknown error occurred.')}, status=status.HTTP_400_BAD_REQUEST)


def register_card_state(request):
    """
    Updates the state of a registered card based on the provided external ID.

    This function validates the input data, retrieves the associated form using the
    external ID, checks the card state from the service, and creates a new card if
    the state indicates success. It handles exceptions and returns appropriate error messages.
    """
    data = request.data

    try:

        form = Form.objects.filter(ext_id=data['result']['ext_id']).first()

        if not form:
            return Response({'message': "ext_id not found"}, status=status.HTTP_404_NOT_FOUND)

        result = Method.register_card_state(ext_id=data['result']['ext_id'])

        if 'result' in result:
            if result['result']['state'] == 5:

                card, created = CardModel.objects.get_or_create(
                    owner=form.owner,
                    card_number=result['result']['card']['number'],
                    defaults={
                        'expire': result['result']['card']['expire'],
                        'balance': 0,
                        'mask': result['result']['card']['number'],
                        'bank': result['result']['card']['bank'],
                        'card_owner_name': result['result']['card']['owner'],
                        'type': 'physical',
                        'pc_type': 2,
                        'active': True,
                    }
                )

                if created:
                    return Response({'message': 'Card created successfully.'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'message': 'Card already exists.'}, status=status.HTTP_200_OK)

        if 'error' in result:
            return Response({'message': result['error']['message']}, status=status.HTTP_400_BAD_REQUEST)

        #
        return Response({'message': "Unexpected response from the service."},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:

        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def remove_card(request):
    pass


def service_infos(request):
    """
    Retrieves TCB service information, either from the cache or by calling the service method.
    """
    service = cache.get('service_info')

    if service is None:
        service = Method.service_info()

        if 'result' in service:
            cache.set('service_info', service, timeout=300)
        else:
            return Response({"error": "Service information not available"}, status=500)

    return Response(service['result'])


def transfer_receiver_info(request):
    """
        Handles the request to check transfer receiver details.

        This function validates input data, calls the appropriate method to
        check the receiver's transfer details based on the provided card number,
        amount, and currency. It returns the result if successful or
        appropriate error messages if validation fails or an exception occurs.
    """
    data = request.data
    serializer = TransferReceiverInfo(data=data)

    if serializer.is_valid():
        try:
            result = Method.transfer_receiver_check(
                card_number=data['card_number'],
                amount=data['amount'],
                currency=data['currency']
            )

            if 'result' in result:
                return Response({
                    "result": result['result']
                })

        except Exception as e:

            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def transfer_create(request):
    data = request.data

    serializers = TransferReceiverInfo(data=data)
    if serializers.is_valid():
        try:
            ext_id = 'SR_APP_TCB_' + f"{uuid.uuid4()}"

            result = Method.transfer_create(card_number=data['card_number'],
                                            amount=data['amount'],
                                            currency=data['currency'],
                                            ext_id=ext_id)

            if 'result' in result:
                monitoring = TransactionsModel()
                monitoring.sender_ext_id = ext_id
                monitoring.sender = request.user
                monitoring.receiver = request.user
                monitoring.sender_owner = request.user
                monitoring.db_state = result['result']['transfer']['debit']['state']
                monitoring.db_description = result['result']['transfer']['debit']['description']
                monitoring.db_amount = result['result']['transfer']['debit']['amount']
                monitoring.debit_currency = result['result']['transfer']['debit']['currency']
                monitoring.db_currency = result['result']['transfer']['debit']['currency']
                monitoring.receiver = data['card_number']
                monitoring.receiver_owner = result['result']['receiver']['owner']
                monitoring.cr_rrn = result['result']['transfer']['credit']['_id']
                monitoring.cr_description = result['result']['transfer']['credit']['description']
                monitoring.cr_currency = result['result']['transfer']['credit']['currency']
                monitoring.cr_state = result['result']['transfer']['credit']['state']
                monitoring.cr_amount = result['result']['transfer']['credit']['amount']
                monitoring.cr_description = result['result']['transfer']['credit']['description']
                monitoring.cr_ext_id = result['result']['transfer']['ext_id']
                monitoring.rate = result['result']['currency']['rate'],
                monitoring.card_to_card =CardHelper.RF_TO_UZB

                monitoring.commision = 0
                monitoring.save()

                return Response({
                    "result": {
                        "form_url": result['result']['transfer']['debit']['form_url'],
                        "ext_id": result['result']['transfer']['ext_id']
                    }
                })

        except Exception as e:

            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


def transfer_callback(request):
    try:
        data = request.data


        if 'result' not in data:
            raise ValidationError("Invalid data format: 'result' key is missing.")

        transfer_info = data['result'].get('transfer')
        if not transfer_info:
            raise ValidationError("Invalid data format: 'transfer' key is missing.")

        ext_id = transfer_info.get('ext_id')
        if not ext_id:
            raise ValidationError("Invalid data format: 'ext_id' key is missing.")


        monitoring = TransactionsModel.objects.filter(sender_ext_id=ext_id).first()
        if not monitoring:
            return Response({
                "message": {
                    "uz": "Ext_Id topilmadi",
                    "ru": "Ext_Id не найден",
                    "eng": "Ext_Id not found"
                }
            })

        monitoring.db_state = transfer_info['debit']['state']
        monitoring.db_description = transfer_info['debit']['description']
        monitoring.cr_state = transfer_info['credit']['state']
        monitoring.cr_description = transfer_info['credit']['description']
        monitoring.sender = data['result']['sender']['number']

        monitoring.save()
        return Response({'message': data['result']})

    except KeyError as e:
        return Response({"message": f"Missing key: {str(e)}"}, status=400)
    except ValidationError as e:
        return Response({"message": str(e)}, status=400)
    except Exception as e:
        return Response({"message": "Error: " + str(e)}, status=500)


"""UZ-->RF"""


def transfer_sender_info(request):
    data = request.data
    serializers = ReceiverInfoCard(data=data)
    if serializers.is_valid():
        result = Method.receiver_check(card_number=data['card_number'])
        if 'result' in result:
            return Response(result['result'])
        return Response({'message': MESSAGE['CardNotFound']},status=status.HTTP_404_NOT_FOUND)
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


def transfer_rf_create(request):
    data = request.data
    user = request.user.phone_number
    serializers = TransferCreateRF(data=data)
    if serializers.is_valid():
        card = CardModel.objects.filter(card_uuid=data['token']).first()
        if not card:
            return Response({"message": MESSAGE['CardNotFound']},status=status.HTTP_404_NOT_FOUND)
        ext_id = 'SR_UZ_RF_' + f"{uuid.uuid4()}"
        result = Method.transfer_rf_create(ext_id=ext_id, card_number=card.card_number,
                                           expire=card.expire, currency=data['currency'],
                                           amount=data['amount'],receiver=data['receiver'])
        if 'result' in result:
            code = random.randint(100000, 999999)
            encryptions = encrypt_message(message=str(code))
            send_message = send_sms(phone=f'+{user}',
                                    text=f'Kod xech kimga bermang {code}')
            otp = OtpModel.objects.create(
                user=request.user,
                phone_number=user,
                otp_token=encryptions,

            )
            otp.save()
            monitoring = TransactionsModel()
            monitoring.sender = card.card_number
            monitoring.expire = card.expire
            monitoring.db_amount = result['result']['transfer']['debit']['amount']
            monitoring.sender_ext_id = result['result']['transfer']['ext_id']
            monitoring.sender_owner = request.user
            monitoring.db_rrn = result['result']['transfer']['tr_id']
            monitoring.db_state = result['result']['transfer']['debit']['state']
            monitoring.db_description = result['result']['transfer']['debit']['description']
            monitoring.db_currency = result['result']['transfer']['debit']['currency']
            monitoring.receiver = result['result']['receiver']['number']
            monitoring.receiver_owner = result['result']['receiver']['number']
            monitoring.cr_rrn = result['result']['transfer']['tr_id']
            monitoring.cr_state = result['result']['transfer']['credit']['state']
            monitoring.cr_amount = result['result']['transfer']['credit']['amount']
            monitoring.cr_description = result['result']['transfer']['credit']['description']
            monitoring.cr_currency = result['result']['transfer']['credit']['currency']
            monitoring.credit_currency = result['result']['transfer']['credit']['currency']
            monitoring.cr_ext_id =result['result']['transfer']['ext_id']
            monitoring.rate = result['result']['currency']['rate']
            monitoring.card_to_card = CardHelper.UZB_TO_RF
            monitoring.commision = 0
            monitoring.save()

            return Response({"ext_id":
                                 result["result"]['transfer']['ext_id'],
                             "token":encryptions})
        return Response({"message": result['message']},status=status.HTTP_400_BAD_REQUEST)

    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


def transfer_rf_confirm(request):
    data = request.data
    serializers = TransferStateSerializer(data=data)
    if serializers.is_valid():
        if not data['code']:
            return Response({"message":"Code not found"})
        otp = OtpModel.objects.filter(otp_token=f"b'{data['token']}'").first()

        if not otp:
            Response({"message": "OTP Token not found"}, status=status.HTTP_400_BAD_REQUEST)
        monitoring = TransactionsModel.objects.filter(sender_ext_id=data['ext_id']).first()
        decryptions = decrypt_message(encrypted_message=otp.otp_token)

        if int(data['code']) != int(decryptions):
            otp.tried = +1
            otp.save()
            if otp.tried == 3:
                otp.expire = True
                otp.save()
            return Response({"message": "OTP Code wrong"}, status=status.HTTP_400_BAD_REQUEST)
        elif otp.is_expired(expiration_time=120):
            otp.expire = True
            otp.save()  # 60 seconds expiration time
            return Response({"message": "OTP Token expired"}, status=status.HTTP_400_BAD_REQUEST)
        elif otp.expire == True:
            return Response({"message": "OTP Token expired"}, status=status.HTTP_400_BAD_REQUEST)

        elif int(data['code']) == int(decryptions):
            if not monitoring:
                return Response({"message": "Ext_Id Not Found"},status=status.HTTP_404_NOT_FOUND)
            result = Method.transfer_rf_confirm(ext_id=data['ext_id'])
            if 'result' in result:

                monitoring.db_state = result['result']['transfer']['debit']['state']
                monitoring.db_description = result['result']['transfer']['debit']['description']
                monitoring.cr_state = result['result']['transfer']['credit']['state']
                monitoring.cr_description = result['result']['transfer']['credit']['description']
                monitoring.save()
                return Response({"message": MESSAGE['PaymentSuccess']})
            return Response({"message": result},status=status.HTTP_400_BAD_REQUEST)
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

def transfer_rf_state(request):
    data = request.data
    serializers = TransferStateSerializer(data=data)
    if serializers.is_valid():
        state = Method.transfer_rf_state(ext_id=data['ext_id'])
        if 'result' in state:
            return Response({"message":state["result"] })
        return Response({"message": state })
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)