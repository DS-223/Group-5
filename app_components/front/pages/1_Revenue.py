import streamlit as st
import pandas as pd
import requests
from dotenv import load_dotenv
import os
import plotly.express as px

st.set_page_config(page_title="Revenue Insights", layout="wide")
st.title("Revenue Insights")

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
API_URL = os.getenv("API_REVENUE_ENDPOINT")

theme_teal = "#008080"
text_color = "#f0f0f0"
bar_color = "#62a6a8"
label_color = "#f0f0f0"

@st.cache_data(show_spinner=True)
def fetch_revenue_data():
    """
    Fetches revenue data from the API, parses it into a DataFrame,
    and prepares it for visualization.

    Returns:
        pd.DataFrame: A DataFrame containing 'Month', 'Revenue', and parsed datetime for sorting.
    """
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and isinstance(data[0], list):
                df = pd.DataFrame(data, columns=["Month", "Revenue"])
            elif isinstance(data[0], dict):
                df = pd.DataFrame(data)
                df.rename(columns={"month": "Month", "revenue": "Revenue"}, inplace=True)
            else:
                st.error("Unexpected API data format.")
                return pd.DataFrame()
            df["Month_dt"] = pd.to_datetime(df["Month"], format="%b %Y")
            df = df.sort_values("Month_dt")
            return df
        else:
            st.error(f"API returned status code: {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching data from API: {e}")
        return pd.DataFrame()

df = fetch_revenue_data()

if not df.empty:
    fig = px.bar(
        df,
        x="Month",
        y="Revenue",
        title="Monthly Revenue Overview",
        text_auto=".2s",
        labels={"Revenue": "Revenue", "Month": "Month"}
    )

    fig.update_layout(
        title=dict(
            text="Monthly Revenue Overview",
            font=dict(size=24, color=label_color)
        ),
        font=dict(family="Segoe UI", size=14),
        xaxis=dict(
            title=dict(text="Month", font=dict(size=16, color=label_color)),
            tickfont=dict(color=label_color)
        ),
        yaxis=dict(
            title=dict(text="Revenue", font=dict(size=16, color=label_color)),
            tickfont=dict(color=label_color)
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=60, b=60)
    )
    fig.update_traces(
        marker_color=bar_color,
        textfont_size=12,
        textfont_color=text_color
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Revenue data not available.")
