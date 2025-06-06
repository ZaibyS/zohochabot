
# from logger.custom_logger import setup_logger
# from openai import OpenAI
# import json

# from .tools_functions import add_visitor, retrieve_experts
# from .tools import add_visitor_tool, retrieve_expert_tool
# from config.config import MODEL_NAME

# logger = setup_logger()

# def generate_visitor_reply(conversation, system_prompt, visitor_id):
#     logger.info("Generating WhatsApp visitor reply with LLM + tools")

#     try:
#         client = OpenAI()

#         messages = [{"role": "system", "content": system_prompt}]
#         if conversation:
#             for m in conversation:
#                 role = "user" if m[0] != "bot" else "assistant"
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
#                 tool_result = add_visitor(
#                     name=args["name"],
#                     email=args["email"],
#                     phone=visitor_id,
#                     consent=args["consent"]
#                 )
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

#         return response.output_text

#     except Exception as e:
#         logger.error("LLM error: %s", e)
#         return "Thanks for reaching out! Our team will get back to you shortly."

# def generate_client_reply(conversation, system_prompt):
#     logger.info("Generating WhatsApp client reply with LLM + tools")

#     try:
#         client = OpenAI()

#         messages = [{"role": "system", "content": system_prompt}]
#         if conversation:
#             for m in conversation:
#                 role = "user" if m[0] != "bot" else "assistant"
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

#         return response.output_text

#     except Exception as e:
#         logger.error("LLM error: %s", e)
#         return "Thanks for reaching out! Our team will get back to you shortly."



# ///////////////////////////////////////////////////////////////////////////////////////////

# openai_flow_functions.py

import json
from openai import OpenAI
from logger.custom_logger import setup_logger
from .tools_functions import add_visitor, retrieve_experts
from .tools import add_visitor_tool, retrieve_expert_tool
from config.config import MODEL_NAME

logger = setup_logger()


def generate_visitor_reply(conversation, system_prompt, visitor_id):
    """
    Handles new user or visitor conversation and triggers add_visitor if tool call detected.
    """
    logger.info("🤖 Generating WhatsApp visitor reply via LLM")

    try:
        client = OpenAI()

        messages = [{"role": "system", "content": system_prompt}]
        for sender, msg in conversation:
            role = "user" if sender != "bot" else "assistant"
            messages.append({"role": role, "content": msg})

        # First LLM response
        response = client.responses.create(
            model=MODEL_NAME,
            input=messages,
            tools=[add_visitor_tool],
            temperature=0.5
        )

        reply = response.output[0]

        # 📦 Tool call: add_visitor
        if reply.type == "function_call" and reply.name == "add_visitor":
            logger.info("📦 LLM tool call detected: add_visitor")

            tool_call = reply
            args = json.loads(tool_call.arguments)

            result = add_visitor(
                name=args["name"],
                email=args["email"],
                phone=visitor_id,
                consent=args["consent"]
            )
            logger.info("✅ add_visitor result: %s", result)

            # Add tool call + output to messages
            messages.append({
                "type": "function_call",
                "name": "add_visitor",
                "arguments": json.dumps(args)
            })
            messages.append({
                "type": "function_call_output",
                "call_id": tool_call.call_id,
                "output": result
            })

            # Follow-up LLM response after tool completion
            follow_up = client.responses.create(
                model=MODEL_NAME,
                input=messages,
                tools=[add_visitor_tool],
                temperature=0.5
            )

            return follow_up.output_text

        return response.output_text

    except Exception as e:
        logger.error("❌ LLM error (visitor): %s", e)
        return "Hi! Please share your email so our team can get in touch and complete your onboarding."


def generate_client_reply(conversation, system_prompt):
    """
    Handles client flow including expert matching using retrieve_experts tool.
    """
    logger.info("🤖 Generating WhatsApp client reply via LLM")

    try:
        client = OpenAI()

        messages = [{"role": "system", "content": system_prompt}]
        for sender, msg in conversation:
            role = "user" if sender != "bot" else "assistant"
            messages.append({"role": role, "content": msg})

        # Initial response
        response = client.responses.create(
            model=MODEL_NAME,
            input=messages,
            tools=[retrieve_expert_tool],
            temperature=0.5
        )

        reply = response.output[0]

        # 📦 Tool call: retrieve_experts
        if reply.type == "function_call" and reply.name == "retrieve_experts":
            logger.info("📦 LLM tool call detected: retrieve_experts")

            tool_result = retrieve_experts()

            messages.append({
                "type": "function_call",
                "name": "retrieve_experts",
                "arguments": "{}"
            })
            messages.append({
                "type": "function_call_output",
                "call_id": reply.call_id,
                "output": json.dumps(tool_result)
            })

            follow_up = client.responses.create(
                model=MODEL_NAME,
                input=messages,
                tools=[retrieve_expert_tool],
                temperature=0.5
            )

            return follow_up.output_text

        return response.output_text

    except Exception as e:
        logger.error("❌ LLM error (client): %s", e)
        return "Thanks for reaching out! Our team will get back to you shortly."


def generate_onboard_reply(conversation, system_prompt):
    """
    Responds to a client who has registered but is not yet onboarded (flag=False).
    """
    logger.info("🤖 Generating onboarding client reply via LLM")

    try:
        client = OpenAI()

        messages = [{"role": "system", "content": system_prompt}]
        for sender, msg in conversation:
            role = "user" if sender != "bot" else "assistant"
            messages.append({"role": role, "content": msg})

        response = client.responses.create(
            model=MODEL_NAME,
            input=messages,
            tools=[],  # no tools used during onboarding
            temperature=0.5
        )

        return response.output_text

    except Exception as e:
        logger.error("❌ LLM error (onboard): %s", e)
        return "You're already registered! Our team will reach out soon to complete your onboarding."
