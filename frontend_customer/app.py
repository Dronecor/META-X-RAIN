import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/api/v1")
CHAT_ENDPOINT = f"{API_URL}/chat/message"

st.set_page_config(page_title="ShopBuddy", page_icon="🛍️", layout="wide")

# -----------------------------------------------------------------------------
# Customer Identification & Login
# -----------------------------------------------------------------------------
if "user_info" not in st.session_state:
    st.session_state.user_info = None

if not st.session_state.user_info:
    st.title("👋 Welcome to ShopBuddy!")
    st.write("Please sign in to continue your personalized shopping experience.")
    
    with st.form("login_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number (Optional)")
        submit = st.form_submit_button("Sign In")
        
        if submit:
            if name and email:
                st.session_state.user_info = {
                    "full_name": name,
                    "email": email,
                    "user_id": email 
                }
                st.rerun()
            else:
                st.error("Please provide at least Name and Email.")
    st.stop()

# -----------------------------------------------------------------------------
# Main Interface: Sidebar for Conversation Management
# -----------------------------------------------------------------------------
user = st.session_state.user_info

# Initialize conversation state
if "active_conversation_id" not in st.session_state:
    st.session_state.active_conversation_id = None
if "conversations" not in st.session_state:
    st.session_state.conversations = {}
if "current_messages" not in st.session_state:
    st.session_state.current_messages = []

# Sidebar: User Profile & Conversation List
with st.sidebar:
    st.title(f"Hello, {user['full_name']}! 👋")
    
    if st.button("🚪 Sign Out", use_container_width=True):
        st.session_state.user_info = None
        st.session_state.conversations = {}
        st.session_state.current_messages = []
        st.session_state.active_conversation_id = None
        st.rerun()
    
    st.divider()
    
    # New Conversation Button
    if st.button("➕ New Conversation", use_container_width=True, type="primary"):
        # Generate a new conversation ID
        new_conv_id = f"conv_{len(st.session_state.conversations) + 1}"
        st.session_state.conversations[new_conv_id] = {
            "title": f"Chat {len(st.session_state.conversations) + 1}",
            "messages": [{"role": "assistant", "content": "Hi! How can I help you find your perfect look today?"}]
        }
        st.session_state.active_conversation_id = new_conv_id
        st.session_state.current_messages = st.session_state.conversations[new_conv_id]["messages"]
        st.rerun()
    
    st.subheader("Your Conversations")
    
    # Load past conversations from backend on first load
    if not st.session_state.conversations:
        try:
            # Fetch user's conversation history
            res = requests.get(f"{API_URL}/admin/conversations")
            if res.status_code == 200:
                all_convs = res.json()
                # Filter for this user (by email in customer field)
                user_convs = [c for c in all_convs if user['email'] in c.get('customer', '')]
                
                for idx, conv in enumerate(user_convs):
                    conv_id = f"conv_{conv['id']}"
                    # Fetch full conversation details
                    detail_res = requests.get(f"{API_URL}/admin/conversations/{conv['id']}")
                    if detail_res.status_code == 200:
                        conv_data = detail_res.json()
                        messages = []
                        for msg in conv_data['messages']:
                            role = "user" if msg['sender'] == 'user' else "assistant"
                            messages.append({"role": role, "content": msg['content']})
                        
                        st.session_state.conversations[conv_id] = {
                            "title": conv.get('summary', f"Chat {idx+1}")[:30] + "...",
                            "messages": messages
                        }
        except Exception as e:
            st.error(f"Could not load past conversations: {e}")
    
    # Display conversation list
    if st.session_state.conversations:
        for conv_id, conv_data in st.session_state.conversations.items():
            if st.button(f"💬 {conv_data['title']}", key=conv_id, use_container_width=True):
                st.session_state.active_conversation_id = conv_id
                st.session_state.current_messages = conv_data["messages"]
                st.rerun()
    else:
        st.info("No conversations yet. Start a new one!")

# -----------------------------------------------------------------------------
# Main Chat Area
# -----------------------------------------------------------------------------
st.title("🛍️ ShopBuddy")

if not st.session_state.active_conversation_id:
    st.info("👈 Click 'New Conversation' to start chatting!")
    st.stop()

# Styling
st.markdown("""
<style>
    .chat-message { padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex }
    .chat-message.user { background-color: #2b313e }
    .chat-message.bot { background-color: #475063 }
    
    /* Make images look great */
    .chat-message img {
        max-width: 100%;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-top: 10px;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
</style>
""", unsafe_allow_html=True)

# Display current conversation
for msg in st.session_state.current_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("Ask about clothes, orders, etc..."):
    # Add user message
    st.session_state.current_messages.append({"role": "user", "content": prompt})
    st.session_state.conversations[st.session_state.active_conversation_id]["messages"] = st.session_state.current_messages
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call backend
    with st.spinner("Thinking..."):
        try:
            payload = {
                "message": prompt,
                "user_id": user["user_id"],
                "user_name": user["full_name"],
                "email": user["email"]
            }
            response = requests.post(CHAT_ENDPOINT, json=payload)
            if response.status_code == 200:
                bot_reply = response.json().get("response", "Error.")
            else:
                bot_reply = f"Error: {response.status_code}"
        except Exception as e:
            bot_reply = f"Connection Error: {e}"

    # Add bot reply
    st.session_state.current_messages.append({"role": "assistant", "content": bot_reply})
    st.session_state.conversations[st.session_state.active_conversation_id]["messages"] = st.session_state.current_messages
    
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
    
    st.rerun()
