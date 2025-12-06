import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/api/v1")
CHAT_ENDPOINT = f"{API_URL}/chat/message"

st.set_page_config(page_title="ShopBuddy", page_icon="🛍️")

# -----------------------------------------------------------------------------
# Customer Identification
# -----------------------------------------------------------------------------
if "user_info" not in st.session_state:
    st.session_state.user_info = None

if not st.session_state.user_info:
    st.title("👋 Welcome to ShopBuddy!")
    st.write("Please sign in so we can personalize your experience.")
    
    with st.form("login_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number (Optional, for WhatsApp)")
        submit = st.form_submit_button("Start Shopping")
        
        if submit:
            if name and email:
                st.session_state.user_info = {
                    "full_name": name,
                    "email": email,
                    # Primary ID: Use Email or Phone
                    "user_id": email 
                }
                st.rerun()
            else:
                st.error("Please provide at least Name and Email.")
    st.stop()

# -----------------------------------------------------------------------------
# Main Chat Interface
# -----------------------------------------------------------------------------
user = st.session_state.user_info

st.title(f"🛍️ ShopBuddy")
st.caption(f"Hello, {user['full_name']}! I'm your personalized AI fashion assistant.")

if st.sidebar.button("Sign Out"):
    st.session_state.user_info = None
    st.rerun()

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

# Session History
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": "How can I help you find your perfect look today?"})

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Image Upload
with st.sidebar:
    st.header("📸 Visual Search")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Your Upload", use_container_width=True)
        if st.button("Search"):
            with st.spinner("Analyzing..."):
                mock_url = "http://example.com/uploaded.jpg"
                try:
                    payload = {
                        "message": "Find products like this image.", 
                        "image_url": mock_url,
                        "user_id": user["user_id"],
                        "user_name": user["full_name"],
                        "email": user["email"]
                    }
                    response = requests.post(CHAT_ENDPOINT, json=payload)
                    if response.status_code == 200:
                            bot_reply = response.json().get("response")
                            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                            st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

# Text Input
if prompt := st.chat_input("Ask about clothes, orders, etc..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

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
                bot_reply = f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            bot_reply = f"Connection Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
