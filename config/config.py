import os
from dotenv import load_dotenv
from logger.custom_logger import setup_logger

logger = setup_logger()
load_dotenv()
from pathlib import Path
from autogen import config_list_from_json, LLMConfig
# Load .env from the same directory as config.py
load_dotenv(Path(__file__).parent / '.env')
try:
    logger.info("Loading environment variables from .env file.")
    EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT")
    EMAIL_APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")
    IMAP_SERVER = os.getenv("IMAP_SERVER")
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    DB_PATH = os.getenv("DB_PATH")
    MODEL_NAME = os.getenv("MODEL_NAME")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # WhatsApp Cloud API Configuration
    WHATSAPP_API_URL = os.getenv("WHATSAPP_API_URL")
    WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")

    VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
    # Database Path
    DB_PATH = os.getenv("DB_PATH")

    # Headers for WhatsApp API
    HEADERS = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }


    llm_config = LLMConfig(
            api_type="openai",
            api_key=OPENAI_API_KEY,
            model=MODEL_NAME
    )
except:
    logger.error("Failed to load environment variables. Please check your .env file.")



