import streamlit as st
import pandas as pd
import requests
from dotenv import load_dotenv
import os

st.set_page_config(page_title="Transaction Search", layout="wide")
st.title("Transaction Search")

if 'mode' not in st.session_state:
    st.session_state['mode'] = 'Light Mode'
mode = st.session_state['mode']

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
API_TRANSACTIONS_ENDPOINT = os.getenv("API_TRANSACTIONS_ENDPOINT")

if not API_TRANSACTIONS_ENDPOINT:
    raise ValueError("API_TRANSACTIONS_ENDPOINT is not set in .env")

theme_teal = "#008080"
theme_light_text = "#ffffff"
theme_dark_text = "#f0f0f0"

text_color = theme_dark_text if mode == "Dark Mode" else theme_light_text

def get_transactions_by_customer_id(customer_id: int):
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

if mode == "Light Mode":
    st.markdown("""
        <style>
        .stApp {
            background-color: #e0f7f9;
            font-family: 'Segoe UI', sans-serif;
            color: #006d77;
        }
        .block-container {
            padding-top: 1rem;
            background-color: white;
            border-radius: 12px;
            box-shadow: 0px 8px 30px rgba(0, 0, 0, 0.05);
        }
        section[data-testid="stSidebar"] {
            background: linear-gradient(to bottom, #a0e9eb, #e0f7f9);
        }
        section[data-testid="stSidebar"] * {
            color: #006d77 !important;
        }
        h1, h2, h3 {
            font-weight: 700;
            color: #008080;
        }
        footer {
            visibility: hidden;
        }
        header[data-testid="stHeader"] {
            background: none;
        }

        /* Input label text */
        label {
            color: #006d77 !important;
        }

        /* Input text color */
        input {
            color: #ffffff !important;
        }

        /* Success box text (including number) */
        .stAlert-success * {
            color: #008080 !important;
            font-weight: 600;
            font-size: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
else:
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
        </style>
    """, unsafe_allow_html=True)
