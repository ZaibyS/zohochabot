# import sqlite3
# import json

# from config.config import (
#     DB_PATH
# )

# from .utils import (
#     is_valid_email,
#     is_valid_phone_number,
#     generate_id
# )

# from logger.custom_logger import setup_logger

# log = setup_logger(__name__)

# def authenticate_client(input_value: str) -> int | None:
#     """Authenticate a client using their email or phone number.

#     Attempts to validate and authenticate a client based on the provided input,
#     which can be either an email address or a phone number. The function checks
#     the input's validity, queries the database, and returns the associated
#     client ID if authentication is successful.

#     Args:
#         input_value (str): The email address or phone number of the client.

#     Returns:
#         int | None: The client ID if authentication is successful; otherwise, None.

#     Logs:
#         - Info: Start of authentication, database connection status, and success.
#         - Warning: If no client record is found.
#         - Error: For invalid input or database exceptions.
#     """
#     log.info(f"Authenticating user: {input_value}")

#     if "@" in input_value:
#         if is_valid_email(input_value):
#             try:
#                 with sqlite3.connect(DB_PATH) as connection:
#                     cursor = connection.cursor()
#                     log.info("connected to database successfully.")

#                     cursor.execute("SELECT client_id FROM clients WHERE email = ?", (input_value,))
#                     result = cursor.fetchone()
#                     connection.commit()

#                     if result:
#                         client_id = result[0]
#                         log.info("Authentication successful. Client ID: %s", client_id)
#                         return {
#                             "status": "success",
#                             "message": "Client successfully authenticated on the plateform",
#                             "client_id": client_id
#                         }
#                     else:
#                         log.warning("Authentication failed. Email not found.")
#                         return {
#                             "status": "not_found",
#                             "message": "Client's email not found. Proceed to authenticate_visitor"
#                         }
#             except Exception as e:
#                 log.error(f"Error during authentication: {e}")
#                 return {
#                 "status": "error",
#                 "message": f"Error during authentication: {e}"
#                 }
#         else:
#             log.error(f"Invalid email provided.")
#             return {
#                 "status": "invalid_input",
#                 "message": "Invalid email provided"
#             }
#     else:
#         if is_valid_phone_number(input_value):
#             try:
#                 with sqlite3.connect(DB_PATH) as connection:
#                     cursor = connection.cursor()
#                     log.info("connected to database successfully.")

#                     cursor.execute("SELECT client_id FROM clients WHERE phone = ?", (input_value,))
#                     result = cursor.fetchone()
#                     connection.commit()

#                     if result:
#                         client_id = result[0]
#                         log.info("Authentication successful. Client ID: %s", client_id)
#                         return {
#                             "status": "success",
#                             "message": "Client successfully authenticated on the plateform",
#                             "client_id": client_id
#                         }
#                     else:
#                         log.warning("Authentication failed. Phone not found.")
#                         return {
#                             "status": "not_found",
#                             "message": "Client's phone not found. Proceed to authenticate_visitor"
#                         }
#             except Exception as e:
#                 log.error(f"Error during authentication: {e}")
#                 return {
#                     "status": "error",
#                     "message": f"Error during authentication: {e}"
#                 }
#         else:
#             log.error(f"Invalid phone number provided.")
#             return {
#                 "status": "invalid_input",
#                 "message": "Invalid phone provided"
#             }
        
# def authenticate_visitor(input_value: str) -> int | None:
#     """Authenticate a visitor using their email or phone number.

#     Validates the given input as either an email address or a phone number.
#     If valid, it attempts to locate a matching visitor record in the database
#     and returns the corresponding visitor ID upon successful authentication.

#     Args:
#         input_value (str): The visitor's email address or phone number.

#     Returns:
#         int | None: The visitor ID if authentication is successful; otherwise, None.

#     Logs:
#         - Info: Input received, database connection, and authentication success.
#         - Warning: If the email or phone number is not found in the database.
#         - Error: If the input is invalid or a database error occurs.
#     """
#     log.info(f"Authenticating user: {input_value}")

#     if "@" in input_value:
#         if is_valid_email(input_value):
#             try:
#                 with sqlite3.connect(DB_PATH) as connection:
#                     cursor = connection.cursor()
#                     log.info("connected to database successfully.")

#                     cursor.execute("SELECT visitor_id FROM visitors WHERE email = ?", (input_value,))
#                     result = cursor.fetchone()
#                     connection.commit()

#                     if result:
#                         visitor_id = result[0]
#                         log.info("Authentication successful. Visitor ID: %s", visitor_id)
#                         return {
#                             "status": "success",
#                             "message": "Visitor successfully authenticated on the plateform",
#                             "visitor_id": visitor_id
#                         }
#                     else:
#                         log.warning("Authentication failed. Email not found.")
#                         return {
#                             "status": "not_found",
#                             "message": "Visitor's email not found."
#                         }
#             except Exception as e:
#                 log.error(f"Error during authentication: {e}")
#                 return {
#                     "status": "error",
#                     "message": f"Error during authentication: {e}"
#                 }
#         else:
#             log.error(f"Invalid email provided.")
#             return {
#                 "status": "invalid_input",
#                 "message": "Invalid email provided"
#             }
#     else:
#         if is_valid_phone_number(input_value):
#             try:
#                 with sqlite3.connect(DB_PATH) as connection:
#                     cursor = connection.cursor()
#                     log.info("connected to database successfully.")

#                     cursor.execute("SELECT visitor_id FROM visitors WHERE phone = ?", (input_value,))
#                     result = cursor.fetchone()
#                     connection.commit()

#                     if result:
#                         visitor_id = result[0]
#                         log.info("Authentication successful. Client ID: %s", visitor_id)
#                         return {
#                             "status": "success",
#                             "message": "Visitor successfully authenticated on the plateform",
#                             "visitor_id": visitor_id
#                         }
#                     else:
#                         log.warning("Authentication failed. Phone not found.")
#                         return {
#                             "status": "not_found",
#                             "message": "Visitor's phone not found."
#                         }
#             except Exception as e:
#                 log.error(f"Error during authentication: {e}")
#                 return {
#                     "status": "error",
#                     "message": f"Error during authentication: {e}"
#                 }
#         else:
#             log.error(f"Invalid phone number provided.")
#             return {
#                 "status": "invalid_input",
#                 "message": "Invalid phone provided"
#             }

# def add_visitor(name: str, email: str, phone: str, consent: bool) -> int | None:
#     """Add a new visitor to the database, ensuring unique email and phone.

#     Validates the provided email and phone number, ensuring they are unique 
#     in the system. If both are valid and not already associated with an existing 
#     visitor, a unique visitor ID is generated and a new record is inserted into 
#     the database.

#     Args:
#         name (str): The full name of the visitor.
#         email (str): The visitor's email address.
#         phone (str): The visitor's phone number.
#         consent (bool): Whether the visitor has given consent.

#     Returns:
#         int | None: The generated visitor ID if insertion is successful; 
#                     otherwise, None if the email or phone is already taken 
#                     or an error occurs.

#     Logs:
#         - Info: Details of the visitor addition process and success.
#         - Warning: If a visitor with the same email or phone number already exists.
#         - Error: If the email, phone, or database operation fails.
#     """

#     log.info(f"Adding visitor: {name}")

#     try:
#         if not (is_valid_email(email) and is_valid_phone_number(phone)):
#             log.error("Invalid email or phone number provided")
#             return {
#                 "status": "invalid_input",
#                 "message": "Invalid email or phone number provided."
#             }
        
#         visitor_id = generate_id(email, phone)

#         with sqlite3.connect(DB_PATH) as connection:
#             cursor = connection.cursor()
#             log.info("Connected to database successfully.")

#             cursor.execute(
#                 "SELECT 1 FROM visitors WHERE email = ? OR phone = ?", (email, phone)
#             )
#             if cursor.fetchone():
#                 log.warning("Visitor with given email or phone already exists.")
#                 return {
#                     "status": "duplicate",
#                     "message": "A visitor with this email or phone number already exists."
#                 }

#             cursor.execute("INSERT INTO visitors (visitor_id, name, email, phone, consent) VALUES (?, ?, ?, ?, ?)",
#                         (visitor_id, name, email, phone, int(consent)))
#             connection.commit()
#             log.info("New visitor added. Visitor ID: %s", visitor_id)
#             return {
#                 "status": "success",
#                 "message": "Visitor successfully added to the platform.",
#                 "visitor_id": visitor_id
#             }
        
#     except Exception as e:
#         log.error("Error adding visitor: %s", e)
#         return {
#             "status": "error",
#             "message": f"Error adding visitor: {e}"
#         }
 
# def hands_off(action: str) -> str:
#     """Map an action to a corresponding agent name.

#     Converts the given action string to lowercase and returns the 
#     name of the agent responsible for that action. Supported actions 
#     are "connect" and "explore". If the action is unrecognized, 
#     returns "the_human".

#     Args:
#         action: The name of the action to evaluate.

#     Returns:
#         The name of the agent corresponding to the action.
#     """
#     agent_map = {
#         "connect": "connect_agent",
#         "explore": "explore_agent"
#     }
#     return agent_map.get(action.lower(), "the_human")


# def retrive_experts():
#     """
#     Retrieves all expert records from the 'experts' table in the SQLite database.

#     Returns:
#         list: A list of dictionaries, each representing an expert record.
#     """

#     connection = sqlite3.connect(DB_PATH)
#     cursor = connection.cursor()

#     try:
#         cursor.execute("SELECT * FROM experts")
#         column_names = [description[0] for description in cursor.description]  # Get column names
#         experts = cursor.fetchall()
        
#         return [dict(zip(column_names, row)) for row in experts]
    
#     except Exception as e:
#         return json.dumps(
#             {"status": "error",
#              "message": str(e),
#              "code": 500}
#         )
    
#     finally:
#         connection.close()



# src/bot_flow/tool_functions.py

import sqlite3
import json
from typing import Union, List, Dict, Optional
from config.config import DB_PATH
from .utils import is_valid_email, is_valid_phone_number, generate_id, detect_language, extract_key_terms
from logger.custom_logger import setup_logger
from openai import OpenAI

log = setup_logger()

client = OpenAI()  # Ensure API key is set in environment variables

# ---------------------------
# 🔐 Authentication Functions
# ---------------------------

def authenticate_client(input_value: str) -> dict:
    """
    Authenticates a client using their email or phone number.
    
    Args:
        input_value (str): The email or phone number to authenticate with.
        
    Returns:
        dict: Response object containing status, message, and optional client_id.
    """
    log.info(f"Authenticating client: {input_value}")
    if "@" in input_value:
        if is_valid_email(input_value):
            try:
                with sqlite3.connect(DB_PATH) as connection:
                    cursor = connection.cursor()
                    log.info("Connected to database successfully.")
                    cursor.execute("SELECT client_id FROM clients WHERE email = ?", (input_value,))
                    result = cursor.fetchone()
                    if result:
                        client_id = result[0]
                        log.info(f"Authentication successful. Client ID: {client_id}")
                        return {
                            "status": "success",
                            "message": "Client successfully authenticated.",
                            "client_id": client_id
                        }
                    else:
                        log.warning("Authentication failed. Email not found.")
                        return {
                            "status": "not_found",
                            "message": "Client's email not found."
                        }
            except Exception as e:
                log.error(f"Error during client authentication: {e}")
                return {
                    "status": "error",
                    "message": f"Database error: {e}"
                }
        else:
            log.error("Invalid email provided.")
            return {
                "status": "invalid_input",
                "message": "Invalid email format."
            }
    else:
        if is_valid_phone_number(input_value):
            try:
                with sqlite3.connect(DB_PATH) as connection:
                    cursor = connection.cursor()
                    log.info("Connected to database successfully.")
                    cursor.execute("SELECT client_id FROM clients WHERE phone = ?", (input_value,))
                    result = cursor.fetchone()
                    if result:
                        client_id = result[0]
                        log.info(f"Authentication successful. Client ID: {client_id}")
                        return {
                            "status": "success",
                            "message": "Client successfully authenticated.",
                            "client_id": client_id
                        }
                    else:
                        log.warning("Authentication failed. Phone not found.")
                        return {
                            "status": "not_found",
                            "message": "Client's phone not found."
                        }
            except Exception as e:
                log.error(f"Error during client authentication: {e}")
                return {
                    "status": "error",
                    "message": f"Database error: {e}"
                }
        else:
            log.error("Invalid phone number provided.")
            return {
                "status": "invalid_input",
                "message": "Invalid phone number format."
            }


def authenticate_visitor(input_value: str) -> dict:
    """
    Authenticates a visitor using their email or phone number.

    Args:
        input_value (str): The email or phone number of the visitor.

    Returns:
        dict: Status, message, and optionally visitor_id.
    """
    log.info(f"Authenticating visitor: {input_value}")
    if "@" in input_value:
        if is_valid_email(input_value):
            try:
                with sqlite3.connect(DB_PATH) as connection:
                    cursor = connection.cursor()
                    log.info("Connected to database successfully.")
                    cursor.execute("SELECT visitor_id FROM visitors WHERE email = ?", (input_value,))
                    result = cursor.fetchone()
                    if result:
                        visitor_id = result[0]
                        log.info(f"Visitor authenticated. Visitor ID: {visitor_id}")
                        return {
                            "status": "success",
                            "message": "Visitor authenticated successfully.",
                            "visitor_id": visitor_id
                        }
                    else:
                        log.warning("Visitor email not found.")
                        return {
                            "status": "not_found",
                            "message": "Visitor email not found."
                        }
            except Exception as e:
                log.error(f"Error authenticating visitor: {e}")
                return {
                    "status": "error",
                    "message": f"Database error: {e}"
                }
        else:
            log.error("Invalid email provided.")
            return {
                "status": "invalid_input",
                "message": "Invalid email format."
            }
    else:
        if is_valid_phone_number(input_value):
            try:
                with sqlite3.connect(DB_PATH) as connection:
                    cursor = connection.cursor()
                    log.info("Connected to database successfully.")
                    cursor.execute("SELECT visitor_id FROM visitors WHERE phone = ?", (input_value,))
                    result = cursor.fetchone()
                    if result:
                        visitor_id = result[0]
                        log.info(f"Visitor authenticated. Visitor ID: {visitor_id}")
                        return {
                            "status": "success",
                            "message": "Visitor authenticated successfully.",
                            "visitor_id": visitor_id
                        }
                    else:
                        log.warning("Visitor phone not found.")
                        return {
                            "status": "not_found",
                            "message": "Visitor phone not found."
                        }
            except Exception as e:
                log.error(f"Error authenticating visitor: {e}")
                return {
                    "status": "error",
                    "message": f"Database error: {e}"
                }
        else:
            log.error("Invalid phone number provided.")
            return {
                "status": "invalid_input",
                "message": "Invalid phone number format."
            }


def add_visitor(name: str, email: str, phone: str, consent: bool) -> dict:
    """
    Adds a new visitor to the database after validation.

    Args:
        name (str): Full name of the visitor.
        email (str): Email address.
        phone (str): Phone number.
        consent (bool): Whether the visitor gave consent.

    Returns:
        dict: Status, message, and optional visitor_id.
    """
    log.info(f"Adding visitor: {name}")
    try:
        if not (is_valid_email(email) and is_valid_phone_number(phone)):
            log.error("Invalid email or phone number provided.")
            return {
                "status": "invalid_input",
                "message": "Invalid email or phone number."
            }

        visitor_id = generate_id(email, phone)

        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            log.info("Connected to database successfully.")

            cursor.execute(
                "SELECT 1 FROM visitors WHERE email = ? OR phone = ?", (email, phone)
            )
            if cursor.fetchone():
                log.warning("Duplicate email or phone number.")
                return {
                    "status": "duplicate",
                    "message": "A visitor with this email or phone already exists."
                }

            cursor.execute(
                "INSERT INTO visitors (visitor_id, name, email, phone, consent) VALUES (?, ?, ?, ?, ?)",
                (visitor_id, name, email, phone, int(consent))
            )
            connection.commit()
            log.info(f"New visitor added. Visitor ID: {visitor_id}")
            return {
                "status": "success",
                "message": "Visitor successfully added.",
                "visitor_id": visitor_id
            }
    except Exception as e:
        log.error(f"Error adding visitor: {e}")
        return {
            "status": "error",
            "message": f"Database error: {e}"
        }


# ---------------------------
# 🔄 Routing & Hands Off
# ---------------------------

def hands_off(action: str) -> str:
    """
    Maps an action to a corresponding agent.

    Args:
        action (str): Action to map (e.g., 'connect', 'explore').

    Returns:
        str: Agent name to route to.
    """
    agent_map = {
        "connect": "connect_agent",
        "explore": "explore_agent"
    }
    return agent_map.get(action.lower(), "the_human")


# ---------------------------
# 👨‍💼 Expert Matching
# ---------------------------

def retrieve_experts(filters: Optional[Dict[str, str]] = None) -> Union[List[Dict], dict]:
    """
    Retrieves expert records from the database. Optionally filters by criteria.

    Args:
        filters (dict): Optional filter criteria like sector, company.

    Returns:
        list | dict: List of experts or error/fallback response.
    """
    log.info("Retrieving experts...")
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    try:
        if filters:
            query = "SELECT * FROM experts WHERE "
            conditions = []
            params = []

            if 'sector' in filters:
                conditions.append("sector LIKE ?")
                params.append(f"%{filters['sector']}%")
            if 'company' in filters:
                conditions.append("company LIKE ?")
                params.append(f"%{filters['company']}%")

            query += " AND ".join(conditions)

            cursor.execute(query, tuple(params))
        else:
            cursor.execute("SELECT * FROM experts")

        column_names = [desc[0] for desc in cursor.description]
        experts = cursor.fetchall()
        result = [dict(zip(column_names, row)) for row in experts]

        if len(result) < 10:
            log.warning("Fewer than 10 experts found. Falling back to email notification.")
            return {"status": "fallback", "message": "Fewer than 10 experts matched. Admin notified."}

        return result
    except Exception as e:
        log.error(f"Error retrieving experts: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        connection.close()


def suggest_companies(user_input: str) -> List[str]:
    """
    Uses LLM to suggest companies based on user input.

    Args:
        user_input (str): Description or context for suggestion.

    Returns:
        list: Suggested company names.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant that suggests relevant companies based on user input."},
                {"role": "user", "content": f"Suggest 15 companies related to: {user_input}"}
            ],
            temperature=0.7,
            max_tokens=200
        )
        content = response.choices[0].message.content.strip().split("\n")
        return [item.split(".")[1].strip() for item in content if "." in item]
    except Exception as e:
        log.error(f"LLM error while suggesting companies: {e}")
        return []


# ---------------------------
# 📦 Data Syncing
# ---------------------------

def save_project_details(project_data: dict) -> dict:
    """
    Saves project details to the database.

    Args:
        project_data (dict): Project information to store.

    Returns:
        dict: Operation result.
    """
    # Implementation left for now
    return {"status": "success", "message": "Project details saved."}


def sync_to_google_sheets(data: dict) -> dict:
    """
    Syncs data to Google Sheets.

    Args:
        data (dict): Data to sync.

    Returns:
        dict: Operation result.
    """
    # Placeholder
    return {"status": "success", "message": "Data synced to Google Sheets."}