# streamlit_app/app.py

# bot_flow/bot_flow.py
import streamlit as st
from src.bot_flow.tools_functions import (
    authenticate_client,
    authenticate_visitor,
    add_visitor
)
from src.bot_flow.utils import is_valid_email, is_valid_phone_number, generate_id

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "step" not in st.session_state:
    st.session_state.step = "ask_credentials"

if "email" not in st.session_state:
    st.session_state.email = ""

if "phone" not in st.session_state:
    st.session_state.phone = ""

if "user_type" not in st.session_state:
    st.session_state.user_type = None

if "client_info" not in st.session_state:
    st.session_state.client_info = None


# Helper functions
def is_valid_input(input_value):
    return is_valid_email(input_value) or is_valid_phone_number(input_value)


def get_user_type(input_value):
    result = authenticate_client(input_value)
    if result["status"] == "success":
        return "client", result["client_id"]

    result = authenticate_visitor(input_value)
    if result["status"] == "success":
        return "visitor", result["visitor_id"]

    return "new", None


# UI
st.title("💬 Zoho Chatbot")

# Display chat history
for msg in st.session_state.chat_history:
    if msg["role"] == "bot":
        st.markdown(f"<div style='text-align:left; color:#262626'><b>Bot:</b> {msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align:right; color:#0078ff'><b>You:</b> {msg['content']}</div>", unsafe_allow_html=True)

# Input field
def send_message():
    user_input = st.session_state.user_input.strip()
    if not user_input:
        return

    st.session_state.chat_history.append({"role": "user", "content": user_input})

    if st.session_state.step == "ask_credentials":
        if not is_valid_input(user_input):
            st.session_state.chat_history.append({
                "role": "bot",
                "content": "Please provide a valid email or phone number."
            })
            return

        user_type, user_id = get_user_type(user_input)

        if user_type == "client":
            st.session_state.user_type = "client"
            st.session_state.client_info = {"client_id": user_id}
            st.session_state.step = "intent_selection"
            st.session_state.chat_history.append({
                "role": "bot",
                "content": "How can I help you today?\n\n1. Explore our platform\n2. Connect with an expert"
            })

        elif user_type == "visitor":
            st.session_state.user_type = "visitor"
            st.session_state.visitor_id = user_id
            st.session_state.chat_history.append({
                "role": "bot",
                "content": "Please provide the other credential (email or phone)."
            })

        elif user_type == "new":
            st.session_state.user_type = "new"
            if is_valid_email(user_input):
                st.session_state.email = user_input
                st.session_state.chat_history.append({
                    "role": "bot",
                    "content": "Please provide your phone number."
                })
            else:
                st.session_state.phone = user_input
                st.session_state.chat_history.append({
                    "role": "bot",
                    "content": "Please provide your email address."
                })

    elif st.session_state.step == "collect_second_credential":
        if not is_valid_input(user_input):
            st.session_state.chat_history.append({
                "role": "bot",
                "content": "Invalid input. Please provide a valid email or phone number."
            })
            return

        if is_valid_email(user_input):
            st.session_state.email = user_input
        elif is_valid_phone_number(user_input):
            st.session_state.phone = user_input

        name = "Temporary Name"
        consent = True
        result = add_visitor(name, st.session_state.email, st.session_state.phone, consent)

        if result["status"] == "success":
            st.session_state.visitor_id = result["visitor_id"]
            st.session_state.step = "intent_selection"
            st.session_state.chat_history.append({
                "role": "bot",
                "content": "Thank you! You're now registered. How can I help you today?\n\n1. Explore our platform\n2. Connect with an expert"
            })

    elif st.session_state.step == "intent_selection":
        choice = user_input.lower()
        if "explore" in choice:
            st.session_state.chat_history.append({
                "role": "bot",
                "content": "Welcome to our platform! Here's what we offer..."
            })
        elif "connect" in choice:
            st.session_state.chat_history.append({
                "role": "bot",
                "content": "Connecting you with experts..."
            })
        else:
            st.session_state.chat_history.append({
                "role": "bot",
                "content": "I didn't understand that. Please type 'Explore' or 'Connect'."
            })

    st.session_state.user_input = ""  # Clear input box


# Text input
st.text_input("Type your message...", key="user_input", on_change=send_message)