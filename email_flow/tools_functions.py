# import os
# import sqlite3
# import json
# from .utils import is_valid_email, is_valid_phone_number, generate_id, generate_temp_id

# from config.config import DB_PATH
# from logger.custom_logger import setup_logger

# log = setup_logger()

# def retrieve_experts():
#     log.info("Retrieving experts from database...")
#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             cursor = connection.cursor()
#             log.info("Connected to database successfully.")

#             cursor.execute("SELECT * FROM experts")
#             column_names = [description[0] for description in cursor.description]
#             experts = cursor.fetchall()
#             log.info("Experts retrieved successfully.")
#             return [dict(zip(column_names, row)) for row in experts]
    
#     except sqlite3.Error as e:
#         log.error("Failed to retrieve experts: %s", e)
#         return {"status": "error", "message": str(e), "code": 500}
    
#     except Exception as e:
#         log.error("Unexpected error: %s", e)
#         return {"status": "error", "message": str(e), "code": 500}
    
# def add_visitor(name: str, email: str, phone: str, consent: bool):
#     log.info("Adding new visitor: %s with email: %s and phone: %s", name, email, phone)
    
#     if not is_valid_email(email):
#         log.critical("Process: Adding visitor aborted.")
#         return None
    
#     if not is_valid_phone_number(phone):
#         log.critical("Process: Adding visitor aborted.")
#         return None
    
#     visitor_id = generate_id(email, phone)
#     temp_id = generate_temp_id(email)

#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             cursor = connection.cursor()
#             log.info("Connected to database successfully.")
            
#             cursor.execute("INSERT INTO visitors (visitor_id, name, email, phone, consent) VALUES (?, ?, ?, ?, ?)",
#                         (visitor_id, name, email, phone, int(consent)))
#             connection.commit()
#             log.info("Visitor added successfully.")

#             cursor.execute("UPDATE chat_history SET user_id = ? WHERE user_id = ?", (visitor_id, temp_id))
#             connection.commit()

#             os.environ["FLAG"] = 'false'
#             os.environ["USER_ID"] = visitor_id
#             log.info("Flag set to false and USER_ID updated.")

#             return json.dumps({"status": "success", "code": 200})
    
#     except sqlite3.IntegrityError as e:
#         log.error(f"Visitor already exists: {e}")
#         return json.dumps({"status": "error", "message": "Visitor already exists", "code": 409})
    
#     except Exception as e:
#         log.error(f"Error adding visitor: {e}")
#         return json.dumps({"status": "error", "message": str(e), "code": 500})


# import os
# import sqlite3
# import json
# from .utils import is_valid_email, is_valid_phone_number, generate_id, generate_temp_id
# from config.config import DB_PATH
# from logger.custom_logger import setup_logger

# log = setup_logger()

# def retrieve_experts():
#     log.info("Retrieving experts from database...")
#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             cursor = connection.cursor()
#             log.info("Connected to database successfully.")

#             cursor.execute("SELECT * FROM experts")
#             column_names = [description[0] for description in cursor.description]
#             experts = cursor.fetchall()
#             log.info("Experts retrieved successfully.")
#             return [dict(zip(column_names, row)) for row in experts]
    
#     except sqlite3.Error as e:
#         log.error("Failed to retrieve experts: %s", e)
#         return {"status": "error", "message": str(e), "code": 500}
    
#     except Exception as e:
#         log.error("Unexpected error: %s", e)
#         return {"status": "error", "message": str(e), "code": 500}

# def add_visitor(name: str, email: str, phone: str, consent: bool):
#     log.info("Adding new visitor: %s with email: %s and phone: %s", name, email, phone)
    
#     if not is_valid_email(email):
#         log.critical("Process: Adding visitor aborted.")
#         return None
    
#     if not is_valid_phone_number(phone):
#         log.critical("Process: Adding visitor aborted.")
#         return None
    
#     visitor_id = generate_id(email, phone)
#     temp_id = generate_temp_id(email)

#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             cursor = connection.cursor()
#             log.info("Connected to database successfully.")
            
#             cursor.execute("INSERT INTO visitors (visitor_id, name, email, phone, consent) VALUES (?, ?, ?, ?, ?)",
#                         (visitor_id, name, email, phone, int(consent)))
#             connection.commit()
#             log.info("Visitor added successfully.")

#             cursor.execute("UPDATE chat_history SET user_id = ? WHERE user_id = ?", (visitor_id, temp_id))
#             connection.commit()

#             os.environ["FLAG"] = 'false'
#             os.environ["USER_ID"] = visitor_id
#             log.info("Flag set to false and USER_ID updated.")

#             return json.dumps({"status": "success", "code": 200})
    
#     except sqlite3.IntegrityError as e:
#         log.error(f"Visitor already exists: {e}")
#         return json.dumps({"status": "error", "message": "Visitor already exists", "code": 409})
    
#     except Exception as e:
#         log.error(f"Error adding visitor: {e}")
#         return json.dumps({"status": "error", "message": str(e), "code": 500})

# def promote_visitor_to_client(email: str, phone: str, name: str):
#     """
#     Move a visitor to the clients table with flag=False (not fully onboarded).
#     This assumes phone is newly provided and valid.
#     """
#     if not is_valid_email(email) or not is_valid_phone_number(phone):
#         log.error("Invalid email or phone during promotion.")
#         return {"status": "error", "message": "Invalid email or phone."}

#     client_id = generate_id(email, phone)

#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             cursor = connection.cursor()
#             log.info("Connected to database for promotion.")

#             # Insert into clients with flag=False
#             cursor.execute("""
#                 INSERT INTO clients (client_id, name, email, phone, flag)
#                 VALUES (?, ?, ?, ?, ?)
#             """, (client_id, name, email, phone, False))
#             connection.commit()

#             # Delete from visitors
#             cursor.execute("DELETE FROM visitors WHERE email = ?", (email,))
#             connection.commit()

#             log.info("Visitor promoted to client with flag=False.")
#             return {"status": "success", "code": 200}

#     except sqlite3.IntegrityError as e:
#         log.error("Client already exists: %s", e)
#         return {"status": "error", "message": "Client already exists.", "code": 409}
#     except Exception as e:
#         log.error("Promotion error: %s", e)
#         return {"status": "error", "message": str(e), "code": 500}



# /////////////////////////////////////////////////////////////////////////////////


import os
import sqlite3
import json
from .utils import is_valid_email, is_valid_phone_number, generate_id, generate_temp_id
from config.config import DB_PATH
from logger.custom_logger import setup_logger

log = setup_logger()


def retrieve_experts():
    log.info("Retrieving experts from database...")
    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            log.info("Connected to database successfully.")

            cursor.execute("SELECT * FROM experts")
            column_names = [description[0] for description in cursor.description]
            experts = cursor.fetchall()
            log.info("Experts retrieved successfully.")
            return [dict(zip(column_names, row)) for row in experts]

    except Exception as e:
        log.error("Failed to retrieve experts: %s", e)
        return {"status": "error", "message": str(e), "code": 500}


def add_visitor(name: str, email: str, phone: str, consent: bool):
    log.info("Adding new visitor: %s, email: %s, phone: %s", name, email, phone)

    if not is_valid_email(email) or not is_valid_phone_number(phone):
        log.critical("Invalid email or phone. Aborting visitor creation.")
        return None

    visitor_id = generate_id(email, phone)
    temp_id = generate_temp_id(email)

    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            log.info("Connected to database.")

            cursor.execute("""
                INSERT INTO visitors (visitor_id, name, email, phone, consent)
                VALUES (?, ?, ?, ?, ?)
            """, (visitor_id, name, email, phone, int(consent)))
            connection.commit()

            cursor.execute("UPDATE chat_history SET user_id = ? WHERE user_id = ?", (visitor_id, temp_id))
            connection.commit()

            os.environ["FLAG"] = "false"
            os.environ["USER_ID"] = visitor_id

            log.info("Visitor added with temporary ID. Awaiting promotion.")
            return json.dumps({"status": "success", "code": 200})

    except sqlite3.IntegrityError as e:
        log.warning("Visitor may already exist: %s", e)
        return json.dumps({"status": "error", "message": "Visitor already exists", "code": 409})

    except Exception as e:
        log.error("Failed to add visitor: %s", e)
        return json.dumps({"status": "error", "message": str(e), "code": 500})


# def promote_visitor_to_client(email: str, phone: str, name: str):
#     log.info("Promoting visitor to client...")

#     if not is_valid_email(email) or not is_valid_phone_number(phone):
#         log.error("Invalid email or phone for promotion.")
#         return {"status": "error", "message": "Invalid email or phone."}

#     client_id = generate_id(email, phone)

#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             cursor = connection.cursor()
#             log.info("Connected to database.")

#             cursor.execute("""
#                 INSERT INTO clients (client_id, name, email, phone, flag)
#                 VALUES (?, ?, ?, ?, ?)
#             """, (client_id, name, email, phone, False))
#             connection.commit()

#             cursor.execute("DELETE FROM visitors WHERE phone = ? OR email = ?", (phone, email))
#             connection.commit()

#             log.info("Visitor promoted successfully.")
#             return {"status": "success", "code": 200}

#     except sqlite3.IntegrityError as e:
#         log.warning("Client already exists: %s", e)
#         return {"status": "error", "message": "Client already exists", "code": 409}

#     except Exception as e:
#         log.error("Error promoting visitor: %s", e)
#         return {"status": "error", "message": str(e), "code": 500}


# def update_visitor_phone(email: str, phone: str):
#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             cursor = connection.cursor()
#             cursor.execute("UPDATE visitors SET phone = ? WHERE email = ?", (phone, email))
#             connection.commit()
#             log.info("✅ Visitor phone updated.")
#     except Exception as e:
#         log.error("❌ Failed to update visitor phone: %s", e)


# def try_promote_visitor_if_ready(email: str):
#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             cursor = connection.cursor()
#             cursor.execute("SELECT name, phone FROM visitors WHERE email = ?", (email,))
#             row = cursor.fetchone()
#             if row:
#                 name, phone = row
#                 if phone and is_valid_phone_number(phone):
#                     return promote_visitor_to_client(email=email, phone=phone, name=name)
#     except Exception as e:
#         log.error("Failed to promote visitor after validation: %s", e)
