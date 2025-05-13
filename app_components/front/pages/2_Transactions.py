import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os

# ---------------------- Page Config ----------------------
st.set_page_config(page_title="Transaction Analysis", layout="wide")
st.title("Transaction Analysis")

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
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {background: none;}
    </style>
""", unsafe_allow_html=True)

load_dotenv()
API_ENDPOINT = os.getenv("API_TRANSACTIONS_BYSTORE_ENDPOINT")
API_MONTHLY_ENDPOINT = os.getenv("API_TRANSACTIONS_MONTH_ENDPOINT")

theme_teal = "#00b3b3"
text_color = "#f0f0f0"

# --------------------------------------------
# Section 1: Total Transaction Amount by Store
# --------------------------------------------

st.subheader("Total Transaction Amount by Store")

if API_ENDPOINT:
    try:
        # Fetch data from the specified API endpoint
        response = requests.get(API_ENDPOINT)
        response.raise_for_status()
        data = response.json()

        # Parse data into a DataFrame
        df = pd.DataFrame(data)

        # Check if the DataFrame is empty and display warning if so
        if df.empty:
            st.warning("No transaction data found.")
        else:
            # Sort data by total_amount in descending order
            df = df.sort_values("total_amount", ascending=False)

            # Create a bar chart using Plotly
            fig = px.bar(
                df,
                x="store",
                y="total_amount",
                title="Transaction Amounts by Store",
                labels={"store": "Store", "total_amount": "Total Amount"},
                color="total_amount",
                color_continuous_scale=[[0, theme_teal], [1, "#007777"]]
            )

            # Customize chart layout
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color=text_color),
                xaxis_tickangle=-45,
                xaxis=dict(title_font=dict(color=text_color), tickfont=dict(color=text_color)),
                yaxis=dict(title_font=dict(color=text_color), tickfont=dict(color=text_color)),
                title_font=dict(color=text_color)
            )

            # Display the chart
            st.plotly_chart(fig, use_container_width=True)

    except requests.exceptions.RequestException as e:
        # Handle any errors during API request
        st.error(f"Failed to fetch data: {e}")
else:
    # Error if the API endpoint is not set
    st.error("API endpoint not set in .env file. Please set `API_TRANSACTIONS_BYSTORE_ENDPOINT`.")

# ------------------------------------------------
# Section 2: Monthly Transaction Trend by Store
# ------------------------------------------------

st.subheader("Monthly Transaction Trend by Store")

if API_MONTHLY_ENDPOINT:
    try:
        # Fetch monthly transaction data from the specified API endpoint
        response = requests.get(API_MONTHLY_ENDPOINT)
        response.raise_for_status()
        monthly_data = response.json()

        # Parse the monthly data into a DataFrame
        monthly_df = pd.DataFrame(monthly_data)

        # Check if the DataFrame is empty and display warning if so
        if monthly_df.empty:
            st.warning("No monthly transaction data found.")
        else:
            # Convert 'month' column to datetime and sort the DataFrame by month
            monthly_df["month"] = pd.to_datetime(monthly_df["month"], format="%b %Y")
            monthly_df.sort_values("month", inplace=True)

            # Create a line chart using Plotly
            fig = px.line(
                monthly_df,
                x="month",
                y="total_amount",
                color="store",
                title="Monthly Transaction Trends by Store",
                labels={"month": "Month", "total_amount": "Total Amount", "store": "Store"},
            )

            # Customize chart layout
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color=text_color),
                xaxis=dict(
                    tickformat="%b\n%Y",
                    title_font=dict(color=text_color),
                    tickfont=dict(color=text_color)
                ),
                yaxis=dict(
                    title_font=dict(color=text_color),
                    tickfont=dict(color=text_color)
                ),
                title_font=dict(color=text_color),
                legend_title_font=dict(color=text_color),
                legend_font=dict(color=text_color)
            )

            # Display the chart
            st.plotly_chart(fig, use_container_width=True)

    except requests.exceptions.RequestException as e:
        # Handle any errors during API request
        st.error(f"Failed to fetch monthly data: {e}")
else:
    # Error if the API monthly endpoint is not set
    st.error("Monthly API endpoint not set in .env file.")
