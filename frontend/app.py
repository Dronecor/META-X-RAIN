import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# 1. Config & Setup (Must be first)
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Agentic CRM Platform", layout="wide", page_icon="🛍️")

# Load environment from ROOT directory (parent of frontend/)
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
dotenv_path = os.path.join(root_dir, ".env")
load_dotenv(dotenv_path)

API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/api/v1")
CHAT_ENDPOINT = f"{API_URL}/chat/message"

# -----------------------------------------------------------------------------
# 2. Main Navigation
# -----------------------------------------------------------------------------
st.sidebar.title("Navigation")
role = st.sidebar.radio("Select Persona", ["Customer Portal", "Business Admin"])

# -----------------------------------------------------------------------------
# 3. Customer Portal Logic (Chat)
# -----------------------------------------------------------------------------
if role == "Customer Portal":
    st.title("🛍️ ShopBuddy")
    st.caption("Your personalized AI fashion assistant. Ask about clothes, track orders, or upload images!")
    
    # Custom CSS for chat
    st.markdown("""
    <style>
        .chat-message { padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex }
        .chat-message.user { background-color: #2b313e }
        .chat-message.bot { background-color: #475063 }
    </style>
    """, unsafe_allow_html=True)

    # Session State for History
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({"role": "assistant", "content": "Hi! I'm ShopBuddy. How can I help you find your perfect look today?"})

    # Display History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Image Upload (Sidebar inside Customer View)
    with st.sidebar:
        st.divider()
        st.header("📸 Visual Search")
        uploaded_file = st.file_uploader("Upload an image to find tailored matches", type=["jpg", "png", "jpeg"])
        
        if uploaded_file:
            st.image(uploaded_file, caption="Your Upload", use_container_width=True)
            if st.button("Search with Image"):
                with st.spinner("Analyzing style..."):
                    # Mock URL for hackathon
                    mock_url = "http://example.com/uploaded_image.jpg" 
                    
                    try:
                        payload = {"message": "Find products like this image.", "image_url": mock_url}
                        response = requests.post(CHAT_ENDPOINT, json=payload)
                        if response.status_code == 200:
                             bot_reply = response.json().get("response")
                             st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                             st.rerun() 
                    except Exception as e:
                        st.error(f"Error: {e}")

    # Chat Input
    if prompt := st.chat_input("What are you looking for?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Thinking..."):
            try:
                payload = {"message": prompt}
                response = requests.post(CHAT_ENDPOINT, json=payload)
                if response.status_code == 200:
                    bot_reply = response.json().get("response", "Sorry, I didn't get that.")
                else:
                    bot_reply = f"Error: {response.status_code} - {response.text}"
            except Exception as e:
                bot_reply = f"Connection Error: {e}"

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        with st.chat_message("assistant"):
            st.markdown(bot_reply)

# -----------------------------------------------------------------------------
# 4. Admin Dashboard Logic
# -----------------------------------------------------------------------------
elif role == "Business Admin":
    st.title("Admin Dashboard - Agentic AI CRM")
    
    # Inner Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Dashboard", "Orders", "Products", "Customers", "Conversations"])
    
    with tab1: # Dashboard
        st.header("Overview")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Sales", "$12,450", "+15%")
        col2.metric("Active Conversations", "24", "3 active")
        col3.metric("Pending Orders", "5", "-2")
        
        st.subheader("System Health")
        try:
            health_url = API_URL.replace("/api/v1", "/health")
            res = requests.get(health_url, timeout=2)
            if res.status_code == 200:
                st.success(f"System is ONLINE. Connected to {health_url}")
            else:
                st.warning(f"System Unreachable. Status: {res.status_code}")
        except Exception as e:
            st.error(f"System OFFLINE: {e}")

    with tab2: # Orders
        st.header("Order Management")
        st.write("Fetching orders from database...")
        # Placeholder data
        data = {
            "Order ID": [1001, 1002, 1003],
            "Customer": ["Alice", "Bob", "Charlie"],
            "Status": ["Shipped", "Pending", "Delivered"],
            "Total": [150.00, 89.99, 210.50]
        }
        st.dataframe(pd.DataFrame(data), use_container_width=True)

    with tab3: # Products
        st.header("Product Catalog")
        st.write("Catalog synced with Vector Database.")
        products = {
            "ID": [1, 2, 3],
            "Name": ["Summer Dress", "Slim Fit Jeans", "Leather Jacket"],
            "Stock": [15, 30, 8],
            "Price": [45.00, 55.00, 120.00]
        }
        st.dataframe(pd.DataFrame(products), use_container_width=True)
        
    with tab4: # Customers
        st.header("Customer Database")
        st.write("View customer profiles and history.")

    with tab5: # Conversations
        st.header("AI Conversation Logs")
        st.write("Review active customer interactions and AI-generated summaries.")
        try:
            res = requests.get(f"{API_URL}/admin/conversations")
            if res.status_code == 200:
                conversations = res.json()
                if conversations:
                    df = pd.DataFrame(conversations)
                    df = df[["id", "customer", "summary", "last_active", "platform"]]
                    st.dataframe(df, use_container_width=True)
                    
                    st.subheader("Deep Dive")
                    selected_id = st.number_input("Enter Conversation ID:", min_value=1, step=1)
                    if st.button("Load Chat History"):
                        chat_res = requests.get(f"{API_URL}/admin/conversations/{selected_id}")
                        if chat_res.status_code == 200:
                            chat_data = chat_res.json()
                            st.markdown(f"**Summary:** {chat_data['summary']}")
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
