import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os

st.set_page_config(page_title="Transaction Analysis", layout="wide")
st.title("Transaction Analysis")

load_dotenv()
API_ENDPOINT = os.getenv("API_TRANSACTIONS_BYSTORE_ENDPOINT")

if 'mode' not in st.session_state:
    st.session_state['mode'] = 'Light Mode'

mode = st.session_state['mode']

if mode == "Light Mode":
    st.markdown("""
        <style>
        .stApp {background-color: #e0f7f9; font-family: 'Segoe UI', sans-serif; color: #006d77;}
        .block-container {padding-top: 1rem; background-color: white; border-radius: 12px; box-shadow: 0px 8px 30px rgba(0, 0, 0, 0.05);}
        section[data-testid="stSidebar"] {background: linear-gradient(to bottom, #a0e9eb, #e0f7f9);}
        section[data-testid="stSidebar"] * {color: #006d77 !important;}
        h1, h2, h3 {font-weight: 700; color: #008080;}
        footer {visibility: hidden;}
        header[data-testid="stHeader"] {background: none;}
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

st.subheader("Total Transaction Amount by Store")

if API_ENDPOINT:
    try:
        response = requests.get(API_ENDPOINT)
        response.raise_for_status()
        data = response.json()

        df = pd.DataFrame(data)

        if df.empty:
            st.warning("No transaction data found.")
        else:
            df = df.sort_values("total_amount", ascending=False)

            fig = px.bar(
                df,
                x="store",
                y="total_amount",
                title="Transaction Amounts by Store",
                labels={"store": "Store", "total_amount": "Total Amount"},
                color="total_amount",
                color_continuous_scale="Tealgrn"
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)

    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch data: {e}")
else:
    st.error("API endpoint not set in .env file. Please set `API_TRANSACTIONS_BYSTORE_ENDPOINT`.")


st.subheader("Monthly Transaction Trend by Store")

API_MONTHLY_ENDPOINT = os.getenv("API_TRANSACTIONS_MONTH_ENDPOINT")

if API_MONTHLY_ENDPOINT:
    try:
        response = requests.get(API_MONTHLY_ENDPOINT)
        response.raise_for_status()
        monthly_data = response.json()

        # Convert to DataFrame
        monthly_df = pd.DataFrame(monthly_data)

        if monthly_df.empty:
            st.warning("No monthly transaction data found.")
        else:
            # Ensure correct types
            monthly_df["month"] = pd.to_datetime(monthly_df["month"], format="%b %Y")
            monthly_df.sort_values("month", inplace=True)

            # Line chart with one line per store
            fig = px.line(
                monthly_df,
                x="month",
                y="total_amount",
                color="store",
                title="Monthly Transaction Trends by Store",
                labels={"month": "Month", "total_amount": "Total Amount", "store": "Store"},
            )
            fig.update_layout(xaxis=dict(tickformat="%b\n%Y"), legend_title="Store")
            st.plotly_chart(fig, use_container_width=True)

    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch monthly data: {e}")
else:
    st.error("Monthly API endpoint not set in .env file.")
