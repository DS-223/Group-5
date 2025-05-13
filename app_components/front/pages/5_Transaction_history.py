import streamlit as st
import pandas as pd
import requests
from dotenv import load_dotenv
import os

st.set_page_config(page_title="Transaction Search", layout="wide")
st.title("Transaction Search")

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
API_TRANSACTIONS_ENDPOINT = os.getenv("API_TRANSACTIONS_ENDPOINT")

if not API_TRANSACTIONS_ENDPOINT:
    raise ValueError("API_TRANSACTIONS_ENDPOINT is not set in .env")

def get_transactions_by_customer_id(customer_id: int):
    """
    Fetch transaction data for a specific customer by ID from the API.

    Parameters:
        customer_id (int): The ID of the customer.

    Returns:
        pd.DataFrame: A DataFrame containing the transactions, or empty if none found or on error.
    """
    try:
        url = f"{API_TRANSACTIONS_ENDPOINT}/{customer_id}/transactions"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if not data:
                return pd.DataFrame()
            return pd.DataFrame(data)
        return pd.DataFrame()
    except Exception as e:
        st.error(f"API error: {e}")
        return pd.DataFrame()

cust_id_input = st.text_input("Enter Customer ID to view their transactions")

if cust_id_input:
    try:
        cust_id = int(cust_id_input)
        result = get_transactions_by_customer_id(cust_id)
        if not result.empty:
            st.success(f"{len(result)} transactions found for Customer ID {cust_id}:")
            st.dataframe(result)
        else:
            st.warning("No transactions found for this customer.")
    except ValueError:
        st.error("Please enter a valid numeric Customer ID.")

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
