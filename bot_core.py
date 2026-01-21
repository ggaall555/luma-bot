from flask import Flask, request
import os

app = Flask(__name__)

VERIFY_TOKEN = "luma_verify_token"

@app.route("/")
def index():
    return "LUMA bot is running 🤖✨", 200


@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Forbidden", 403

    if request.method == "POST":
        data = request.get_json()
        print("Incoming webhook:", data)
        return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
