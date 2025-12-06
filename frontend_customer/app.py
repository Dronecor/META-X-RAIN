import streamlit as st
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

# Config
API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/api/v1")
CHAT_ENDPOINT = f"{API_URL}/chat/message"

st.set_page_config(page_title="ShopBuddy - Your AI Fashion Stylist", page_icon="🛍️")

# Styling
st.markdown("""
<style>
    .chat-message {
        padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
    }
    .chat-message.user {
        background-color: #2b313e
    }
    .chat-message.bot {
        background-color: #475063
    }
    .stTextInput input {
        color: black !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛍️ ShopBuddy")
st.caption("Your personalized AI fashion assistant. Ask about clothes, track orders, or upload images!")

# Session State for History
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Initial Greeting
    st.session_state.messages.append({"role": "assistant", "content": "Hi! I'm ShopBuddy. How can I help you find your perfect look today?"})

# Display History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("What are you looking for?"):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call Backend
    with st.spinner("Thinking..."):
        try:
            payload = {"message": prompt}
            # Simulate image handling if needed (future feature)
            
            response = requests.post(CHAT_ENDPOINT, json=payload)
            if response.status_code == 200:
                bot_reply = response.json().get("response", "Sorry, I didn't get that.")
            else:
                bot_reply = f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            bot_reply = f"Connection Error: {e}"

    # Add bot reply to state
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

# Image Upload (Sidebar or separate section)
with st.sidebar:
    st.header("📸 Visual Search")
    uploaded_file = st.file_uploader("Upload an image to find tailored matches", type=["jpg", "png", "jpeg"])
    
    if uploaded_file:
        st.image(uploaded_file, caption="Your Upload", use_container_width=True)
        if st.button("Search with Image"):
            with st.spinner("Analyzing style..."):
                # In a real app, upload image to S3/Cloudinary first, get URL, then send to backend
                # For this Hackathon demo, we might mock the URL if we don't have S3 set up.
                mock_url = "http://example.com/uploaded_image.jpg" 
                
                try:
                    payload = {"message": "Find products like this image.", "image_url": mock_url}
                    response = requests.post(CHAT_ENDPOINT, json=payload)
                    if response.status_code == 200:
                         bot_reply = response.json().get("response")
                         st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                         st.rerun() # Refresh to show in chat
                except Exception as e:
                    st.error(f"Error: {e}")
