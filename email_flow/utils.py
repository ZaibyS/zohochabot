# import uuid
# from email_validator import validate_email, EmailNotValidError
# import phonenumbers
# from phonenumbers.phonenumberutil import NumberParseException
# import sqlite3
# import json
# import os

# from logger.custom_logger import setup_logger

# log = setup_logger()

# def is_valid_email(email: str) -> bool:
#     log.info(f"Validating email: {email}")
#     try:
#         validate_email(email)
#         log.info(f"Email {email} is valid.")
#         return True
#     except EmailNotValidError:
#         log.error(f"Email {email} is not valid.")
#         return False
    
# def is_valid_phone_number(phone: str) -> bool:
#     log.info(f"Validating phone number: {phone}")
#     try:
#         parsed_number = phonenumbers.parse(phone, None)
#         phonenumbers.is_valid_number(parsed_number)
#         log.info(f"Phone number {phone} is valid.")
#         return True
#     except NumberParseException:
#         log.error(f"Phone number {phone} is not valid.")
#         return False

# def generate_id(email: str, phone: str) -> str:
#     log.info(f"Generating ID for email: {email} and phone: {phone}")
#     if is_valid_email(email) and is_valid_phone_number(phone):
#         try:
#             name = f"{email}-{phone}"
#             id = str(uuid.uuid5(uuid.NAMESPACE_DNS, name))
#             log.info(f"Generated ID: {id}")
#             return id
#         except Exception as e:
#             log.error(f"Error generating ID: {e}")
#             return None
#     else:
#         log.error(f"Invalid email or phone number provided.")
#         return None
    
# def authentication_email(DB_PATH, email: str) -> int | None:
#     log.info(f"Authenticating user with email: {email}")
    
#     if not is_valid_email(email):
#         log.critical("Authentication aborted.")
#         return None

#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             cursor = connection.cursor()
#             log.info("Connected to database successfully.")
            
#             cursor.execute("SELECT client_id FROM clients WHERE email = ?", (email,))
#             result = cursor.fetchone()
            
#             if result:
#                 client_id = result[0]
#                 log.info("Authentication successful. Client ID: %s", client_id)
#                 return client_id
#             else:
#                 log.warning("Authentication failed. Email not found.")
#                 return None
    
#     except Exception as e:
#         log.error(f"Error during authentication: {e}")
#         return None

# def generate_temp_id(input_value: str) -> str:
#     log.info(f"Generating ID for input value: {input_value}")
    
#     if "@" in input_value:
#         if not is_valid_email(input_value):
#             log.error(f"Invalid email provided.")
#             return None
#     else:
#         if not is_valid_phone_number(input_value):
#             log.error(f"Invalid phone number provided.")
#             return None
    
#     try:
#         id = str(uuid.uuid5(uuid.NAMESPACE_DNS, input_value))
#         log.info(f"Generated ID: {id}")
#         return id
#     except Exception as e:
#         log.error(f"Error generating ID: {e}")
#         return None
    
# def is_list_meaningfully_empty(my_list):
#     return all(item.strip() == b'' for item in my_list)

# def authenticate_visitor(DB_PATH, email: str) -> str | None:
#     log.info(f"Authenticating visitor with email: {email}")
    
#     if not is_valid_email(email):
#         log.critical("Authentication aborted.")
#         return None

#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             cursor = connection.cursor()
#             log.info("Connected to database successfully.")
            
#             cursor.execute("SELECT visitor_id FROM visitors WHERE email = ?", (email,))
#             result = cursor.fetchone()
            
#             if result:
#                 visitor_id = result[0]
#                 log.info("Authentication successful. Visitor ID: %s", visitor_id)
#                 return visitor_id
#             else:
#                 log.warning("Authentication failed. Email not found.")
#                 return None
    
#     except Exception as e:
#         log.error(f"Error during authentication: {e}")
#         return None




# ///////////////////////////////////////////////////////////////////////////////////////////


import uuid
from email_validator import validate_email, EmailNotValidError
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
import sqlite3
import os
from logger.custom_logger import setup_logger
import re

log = setup_logger()


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
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{email}-{phone}"))
    return None


def generate_temp_id(value: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, value))


def is_list_meaningfully_empty(my_list):
    return all(item.strip() == b'' for item in my_list)


def authentication_email(DB_PATH, value: str):
    """Check client by email or phone."""
    is_email = "@" in value
    column = "email" if is_email else "phone"

    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT client_id, flag FROM clients WHERE {column} = ?", (value,))
            result = cursor.fetchone()
            if result:
                return result  # (client_id, flag)
    except Exception as e:
        log.error("Client authentication error: %s", e)

    return None



def authenticate_visitor(DB_PATH, value: str):
    """Check visitor by email or phone."""
    is_email = "@" in value
    column = "email" if is_email else "phone"

    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT visitor_id FROM visitors WHERE {column} = ?", (value,))
            result = cursor.fetchone()
            if result:
                return result[0]
    except Exception as e:
        log.error("Visitor authentication error: %s", e)

    return None
def update_visitor_phone(DB_PATH, email, phone):
    """Updates the visitor's phone number if it's a valid one."""
    log.info(f"Trying to update phone for visitor {email} to {phone}")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE visitors SET phone = ? WHERE email = ?", (phone, email))
            conn.commit()
            log.info("Visitor phone updated.")
            return True
    except Exception as e:
        log.error(f"Error updating visitor phone: {e}")
        return False

def try_promote_visitor_if_ready(DB_PATH, email):
    """Promotes a visitor to client if both email and phone exist."""
    log.info(f"Checking visitor {email} for promotion.")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT name, email, phone FROM visitors WHERE email = ?", (email,))
            result = cursor.fetchone()

            if not result:
                log.warning("Visitor not found.")
                return False

            name, email, phone = result
            if not name:
                name = "User"

            # Ensure both email and phone are valid
            from .tools_functions import promote_visitor_to_client
            from .utils import is_valid_email, is_valid_phone_number

            if is_valid_email(email) and is_valid_phone_number(phone):
                promote_visitor_to_client(email=email, phone=phone, name=name)
                log.info("Visitor promoted to client.")
                return True
            else:
                log.warning("Not enough info to promote visitor yet.")
                return False

    except Exception as e:
        log.error(f"Promotion check failed: {e}")
        return False




import uuid
import sqlite3
from email_validator import validate_email, EmailNotValidError
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from logger.custom_logger import setup_logger

from .db_flow_functions import insert_visitor, promote_visitor_to_client

log = setup_logger()


# ✅ Validation helpers
def is_valid_email(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False


def is_valid_phone(phone: str) -> bool:
    try:
        parsed = phonenumbers.parse(phone, None)
        return phonenumbers.is_valid_number(parsed)
    except NumberParseException:
        return False


# ✅ Generate permanent or temporary IDs


def generate_temp_id(value: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, value))


def generate_client_id(email: str, phone: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{email}-{phone}"))

# ✅ Utility
def is_list_meaningfully_empty(my_list):
    return all(item.strip() == b'' for item in my_list)


# ✅ Authentication checks
def authentication_email(DB_PATH, value: str):
    """Check client by email or phone."""
    is_email = "@" in value
    column = "email" if is_email else "phone"

    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT client_id, flag FROM clients WHERE {column} = ?", (value,))
            result = cursor.fetchone()
            if result:
                return result  # (client_id, flag)
    except Exception as e:
        log.error("Client authentication error: %s", e)

    return None


def authenticate_visitor(DB_PATH, value: str):
    """Check visitor by email or phone."""
    is_email = "@" in value
    column = "email" if is_email else "phone"

    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT visitor_id FROM visitors WHERE {column} = ?", (value,))
            result = cursor.fetchone()
            if result:
                return result[0]
    except Exception as e:
        log.error("Visitor authentication error: %s", e)

    return None


# ✅ Update phone for visitor
def update_visitor_phone(DB_PATH, email, phone):
    """Updates the visitor's phone number if it's a valid one."""
    log.info(f"Trying to update phone for visitor {email} to {phone}")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE visitors SET phone = ? WHERE email = ?", (phone, email))
            conn.commit()
            log.info("Visitor phone updated.")
            return True
    except Exception as e:
        log.error(f"Error updating visitor phone: {e}")
        return False

def authentication_phone(DB_PATH, phone: str):
    """
    Checks if a user exists in the clients table using their phone number.
    Returns (client_id, flag) if found, else None.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT client_id, flag FROM clients WHERE phone = ?", (phone,))
            result = cursor.fetchone()
            return result if result else None
    except Exception as e:
        log.error(f"authentication_phone() error: {e}")
        return None
def is_valid_phone_number(phone: str) -> bool:
    try:
        parsed = phonenumbers.parse(phone, None)
        return phonenumbers.is_valid_number(parsed)
    except NumberParseException:
        return False
def extract_phone_number(text):
    """Extracts phone number from text using simple pattern matching"""
    import re
    # Match international format (+countrycode) or local format (0...)
    pattern = r'(\+?\d{2,3}?\s?\d{3}\s?\d{3}\s?\d{4})'
    matches = re.findall(pattern, text)
    if matches:
        # Clean spaces and return first match
        return matches[0].replace(" ", "")
    return None  
# ✅ Promote visitor to client
def promote_visitor_to_client(phone: str, email: str, DB_PATH: str):
    """Promote visitor to client and delete visitor record"""
    client_id = generate_client_id(email, phone)
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            
            # Check if client already exists
            cursor.execute("""
                SELECT client_id FROM clients 
                WHERE email = ? OR phone LIKE ? OR phone LIKE ?
            """, (email, f"%{phone.lstrip('+')}", f"%{phone.lstrip('0')}"))
            if cursor.fetchone():
                return {"status": "exists", "message": "Client already exists"}
            
            # Insert into clients
            cursor.execute("""
                INSERT INTO clients (client_id, name, email, phone, flag)
                VALUES (?, ?, ?, ?, ?)
            """, (client_id, "Client", email, phone, False))
            
            # Delete from visitors (by email or phone)
            cursor.execute("""
                DELETE FROM visitors 
                WHERE email = ? OR phone = ?
            """, (email, phone))
            
            conn.commit()
            return {"status": "success", "client_id": client_id}
            
    except sqlite3.IntegrityError as e:
        return {"status": "exists", "message": str(e)}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    
def authentication_user(DB_PATH, value: str):
    """Check client by email OR phone"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            # Check if value is email or phone
            if "@" in value:  # Assume it's email
                cursor.execute("""
                    SELECT client_id, flag FROM clients 
                    WHERE email = ?
                """, (value,))
            else:  # Assume it's phone
                # Normalize phone number by removing + and leading 0 if needed
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

# //////////////////////////////////////////////////////////////////////////


# import uuid
# import sqlite3
# from email_validator import validate_email, EmailNotValidError
# import phonenumbers
# from phonenumbers.phonenumberutil import NumberParseException
# from logger.custom_logger import setup_logger

# log = setup_logger()

# def is_valid_email(email: str) -> bool:
#     try:
#         validate_email(email)
#         return True
#     except EmailNotValidError:
#         return False

# def is_valid_phone(phone: str) -> bool:
#     try:
#         parsed = phonenumbers.parse(phone, None)
#         return phonenumbers.is_valid_number(parsed)
#     except NumberParseException:
#         return False

# def generate_temp_id(value: str) -> str:
#     return str(uuid.uuid5(uuid.NAMESPACE_DNS, value))

# def generate_client_id(email: str, phone: str) -> str:
#     return str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{email}-{phone}"))

# def authentication_email(DB_PATH, email: str):
#     try:
#         with sqlite3.connect(DB_PATH) as conn:
#             cursor = conn.cursor()
#             cursor.execute("SELECT client_id, flag FROM clients WHERE email = ?", (email,))
#             return cursor.fetchone()  # (client_id, flag)
#     except Exception as e:
#         log.error("Client auth error: %s", e)
#         return None

# def authenticate_visitor(DB_PATH, email: str):
#     try:
#         with sqlite3.connect(DB_PATH) as conn:
#             cursor = conn.cursor()
#             cursor.execute("SELECT visitor_id FROM visitors WHERE email = ?", (email,))
#             result = cursor.fetchone()
#             return result[0] if result else None
#     except Exception as e:
#         log.error("Visitor auth error: %s", e)
#         return None
# # Add this to your utils.py file
# def is_list_meaningfully_empty(my_list):
#     """
#     Check if a list is empty or contains only empty strings/bytes
#     Returns True if all items are empty (after stripping), False otherwise
#     """
#     if not my_list:
#         return True
#     return all(
#         (isinstance(item, bytes) and item.strip() == b'') or 
#         (isinstance(item, str) and item.strip() == '')
#         for item in my_list
#     )
    
# def authentication_phone(DB_PATH, phone: str):
#     """
#     Checks if a user exists in the clients table using their phone number.
#     Returns (client_id, flag) if found, else None.
#     """
#     try:
#         with sqlite3.connect(DB_PATH) as conn:
#             cursor = conn.cursor()
#             cursor.execute("SELECT client_id, flag FROM clients WHERE phone = ?", (phone,))
#             result = cursor.fetchone()
#             return result if result else None
#     except Exception as e:
#         log.error(f"authentication_phone() error: {e}")
#         return None
# def is_valid_phone_number(phone: str) -> bool:
#     try:
#         parsed = phonenumbers.parse(phone, None)
#         return phonenumbers.is_valid_number(parsed)
#     except NumberParseException:
#         return False