import requests
import base64
from datetime import datetime
from config import Config

def generate_password():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = Config.SHORTCODE + Config.PASSKEY + timestamp
    online_password = base64.b64encode(data_to_encode.encode()).decode('utf-8')
    return online_password, timestamp

def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(Config.CONSUMER_KEY, Config.CONSUMER_SECRET))
    access_token = response.json().get("access_token")
    return access_token
