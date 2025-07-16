import requests
from django.conf import settings

def send_verification_code(phone, code):
    url = 'https://api.sms.ir/v1/send'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': settings.SMS_API_KEY
    }
    payload = {
        'mobile': phone,
        'message': f'کد تأیید شما: {code}'
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
