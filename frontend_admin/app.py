import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Config
load_dotenv()
API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/api/v1")

st.set_page_config(page_title="Admin Dashboard", layout="wide", page_icon="🔒")

# -----------------------------------------------------------------------------
# Auth Logic: Simple Password Protection
# -----------------------------------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login():
    st.title("🔒 Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # Hardcoded for hackathon speed - move to .env in real app
        if username == "admin" and password == "admin":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid credentials")

if not st.session_state.authenticated:
    login()
    st.stop()

# -----------------------------------------------------------------------------
# Admin Dashboard (Only reachable if authenticated)
# -----------------------------------------------------------------------------

st.sidebar.title(f"Welcome, Admin")
if st.sidebar.button("Logout"):
    st.session_state.authenticated = False
    st.rerun()

st.title("Admin Dashboard - Agentic AI CRM")

tab1, tab2, tab3 = st.tabs(["Conversations", "Orders", "System Health"])

with tab1: # Conversations
    st.header("AI Conversation Logs")
    st.write("Review active customer interactions and AI-generated summaries.")
    if st.button("Refresh Logs"):
        st.rerun()
        
    try:
        res = requests.get(f"{API_URL}/admin/conversations")
        if res.status_code == 200:
            conversations = res.json()
            if conversations:
                df = pd.DataFrame(conversations)
                df = df[["id", "customer", "summary", "last_active", "platform"]]
                st.dataframe(df, use_container_width=True)
                
                st.subheader("Deep Dive")
                col_id, col_btn = st.columns([1, 3])
                selected_id = col_id.number_input("Enter Conversation ID:", min_value=1, step=1)
                if col_btn.button("Load Chat History"):
                    chat_res = requests.get(f"{API_URL}/admin/conversations/{selected_id}")
                    if chat_res.status_code == 200:
                        chat_data = chat_res.json()
                        st.markdown(f"**Chat Summary:** {chat_data['summary']}")
                        st.divider()
                        for msg in chat_data["messages"]:
                            role_icon = "👤" if msg['sender'] == 'user' else "🤖"
                            st.text(f"{role_icon} {msg['sender'].upper()}: {msg['content']}")
                    else:
                        st.error("Conversation not found.")
            else:
                st.info("No conversations yet.")
        else:
            st.error(f"Failed to fetch data: {res.status_code}")
    except Exception as e:
        st.error(f"Connection error: {e}")

with tab2: # Orders
    st.header("Order Management")
    # Placeholder data
    data = {"Order ID": [101, 102], "Customer": ["Dave", "Eve"], "Status": ["Pending", "Shipped"], "Total": [120, 85]}
    st.dataframe(pd.DataFrame(data), use_container_width=True)

with tab3: # Health
    try:
        health_url = API_URL.replace("/api/v1", "/health")
        res = requests.get(health_url, timeout=2)
        if res.status_code == 200:
            st.success(f"Backend is ONLINE. DB Connected.")
        else:
            st.warning(f"Backend returned {res.status_code}")
    except Exception as e:
        st.error(f"Backend Offline: {e}")
