# import sqlite3

# from logger.custom_logger import setup_logger

# log = setup_logger()

# def save_message(DB_PATH, is_client, sender, message, user_id, channel="email"):
#     log.info("Saving message to database...")
#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             log.info("Connected to database successfully.")
#             cursor = connection.cursor()
#             cursor.execute('''
#             INSERT INTO chat_history (is_client, sender, message, user_id, channel)
#             VALUES (?, ?, ?, ?, ?)
#             ''', (is_client, sender, message, user_id, channel))
#             connection.commit()
#             log.info("Saved to database successfully.")
#     except sqlite3.Error as e:
#         log.error("Failed to save to database: %s", e)

# def get_conversation(DB_PATH, user_id):
#     log.info("Fetching conversation history from database...")
#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             log.info("Connected to database successfully.")
#             cursor = connection.cursor()
#             cursor.execute('''
#                 SELECT sender, message FROM chat_history
#                 WHERE user_id = ?
#                 ORDER BY timestamp ASC
#             ''', (user_id,))
#             history = cursor.fetchall()
#             log.info("Conversation history fetched successfully.")
#             return history
#     except sqlite3.Error as e:
#         log.error("Failed to fetch conversation history: %s", e)
#         return [] 

# /////////////////////////////////////////////////////////////////////////////////

# import sqlite3
# from logger.custom_logger import setup_logger

# log = setup_logger()

# def save_message(DB_PATH, is_client, sender, message, user_id, channel="email"):
#     log.info("Saving message to database...")
#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             log.info("Connected to database successfully.")
#             cursor = connection.cursor()
#             cursor.execute('''
#                 INSERT INTO chat_history (is_client, sender, message, user_id, channel)
#                 VALUES (?, ?, ?, ?, ?)
#             ''', (is_client, sender, message, user_id, channel))
#             connection.commit()
#             log.info("Saved to database successfully.")
#     except sqlite3.Error as e:
#         log.error("Failed to save to database: %s", e)

# def get_conversation(DB_PATH, user_id, limit=20):
#     log.info("Fetching conversation history from database...")
#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             log.info("Connected to database successfully.")
#             cursor = connection.cursor()
#             cursor.execute('''
#                 SELECT sender, message FROM chat_history
#                 WHERE user_id = ?
#                 ORDER BY timestamp DESC
#                 LIMIT ?
#             ''', (user_id, limit))
#             history = cursor.fetchall()
#             log.info("Conversation history fetched successfully.")
#             return list(reversed(history))  # Oldest first
#     except sqlite3.Error as e:
#         log.error("Failed to fetch conversation history: %s", e)
#         return []



import sqlite3
from logger.custom_logger import setup_logger

log = setup_logger()

def save_message(DB_PATH, is_client, sender, message, user_id, channel="whatsapp"):
    if not is_client:
        log.info("Skipping chat_history save for visitor.")
        return  # Visitors' messages should not be saved to chat_history

    log.info("Saving client message to chat_history...")
    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO chat_history (is_client, sender, message, user_id, channel)
                VALUES (?, ?, ?, ?, ?)
            ''', (is_client, sender, message, user_id, channel))
            connection.commit()
            log.info("Message saved to chat_history.")
    except sqlite3.Error as e:
        log.error("Failed to save message: %s", e)

def get_conversation(DB_PATH, user_id, limit=20):
    log.info("Fetching conversation history...")
    try:
        with sqlite3.connect(DB_PATH) as connection:
            cursor = connection.cursor()
            cursor.execute('''
                SELECT sender, message FROM chat_history
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (user_id, limit))
            history = cursor.fetchall()
            return list(reversed(history))  # For chronological context
    except sqlite3.Error as e:
        log.error("Error fetching chat history: %s", e)
        return []

def insert_visitor(DB_PATH, temp_id, email=None, phone=None, name="Visitor"):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO visitors (visitor_id, name, email, phone, consent)
                VALUES (?, ?, ?, ?, ?)
            ''', (temp_id, name, email, phone or "", True))  # Default consent=True
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        log.warning("Visitor already exists")
        return False
    except Exception as e:
        log.error(f"Error inserting visitor: {e}")
        return False

def promote_visitor_to_client(DB_PATH, visitor_id, client_data):
    """Move visitor to clients table and delete visitor records"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Insert into clients
        cursor.execute("""
            INSERT INTO clients (client_id, email, phone, flag)
            VALUES (?, ?, ?, ?)
        """, (client_data['client_id'], client_data['email'], 
              client_data['phone'], False))
        
        # Delete from visitors
        cursor.execute("DELETE FROM visitors WHERE visitor_id = ?", (visitor_id,))
        
        conn.commit()
        return {"status": "success", "client_id": client_data['client_id']}
    except Exception as e:
        conn.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()













# /////////////////////////////////////////////////////////////////////////////////////

