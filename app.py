from flask import Flask, request, jsonify
import requests
import json
import time

app = Flask(__name__)

# تابع ارسال درخواست به تلگرام
def send_to_telegram(token, payload):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    # اگر payload شامل 'action' بود، یعنی تایپ ایندیکاتور
    if 'action' in payload:
        action_url = f"https://api.telegram.org/bot{token}/sendChatAction"
        requests.post(action_url, json=payload)
        return {"ok": True, "result": "typing"}
    
    # ارسال پیام معمولی
    response = requests.post(url, json=payload, timeout=30)
    return response.json()

# تابع ارسال کیبورد (همان متد بالا ولی با reply_markup)
def send_with_keyboard(token, payload):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    response = requests.post(url, json=payload, timeout=30)
    return response.json()

@app.route('/send', methods=['POST'])
def handle_send():
    try:
        data = request.json
        token = data.get('token')
        payload = data.get('payload')
        
        if not token or not payload:
            return jsonify({"error": "Missing token or payload"}), 400
        
        # اگر payload شامل action باشد (برای تایپ ایندیکاتور)
        if 'action' in payload:
            result = send_to_telegram(token, payload)
            return jsonify(result)
        
        # ارسال پیام با کیبورد
        result = send_with_keyboard(token, payload)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Telegram Proxy Service is running!"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
