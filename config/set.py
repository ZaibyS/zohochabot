import sqlite3
from logger.custom_logger import setup_logger

log = setup_logger(__name__)
from config.config import DB_PATH


def set_client_flag_true(DB_PATH, identifier, by="phone"):
    """
    Sets the flag = 1 (True) for a client in the clients table.
    
    :param DB_PATH: Path to the database
    :param identifier: phone number, email, or client_id
    :param by: one of 'phone', 'email', or 'client_id'
    :return: status dict
    """
    valid_columns = {"phone", "email", "client_id"}
    if by not in valid_columns:
        return {"status": "error", "message": "Invalid identifier column"}

    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            cursor.execute(f"""
                UPDATE clients SET flag = 1 WHERE {by} = ?
            """, (identifier,))
            conn.commit()

            if cursor.rowcount == 0:
                log.warning("No client found with %s = %s", by, identifier)
                return {"status": "not_found", "message": "No matching client found"}
            
            log.info("✅ Client flag updated to True where %s = %s", by, identifier)
            return {"status": "success", "message": f"Flag set for {by} = {identifier}"}

    except Exception as e:
        log.error("❌ Error updating client flag: %s", e)
        return {"status": "error", "message": str(e)}


set_client_flag_true(DB_PATH, "fahadshafique1133@gmail.com", by="email")