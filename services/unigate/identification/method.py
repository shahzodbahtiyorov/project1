import os
import requests
from django.http import JsonResponse

from super_app import settings


def get_access_token(code):
    print(settings.dotenv_config.get('MY_ID_GRANT_TYPE'),"$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print(settings.dotenv_config.get('MY_ID_CLIENT_ID'),"$#$@#$$$$$$$$$$$$$$$$$$$$$$@")
    print(settings.dotenv_config.get('MY_ID_CLIENT_SECRET_KEY'),"%%%%%%%%%%%$#%#$%#$%#$%#$%#$%")


    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = f"grant_type={settings.dotenv_config.get('MY_ID_GRANT_TYPE')}&code={code}&client_id={settings.dotenv_config.get('MY_ID_CLIENT_ID')}&client_secret={settings.dotenv_config.get('MY_ID_CLIENT_SECRET_KEY')}"

    endpoint = 'api/v1/oauth2/access-token'

    print(payload,"bu payload")

    try:
        print(f"Making request to: {settings.dotenv_config.get('MY_ID_URL')+endpoint}")
        response = requests.post(settings.dotenv_config.get('MY_ID_URL') + endpoint,
                                 headers=headers, data=payload)
        print(response.text,"bu ###########################################")

        response.raise_for_status()
        response_data = response.json()


    except ValueError:
        return {
            'message': f"Invalid JSON response: {response.text}"
        }

    return response_data


def get_user_profile(access_token):
    endpoint = 'api/v1/users/me'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    profile_response = requests.get(settings.dotenv_config.get('MY_ID_URL') + endpoint,
                                    headers=headers)
    print(profile_response.text,"%%%%%%%%%%%%%%%%%%%%%")
    profile_data = profile_response.json()

    return profile_data
