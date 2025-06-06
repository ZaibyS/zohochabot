from flask import Flask, request
from logger.custom_logger import setup_logger

log = setup_logger(__name__)
app = Flask(__name__)
incoming_message_callback = None
VERIFY_TOKEN = None

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    """
    Webhook endpoint for WhatsApp Cloud API.
    Handles both verification (GET) and message receipt (POST).
    """
    global VERIFY_TOKEN

    if request.method == "GET":
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if verify_token == VERIFY_TOKEN:
            log.info("✅ Webhook verified successfully with token.")
            return challenge, 200
        else:
            log.warning("❌ Webhook verification failed.")
            return "Invalid verification token", 403

    elif request.method == "POST":
        data = request.get_json(force=True)
        if not data:
            log.warning("⚠️ Received empty or malformed JSON payload.")
            return "Invalid payload", 400

        log.info("📨 Received WhatsApp message payload: %s", data)

        if incoming_message_callback:
            try:
                incoming_message_callback(data)
            except Exception as e:
                log.error("❌ Error in callback execution: %s", e)
                return "Callback error", 500
        else:
            log.warning("⚠️ No incoming message callback set.")

        return "OK", 200

@app.route("/", methods=["GET"])
def root():
    return "✅ WhatsApp Webhook Server is running!", 200

def start_webhook(callback, port=5005, verify_token=None):
    """
    Starts the webhook Flask server.
    """
    global incoming_message_callback, VERIFY_TOKEN
    incoming_message_callback = callback
    VERIFY_TOKEN = verify_token

    log.info(f"🚀 Starting WhatsApp webhook server on port {port} with token verification.")
    app.run(host="0.0.0.0", port=port)

