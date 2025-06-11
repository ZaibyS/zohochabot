# import json

# from autogen import (
#     register_function,
#     GroupChat,
#     GroupChatManager,
#     Agent
# )

# from src.bot_flow.tools_functions import (
#     authenticate_client,
#     authenticate_visitor,
#     add_visitor,
#     hands_off,
#     retrive_experts
# )

# from src.bot_flow.agents import (
#     auth_agent,
#     explore_agent,
#     connect_agent,
#     the_human,
#     executor_agent,
#     intent_agent,

# )

# from src.bot_flow.flow import custom_speaker_selection_func

# from logger.custom_logger import setup_logger

# log = setup_logger()

# register_function(
#     authenticate_visitor,
#     caller=auth_agent,
#     executor=executor_agent,
#     description="Checks whether the user is a known visitor in the platform based on their email or phone number.",
# )

# register_function(
#     authenticate_client,
#     caller=auth_agent,
#     executor=executor_agent,
#     description="Verifies if the client is already registered in the platform using their email or phone number.",
# )

# register_function(
#     add_visitor,
#     caller=auth_agent,
#     executor=executor_agent,
#     description="Adds a new visitor to the platform by storing their name, email, phone number, and consent, or returns the existing visitor ID if they are already registered.",
# )

# register_function(
#     hands_off    ,
#     caller=intent_agent,
#     executor=executor_agent,
#     description="This function determines which specialized agent (e.g., explore_agent or connect_agent) should handle the next part of the conversation based on the client's intent. It returns the name of the agent to hand off to.",
# )

# register_function(
#     retrive_experts    ,
#     caller=connect_agent,
#     executor=executor_agent,
#     description="This function retrieves a list of all expert profiles stored in the database. It returns detailed information including name, email, qualifications, past companies, country, areas of expertise, years of experience, and timestamp. It is typically used by the connect_agent to find and display relevant experts to the client.",
# )
    
# planning_chat = GroupChat(
#     agents=[the_human, auth_agent, executor_agent, intent_agent, connect_agent, explore_agent],
#     messages=[],
#     max_round=100,
#     speaker_selection_method=custom_speaker_selection_func,
# )

# planning_manager = GroupChatManager(
#     groupchat=planning_chat,
# )

# design_chat_result = planning_manager.initiate_chat(
#     recipient=the_human, message="Hello! To get started, could you please provide either your email address or your phone number? This will help me verify your registration status."
# )

# print("Design Chat Result:", design_chat_result.chat_history)










# ///////////////////////////////////////////////////////////////////////////////////////////////////


# main.py
print("Ku nai chal raha")
from autogen import register_function, GroupChat, GroupChatManager
from src.bot_flow.tools_functions import (
    authenticate_client, authenticate_visitor,
    add_visitor, hands_off, retrieve_experts,
    suggest_companies
)
from src.bot_flow.agents import (
    auth_agent, explore_agent, connect_agent,
    the_human, executor_agent, intent_agent
)
from src.bot_flow.flow import custom_speaker_selection_func, ConversationState
from logger.custom_logger import setup_logger

log = setup_logger()

# Register functions
register_function(authenticate_visitor, caller=auth_agent, executor=executor_agent, description="Auth visitor by email/phone")
register_function(authenticate_client, caller=auth_agent, executor=executor_agent, description="Auth client by email/phone")
register_function(add_visitor, caller=auth_agent, executor=executor_agent, description="Add new visitor to database")
register_function(hands_off, caller=intent_agent, executor=executor_agent, description="Route to appropriate agent")
register_function(retrieve_experts, caller=connect_agent, executor=executor_agent, description="Retrieve experts from Zoho DB")
register_function(suggest_companies, caller=explore_agent, executor=executor_agent, description="Suggest companies using LLM")

# Agents
agents = [the_human, auth_agent, executor_agent, intent_agent, connect_agent, explore_agent]

planning_chat = GroupChat(
    agents=agents,
    messages=[],
    max_round=50,
    speaker_selection_method=custom_speaker_selection_func
)
planning_chat.state = ConversationState()

manager = GroupChatManager(groupchat=planning_chat)

def start_chat():
    welcome_msg = (
        "Welcome to our Expert Matching Platform!\n\n"
        "To get started, could you please provide either:\n"
        "1. Your email address\n"
        "2. Your phone number\n\n"
        "This will help me verify your account."
    )
    manager.initiate_chat(recipient=the_human, message=welcome_msg)

if __name__ == "__main__":
    start_chat()