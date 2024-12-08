import requests
from django.conf import settings

headers = {
    "Authorization": f"{settings.SMS_API_KEY}",
    "Content-Type": "application/json"
}

def send_otp(mobile,otp):
    url = "https://api.sms.cx/otp"

    payload = {
        'api_key': 'vRSzlaQEo8KS21lEQslhwHHTGwHTnk66T8DXSw5x',
        'msg':otp,
        'to': mobile
    }
    response = requests.request("POST", url, data=payload)
    print("res",response)
    return response.json()