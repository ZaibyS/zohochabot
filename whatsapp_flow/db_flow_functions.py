# import sqlite3
# from logger.custom_logger import setup_logger

# log = setup_logger()

# def save_message(DB_PATH, is_client, sender, message, user_id, channel="whatsapp"):
#     log.info("Saving WhatsApp message to database...")
#     try:
#         with sqlite3.connect(DB_PATH) as connection:
#             log.info("Connected to database successfully.")
#             cursor = connection.cursor()
#             cursor.execute('''
#             INSERT INTO chat_history (is_client, sender, message, user_id, channel)
#             VALUES (?, ?, ?, ?, ?)
#             ''', (is_client, sender, message, user_id, channel))
#             connection.commit()
#             log.info("Saved WhatsApp message to database successfully.")
#     except sqlite3.Error as e:
#         log.error("Failed to save WhatsApp message to database: %s", e)

# def get_conversation(DB_PATH, user_id):
#     log.info("Fetching WhatsApp conversation history from database...")
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
#         log.error("Failed to fetch WhatsApp conversation history: %s", e)
#         return []


import sqlite3
from logger.custom_logger import setup_logger

log = setup_logger()

def save_message(DB_PATH, is_client, sender, message, user_id, channel="whatsapp"):
    log.info("Saving WhatsApp message to database...")
    try:
        with sqlite3.connect(DB_PATH) as connection:
            log.info("Connected to database successfully.")
            cursor = connection.cursor()
            cursor.execute('''
                INSERT INTO chat_history (is_client, sender, message, user_id, channel)
                VALUES (?, ?, ?, ?, ?)
            ''', (is_client, sender, message, user_id, channel))
            connection.commit()
            log.info("Saved WhatsApp message to database successfully.")
    except sqlite3.Error as e:
        log.error("Failed to save WhatsApp message to database: %s", e)

def get_conversation(DB_PATH, user_id, limit=20):
    log.info("Fetching WhatsApp conversation history from database...")
    try:
        with sqlite3.connect(DB_PATH) as connection:
            log.info("Connected to database successfully.")
            cursor = connection.cursor()
            cursor.execute('''
                SELECT sender, message FROM chat_history
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (user_id, limit))
            history = cursor.fetchall()
            log.info(list(history))
            log.info("Conversation history fetched successfully.")
            return list(reversed(history))  # Oldest first for LLM flow
    except sqlite3.Error as e:
        log.error("Failed to fetch WhatsApp conversation history: %s", e)
        return []
