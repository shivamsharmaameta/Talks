from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import random
import json
import requests
from email.message import EmailMessage

app = Flask(__name__)
CORS(app)

otp_store = {}

FIREBASE_DB_URL = "https://chat-app-da6da-default-rtdb.asia-southeast1.firebasedatabase.app/users.json"  # replace this

SENDER_EMAIL = "shivamameta97@gmail.com"  # replace
APP_PASSWORD = "tjru mndg ybst gyie"     # replace

@app.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    otp = str(random.randint(100000, 999999))
    otp_store[email] = otp

    try:
        msg = EmailMessage()
        msg['Subject'] = "OTP Chat App"
        msg['From'] = SENDER_EMAIL
        msg['To'] = email
        msg.set_content(f"Hello,\n\nYour OTP is: {otp}\n\nThanks,\nShivam's App Team")

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(SENDER_EMAIL, APP_PASSWORD)
            server.send_message(msg)

        return jsonify({"message": "OTP sent"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')

    if otp_store.get(email) == otp:
        # Save to Firebase
        user_data = {"email": email}
        firebase = requests.post(FIREBASE_DB_URL, data=json.dumps(user_data))
        return jsonify({"message": "OTP verified and user registered"})
    else:
        return jsonify({"error": "Invalid OTP"}), 400

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
