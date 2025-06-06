import requests
import json
from logger.custom_logger import setup_logger

log = setup_logger(__name__)

class WhatsAppAPI:
    def __init__(self, api_url, api_key, phone_number_id):
        self.api_url = api_url
        self.api_key = api_key
        self.phone_number_id = phone_number_id

    def send_message(self, to, message):
        log.info("Sending WhatsApp message to %s", to)
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "text",
                "text": {"body": message}
            }

            url = f"{self.api_url}/{self.phone_number_id}/messages"
            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 200:
                log.info("WhatsApp message sent successfully.")
            else:
                log.error("Failed to send WhatsApp message: %s", response.text)

        except Exception as e:
            log.error("Exception during sending WhatsApp message: %s", e)

    def parse_incoming_message(self, data):
        log.info("Parsing incoming WhatsApp message")

        try:
            entry = data.get("entry", [])[0]
            changes = entry.get("changes", [])[0]
            value = changes.get("value", {})

            messages = value.get("messages", [])
            if not messages:
                log.warning("No message found in payload.")
                return None

            message = messages[0]
            sender = message.get("from")
            body = message.get("text", {}).get("body")

            return {"from": sender, "body": body}

        except Exception as e:
            log.error("Failed to parse WhatsApp message: %s", e)
            return None
