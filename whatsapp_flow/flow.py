# def process_whatsapp_message(DB_PATH, system_prompt_visitor, system_prompt_client, incoming_data):
#     message_data = wa_api.parse_incoming_message(incoming_data)
#     if not message_data:
#         return

#     sender_phone = message_data["from"]
#     body = message_data["body"].strip()
#     log.info(f"📨 Incoming WhatsApp message from {sender_phone}: {body}")

#     # Step 1: Check if user is already a client (onboarded or in progress)
#     client_record = authentication_email(DB_PATH, sender_phone)
#     if client_record:
#         client_id, flag = client_record

#         # ✅ Treat all clients (flag True or False) the same way using generate_client_reply
#         save_message(DB_PATH, is_client=True, sender=sender_phone, message=body, user_id=client_id, channel="whatsapp")
#         conversation = get_conversation(DB_PATH, user_id=client_id, limit=20)
#         reply = generate_client_reply(conversation, system_prompt_client)
#         save_message(DB_PATH, is_client=True, sender="bot", message=reply, user_id=client_id, channel="whatsapp")
#         wa_api.send_message(sender_phone, reply)
#         return

#     # Step 2: If user exists as a visitor
#     visitor_id = authenticate_visitor(DB_PATH, sender_phone)
#     elif visitor_id:
#         log.info("🔁 Returning visitor")

#         if is_valid_email(body):
#             # ✅ Promote to client immediately if email is valid
#             promotion_result = promote_visitor_to_client(phone=sender_phone, email=body, DB_PATH=DB_PATH)
#             log.info("📬 Promotion result: %s", promotion_result)

#             if promotion_result.get("status") == "success":
#                 new_client_record = authentication_email(DB_PATH, sender_phone)
#                 if new_client_record:
#                     new_client_id, _ = new_client_record
#                     save_message(DB_PATH, is_client=True, sender=sender_phone, message=body, user_id=new_client_id, channel="whatsapp")

#                     # ✅ First-time welcome message
#                     reply = "🎉 Thank you! We've received your email. Our team will contact you shortly to complete the onboarding process."
#                     save_message(DB_PATH, is_client=True, sender="bot", message=reply, user_id=new_client_id, channel="whatsapp")
#                     wa_api.send_message(sender_phone, reply)
#                 return

#             elif promotion_result.get("status") == "exists":
#                 # If already in clients due to DB conflict, treat them as normal client
#                 client_record = authentication_email(DB_PATH, sender_phone)
#                 if client_record:
#                     client_id, _ = client_record
#                     save_message(DB_PATH, is_client=True, sender=sender_phone, message=body, user_id=client_id, channel="whatsapp")
#                     conversation = get_conversation(DB_PATH, user_id=client_id, limit=20)
#                     reply = generate_client_reply(conversation, system_prompt_client)
#                     save_message(DB_PATH, is_client=True, sender="bot", message=reply, user_id=client_id, channel="whatsapp")
#                     wa_api.send_message(sender_phone, reply)
#                 return

#         # ❗ User is still a visitor but hasn't sent a valid email yet
#         wa_api.send_message(sender_phone, "📩 Please provide your email to proceed with onboarding.")
#         return

#     # Step 3: Completely new user → insert into visitors and ask for email
#     log.info("📅 New visitor detected")
#     temp_id = generate_temp_id(sender_phone)

#     try:
#         add_visitor(visitor_id=temp_id, name="WhatsApp User", email="", phone=sender_phone, consent=True, DB_PATH=DB_PATH)
#         log.info("✅ Visitor inserted successfully")
#     except Exception as e:
#         log.warning("⚠️ Visitor insert failed or already exists: %s", str(e))
#         return

#     # First contact → ask for email
#     wa_api.send_message(sender_phone, "📩 Please provide your email to proceed with onboarding.")


# flow.py
# import os
# from dotenv import load_dotenv
# from .whatsapp_flow_functions import WhatsAppAPI
# from .db_flow_functions import save_message, get_conversation
# from .utils import (
#     authentication_email,
#     generate_temp_id,
#     authenticate_visitor,
#     is_valid_email
# )
# from .openai_flow_functions import (
#     generate_client_reply,
# )
# from .tools_functions import (
#     promote_visitor_to_client,
#     try_promote_visitor_if_ready,
#     # update_visitor_email,
#     add_visitor
# )
# from logger.custom_logger import setup_logger

# log = setup_logger(__name__)
# load_dotenv()

# wa_api = None


# def init(api_url, api_key, phone_number_id):
#     global wa_api
#     wa_api = WhatsAppAPI(api_url, api_key, phone_number_id)




# def process_whatsapp_message(DB_PATH, system_prompt_visitor, system_prompt_client, incoming_data):
#     message_data = wa_api.parse_incoming_message(incoming_data)
#     if not message_data:
#         return

#     sender_phone = message_data["from"]
#     body = message_data["body"].strip()
#     log.info(f"📨 Incoming WhatsApp message from {sender_phone}: {body}")

#     # Step 1: Check if user is already a client (onboarded or in progress)
#     client_record = authentication_email(DB_PATH, sender_phone)
#     if client_record:
#         client_id, flag = client_record

#         # ✅ Treat all clients (flag True or False) the same way using generate_client_reply
#         save_message(DB_PATH, is_client=True, sender=sender_phone, message=body, user_id=client_id, channel="whatsapp")
#         conversation = get_conversation(DB_PATH, user_id=client_id, limit=20)
#         reply = generate_client_reply(conversation, system_prompt_client)
#         save_message(DB_PATH, is_client=True, sender="bot", message=reply, user_id=client_id, channel="whatsapp")
#         wa_api.send_message(sender_phone, reply)
#         return

#     # Step 2: If user exists as a visitor
#     elif (visitor_id := authenticate_visitor(DB_PATH, sender_phone)):
#         log.info("🔁 Returning visitor")

#         if is_valid_email(body):
#             # ✅ Promote to client immediately if email is valid
#             promotion_result = promote_visitor_to_client(phone=sender_phone, email=body, DB_PATH=DB_PATH)
#             log.info("📬 Promotion result: %s", promotion_result)

#             if promotion_result.get("status") == "success":
#                 new_client_record = authentication_email(DB_PATH, sender_phone)
#                 if new_client_record:
#                     new_client_id, _ = new_client_record
#                     save_message(DB_PATH, is_client=True, sender=sender_phone, message=body, user_id=new_client_id, channel="whatsapp")

#                     # ✅ First-time welcome message
#                     reply = "🎉 Thank you! We've received your email. Our team will contact you shortly to complete the onboarding process."
#                     save_message(DB_PATH, is_client=True, sender="bot", message=reply, user_id=new_client_id, channel="whatsapp")
#                     wa_api.send_message(sender_phone, reply)
#                 return

#             elif promotion_result.get("status") == "exists":
#                 # If already in clients due to DB conflict, treat them as normal client
#                 client_record = authentication_email(DB_PATH, sender_phone)
#                 if client_record:
#                     client_id, _ = client_record
#                     save_message(DB_PATH, is_client=True, sender=sender_phone, message=body, user_id=client_id, channel="whatsapp")
#                     conversation = get_conversation(DB_PATH, user_id=client_id, limit=20)
#                     reply = generate_client_reply(conversation, system_prompt_client)
#                     save_message(DB_PATH, is_client=True, sender="bot", message=reply, user_id=client_id, channel="whatsapp")
#                     wa_api.send_message(sender_phone, reply)
#                 return

#         # ❗ User is still a visitor but hasn't sent a valid email yet
#         wa_api.send_message(sender_phone, "📩 Please provide your email to proceed with onboarding.")
#         return

#     # Step 3: Completely new user → insert into visitors and ask for email
#     else:
#         log.info("📅 New visitor detected")
#         temp_id = generate_temp_id(sender_phone)

#         try:
#             add_visitor(visitor_id=temp_id, name="WhatsApp User", email="", phone=sender_phone, consent=True, DB_PATH=DB_PATH)
#             log.info("✅ Visitor inserted successfully")
#         except Exception as e:
#             log.warning("⚠️ Visitor insert failed or already exists: %s", str(e))
#             return

#         # First contact → ask for email
#         wa_api.send_message(sender_phone, "📩 Please provide your email to proceed with onboarding.")












# ////
import os
from dotenv import load_dotenv
from .whatsapp_flow_functions import WhatsAppAPI
from .db_flow_functions import save_message, get_conversation
from .utils import (
    authentication_email,
    generate_temp_id,
    authenticate_visitor,
    is_valid_email,
    authentication_user
)
from .openai_flow_functions import (
    generate_client_reply,
    generate_visitor_reply,
    generate_onboard_reply
)
from .tools_functions import (
    promote_visitor_to_client,
    try_promote_visitor_if_ready,
    add_visitor
)
from logger.custom_logger import setup_logger

log = setup_logger(__name__)
load_dotenv()

wa_api = None

def init(api_url, api_key, phone_number_id):
    global wa_api
    wa_api = WhatsAppAPI(api_url, api_key, phone_number_id)

# def process_whatsapp_message(DB_PATH, system_prompt_visitor, system_prompt_client, incoming_data):
#     message_data = wa_api.parse_incoming_message(incoming_data)
#     if not message_data:
#         return

#     sender_phone = message_data["from"]
#     body = message_data["body"].strip()
#     log.info(f"📨 Incoming WhatsApp message from {sender_phone}: {body}")

#     # Step 1: Check if user exists in clients table
#     client_record = authentication_email(DB_PATH, sender_phone)
#     if client_record:
#         client_id, flag = client_record
        
#         # Save the incoming message
#         save_message(DB_PATH, is_client=True, sender=sender_phone, 
#                     message=body, user_id=client_id, channel="whatsapp")
        
#         conversation = get_conversation(DB_PATH, user_id=client_id, limit=20)
        
#         # Check flag status (0 = not onboarded, 1 = onboarded)
#         if flag == 0:
#             # Fully onboarded client - use client prompt
#             log.info("🔄 Registered but not onboarded client detected")
#             reply = generate_client_reply(conversation, system_prompt_client)
#         else:
#             # Registered but not onboarded - use visitor prompt
#             log.info("👔 Fully onboarded client detected")
#             reply = generate_onboard_reply(conversation, system_prompt_visitor)
        
#         save_message(DB_PATH, is_client=True, sender="bot", 
#                     message=reply, user_id=client_id, channel="whatsapp")
#         wa_api.send_message(sender_phone, reply)
#         return

#     # Step 2: Check if user exists as visitor
#     elif (visitor_id := authenticate_visitor(DB_PATH, sender_phone)):
#         log.info("🔁 Returning visitor detected")
        
#         if is_valid_email(body):
#             # Attempt promotion to client if email is valid
#             promotion_result = promote_visitor_to_client(
#                 phone=sender_phone, 
#                 email=body, 
#                 DB_PATH=DB_PATH
#             )
#             log.info(f"📬 Promotion result: {promotion_result}")

#             if promotion_result.get("status") == "success":
#                 new_client_record = authentication_email(DB_PATH, sender_phone)
#                 if new_client_record:
#                     new_client_id, flag = new_client_record
#                     save_message(DB_PATH, is_client=True, sender=sender_phone, 
#                                 message=body, user_id=new_client_id, channel="whatsapp")
                    
#                     # Use visitor prompt since flag is likely 0 (not onboarded)
#                     reply = generate_onboard_reply([], system_prompt_visitor)
#                     save_message(DB_PATH, is_client=True, sender="bot", 
#                                 message=reply, user_id=new_client_id, channel="whatsapp")
#                     wa_api.send_message(sender_phone, reply)
#                 return
#             elif promotion_result.get("status") == "exists":
#                 # Handle case where client already exists (should be caught in Step 1)
#                 client_record = authentication_email(DB_PATH, sender_phone)
#                 if client_record:
#                     client_id, flag = client_record
#                     save_message(DB_PATH, is_client=True, sender=sender_phone, 
#                                 message=body, user_id=client_id, channel="whatsapp")
#                     conversation = get_conversation(DB_PATH, user_id=client_id, limit=20)
#                     reply = generate_onboard_reply(conversation, system_prompt_visitor)
#                     save_message(DB_PATH, is_client=True, sender="bot", 
#                                 message=reply, user_id=client_id, channel="whatsapp")
#                     wa_api.send_message(sender_phone, reply)
#                 return

#         # Still a visitor - ask for valid email
#         wa_api.send_message(sender_phone, "📩 Please provide a valid email address to proceed with onboarding.")
#         return

#     # Step 3: Completely new user
#     else:
#         log.info("📅 New visitor detected")
#         temp_id = generate_temp_id(sender_phone)

#         try:
#             add_visitor(visitor_id=temp_id, name="WhatsApp User", email="", 
#                        phone=sender_phone, consent=True, DB_PATH=DB_PATH)
#             log.info("✅ Visitor inserted successfully")
#         except Exception as e:
#             log.warning(f"⚠️ Visitor insert failed or already exists: {str(e)}")
#             return

#         # First contact - ask for email
#         wa_api.send_message(sender_phone, "👋 Welcome! Please provide your email address to begin the onboarding process.")


def process_whatsapp_message(DB_PATH, system_prompt_visitor, system_prompt_client, incoming_data):
    message_data = wa_api.parse_incoming_message(incoming_data)
    if not message_data:
        return

    sender_phone = message_data["from"]
    body = message_data["body"].strip()
    log.info(f"📨 Incoming WhatsApp message from {sender_phone}: {body}")

    # Step 1: Check if user exists in clients table
    client_record = authentication_user(DB_PATH, sender_phone)
    if client_record:
        client_id, flag = client_record
        
        # Save the incoming message
        save_message(DB_PATH, is_client=True, sender=sender_phone, 
                    message=body, user_id=client_id, channel="whatsapp")
        
        conversation = get_conversation(DB_PATH, user_id=client_id, limit=20)
        
        # Check flag status (0 = not onboarded, 1 = onboarded)
        if flag == 0:
            # Fully onboarded client - use client prompt
            log.info("🔄 Registered but not onboarded client detected")
            reply = generate_client_reply(conversation, system_prompt_client)
        else:
            # Registered but not onboarded - use visitor prompt
            log.info("👔 Fully onboarded client detected")
            reply = generate_onboard_reply(conversation, system_prompt_visitor)
        
        save_message(DB_PATH, is_client=True, sender="bot", 
                    message=reply, user_id=client_id, channel="whatsapp")
        wa_api.send_message(sender_phone, reply)
        return

    # Step 2: Check if user exists as visitor
    elif (visitor_id := authenticate_visitor(DB_PATH, sender_phone)):
        log.info("🔁 Returning visitor detected")
        
        if is_valid_email(body):
            # Attempt promotion to client if email is valid
            promotion_result = promote_visitor_to_client(
                phone=sender_phone, 
                email=body, 
                DB_PATH=DB_PATH
            )
            log.info(f"📬 Promotion result: {promotion_result}")

            if promotion_result.get("status") == "success":
                new_client_record = authentication_email(DB_PATH, sender_phone)
                if new_client_record:
                    new_client_id, flag = new_client_record
                    save_message(DB_PATH, is_client=True, sender=sender_phone, 
                                message=body, user_id=new_client_id, channel="whatsapp")
                    
                    # Hardcoded success message for newly promoted clients
                    reply = "Thank you for providing your email. Our team will call you soon for the onboarding process."
                    save_message(DB_PATH, is_client=True, sender="bot", 
                                message=reply, user_id=new_client_id, channel="whatsapp")
                    wa_api.send_message(sender_phone, reply)
                return
            elif promotion_result.get("status") == "exists":
                # Handle case where client already exists (should be caught in Step 1)
                client_record = authentication_email(DB_PATH, sender_phone)
                if client_record:
                    client_id, flag = client_record
                    save_message(DB_PATH, is_client=True, sender=sender_phone, 
                                message=body, user_id=client_id, channel="whatsapp")
                    conversation = get_conversation(DB_PATH, user_id=client_id, limit=20)
                    reply = generate_onboard_reply(conversation, system_prompt_visitor)
                    save_message(DB_PATH, is_client=True, sender="bot", 
                                message=reply, user_id=client_id, channel="whatsapp")
                    wa_api.send_message(sender_phone, reply)
                return

        # Still a visitor - ask for valid email
        wa_api.send_message(sender_phone, "📩 Please provide a valid email address to proceed with onboarding.")
        return

    # Step 3: Completely new user
    else:
        log.info("📅 New visitor detected")
        temp_id = generate_temp_id(sender_phone)

        try:
            add_visitor(visitor_id=temp_id, name="WhatsApp User", email="", 
                       phone=sender_phone, consent=True, DB_PATH=DB_PATH)
            log.info("✅ Visitor inserted successfully")
        except Exception as e:
            log.warning(f"⚠️ Visitor insert failed or already exists: {str(e)}")
            return

        # First contact - ask for email
        wa_api.send_message(sender_phone, "👋 Welcome! Please provide your email address to begin the onboarding process.")