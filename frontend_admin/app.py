import streamlit as st
import requests
import pandas as pd
import os

# Configuration
BACKEND_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000/api/v1")
st.set_page_config(page_title="ShopBuddy Admin", page_icon="🛍️", layout="wide")

# Styling
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
    }
    .status-badge {
        padding: 5px 10px;
        border-radius: 15px;
        color: white;
        font-weight: bold;
        text-align: center;
        display: inline-block;
    }
    .paid { background-color: #28a745; }
    .pending { background-color: #ffc107; color: black; }
    .shipped { background-color: #17a2b8; }
    .cancelled { background-color: #dc3545; }
</style>
""", unsafe_allow_html=True)

# Helper Functions
def fetch_conversations():
    try:
        resp = requests.get(f"{BACKEND_URL}/admin/conversations")
        if resp.status_code == 200:
            return resp.json()
        return []
    except Exception as e:
        st.error(f"Error fetching conversations: {e}")
        return []

def fetch_orders():
    try:
        resp = requests.get(f"{BACKEND_URL}/admin/orders")
        if resp.status_code == 200:
            return resp.json()
        return []
    except Exception as e:
        st.error(f"Error fetching orders: {e}")
        return []

def update_order_status(order_id, status):
    try:
        resp = requests.post(f"{BACKEND_URL}/admin/orders/{order_id}/verify?status={status}")
        if resp.status_code == 200:
            st.success(f"Order #{order_id} updated to {status}")
            st.rerun()
        else:
            st.error("Failed to update status")
    except Exception as e:
        st.error(f"Error updating order: {e}")

def create_product(product_data):
    try:
        resp = requests.post(f"{BACKEND_URL}/products/", json=product_data)
        if resp.status_code == 200:
            st.success("Product created successfully!")
            return resp.json()
        else:
            st.error(f"Failed to create product: {resp.text}")
            return None
    except Exception as e:
        st.error(f"Error creating product: {e}")
        return None

def fetch_products():
    try:
        resp = requests.get(f"{BACKEND_URL}/products/")
        if resp.status_code == 200:
            return resp.json()
        return []
    except Exception as e:
        st.error(f"Error fetching products: {e}")
        return []

def upload_image(file):
    try:
        files = {"file": file}
        resp = requests.post(f"{BACKEND_URL}/utils/upload", files=files)
        if resp.status_code == 200:
            data = resp.json()
            # If path returned is relative, prepend URL (hack for display, but backend stores relative)
            # The backend stores relative path. We return what the backend returns.
            return data.get("url")
        else:
            st.error("Image upload failed")
            return None
    except Exception as e:
        st.error(f"Error uploading image: {e}")
        return None

# Authentication
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("🔒 Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        # Simple env-based auth
        valid_user = os.getenv("ADMIN_USERNAME", "admin")
        valid_pass = os.getenv("ADMIN_PASSWORD", "admin")
        
        if username == valid_user and password == valid_pass:
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid credentials")

if not st.session_state.logged_in:
    login()
else:
    # Sidebar Logout
    st.sidebar.title("ShopBuddy Admin 🛍️")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
        
    page = st.sidebar.radio("Navigate", ["Dashboard", "Order Verification", "Product Management"])

    # --- DASHBOARD ---
    if page == "Dashboard":
        st.title("📊 Admin Dashboard")
        
        convs = fetch_conversations()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Active Conversations", len(convs))
        with col2:
            st.metric("System Status", "Online 🟢")

        st.subheader("Recent Conversations")
        if convs:
            df = pd.DataFrame(convs)
            # Simplify display
            display_df = df[['id', 'customer', 'platform', 'summary', 'last_active']]
            st.dataframe(display_df, use_container_width=True)
        else:
            st.info("No active conversations found.")

    # --- ORDER VERIFICATION ---
    elif page == "Order Verification":
        st.title("📦 Order Verification")
        
        orders = fetch_orders()
        
        if orders:
            for order in orders:
                with st.expander(f"Order #{order['id']} - {order['status'].upper()} - ₦{order['total_amount']}"):
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
                    
                    with col1:
                        st.write(f"**Customer:** User {order['customer_id']}")
                        st.write(f"**Date:** {order['created_at']}")
                        st.write(f"**Items:** {len(order.get('items', []))}")
                    
                    with col2:
                        current_status = order['status']
                        st.markdown(f'<span class="status-badge {current_status}">{current_status.upper()}</span>', unsafe_allow_html=True)
                    
                    with col4:
                        st.write("Actions:")
                        ic1, ic2, ic3 = st.columns(3)
                        if order['status'] == 'pending':
                            if ic1.button("Verify Pay", key=f"pay_{order['id']}"):
                                update_order_status(order['id'], 'paid')
                            if ic3.button("Cancel", key=f"cancel_{order['id']}"):
                                update_order_status(order['id'], 'cancelled')
                        elif order['status'] == 'paid':
                            if ic2.button("Ship", key=f"ship_{order['id']}"):
                                update_order_status(order['id'], 'shipped')
                            if ic3.button("Cancel", key=f"cancel_{order['id']}"):
                                update_order_status(order['id'], 'cancelled')
        else:
            st.info("No orders found.")

    # --- PRODUCT MANAGEMENT ---
    elif page == "Product Management":
        st.title("📦 Product Management")
        
        tab1, tab2 = st.tabs(["Add New Product", "View Products"])
        
        with tab1:
            st.header("Add New Product")
            
            # Check if we just added a product
            if "product_added" not in st.session_state:
                st.session_state.product_added = False
            
            if st.session_state.product_added:
                if st.button("🔄 Add Another Product"):
                    st.session_state.product_added = False
                    st.rerun()
                st.info("Reload to add a new product.")
            else:
                with st.form("product_form", clear_on_submit=False):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        name = st.text_input("Product Name")
                        price = st.number_input("Price (₦)", min_value=0.0, step=0.01)
                        category = st.text_input("Category", placeholder="e.g. suit, dress, shirt")
                        
                    with col2:
                        stock = st.number_input("Stock Quantity", min_value=0, step=1)
                        description = st.text_area("Description")
                        
                    uploaded_file = st.file_uploader("Product Image", type=['png', 'jpg', 'jpeg'])
                    
                    submitted = st.form_submit_button("Create Product")
                    
                    if submitted:
                        if not name or not price:
                            st.error("Name and Price are required.")
                        else:
                            image_url = ""
                            if uploaded_file:
                                with st.spinner("Uploading image..."):
                                    url = upload_image(uploaded_file)
                                    if url:
                                        image_url = url
                                        st.success("Image uploaded!")
                            
                            product_data = {
                                "name": name,
                                "description": description,
                                "price": price,
                                "category": category,
                                "stock_quantity": stock,
                                "image_url": image_url
                            }
                            
                            with st.spinner("Creating product and generating description..."):
                                result = create_product(product_data)
                            
                            if result:
                                 st.balloons()
                                 st.session_state.product_added = True
                                 
                                 st.success("Product Created!")
                                 st.subheader("Generated Details:")
                                 st.json(result)
                                 
                                 if result.get("visual_description"):
                                     st.info(f"✨ AI Visual Description: {result['visual_description']}")
                                 else:
                                     st.warning("No visual description generated (or image missing).")
                                     
                                 st.rerun()

        with tab2:
            st.header("Product Inventory")
            products = fetch_products()
            if products:
                # Convert to DataFrame for better display
                df = pd.DataFrame(products)
                
                # Reorder columns if they exist
                cols = ['id', 'name', 'category', 'price', 'stock_quantity', 'visual_description']
                existing_cols = [c for c in cols if c in df.columns]
                other_cols = [c for c in df.columns if c not in existing_cols]
                
                st.dataframe(df[existing_cols + other_cols], use_container_width=True)
            else:
                st.info("No products found in the database. Add some!")
