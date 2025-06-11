# src/bot_flow/utils.py

import uuid
from langdetect import detect
from email_validator import validate_email, EmailNotValidError
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from PyPDF2 import PdfReader
import re

from logger.custom_logger import setup_logger
log = setup_logger()

def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

def extract_key_terms(text):
    # Simple keyword extractor
    sectors = re.findall(r"(technology|healthcare|finance|energy)", text.lower())
    companies = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b", text)
    countries = re.findall(r"\b(?:United\s+States|Canada|Germany|France|Japan)\b", text)
    return {
        "sectors": list(set(sectors)),
        "companies": list(set(companies)),
        "countries": list(set(countries))
    }

def is_valid_email(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def is_valid_phone_number(phone: str) -> bool:
    try:
        parsed = phonenumbers.parse(phone, None)
        return phonenumbers.is_valid_number(parsed)
    except NumberParseException:
        return False

def generate_id(email: str, phone: str) -> str:
    if is_valid_email(email) and is_valid_phone_number(phone):
        try:
            name = f"{email}-{phone}"
            return str(uuid.uuid5(uuid.NAMESPACE_DNS, name))
        except Exception as e:
            print(e)
            return None
    return None