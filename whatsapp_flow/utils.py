# import uuid
# from email_validator import validate_email, EmailNotValidError
# import phonenumbers
# from phonenumbers.phonenumberutil import NumberParseException
# import sqlite3
# import os
# from logger.custom_logger import setup_logger

# log = setup_logger()

# def is_valid_email(email: str) -> bool:
#     try:
#         validate_email(email)
#         return True
#     except EmailNotValidError:
#         return False

# def is_valid_phone_number(phone: str) -> bool:
#     try:
#         parsed_number = phonenumbers.parse(phone, None)
#         return phonenumbers.is_valid_number(parsed_number)
#     except NumberParseException:
#         return False

# def generate_id(email: str, phone: str) -> str:
#     if is_valid_email(email) and is_valid_phone_number(phone):
#         return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{email}-{phone}"))
#     return None

# def generate_temp_id(input_value: str) -> str:
#     return str(uuid.uuid5(uuid.NAMESPACE_DNS, input_value))

# def authentication_email(DB_PATH, email: str) -> int | None:
#     if not is_valid_email(email):
#         return None

#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             cursor = connection.cursor()
#             cursor.execute("SELECT client_id FROM clients WHERE email = ?", (email,))
#             result = cursor.fetchone()

#             return result[0] if result else None

#     except Exception as e:
#         log.error(f"Authentication error: {e}")
#         return None

# def is_list_meaningfully_empty(my_list):
#     return all(item.strip() == b'' for item in my_list)

# def authenticate_visitor(DB_PATH, email: str) -> str | None:
#     if not is_valid_email(email):
#         return None

#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             cursor = connection.cursor()
#             cursor.execute("SELECT visitor_id FROM visitors WHERE email = ?", (email,))
#             result = cursor.fetchone()

#             return result[0] if result else None

#     except Exception as e:
#         log.error(f"Visitor auth error: {e}")
#         return None



# /////////////////////////////////////////////////////////////////////////
import uuid
import sqlite3
import os
from email_validator import validate_email, EmailNotValidError
from logger.custom_logger import setup_logger
from config.config import DB_PATH

log = setup_logger()

def is_valid_email(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

# NOTE: no longer validating phone here for WhatsApp — not needed.
def is_valid_phone_number(phone: str) -> bool:
    return True  # Always true in WhatsApp context

def generate_id(email: str, phone: str) -> str:
    """
    Generates a stable UUID from email + phone (used as client_id or visitor_id).
    """
    if not email:
        email = "unknown@temp.com"
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{email}-{phone}"))

def generate_temp_id(value: str) -> str:
    """
    Generates a temp UUID based on phone number or email alone.
    """
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, value))

def authentication_email(DB_PATH, identifier: str):
    """
    Checks if a user is in the clients table using phone or email.
    Returns (client_id, flag) if found.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            if "@" in identifier:
                cursor.execute("SELECT client_id, flag FROM clients WHERE email = ?", (identifier,))
            else:
                cursor.execute("SELECT client_id, flag FROM clients WHERE phone = ?", (identifier,))

            result = cursor.fetchone()
            return result if result else None

    except Exception as e:
        log.error(f"authentication_email() error: {e}")
        return None

def authenticate_visitor(DB_PATH, identifier: str):
    """
    Checks if a visitor exists using email or phone.
    Returns visitor_id if found.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            if "@" in identifier:
                cursor.execute("SELECT visitor_id FROM visitors WHERE email = ?", (identifier,))
            else:
                cursor.execute("SELECT visitor_id FROM visitors WHERE phone = ?", (identifier,))

            result = cursor.fetchone()
            return result[0] if result else None

    except Exception as e:
        log.error(f"authenticate_visitor() error: {e}")
        return None

def is_list_meaningfully_empty(my_list):
    """
    Returns True if all items in the list are empty/blank.
    """
    return all(str(item).strip() == '' for item in my_list)


    
def authentication_user(DB_PATH, value: str):
    """Check client by email OR phone"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            if "@" in value:  # Email check
                cursor.execute("""
                    SELECT client_id, flag FROM clients 
                    WHERE email = ?
                """, (value,))
            else:  # Phone check
                # Normalize phone number (remove + and leading 0)
                normalized_phone = value.lstrip('+').lstrip('0')
                cursor.execute("""
                    SELECT client_id, flag FROM clients 
                    WHERE phone LIKE ? OR phone LIKE ?
                """, (f"%{normalized_phone}", f"%{value}"))
            
            result = cursor.fetchone()
            if result:
                return result  # (client_id, flag)
    except Exception as e:
        log.error(f"Authentication error: {e}")
    return None