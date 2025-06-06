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
#     log.info("Adding new visitor: %s with phone: %s and email: %s", name, phone, email)

#     if not is_valid_email(email):
#         log.critical("Invalid email format. Aborting visitor addition.")
#         return None

#     if not is_valid_phone_number(phone):
#         log.critical("Invalid phone format. Aborting visitor addition.")
#         return None

#     visitor_id = generate_id(email, phone)
#     temp_id = generate_temp_id(phone)

#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             cursor = connection.cursor()
#             log.info("Connected to database successfully.")

#             cursor.execute("""
#                 INSERT INTO visitors (visitor_id, name, email, phone, consent)
#                 VALUES (?, ?, ?, ?, ?)
#             """, (visitor_id, name, email, phone, int(consent)))
#             connection.commit()
#             log.info("Visitor added successfully.")

#             cursor.execute("UPDATE chat_history SET user_id = ? WHERE user_id = ?", (visitor_id, temp_id))
#             connection.commit()

#             os.environ["FLAG"] = 'false'
#             os.environ["USER_ID"] = visitor_id
#             log.info("Flag set to false and USER_ID updated.")

#             return json.dumps({"status": "success", "code": 200})

#     except sqlite3.IntegrityError as e:
#         log.error("Visitor already exists: %s", e)
#         return json.dumps({"status": "error", "message": "Visitor already exists", "code": 409})

#     except Exception as e:
#         log.error("Error adding visitor: %s", e)
#         return json.dumps({"status": "error", "message": str(e), "code": 500})

# def promote_visitor_to_client(email: str, phone: str, name: str):
#     log.info("Promoting visitor to client (WhatsApp)...")

#     if not is_valid_email(email) or not is_valid_phone_number(phone):
#         log.error("Invalid email or phone during promotion.")
#         return {"status": "error", "message": "Invalid email or phone."}

#     client_id = generate_id(email, phone)

#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             cursor = connection.cursor()
#             log.info("Connected to database for promotion.")

#             cursor.execute("""
#                 INSERT INTO clients (client_id, name, email, phone, flag)
#                 VALUES (?, ?, ?, ?, ?)
#             """, (client_id, name, email, phone, False))
#             connection.commit()

#             cursor.execute("DELETE FROM visitors WHERE phone = ?", (phone,))
#             connection.commit()

#             log.info("Visitor promoted to client with flag=False.")
#             return {"status": "success", "code": 200}

#     except sqlite3.IntegrityError as e:
#         log.error("Client already exists: %s", e)
#         return {"status": "error", "message": "Client already exists.", "code": 409}

#     except Exception as e:
#         log.error("Promotion error: %s", e)
#         return {"status": "error", "message": str(e), "code": 500}




# ///////////////////////////////////////////////////////////////////////////////////////////////////////

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
#     log.info("Adding new visitor: %s with phone: %s and email: %s", name, phone, email)

#     if not is_valid_email(email) or not is_valid_phone_number(phone):
#         log.critical("Invalid email or phone. Aborting visitor addition.")
#         return None

#     visitor_id = generate_id(email, phone)
#     temp_id = generate_temp_id(phone)

#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             cursor = connection.cursor()

#             cursor.execute("""
#                 INSERT INTO visitors (visitor_id, name, email, phone, consent)
#                 VALUES (?, ?, ?, ?, ?)
#             """, (visitor_id, name, email, phone, int(consent)))
#             connection.commit()

#             cursor.execute("UPDATE chat_history SET user_id = ? WHERE user_id = ?", (visitor_id, temp_id))
#             connection.commit()

#             os.environ["FLAG"] = 'false'
#             os.environ["USER_ID"] = visitor_id

#             return json.dumps({"status": "success", "code": 200})

#     except sqlite3.IntegrityError as e:
#         log.error("Visitor already exists: %s", e)
#         return json.dumps({"status": "error", "message": "Visitor already exists", "code": 409})

#     except Exception as e:
#         log.error("Error adding visitor: %s", e)
#         return json.dumps({"status": "error", "message": str(e), "code": 500})


# def promote_visitor_to_client(email: str, phone: str, name: str):
#     log.info("Promoting visitor to client...")

#     if not is_valid_email(email) or not is_valid_phone_number(phone):
#         log.error("Invalid email or phone during promotion.")
#         return {"status": "error", "message": "Invalid email or phone."}

#     client_id = generate_id(email, phone)

#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             cursor = connection.cursor()

#             cursor.execute("""
#                 INSERT INTO clients (client_id, name, email, phone, flag)
#                 VALUES (?, ?, ?, ?, ?)
#             """, (client_id, name, email, phone, False))
#             connection.commit()

#             cursor.execute("DELETE FROM visitors WHERE phone = ?", (phone,))
#             connection.commit()

#             return {"status": "success", "code": 200}

#     except sqlite3.IntegrityError as e:
#         log.error("Client already exists: %s", e)
#         return {"status": "error", "message": "Client already exists.", "code": 409}

#     except Exception as e:
#         log.error("Promotion error: %s", e)
#         return {"status": "error", "message": str(e), "code": 500}


# # ✅ NEW: update visitor's email (for WhatsApp flow)
# def update_visitor_email(DB_PATH, visitor_id, email):
#     if not is_valid_email(email):
#         log.error("Invalid email format")
#         return False

#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             cursor = connection.cursor()
#             cursor.execute("UPDATE visitors SET email = ? WHERE visitor_id = ?", (email, visitor_id))
#             connection.commit()
#             log.info("Visitor email updated successfully.")
#             return True
#     except Exception as e:
#         log.error("Failed to update visitor email: %s", e)
#         return False


# # ✅ NEW: promote if visitor has both phone and email
# def try_promote_visitor_if_ready(visitor_id):
#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             cursor = connection.cursor()
#             cursor.execute("SELECT name, email, phone FROM visitors WHERE visitor_id = ?", (visitor_id,))
#             row = cursor.fetchone()

#             if row:
#                 name, email, phone = row
#                 if is_valid_email(email) and is_valid_phone_number(phone):
#                     return promote_visitor_to_client(email=email, phone=phone, name=name)
#                 else:
#                     log.info("Visitor not ready for promotion — missing valid email or phone.")
#                     return {"status": "waiting", "message": "Still waiting for valid email/phone."}
#             else:
#                 log.warning("Visitor not found by visitor_id.")
#                 return {"status": "error", "message": "Visitor not found"}
#     except Exception as e:
#         log.error("Error in try_promote_visitor_if_ready: %s", e)
#         return {"status": "error", "message": str(e), "code": 500}





# ///////////////////////////////////////////////////////////////////////////////////////////////////////


# tools_functions.py
# import os
# import sqlite3
# import json
# from .utils import is_valid_email, generate_id, generate_temp_id
# from config.config import DB_PATH
# from logger.custom_logger import setup_logger

# log = setup_logger()


# def retrieve_experts():
#     """
#     Fetch all expert records from the database.
#     """
#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             cursor = connection.cursor()
#             cursor.execute("SELECT * FROM experts")
#             column_names = [desc[0] for desc in cursor.description]
#             rows = cursor.fetchall()
#             return [dict(zip(column_names, row)) for row in rows]
#     except Exception as e:
#         log.error("Error retrieving experts: %s", e)
#         return {"status": "error", "message": str(e), "code": 500}


# def add_visitor(name: str, email: str, phone: str, consent: bool):
#     """
#     Adds a visitor using phone. Email may be blank. visitor_id == temp_id at this stage.
#     """
#     log.info("Adding new visitor with phone: %s, email: %s", phone, email)

#     # Create temp_id as visitor_id initially
#     visitor_id = generate_temp_id(phone)
#     temp_id = visitor_id

#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             cursor = connection.cursor()

#             cursor.execute("""
#                 INSERT INTO visitors (visitor_id, name, email, phone, consent)
#                 VALUES (?, ?, ?, ?, ?)
#             """, (visitor_id, name, email, phone, int(consent)))
#             connection.commit()

#             cursor.execute("UPDATE chat_history SET user_id = ? WHERE user_id = ?", (visitor_id, temp_id))
#             connection.commit()

#             os.environ["USER_ID"] = visitor_id
#             os.environ["FLAG"] = "false"

#             return json.dumps({"status": "success", "code": 200})

#     except sqlite3.IntegrityError:
#         log.warning("Visitor already exists for phone: %s", phone)
#         return json.dumps({"status": "error", "message": "Visitor already exists", "code": 409})

#     except Exception as e:
#         log.error("Failed to add visitor: %s", str(e))
#         return json.dumps({"status": "error", "message": str(e), "code": 500})


# def update_visitor_email(DB_PATH, visitor_id, email):
#     """
#     Updates visitor's email only if it's valid.
#     """
#     if not is_valid_email(email):
#         return False

#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             cursor = connection.cursor()
#             cursor.execute("UPDATE visitors SET email = ? WHERE visitor_id = ?", (email, visitor_id))
#             connection.commit()
#             return True
#     except Exception as e:
#         log.error("Failed to update visitor email: %s", e)
#         return False


# def promote_visitor_to_client(email: str, phone: str, name: str):
#     """
#     Promotes a visitor to client. Uses email+phone to generate client_id.
#     """
#     if not is_valid_email(email):
#         return {"status": "error", "message": "Invalid email"}

#     client_id = generate_id(email, phone)

#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             cursor = connection.cursor()

#             cursor.execute("""
#                 INSERT INTO clients (client_id, name, email, phone, flag)
#                 VALUES (?, ?, ?, ?, ?)
#             """, (client_id, name, email, phone, False))
#             connection.commit()

#             cursor.execute("DELETE FROM visitors WHERE phone = ?", (phone,))
#             connection.commit()

#             return {"status": "success", "code": 200}

#     except sqlite3.IntegrityError:
#         return {"status": "error", "message": "Client already exists", "code": 409}
#     except Exception as e:
#         return {"status": "error", "message": str(e), "code": 500}


# def try_promote_visitor_if_ready(visitor_id):
#     """
#     Checks if visitor is eligible for promotion (valid email must exist).
#     """
#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             cursor = connection.cursor()
#             cursor.execute("SELECT name, email, phone FROM visitors WHERE visitor_id = ?", (visitor_id,))
#             row = cursor.fetchone()

#             if not row:
#                 return {"status": "error", "message": "Visitor not found"}

#             name, email, phone = row

#             if is_valid_email(email):
#                 return promote_visitor_to_client(email=email, phone=phone)

#             return {"status": "waiting", "message": "Email missing or invalid"}

#     except Exception as e:
#         log.error("Failed to auto-promote visitor: %s", e)
#         return {"status": "error", "message": str(e), "code": 500}


import sqlite3
from .utils import is_valid_email
from logger.custom_logger import setup_logger
from config.config import DB_PATH
from logger.custom_logger import setup_logger

log = setup_logger(__name__)

def retrieve_experts(DB_PATH):
    """
    Fetch all expert records from the database.
    """
    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM experts")
            column_names = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(column_names, row)) for row in rows]
    except Exception as e:
        log.error("Error retrieving experts: %s", e)
        return {"status": "error", "message": str(e), "code": 500}


def add_visitor(visitor_id, name, email, phone, consent, DB_PATH):
    """
    Inserts a new visitor into the visitors table.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO visitors (visitor_id, name, email, phone, consent)
                VALUES (?, ?, ?, ?, ?)
            """, (visitor_id, name, email, phone, consent))
            conn.commit()
        return {"status": "success", "message": "Visitor added"}
    except sqlite3.IntegrityError as e:
        log.warning("Visitor already exists: %s", e)
        return {"status": "exists", "message": "Visitor already exists"}
    except Exception as e:
        log.error("Error adding visitor: %s", e)
        return {"status": "error", "message": str(e)}


import sqlite3
from .utils import is_valid_email
from logger.custom_logger import setup_logger

log = setup_logger(__name__)

def promote_visitor_to_client(phone, email, DB_PATH):
    """
    Promotes visitor directly to clients table and removes from visitors.
    Sets flag = False upon promotion. Pulls name from visitors table.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            # 🔍 Get visitor name
            cursor.execute("SELECT name FROM visitors WHERE phone = ?", (phone,))
            row = cursor.fetchone()

            if not row:
                log.warning("Visitor not found for phone: %s", phone)
                return {"status": "error", "message": "Visitor not found"}

            name = row[0] or "WhatsApp User"

            # 🚀 Insert into clients
            cursor.execute("""
                INSERT INTO clients (name, email, phone, flag)
                VALUES (?, ?, ?, ?)
            """, (name, email, phone, False))

            # 🧹 Remove from visitors
            cursor.execute("DELETE FROM visitors WHERE phone = ?", (phone,))
            conn.commit()

        log.info("✅ Visitor promoted to client: %s", phone)
        return {"status": "success", "message": "Visitor promoted to client"}

    except sqlite3.IntegrityError as e:
        log.warning("⚠️ Client already exists for phone: %s | %s", phone, e)
        return {"status": "exists", "message": "Already in clients"}

    except Exception as e:
        log.error("❌ Error during promotion: %s", e)
        return {"status": "error", "message": str(e)}


def try_promote_visitor_if_ready(visitor_id, DB_PATH):
    """
    If a visitor has a valid email, promotes them to a client.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT email, phone FROM visitors WHERE visitor_id = ?
            """, (visitor_id,))
            row = cursor.fetchone()

            if not row:
                return {"status": "error", "message": "Visitor not found"}

            email, phone = row

            if not is_valid_email(email):
                return {"status": "waiting", "message": "Invalid or missing email"}

            return promote_visitor_to_client(phone, email, DB_PATH)

    except Exception as e:
        log.error("❌ Error in try_promote_visitor_if_ready: %s", e)
        return {"status": "error", "message": str(e)}
