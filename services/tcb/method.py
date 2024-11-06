import uuid
from .dragon import  basic_fire

"""RF->UZ"""
def service_info():
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "service.info",
        "params": {
            "rate": True,
            "commission": True

        }
    }

    return basic_fire(payload)


def card_register(ext_id):
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "card.add",
        "params": {
            "ext_id": ext_id
        }
    }
    return basic_fire(payload)


def register_card_state(ext_id):
    payload = {
        "jsonrpc": "2.0",
        "id":uuid.uuid4().__str__() ,
        "method": "card.state",
        "params": {
            "ext_id": ext_id
        }
    }
    return basic_fire(payload)

def card_state(ext_id):
    payload ={
            "jsonrpc": "2.0",
            "id": uuid.uuid4().__str__(),
            "method": "transfer.state",
            "params": {
                "ext_id": ext_id
            }
        }


    return basic_fire(payload)


def transfer_receiver_check(card_number, amount, currency):
    payload = {

        "method": "transfer.receiver.check",
        "id": uuid.uuid4().__str__(),
        "jsonrpc": "2.0",
        "params": {
            "number": card_number,
            "amount": amount,
            "currency": currency
        }
    }

    return basic_fire(payload)


def transfer_create(card_number, amount, currency,ext_id):
    payload = {
            "jsonrpc": "2.0",
            "id": uuid.uuid4().__str__(),
            "method": "transfer.create",
            "params": {
                "ext_id":ext_id,
                "number": card_number,
                "amount": amount,
                "currency": currency
            }
        }

    return basic_fire(payload)



def transfer_confirm(card_number, amount, currency):
    pass
"""UZ->RF"""


def transfer_sender_check(card_number,expire):
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "transfer.rf.sender.check",
        "params": {
            "card_number": card_number,
            "expire": expire
        }
    }
    return basic_fire(payload)
def receiver_check(card_number):
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "transfer.rf.receiver.check",
        "params": {
            "number": card_number,

        }

    }
    return basic_fire(payload)
def transfer_rf_create(card_number, amount, currency, ext_id,expire,receiver):
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "transfer.rf.create",
        "params": {
            "ext_id":ext_id,
            "number": card_number,
            "expire": expire,
            "amount": amount,
            "currency": currency,
            "receiver":receiver
        }
    }
    return basic_fire(payload)
def transfer_rf_confirm(ext_id):
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "transfer.rf.confirm",
        "params": {
            "ext_id": ext_id
        }
    }
    return basic_fire(payload)
def transfer_rf_state(ext_id):
    payload = {
        "jsonrpc": "2.0",
        "id": uuid.uuid4().__str__(),
        "method": "transfer.rf.state",
        "params": {
            "ext_id": ext_id
        }
    }
    return basic_fire(payload)