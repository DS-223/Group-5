import streamlit as st
import pandas as pd
import requests
from dotenv import load_dotenv
import os

# Set the page title and layout
st.set_page_config(page_title="Personalized Search", layout="wide")

st.title("Personalized Customer Search")

# Load environment variables from the .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
API_CUSTOMER_ENDPOINT = os.getenv("API_CUSTOMER_ENDPOINT")

# Check if the API endpoint is provided in the .env file
if not API_CUSTOMER_ENDPOINT:
    raise ValueError("API_CUSTOMER_ENDPOINT is not set in .env")

# Function to fetch customer data by ID using the API
def get_customer_by_id_api(customer_id: int) -> pd.DataFrame:
    """
    Fetch customer data by ID using a GET request to the provided API endpoint.

    Parameters:
        customer_id (int): The ID of the customer to retrieve.

    Returns:
        pd.DataFrame: A dataframe containing customer data if found, or empty if not found or on error.
    """
    try:
        url = f"{API_CUSTOMER_ENDPOINT}/{customer_id}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "detail" in data:
                return pd.DataFrame()
            return pd.DataFrame([data])
        return pd.DataFrame()
    except Exception as e:
        st.error(f"API error: {e}")
        return pd.DataFrame()

# Create an input field for customer ID
cust_id_input = st.text_input("Enter Customer ID (e.g., 1)")

# Fetch and display customer data based on the input
if cust_id_input:
    try:
        cust_id = int(cust_id_input)
        result = get_customer_by_id_api(cust_id)
        if not result.empty:
            st.success("Customer found:")
            st.dataframe(result)
        else:
            st.warning("Customer not found.")
    except ValueError:
        st.error("Please enter a valid numeric Customer ID.")

# Apply custom styles to the page using markdown
st.markdown("""
    <style>
    .stApp {
        background-color: #001c1c;
        font-family: 'Segoe UI', sans-serif;
        color: #f0f0f0;
    }
    .block-container {
        padding-top: 1rem;
        background-color: #002424;
        border-radius: 12px;
        box-shadow: 0px 8px 30px rgba(255, 255, 255, 0.05);
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #002929, #001c1c);
    }
    section[data-testid="stSidebar"] * {
        color: #f0f0f0 !important;
    }
    h1, h2, h3 {
        font-weight: 700;
        color: #f0f0f0;
    }
    footer {
        visibility: hidden;
    }
    header[data-testid="stHeader"] {
        background: none;
    }
    label {
        color: #f0f0f0 !important;
        font-weight: 600;
    }
    input {
        color: #f0f0f0 !important;
        background-color: #003333 !important;
        border: 1px solid #004d4d !important;
        border-radius: 5px;
    }
    .stTextInput>div>div>input:focus {
        border-color: #00cccc !important;
        box-shadow: 0 0 0 0.1rem #00cccc33 !important;
    }
    .stAlert-success p {
        color: #00e6e6 !important;
        font-weight: 600;
        font-size: 1rem;
    }
    .stAlert-warning p {
        color: #ffd700 !important;
        font-weight: 600;
        font-size: 1rem;
    }
    .stAlert-error p {
        color: #ff4d4d !important;
        font-weight: 600;
        font-size: 1rem;
    }
    </style>
""", unsafe_allow_html=True)
