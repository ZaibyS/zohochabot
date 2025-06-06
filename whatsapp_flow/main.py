from .prompts import system_prompt_client, system_prompt_visitor
from .flow import init, process_whatsapp_message
from .whatsapp_trigger import start_webhook
from config.config import (
    WHATSAPP_API_URL,
    WHATSAPP_ACCESS_TOKEN,
    WHATSAPP_PHONE_NUMBER_ID,
    DB_PATH,
    VERIFY_TOKEN
)
from config.config import WHATSAPP_ACCESS_TOKEN
print("🟢 Using Token Starts With:", WHATSAPP_ACCESS_TOKEN[:10])

if __name__ == "__main__":
    # Initialize WhatsApp API handler
    init(WHATSAPP_API_URL, WHATSAPP_ACCESS_TOKEN, WHATSAPP_PHONE_NUMBER_ID)

    # Define callback on incoming message
    def on_message(data):
        process_whatsapp_message(DB_PATH, system_prompt_client, system_prompt_visitor, data)

    # Start webhook server
    start_webhook(on_message, port=5000, verify_token=VERIFY_TOKEN)
    print("Webhook server started. Listening for incoming messages...")
