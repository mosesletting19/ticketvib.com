from flask import Blueprint, request, jsonify
from models import db, Payment
from utils.safaricom import generate_password, get_access_token
import requests
from config import Config

payments_bp = Blueprint('payments', __name__)

@payments_bp.route('/pay', methods=['POST'])
def pay():
    data = request.json
    phone_number = data['phone']
    amount = data['amount']
    account_reference = "TicketPurchase"
    transaction_desc = "Payment for ticket"

    access_token = get_access_token()
    online_password, timestamp = generate_password()

    payload = {
        "BusinessShortCode": Config.SHORTCODE,
        "Password": online_password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": Config.SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": Config.CALLBACK_URL,
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post("https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest", json=payload, headers=headers)

    return jsonify(response.json())

@payments_bp.route('/callback', methods=['POST'])
def callback():
    data = request.json
    return jsonify({"message": "Callback received", "data": data})

@payments_bp.route('/payments', methods=['GET'])
def get_payments():
    payments = Payment.query.all()
    payments_list = [
        {
            "id": payment.id,
            "name": payment.name,
            "email": payment.email,
            "phone": payment.phone,
            "amount": payment.amount,
            "category": payment.category,
            "tickets": payment.tickets,
            "timestamp": payment.timestamp
        }
        for payment in payments
    ]
    return jsonify(payments_list)
