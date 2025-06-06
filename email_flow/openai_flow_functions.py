# from logger.custom_logger import setup_logger
# from openai import OpenAI
# import json

# from .tools_functions import add_visitor, retrieve_experts
# from .tools import add_visitor_tool, retrieve_expert_tool
# from config.config import EMAIL_ACCOUNT, MODEL_NAME

# logger = setup_logger()

# def generate_visitor_reply(conversation, system_prompt, visitor_email):
#     logger.info("Generating reply using LLM with tool support...")

#     try:
#         client = OpenAI()

#         messages = [{"role": "system", "content": system_prompt}]
#         if conversation:
#             for m in conversation:
#                 role = "user" if m[0] != EMAIL_ACCOUNT else "assistant"
#                 messages.append({"role": role, "content": m[1]})

#         response = client.responses.create(
#             model=MODEL_NAME,
#             input=messages,
#             tools=[add_visitor_tool],
#             temperature=0.5,
#         )

#         reply = response.output[0]

#         if reply.type == "function_call":
#             tool_call = response.output[0]
#             if tool_call.name == "add_visitor":
#                 logger.info("Tool call detected: add_visitor")
#                 args = json.loads(tool_call.arguments)
#                 tool_result = add_visitor(args["name"], email=visitor_email, phone=args["phone"], consent=args["consent"])
#                 logger.info("Tool output: %s", tool_result)

#                 messages.append(tool_call)  
#                 messages.append({                               
#                     "type": "function_call_output",
#                     "call_id": tool_call.call_id,
#                     "output": str(tool_result)
#                 })

#                 follow_up_response = client.responses.create(
#                     model=MODEL_NAME,
#                     input=messages,
#                     temperature=0.5,
#                     tools=[add_visitor_tool],
#                 )

#                 return follow_up_response.output_text
            
#         # logger.critical("Reply: %s", response.output_text)
#         return response.output_text

#     except Exception as e:
#         logger.error("Failed to generate reply: %s", e)
#         return "Thank you for reaching out! We will get back to you shortly."

# def generate_client_reply(conversation, system_prompt):
#     logger.info("Generating reply using LLM with tool support...")

#     try:
#         client = OpenAI()

#         messages = [{"role": "system", "content": system_prompt}]
#         if conversation:
#             for m in conversation:
#                 role = "user" if m[0] != EMAIL_ACCOUNT else "assistant"
#                 messages.append({"role": role, "content": m[1]})

#         response = client.responses.create(
#             model=MODEL_NAME,
#             input=messages,
#             tools=[retrieve_expert_tool],
#             temperature=0.5,
#         )

#         reply = response.output[0]

#         if reply.type == "function_call":
#             tool_call = response.output[0]
            
#             if tool_call.name == "retrieve_experts":
#                 logger.info("Tool call detected: retrieve_experts")
#                 args = json.loads(tool_call.arguments)
#                 tool_result = retrieve_experts()
#                 logger.info("Tool output: %s", tool_result)

#                 messages.append(tool_call)  
#                 messages.append({                               
#                     "type": "function_call_output",
#                     "call_id": tool_call.call_id,
#                     "output": str(tool_result)
#                 })

#                 follow_up_response = client.responses.create(
#                     model=MODEL_NAME,
#                     input=messages,
#                     temperature=0.5,
#                     tools=[retrieve_expert_tool],
#                 )

#                 return follow_up_response.output_text
#         # logger.critical("Reply: %s", response.output_text)
#         return response.output_text

#     except Exception as e:
#         logger.error("Failed to generate reply: %s", e)
#         return "Thank you for reaching out! We will get back to you shortly."




from logger.custom_logger import setup_logger
from openai import OpenAI
from typing import Dict, Any
import json
import os   
from .tools_functions import add_visitor, retrieve_experts
from .tools import add_visitor_tool, retrieve_expert_tool
from .db_flow_functions import insert_visitor
from .utils import generate_temp_id, is_valid_email, is_valid_phone
from config.config import EMAIL_ACCOUNT, MODEL_NAME

logger = setup_logger()


def generate_onboard_reply(conversation, system_prompt, visitor_email):
    logger.info("Generating reply using LLM with tool support...")

    try:
        client = OpenAI()

        # Prepare conversation
        messages = [{"role": "system", "content": system_prompt}]
        if conversation:
            for m in conversation:
                role = "user" if m[0] != EMAIL_ACCOUNT else "assistant"
                messages.append({"role": role, "content": m[1]})

        response = client.responses.create(
            model=MODEL_NAME,
            input=messages,
            tools=[add_visitor_tool],
            temperature=0.5,
        )

        reply = response.output[0]

        # 🛠️ Handle tool-based visitor capture
        if reply.type == "function_call":
            tool_call = response.output[0]
            if tool_call.name == "add_visitor":
                logger.info("Tool call detected: add_visitor")
                args = json.loads(tool_call.arguments)

                name = args.get("name", "Visitor")
                phone = args.get("phone", None)
                consent = args.get("consent", "unspecified")

                # Insert via tool_functions and DB (fallback double safety)
                tool_result = add_visitor(name, email=visitor_email, phone=phone, consent=consent)
                insert_visitor(DB_PATH=os.getenv("DB_PATH"), temp_id=generate_temp_id(visitor_email), email=visitor_email, phone=phone, name=name)

                messages.append(tool_call)
                messages.append({
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": str(tool_result)
                })

                follow_up_response = client.responses.create(
                    model=MODEL_NAME,
                    input=messages,
                    temperature=0.5,
                    tools=[add_visitor_tool],
                )

                return follow_up_response.output_text

        # ⚠️ No tool call: fallback reply, still insert visitor
        logger.info("No tool call made. Fallback visitor insert.")
        insert_visitor(DB_PATH=os.getenv("DB_PATH"),
                       temp_id=generate_temp_id(visitor_email),
                       email=visitor_email,
                       name="Visitor")

        return response.output_text

    except Exception as e:
        logger.error("Failed to generate visitor reply: %s", e)
        return "Thank you for reaching out! We will get back to you shortly."


def generate_client_reply(conversation, system_prompt):
    logger.info("Generating client reply using LLM...")

    try:
        client = OpenAI()

        messages = [{"role": "system", "content": system_prompt}]
        if conversation:
            for m in conversation:
                role = "user" if m[0] != EMAIL_ACCOUNT else "assistant"
                messages.append({"role": role, "content": m[1]})

        response = client.responses.create(
            model=MODEL_NAME,
            input=messages,
            tools=[retrieve_expert_tool],
            temperature=0.5,
        )

        reply = response.output[0]

        if reply.type == "function_call":
            tool_call = response.output[0]

            if tool_call.name == "retrieve_experts":
                logger.info("Tool call detected: retrieve_experts")
                args = json.loads(tool_call.arguments)
                tool_result = retrieve_experts()

                messages.append(tool_call)
                messages.append({
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": str(tool_result)
                })

                follow_up_response = client.responses.create(
                    model=MODEL_NAME,
                    input=messages,
                    temperature=0.5,
                    tools=[retrieve_expert_tool],
                )

                return follow_up_response.output_text

        return response.output_text

    except Exception as e:
        logger.error("Failed to generate client reply: %s", e)
        return "Thank you for reaching out! We will get back to you shortly."
