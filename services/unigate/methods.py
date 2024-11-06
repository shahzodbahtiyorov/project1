
import uuid

import requests

from .dragon import fire


# auth
def login(username, password):
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "login",
        "params": {
            "username": username,
            "password": password
        }}

    return fire(payload)


def bin_check(card_number):
    """the card identifies the pc_type if pc_type =1 uzcard or pc_type=3 humo """
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "bin.check",
        "params": {
            "number": card_number
        }
    }
    return fire(payload)


# card
def card_info(number):
    # state 0 dan boshqasi card blocked va is_corpate true bo'lsa chopish kk
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "card.info",
        "params": {
            "number": number
        }
    }
    return fire(payload)


def card_get_by_phone(phone):
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "card.get.by.phone",
        "params": {
            "phone": phone
        }}
    return fire(payload)


# payments
def payment_create(ext_id, number, expire, amount, receiver_id, merchant_id,
                   terminal_id):  # receiver_id humo/uzcard card_number

    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "payment.get.otp",
        "params": {
            "ext_id": ext_id,
            "number": number,
            "expire": expire,
            "receiver_id": receiver_id,
            "amount": amount,
            "merchant_id": merchant_id,
            "terminal_id": terminal_id
        }
    }
    return fire(payload)


def payment_confirm(ext_id, code):
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "payment.verify",
        "params": {
            "ext_id": ext_id,
            "code": code
        }}
    return fire(payload)


# def payment_cancel(ext_id):
#     payload = {
#         "jsonrpc": "2.0",
#         "id": uuid.uuid4().__str__(),
#         "method": "payment.cancel",
#         "params": {
#             "ext_id": ext_id
#         }
#     }
#     return fire(payload)


def payment_state(ext_id):
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "payment.state",
        "params": {
            "ext_id": ext_id
        }
    }
    return fire(payload)


def card_create(number, expire):
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "card.new.otp",
        "params": {
            "number": number,
            "expire": expire
        }
    }
    return fire(payload)


def get_rate(currency=643):
    try:
        currency = str(currency)

        url = ""

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        rates = response.json()["result"]
        for i in rates:
            if i["code"] == currency:
                return i["rate"]["sell"]

    except:
        return 0


def transfer_create(ext_id, number, amount,merchant_id,terminal_id):
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "transfer.credit.create",
        "params": {
            "ext_id": ext_id,
            "number": number,
            "amount": amount,
            "merchant_id": merchant_id,
            "terminal_id": terminal_id
        }
    }
    return fire(payload)


def transfer_confirm(ext_id):
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "transfer.credit.confirm",
        "params": {
            "ext_id": ext_id

        }
    }
    return fire(payload)


def humo_register(number, expire):
    payload = {
        "jsonrpc": "2.0",
        "id": "{{$randomInt}}",
        "method": "card.register",
        "params": {
            "number": number,
            "expire": expire
        }
    }
    return fire(payload)


def uzcard_verify(ext_id, code):
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "card.new.verify",
        "params": {
            "ext_id": ext_id,
            "code": code

        }
    }
    return fire(payload)



