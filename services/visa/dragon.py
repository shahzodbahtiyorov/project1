visa_url = "http://visa-gateway-django.production.svc.cluster.local:8000/api/v1/jsonrpc"
basic_token = "d7138c75e2c534f4b0545ffdf3e71805397933ffdc33f9537e590c37b255caa1"
import requests
import json


def basic_fire(payload):
        payload = json.dumps(payload)
        headers = {

                'Authorization': f'Bearer {basic_token}',
                'Content-Type': 'application/json'
        }
        response = requests.post(visa_url, headers=headers, data=payload)
        return response.json()
