import os

import requests
from werkzeug.security import generate_password_hash

MERCHANT = os.getenv('MERCHANT_ID')


def send_request(amount, email, mobile, call_back_url, description):
    url = os.getenv('ZARINPAL_WEBSERVICE')
    data = {
        'merchant_id': MERCHANT,
        'amount': amount,
        'callback_url': call_back_url,
        'description': description,
        'metadata': {
            'email': email,
            'mobile': mobile
        }
    }
    return requests.post(url, json=data, headers={'Content-Type': 'application/json'})


def verify(authority, amount):
    url = os.getenv('ZARINPAL_VERIFICATION_GATE')
    data = {
        'merchant_id': MERCHANT,
        'authority': authority,
        'amount': amount
    }
    return requests.post(url, json=data)
