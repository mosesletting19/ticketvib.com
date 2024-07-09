import os
from flask import Flask, request, jsonify
from mpesa_handler import MpesaHandler
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
shortcode = os.getenv("SHORTCODE")
passkey = os.getenv("PASSKEY")
callback_url = os.getenv("CALLBACK_URL")

mpesa = MpesaHandler(consumer_key, consumer_secret, shortcode, passkey)

@app.route('/')
def home():
    return "Flask App is running"

@app.route('/initiate-payment', methods=['POST'])
def initiate_payment():
    data = request.json
    phone = data.get('phone')
    amount = data.get('amount')
    response = mpesa.lipa_na_mpesa_online(phone, amount, callback_url)
    return jsonify(response)

@app.route('/callback', methods=['POST'])
def callback():
    data = request.json
    # Log the callback data to verify
    print("Callback received:", data)
    # Process the callback data here
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3400, debug=True)
