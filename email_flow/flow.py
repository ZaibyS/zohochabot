
# import os
# from dotenv import load_dotenv

# from .email_flow_functions import (
#     fetch_unread_emails,
#     send_email,
# )

# from .db_flow_functions import (
#     save_message,
#     get_conversation
# )

# from .utils import (
#     authentication_email,
#     generate_temp_id,
#     authenticate_visitor,
#     is_valid_phone_number
# )

# from .openai_flow_functions import (
#     generate_visitor_reply,
#     generate_client_reply
# )

# from .tools_functions import promote_visitor_to_client

# from logger.custom_logger import setup_logger

# log = setup_logger(__name__)
# load_dotenv()

# def process_incoming_emails(DB_PATH, system_prompt_not_client, system_prompt_email_generator, EMAIL_ACCOUNT, SMTP_SERVER, IMAP_SERVER, EMAIL_APP_PASSWORD):
#     log.info("Email flow triggered.")
#     try:
#         new_emails = fetch_unread_emails(IMAP_SERVER, EMAIL_ACCOUNT, EMAIL_APP_PASSWORD)
#     except Exception as e:
#         log.error("Failed to fetch unread emails: %s", e)
#         return

#     for email_data in new_emails:
#         try:
#             sender = email_data['from']
#             body = email_data['body'].strip()
#             subject = email_data['subject']
#             message_id = email_data.get('message_id')

#             client_id = authentication_email(DB_PATH, sender)

#             # ✅ Existing Client
#             if client_id:
#                 save_message(DB_PATH, is_client=True, sender=sender, message=body, user_id=client_id, channel="email")
#                 conversation = get_conversation(DB_PATH, user_id=client_id, limit=20)
#                 reply_body = generate_client_reply(conversation, system_prompt_email_generator)
#                 save_message(DB_PATH, is_client=True, sender=EMAIL_ACCOUNT, message=reply_body, user_id=client_id, channel="email")
#                 send_email(sender, "Re: " + subject, reply_body, EMAIL_ACCOUNT, SMTP_SERVER, EMAIL_APP_PASSWORD, in_reply_to=message_id)
#                 continue

#             # ✅ Visitor Found
#             visitor_id = authenticate_visitor(DB_PATH, sender)
#             if visitor_id:
#                 save_message(DB_PATH, is_client=False, sender=sender, message=body, user_id=visitor_id, channel="email")

#                 # If phone number is detected in this message, promote
#                 if is_valid_phone_number(body):
#                     # We'll assume name was sent earlier, fallback to generic if not stored
#                     name = "User"  # Optional: update this logic to remember actual name
#                     result = promote_visitor_to_client(email=sender, phone=body, name=name)
#                     if result.get("status") == "success":
#                         reply = "✅ Thank you for providing your phone number. Our team will contact you shortly to complete the onboarding."
#                         send_email(sender, "Re: " + subject, reply, EMAIL_ACCOUNT, SMTP_SERVER, EMAIL_APP_PASSWORD, in_reply_to=message_id)
#                     continue

#                 # If not phone number, continue with LLM reply
#                 conversation = get_conversation(DB_PATH, user_id=visitor_id)
#                 reply_body = generate_visitor_reply(conversation, system_prompt_not_client, visitor_email=sender)
#                 save_message(DB_PATH, is_client=False, sender=EMAIL_ACCOUNT, message=reply_body, user_id=visitor_id, channel="email")
#                 send_email(sender, "Re: " + subject, reply_body, EMAIL_ACCOUNT, SMTP_SERVER, EMAIL_APP_PASSWORD, in_reply_to=message_id)
#                 continue

#             # ✅ New Visitor (first-time)
#             temp_id = generate_temp_id(sender)
#             save_message(DB_PATH, is_client=False, sender=sender, message=body, user_id=temp_id, channel="email")
#             conversation = get_conversation(DB_PATH, user_id=temp_id)
#             reply_body = generate_visitor_reply(conversation, system_prompt_not_client, visitor_email=sender)
#             save_message(DB_PATH, is_client=False, sender=EMAIL_ACCOUNT, message=reply_body, user_id=temp_id, channel="email")
#             send_email(sender, "Re: " + subject, reply_body, EMAIL_ACCOUNT, SMTP_SERVER, EMAIL_APP_PASSWORD, in_reply_to=message_id)

#         except Exception as e:
#             log.error("Failed to process email from %s: %s", sender, e)




# //////////////////////////////////////////////////////////////////////////


# import os
# from dotenv import load_dotenv

# from .email_flow_functions import (
#     fetch_unread_emails,
#     send_email,
# )

# from .db_flow_functions import (
#     save_message,
#     get_conversation
# )

# from .utils import (
#     authentication_email,
#     generate_temp_id,
#     authenticate_visitor,
#     is_valid_phone_number,
#     update_visitor_phone,
#     try_promote_visitor_if_ready
# )

# from .openai_flow_functions import (
#     generate_visitor_reply,
#     generate_client_reply
# )

# from logger.custom_logger import setup_logger

# log = setup_logger(__name__)
# load_dotenv()

# def process_incoming_emails(DB_PATH, system_prompt_not_client, system_prompt_email_generator,
#                             EMAIL_ACCOUNT, SMTP_SERVER, IMAP_SERVER, EMAIL_APP_PASSWORD):
#     log.info("📩 Email flow triggered.")

#     try:
#         new_emails = fetch_unread_emails(IMAP_SERVER, EMAIL_ACCOUNT, EMAIL_APP_PASSWORD)
#     except Exception as e:
#         log.error("❌ Failed to fetch unread emails: %s", e)
#         return

#     for email_data in new_emails:
#         try:
#             sender = email_data['from']
#             body = email_data['body'].strip()
#             subject = email_data['subject']
#             message_id = email_data.get('message_id')

#             log.info(f"📨 New email from {sender} | Subject: {subject}")

#             # ✅ Step 1: Check if already a client
#             client_record = authentication_email(DB_PATH, sender)
#             if client_record:
#                 client_id, flag = client_record

#                 if flag:  # ✅ flag == True → client flow
#                     log.info(f"✅ Authenticated client [{client_id}] with flag=True")
#                     save_message(DB_PATH, is_client=True, sender=sender, message=body, user_id=client_id, channel="email")

#                     conversation = get_conversation(DB_PATH, user_id=client_id, limit=20)
#                     reply = generate_client_reply(conversation, system_prompt_email_generator)

#                     save_message(DB_PATH, is_client=True, sender=EMAIL_ACCOUNT, message=reply, user_id=client_id, channel="email")
#                     send_email(sender, "Re: " + subject, reply, EMAIL_ACCOUNT, SMTP_SERVER, EMAIL_APP_PASSWORD, in_reply_to=message_id)
#                     continue

#                 else:  # ✅ flag == False → onboarding message
#                     log.info(f"👋 Client [{client_id}] found but flag=False (not onboarded yet)")
#                     onboarding_msg = "You're registered in our system. Our team will contact you soon for an onboarding call."
#                     send_email(sender, "Re: " + subject, onboarding_msg, EMAIL_ACCOUNT, SMTP_SERVER, EMAIL_APP_PASSWORD, in_reply_to=message_id)
#                     continue

#             # ✅ Step 2: Check if returning visitor
#             visitor_id = authenticate_visitor(DB_PATH, sender)
#             if visitor_id:
#                 log.info(f"👀 Visitor found with ID: {visitor_id}")
#                 # ⚠️ Do NOT save visitor chats to main chat_history
#                 # Use save_message only for internal cache (if needed), otherwise skip

#                 # Check if visitor sent phone number
#                 if is_valid_phone_number(body):
#                     update_visitor_phone(sender, phone=body)
#                     try_promote_visitor_if_ready(email=sender)

#                 conversation = get_conversation(DB_PATH, user_id=visitor_id)
#                 reply = generate_visitor_reply(conversation, system_prompt_not_client, visitor_email=sender)

#                 # Reply from system (don't save chat to chat_history)
#                 send_email(sender, "Re: " + subject, reply, EMAIL_ACCOUNT, SMTP_SERVER, EMAIL_APP_PASSWORD, in_reply_to=message_id)
#                 continue

#             # ✅ Step 3: First-time visitor
#             temp_id = generate_temp_id(sender)
#             log.info(f"🆕 New visitor detected. Temp ID: {temp_id}")
#             # Save visitor message to internal cache or temp db (but NOT chat_history)
#             save_message(DB_PATH, is_client=False, sender=sender, message=body, user_id=temp_id, channel="email")

#             conversation = get_conversation(DB_PATH, user_id=temp_id)
#             reply = generate_visitor_reply(conversation, system_prompt_not_client, visitor_email=sender)

#             send_email(sender, "Re: " + subject, reply, EMAIL_ACCOUNT, SMTP_SERVER, EMAIL_APP_PASSWORD, in_reply_to=message_id)

#         except Exception as e:
#             log.error("❌ Failed to process email from %s: %s", sender, e)


# //////////////////////////////////////////////////////////////////////////////

# import os
# from dotenv import load_dotenv

# from .email_flow_functions import (
#     fetch_unread_emails,
#     send_email,
# )

# from .db_flow_functions import (
#     save_message,
#     get_conversation,
#     insert_visitor  # ✅ newly added for visitor insertion
# )

# from .utils import (
#     authentication_email,
#     generate_temp_id,
#     authenticate_visitor,
#     is_valid_phone_number,
#     update_visitor_phone,
#     promote_visitor_to_client
# )

# from .openai_flow_functions import (
#     generate_onboard_reply,
#     generate_client_reply
# )

# from logger.custom_logger import setup_logger

# log = setup_logger(__name__)
# load_dotenv()


# def process_incoming_emails(DB_PATH, system_prompt_not_client, system_prompt_email_generator,
#                             EMAIL_ACCOUNT, SMTP_SERVER, IMAP_SERVER, EMAIL_APP_PASSWORD):
#     log.info("📩 Email flow triggered.")

#     try:
#         new_emails = fetch_unread_emails(IMAP_SERVER, EMAIL_ACCOUNT, EMAIL_APP_PASSWORD)
#     except Exception as e:
#         log.error("❌ Failed to fetch unread emails: %s", e)
#         return

#     for email_data in new_emails:
#         try:
#             sender = email_data['from']
#             body = email_data['body'].strip()
#             subject = email_data['subject']
#             message_id = email_data.get('message_id')

#             log.info(f"📨 New email from {sender} | Subject: {subject}")

#             # ✅ Step 1: Check if already a client
#             client_record = authentication_email(DB_PATH, sender)
#             if client_record:
#                 client_id, flag = client_record

#                 if flag:  # ✅ Client with flag=True → Start flow
#                     log.info(f"✅ Authenticated client [{client_id}] with flag=True")
#                     save_message(DB_PATH, is_client=True, sender=sender, message=body, user_id=client_id, channel="email")

#                     conversation = get_conversation(DB_PATH, user_id=client_id, limit=20)
#                     reply = generate_client_reply(conversation, system_prompt_email_generator)

#                     save_message(DB_PATH, is_client=True, sender=EMAIL_ACCOUNT, message=reply, user_id=client_id, channel="email")
#                     send_email(sender, "Re: " + subject, reply, EMAIL_ACCOUNT, SMTP_SERVER, EMAIL_APP_PASSWORD, in_reply_to=message_id)
#                     continue

#                 else:  # ✅ Client found, flag=False → onboarding
#                     log.info(f"👋 Client [{client_id}] found but flag=False (not onboarded yet)")
#                     onboarding_msg = "You're registered in our system. Our team will contact you soon for an onboarding call."
#                     send_email(sender, "Re: " + subject, onboarding_msg, EMAIL_ACCOUNT, SMTP_SERVER, EMAIL_APP_PASSWORD, in_reply_to=message_id)
#                     continue

#             # ✅ Step 2: Check if returning visitor
#             visitor_id = authenticate_visitor(DB_PATH, sender)
#             if visitor_id:
#                 log.info(f"👀 Visitor found with ID: {visitor_id}")

#                 if is_valid_phone_number(body):
#                     update_visitor_phone(DB_PATH, email=sender, phone=body)
#                     promote_visitor_to_client(DB_PATH, email=sender)

#                 conversation = get_conversation(DB_PATH, user_id=visitor_id)
#                 reply = generate_onboard_reply(conversation, system_prompt_not_client, visitor_email=sender)

#                 send_email(sender, "Re: " + subject, reply, EMAIL_ACCOUNT, SMTP_SERVER, EMAIL_APP_PASSWORD, in_reply_to=message_id)
#                 continue

#             # ✅ Step 3: First-time visitor → insert into visitors table
#             temp_id = generate_temp_id(sender)
#             log.info(f"🆕 New visitor detected. Temp ID: {temp_id}")

#             # ❗ Must insert into DB explicitly
#             inserted = insert_visitor(DB_PATH, temp_id=temp_id, email=sender, phone=None, name="Visitor")
#             if inserted:
#                 log.info(f"✅ Visitor inserted into visitors table: {temp_id}")
#             else:
#                 log.warning(f"⚠️ Visitor insert may have failed or already exists.")

#             conversation = get_conversation(DB_PATH, user_id=temp_id)
#             reply = generate_onboard_reply(conversation, system_prompt_not_client, visitor_email=sender)

#             send_email(sender, "Re: " + subject, reply, EMAIL_ACCOUNT, SMTP_SERVER, EMAIL_APP_PASSWORD, in_reply_to=message_id)

#         except Exception as e:
#             log.error("❌ Failed to process email from %s: %s", sender, e)



# ///////////////////////////////////////////////////////////////////////////////////////////

import os
import sqlite3
from dotenv import load_dotenv
import re
from .email_flow_functions import (
    fetch_unread_emails,
    send_email,
)

from .db_flow_functions import (
    save_message,
    get_conversation,
    insert_visitor
)

from .utils import (
    authentication_email,
    generate_temp_id,
    authenticate_visitor,
    is_valid_phone_number,
    update_visitor_phone,
    promote_visitor_to_client,
    generate_client_id,
    authentication_user
)

from .openai_flow_functions import (
    generate_onboard_reply,
    generate_client_reply
)

from logger.custom_logger import setup_logger

log = setup_logger(__name__)
load_dotenv()

# def process_incoming_emails(DB_PATH, system_prompt_visitor, system_prompt_client,
#                           EMAIL_ACCOUNT, SMTP_SERVER, IMAP_SERVER, EMAIL_APP_PASSWORD):
#     log.info("📩 Starting email processing")
    
#     try:
#         emails = fetch_unread_emails(IMAP_SERVER, EMAIL_ACCOUNT, EMAIL_APP_PASSWORD)
#         if not emails:
#             log.info("No new emails to process")
#             return
#     except Exception as e:
#         log.error(f"❌ Failed to fetch emails: {e}")
#         return

#     for email_data in emails:
#         sender_email = email_data['from']
#         body = email_data['body'].strip()
#         message_id = email_data.get('message_id')
        
#         log.info(f"📨 Processing email from {sender_email}")
#         log.info(f"📝 Email content: {body[:100]}...")  # Log first 100 chars of message

#         # Step 1: Check if user is already a client
#         client_record = authentication_user(DB_PATH, sender_email)
#         if client_record:
#             client_id, flag = client_record
#             log.info(f"✅ Existing client found (flag={flag})")
            
#             save_message(DB_PATH, is_client=True, sender=sender_email,
#                         message=body, user_id=client_id, channel="email")
            
#             conversation = get_conversation(DB_PATH, user_id=client_id, limit=20)
            
#             if flag == 1:  # Fully onboarded
#                 reply = generate_client_reply(conversation, system_prompt_client)
#             else:  # Not fully onboarded
#                 reply = generate_onboard_reply(conversation, system_prompt_visitor, sender_email) or \
#                                 "Thank you for your message. Our team will contact you shortly."
            
#             save_message(DB_PATH, is_client=True, sender="bot",
#                         message=reply, user_id=client_id, channel="email")
#             send_email(sender_email, "Re: Your inquiry", reply, 
#                       EMAIL_ACCOUNT, SMTP_SERVER, EMAIL_APP_PASSWORD, message_id)
#             continue

#         # Step 2: Check if user is a returning visitor
#         visitor_id = authenticate_visitor(DB_PATH, sender_email)
#         if visitor_id:
#             log.info(f"🔁 Returning visitor detected: {visitor_id}")
            
#             # Extract and validate phone number
#             phone_match = re.search(r'(\+?\d[\d\s-]{7,}\d)', body)
#             if phone_match:
#                 phone_number = phone_match.group(1).replace(" ", "").replace("-", "")
#                 log.info(f"📱 Extracted phone number: {phone_number}")
                
#                 if is_valid_phone_number(phone_number):
#                     log.info("✅ Valid phone number format")
                    
#                     # Update visitor record with phone number
#                     if update_visitor_phone(DB_PATH, sender_email, phone_number):
#                         log.info("📝 Updated visitor record with phone number")
                        
#                         # Attempt promotion to client
#                         promotion_result = promote_visitor_to_client(
#                             phone=phone_number,
#                             email=sender_email,
#                             DB_PATH=DB_PATH
#                         )
#                         log.info(f"📬 Promotion result: {promotion_result}")
                        
#                         if promotion_result.get("status") == "success":
#                             client_id = generate_client_id(sender_email, phone_number)
#                             reply = f"Thank you for providing your phone number ({phone_number}). Our team will contact you shortly."
                            
#                             save_message(DB_PATH, is_client=True, sender=sender_email,
#                                        message=body, user_id=client_id, channel="email")
#                             save_message(DB_PATH, is_client=True, sender="bot",
#                                        message=reply, user_id=client_id, channel="email")
#                             send_email(sender_email, "Re: Thank you", reply,
#                                      EMAIL_ACCOUNT, SMTP_SERVER, EMAIL_APP_PASSWORD, message_id)
#                             continue
                            
#                         elif promotion_result.get("status") == "exists":
#                             log.info("ℹ️ Visitor already promoted to client")
#                             client_record = authentication_email(DB_PATH, sender_email)
#                             if client_record:
#                                 client_id, flag = client_record
#                                 reply = "Thank you for your message. We already have your information."
#                                 save_message(DB_PATH, is_client=True, sender=sender_email,
#                                             message=body, user_id=client_id, channel="email")
#                                 save_message(DB_PATH, is_client=True, sender="bot",
#                                             message=reply, user_id=client_id, channel="email")
#                                 send_email(sender_email, "Re: Thank you", reply,
#                                           EMAIL_ACCOUNT, SMTP_SERVER, EMAIL_APP_PASSWORD, message_id)
#                                 continue

#             # If no valid phone number found or promotion failed
#             reply = "Please provide your phone number in international format (e.g., +923001981991) to proceed."
#             send_email(sender_email, "Re: We need your phone number", reply,
#                       EMAIL_ACCOUNT, SMTP_SERVER, EMAIL_APP_PASSWORD, message_id)
#             continue

#         # Step 3: New visitor
#         log.info("📅 New visitor detected")
#         temp_id = generate_temp_id(sender_email)
        
#         try:
#             # Insert visitor with empty phone
#             if insert_visitor(
#                 DB_PATH=DB_PATH,
#                 temp_id=temp_id,
#                 email=sender_email,
#                 phone="",
#                 name="Email User"
#             ):
#                 log.info(f"✅ New visitor created: {temp_id}")
#                 reply = """Welcome! To get started, please reply with:
                
#                 Your phone number in international format (e.g., +923001981991)
                
#                 Our team will then contact you to complete onboarding."""
#             else:
#                 reply = "We already have your information. Please provide your phone number to continue."
                
#             send_email(sender_email, "Re: Welcome", reply,
#                      EMAIL_ACCOUNT, SMTP_SERVER, EMAIL_APP_PASSWORD, message_id)
#         except Exception as e:
#             log.error(f"❌ Visitor creation failed: {e}")
#             reply = "We encountered an error. Please try again later."
#             send_email(sender_email, "Re: Welcome", reply,
#                      EMAIL_ACCOUNT, SMTP_SERVER, EMAIL_APP_PASSWORD, message_id)

def process_incoming_emails(DB_PATH, system_prompt_visitor, system_prompt_client,
                          EMAIL_ACCOUNT, SMTP_SERVER, IMAP_SERVER, EMAIL_APP_PASSWORD):
    log.info("📩 Starting email processing")
    
    try:
        emails = fetch_unread_emails(IMAP_SERVER, EMAIL_ACCOUNT, EMAIL_APP_PASSWORD)
        if not emails:
            log.info("No new emails to process")
            return
    except Exception as e:
        log.error(f"❌ Failed to fetch emails: {e}")
        return

    for email_data in emails:
        sender_email = email_data['from']
        body = email_data['body'].strip()
        message_id = email_data.get('message_id')
        
        log.info(f"📨 Processing email from {sender_email}")

        # Step 1: Check if user is already a client (by email OR phone if provided)
        client_record = authentication_user(DB_PATH, sender_email)
        if client_record:
            client_id, flag = client_record
            log.info(f"✅ Existing client found (flag={flag})")
            
            save_message(DB_PATH, is_client=True, sender=sender_email,
                        message=body, user_id=client_id, channel="email")
            
            conversation = get_conversation(DB_PATH, user_id=client_id, limit=20)
            
            if flag == 1:  # Fully onboarded
                reply = generate_client_reply(conversation, system_prompt_client)
            else:  # Not fully onboarded
                reply = generate_onboard_reply(conversation, system_prompt_visitor, sender_email) or \
                                "Thank you for your message. Our team will contact you shortly."
            
            save_message(DB_PATH, is_client=True, sender="bot",
                        message=reply, user_id=client_id, channel="email")
            send_email(sender_email, "Re: Your inquiry", reply, 
                      EMAIL_ACCOUNT, SMTP_SERVER, EMAIL_APP_PASSWORD, message_id)
            continue

        # Step 2: Check if user is a returning visitor
        visitor_id = authenticate_visitor(DB_PATH, sender_email)
        if visitor_id:
            log.info(f"🔁 Returning visitor detected: {visitor_id}")
            
            # Extract and validate phone number
            phone_match = re.search(r'(\+?\d[\d\s-]{7,}\d)', body)
            if phone_match:
                phone_number = phone_match.group(1).replace(" ", "").replace("-", "")
                log.info(f"📱 Extracted phone number: {phone_number}")
                
                if is_valid_phone_number(phone_number):
                    log.info("✅ Valid phone number format")
                    
                    # Update visitor record with phone number
                    if update_visitor_phone(DB_PATH, sender_email, phone_number):
                        log.info("📝 Updated visitor record with phone number")
                        
                        # Attempt promotion to client (will delete visitor record)
                        promotion_result = promote_visitor_to_client(
                            phone=phone_number,
                            email=sender_email,
                            DB_PATH=DB_PATH
                        )
                        log.info(f"📬 Promotion result: {promotion_result}")
                        
                        if promotion_result.get("status") == "success":
                            client_id = promotion_result["client_id"]
                            reply = f"Thank you for providing your phone number ({phone_number}). Our team will contact you shortly."
                            
                            save_message(DB_PATH, is_client=True, sender=sender_email,
                                       message=body, user_id=client_id, channel="email")
                            save_message(DB_PATH, is_client=True, sender="bot",
                                       message=reply, user_id=client_id, channel="email")
                            send_email(sender_email, "Re: Thank you", reply,
                                     EMAIL_ACCOUNT, SMTP_SERVER, EMAIL_APP_PASSWORD, message_id)
                            continue
                            
                        elif promotion_result.get("status") == "exists":
                            log.info("ℹ️ Visitor already promoted to client")
                            client_record = authentication_user(DB_PATH, sender_email)
                            if client_record:
                                client_id, flag = client_record
                                reply = "Thank you for your message. We already have your information."
                                save_message(DB_PATH, is_client=True, sender=sender_email,
                                            message=body, user_id=client_id, channel="email")
                                save_message(DB_PATH, is_client=True, sender="bot",
                                            message=reply, user_id=client_id, channel="email")
                                send_email(sender_email, "Re: Thank you", reply,
                                          EMAIL_ACCOUNT, SMTP_SERVER, EMAIL_APP_PASSWORD, message_id)
                                continue

            # If no valid phone number found or promotion failed
            reply = "Please provide your phone number in international format (e.g., +923001981991) to proceed."
            send_email(sender_email, "Re: We need your phone number", reply,
                      EMAIL_ACCOUNT, SMTP_SERVER, EMAIL_APP_PASSWORD, message_id)
            continue

        # Step 3: New visitor
        log.info("📅 New visitor detected")
        temp_id = generate_temp_id(sender_email)
        
        try:
            # Insert visitor with empty phone
            if insert_visitor(
                DB_PATH=DB_PATH,
                temp_id=temp_id,
                email=sender_email,
                phone="",
                name="Email User"
            ):
                log.info(f"✅ New visitor created: {temp_id}")
                reply = """Welcome! To get started, please reply with:
                
                Your phone number in international format (e.g., +923001981991)
                
                Our team will then contact you to complete onboarding."""
            else:
                reply = "We already have your information. Please provide your phone number to continue."
                
            send_email(sender_email, "Re: Welcome", reply,
                     EMAIL_ACCOUNT, SMTP_SERVER, EMAIL_APP_PASSWORD, message_id)
        except Exception as e:
            log.error(f"❌ Visitor creation failed: {e}")
            reply = "We encountered an error. Please try again later."
            send_email(sender_email, "Re: Welcome", reply,
                     EMAIL_ACCOUNT, SMTP_SERVER, EMAIL_APP_PASSWORD, message_id)