import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load env variables (mainly for API URL)
load_dotenv()

API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/api/v1")

st.set_page_config(page_title="Agentic CRM Admin", layout="wide")

st.title("Admin Dashboard - Agentic AI CRM")

sidebar = st.sidebar
page = sidebar.radio("Navigation", ["Dashboard", "Orders", "Products", "Customers", "Conversations"])

if page == "Dashboard":
    st.header("Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", "$12,450", "+15%")
    col2.metric("Active Conversations", "24", "3 active")
    col3.metric("Pending Orders", "5", "-2")
    
    st.subheader("Recent Activity")
    st.info("System is running. AI Agents are active.")

elif page == "Orders":
    st.header("Order Management")
    # In a real app, fetch from API
    st.write("Fetching orders from database...")
    # Placeholder data
    data = {
        "Order ID": [1001, 1002, 1003],
        "Customer": ["Alice", "Bob", "Charlie"],
        "Status": ["Shipped", "Pending", "Delivered"],
        "Total": [150.00, 89.99, 210.50]
    }
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

elif page == "Products":
    st.header("Product Catalog")
    st.button("Add New Product")
    st.write("Catalog synced with Vector Database.")
    
    # Placeholder
    products = {
        "ID": [1, 2, 3],
        "Name": ["Summer Dress", "Slim Fit Jeans", "Leather Jacket"],
        "Stock": [15, 30, 8],
        "Price": [45.00, 55.00, 120.00]
    }
    st.dataframe(pd.DataFrame(products), use_container_width=True)

elif page == "Customers":
    st.header("Customer Database")
    st.write("View customer profiles and history.")

elif page == "Conversations":
    st.header("AI Conversation Logs")
    st.write("Review agent interactions.")
    
    st.text_area("Chat Log #1024", "User: Do you have this in red?\nAgent: Yes! Here is the red version...", height=200)

