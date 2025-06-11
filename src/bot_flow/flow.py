# import json
# import ast
# from autogen import (
#     GroupChat,
#     Agent
# )

# from src.bot_flow.agents import (
#     auth_agent,
#     the_human,
#     executor_agent,
#     intent_agent
# )

# from logger.custom_logger import setup_logger

# log = setup_logger(__name__)

# def custom_speaker_selection_func(last_speaker: Agent, groupchat: GroupChat):
#     messages = groupchat.messages

#     log.critical(messages[-1])

#     if last_speaker is the_human:
#         return auth_agent
    
#     elif last_speaker is auth_agent:
#         if messages[-1].get("tool_calls"):
#             return executor_agent
#         else:
#             return the_human 
        
#     elif last_speaker is executor_agent:
#         if messages[-1].get("role") == "tool" and messages[-2]["tool_calls"][0]["function"]["name"] == "authenticate_client":
#             content = ast.literal_eval(messages[-1].get("content"))
#             if content.get("status") == "success":
#                 return intent_agent
        
#         # elif last_speaker is executor_agent and messages[-2].get("name") == "connect_agent":
#         #     return the_human
        
#         # elif messages[-1].get("role") == "tool":
#         #     tool_output = messages[-1].get("content")
#         #     tool_name = messages[-2].get("tool_calls", [{}])[0].get("function", {}).get("name", "")

#         #     if tool_name == "hands_off":
#         #         if tool_output == "connect_agent":
#         #             return connect_agent
                
#         #         elif tool_output == "explore_agent":
#         #             return explore_agent

#         else:
#             return auth_agent   
        
    # elif last_speaker is executor_agent:
    #     return auth_agent

    # if len(messages) <= 1:
    #     return the_human  # Start with the human agent

    # if len(messages) > 2  and last_speaker is the_human and  messages[-2].get("name") == "intent_agent":
    #     return intent_agent
    
    # elif len(messages) > 2  and last_speaker is the_human and messages[-2].get("name") == "connect_agent":
    #     return connect_agent

    # elif last_speaker is the_human:
    #     return auth_agent

    # elif last_speaker is auth_agent:
    #     if messages and messages[-1].get("tool_calls"):
    #         return executor_agent
    #     else:
    #         return the_human 
        
    # elif last_speaker is intent_agent:
    #     if messages and messages[-1].get("tool_calls"):
    #         return executor_agent
    #     else:
    #         return the_human
        
    # elif last_speaker is connect_agent:
    #     if messages and messages[-1].get("tool_calls"):
    #         return executor_agent
    #     else:
    #         return the_human

    # elif last_speaker is executor_agent:
    #     if messages[-1].get("role") == "tool" and messages[-1].get("content") == "{\"status\": \"success\", \"code\": 200}" and messages[-2]["tool_calls"][0]["function"]["name"] == "authentication":
    #         return intent_agent
        
    #     elif last_speaker is executor_agent and messages[-2].get("name") == "connect_agent":
    #         return the_human
        
    #     elif messages[-1].get("role") == "tool":
    #         tool_output = messages[-1].get("content")
    #         tool_name = messages[-2].get("tool_calls", [{}])[0].get("function", {}).get("name", "")

    #         if tool_name == "hands_off":
    #             if tool_output == "connect_agent":
    #                 return connect_agent
                
    #             elif tool_output == "explore_agent":
    #                 return explore_agent
                
    #     return the_human
        
    # else:
    #     return "random"
    
    
    
    
    
    
    
    
    # //////////////////////////////////////////////////////////////////////
    
    
# import ast
# from autogen import (
#     GroupChat,
#     Agent
# )

# from src.bot_flow.agents import (
#     auth_agent,
#     the_human,
#     executor_agent,
#     intent_agent
# )

# from logger.custom_logger import setup_logger

# log = setup_logger(__name__)

# def custom_speaker_selection_func(last_speaker: Agent, groupchat: GroupChat):
#     messages = groupchat.messages
#     log.critical(messages[-1])  # Log last message for debugging

#     if last_speaker is the_human:
#         return auth_agent

#     elif last_speaker is auth_agent:
#         if messages[-1].get("tool_calls"):
#             return executor_agent
#         else:
#             return the_human

#     elif last_speaker is executor_agent:
#         # Check if the last tool response was for authenticate_client
#         if messages[-1].get("role") == "tool" and messages[-2].get("tool_calls", [{}])[0].get("function", {}).get("name") == "authenticate_client":
#             try:
#                 content = ast.literal_eval(messages[-1].get("content"))
#                 if content.get("status") == "success":
#                     return intent_agent
#                 else:
#                     return auth_agent  # fallback if authentication failed
#             except Exception as e:
#                 log.error(f"Error parsing tool response content: {e}")
#                 return auth_agent  # safe fallback on error
#         else:
#             return auth_agent  # default fallback

#     else:
#         return the_human  # default fallback

    
    
    
# ////////////////////////////////////////////////////////////////////////////////////////////////


# src/bot_flow/flow.py

from autogen import GroupChat, Agent
from src.bot_flow.agents import (
    auth_agent, the_human, executor_agent,
    intent_agent, connect_agent, explore_agent
)
from src.bot_flow.utils import detect_language, extract_key_terms
from logger.custom_logger import setup_logger

log = setup_logger(__name__)

class ConversationState:
    def __init__(self):
        self.language = None
        self.client_info = None
        self.project_details = {}
        self.expert_search_params = {}
        self.selected_experts = []
        self.current_channel = "website"
        self.temp_id = None
        self.attachment_data = None

def custom_speaker_selection_func(last_speaker: Agent, groupchat: GroupChat):
    messages = groupchat.messages
    state = groupchat.state if hasattr(groupchat, 'state') else ConversationState()

    last_msg = messages[-1] if messages else {}

    # Auto-detect language once per session
    if not state.language and last_speaker is the_human:
        state.language = detect_language(last_msg.get("content", ""))
        log.info(f"Language detected: {state.language}")

    # Handle attachments
    if "attachment" in last_msg:
        state.attachment_data = last_msg["attachment"]
        key_terms = extract_key_terms(state.attachment_data.text)
        state.project_details.update(key_terms)
        return intent_agent  # Ask follow-up questions

    # Speaker logic
    if last_speaker is the_human:
        if not state.client_info:
            return auth_agent
        elif not state.project_details:
            return intent_agent
        else:
            return connect_agent

    elif last_speaker is auth_agent:
        if last_msg.get("tool_calls"):
            return executor_agent
        return the_human

    elif last_speaker is executor_agent:
        tool_name = last_msg.get("tool_calls", [{}])[0].get("function", {}).get("name", "")
        content = eval(last_msg.get("content"))

        if tool_name == "authenticate_client":
            if content.get("status") == "success":
                state.client_info = content
                return intent_agent

        elif tool_name == "retrieve_experts":
            if isinstance(content, list):
                state.selected_experts = content
                return connect_agent
            elif content.get("status") == "fallback":
                return explore_agent  # Fallback to explore

        return the_human

    elif last_speaker is intent_agent:
        if "connect" in last_msg.get("content", "").lower():
            return connect_agent
        return explore_agent

    return the_human