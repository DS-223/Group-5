import streamlit as st
import pandas as pd
import requests
from dotenv import load_dotenv
import os

st.set_page_config(page_title="Personalized Search", layout="wide")

if 'mode' not in st.session_state:
    st.session_state['mode'] = 'Light Mode'
mode = st.session_state['mode']

st.title("Personalized Customer Search")

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
API_CUSTOMER_ENDPOINT = os.getenv("API_CUSTOMER_ENDPOINT")
if not API_CUSTOMER_ENDPOINT:
    raise ValueError("API_CUSTOMER_ENDPOINT is not set in .env")

def get_customer_by_id_api(customer_id: int):
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

cust_id_input = st.text_input("Enter Customer ID (e.g., 1)")

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

        /* Input field text */
        input {
            color: #ffffff !important;
        }

        /* Success box text fix */
        .stAlert-success p {
            color: #008080 !important;
            font-weight: 600;
            font-size: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        .stApp {background-color: #001c1c; font-family: 'Segoe UI', sans-serif; color: #f0f0f0;}
        .block-container {padding-top: 1rem; background-color: #002424; border-radius: 12px; box-shadow: 0px 8px 30px rgba(255, 255, 255, 0.05);}
        section[data-testid="stSidebar"] {background: linear-gradient(to bottom, #002929, #001c1c);}
        section[data-testid="stSidebar"] * {color: #f0f0f0 !important;}
        h1, h2, h3 {font-weight: 700; color: #f0f0f0;}
        footer {visibility: hidden;}
        header[data-testid="stHeader"] {background: none;}
        </style>
    """, unsafe_allow_html=True)
