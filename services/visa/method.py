from .dragon import basic_fire
import  uuid

def login(username, password):
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "login",
        "params": {
            "username": username,
            "password": password
        }
    }
    return basic_fire(payload)
def card_register(number, expire, is_otp=False):
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "card.register",
        "params": {
            "number": number,
            "expire": expire,
            "is_otp": is_otp

        }}
    return basic_fire(payload)
def card_confirm(ext_id,code):
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "card.register.confirm",
        "params": {
            "application_id": ext_id,
            "code": code
        }
    }
    return basic_fire(payload)

def card_details(card_token):
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "card.details",
        "params": {
            "card_token": card_token
        }
    }
    return basic_fire(payload)


def card_bins(card_number):
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "card.available",
        "params": {
            "number": card_number
        }
    }
    return basic_fire(payload)