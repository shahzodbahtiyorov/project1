from super_app.requests_control.requests import acciodef create_wallet_util(phone_number):    payload = {        "id": "{{$randomUUID}}",        "method": "wallet.create",        "params": {            "name": "super card",            "phone": f"{phone_number}",            "wallet_name": f"Super app {phone_number}-card",            "type": 0        }    }    try:        data = accio(payload, 'ucoin')    except:        return {'result': {'card_number': '0000', 'expire': '0000'}}    if data['status']:        return data