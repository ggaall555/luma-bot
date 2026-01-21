from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# בדיקה שהשרת חי
@app.route("/", methods=["GET"])
def home():
    return "LUMA bot is running 🤖✨", 200


# Webhook של WhatsApp
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    try:
        # חילוץ הודעה נכנסת
        message = (
            data["entry"][0]["changes"][0]["value"]
            ["messages"][0]["text"]["body"]
        )
        sender = (
            data["entry"][0]["changes"][0]["value"]
            ["messages"][0]["from"]
        )

        print("📩 הודעה נכנסת:", message)
        print("👤 מאת:", sender)

        # תשובת בוט בסיסית (זמנית)
        reply_text = (
            "היי 👋\n"
            "אני LUMA 🤖\n"
            "עוזרת ה-AI שלך למציאת מוצרים באליאקספרס 🛒✨\n\n"
            "פשוט תכתבי מה את מחפשת,\n"
            "ואני אמצא עבורך מוצרים מומלצים עם דירוגים טובים ⭐"
        )

        send_whatsapp_message(sender, reply_text)

    except Exception as e:
        print("❌ שגיאה:", e)

    return jsonify(status="ok"), 200


def send_whatsapp_message(to, text):
    import requests

    phone_number_id = os.environ.get("PHONE_NUMBER_ID")
    access_token = os.environ.get("WHATSAPP_TOKEN")

    url = f"https://graph.facebook.com/v19.0/{phone_number_id}/messages"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {
            "body": text
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    print("📤 נשלחה תשובה:", response.status_code, response.text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
