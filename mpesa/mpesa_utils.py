import base64
import requests
from requests.auth import HTTPBasicAuth
from decouple import config

def get_mpesa_access_token():
    consumer_key = config('MPESA_CONSUMER_KEY')
    consumer_secret = config('MPESA_CONSUMER_SECRET')
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    try:
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        mpesa_access_token = r.json().get('access_token')
        return mpesa_access_token
    except Exception as e:
        print(f"Failed to fetch access token: {e}")
        return None