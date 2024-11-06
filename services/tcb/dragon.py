import json
import requests
import hmac
import hashlib
import base64
from super_app import settings
basic_url = settings.dotenv_config.get('TEST_TCB_URL')
basic_token = settings.dotenv_config.get('TEST_TCB_TOKEN')
secret = settings.dotenv_config.get('TEST_TCB_SECRET')



def basic_fire(payload):
    payload_json = json.dumps(payload)


    digest = hmac.new(
        secret.encode(),
        payload_json.encode(),
        hashlib.sha256
    ).digest()

    digest_base64 = base64.b64encode(digest).decode()

    headers = {
        'Authorization': f'Bearer {basic_token}',
        'Content-Type': 'application/json',
        'Header-Login': 'SuperApp_test',
        'Header-Sign': digest_base64
    }

    print("**********UNIGATE*********")
    print("REQUEST: ", payload_json)


    try:
        response = requests.post(basic_url, headers=headers, data=payload_json)
        response.raise_for_status()

        print("RESPONSE: ", response.content)
        print("STATUS: ", response.status_code)

        return response.json()

    except requests.exceptions.Timeout:
        print("Request timed out. Please try again later.")
    except requests.exceptions.TooManyRedirects:
        print("Too many redirects. Check the URL.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    except json.JSONDecodeError:
        print("Failed to decode JSON response.")

    return None