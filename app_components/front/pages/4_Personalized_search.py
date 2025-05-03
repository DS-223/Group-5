import streamlit as st
import pandas as pd
import sqlalchemy as sql
from sqlalchemy import text
from dotenv import load_dotenv
import os

# --- Page Config ---
st.set_page_config(page_title="Personalized Search", layout="wide")

if 'mode' not in st.session_state:
    st.session_state['mode'] = 'Light Mode'
mode = st.session_state['mode']

st.title("Personalized Customer Search")

# --- Load DB URL ---
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))  # up one level to front/.env
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env")
engine = sql.create_engine(DATABASE_URL, echo=False)

# --- DB Query Function ---
def get_customer_by_id(customer_id: int): 
    query = text('SELECT * FROM "DimCustomer" WHERE "CustomerKey" = :cust_id')
    with engine.connect() as conn:
        result = conn.execute(query, {"cust_id": customer_id}).fetchone()
        if result:
            return pd.DataFrame([dict(result._mapping)])
        return pd.DataFrame()


# --- Input Field ---
cust_id_input = st.text_input("Enter Customer ID (e.g., 1)")

if cust_id_input:
    try:
        cust_id = int(cust_id_input)
        result = get_customer_by_id(cust_id)
        if not result.empty:
            st.success("Customer found:")
            st.dataframe(result)
        else:
            st.warning("Customer not found.")
    except ValueError:
        st.error("Please enter a valid numeric Customer ID.")

# --- Mode Styling ---
if mode == "Light Mode":
    st.markdown("""<style>body { background-color: #e0f7f9; color: #006d77; }</style>""", unsafe_allow_html=True)
else:
    st.markdown("""<style>body { background-color: #001c1c; color: #f0f0f0; }</style>""", unsafe_allow_html=True)
