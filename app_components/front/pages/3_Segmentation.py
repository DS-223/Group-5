import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os

st.set_page_config(page_title="Customer Segmentation", layout="wide")
st.title("Customer Segmentation")

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

theme_teal = "#008080"
theme_light_text = "#ffffff"
theme_dark_text = "#f0f0f0"
bar_color = "#62a6a8"

text_color = theme_dark_text if mode == "Dark Mode" else theme_light_text
label_color = theme_teal if mode == "Light Mode" else theme_dark_text

load_dotenv()
API_URL = os.getenv("API_SEGMENTATION_ENDPOINT")

@st.cache_data(show_spinner=True)
def fetch_segment_distribution():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(list(data.items()), columns=["Segment", "Count"])
            df = df.sort_values("Count", ascending=False)
            return df
        else:
            st.error(f"API returned status code: {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching segment data: {e}")
        return pd.DataFrame()

df = fetch_segment_distribution()

if not df.empty:
    fig = px.bar(
        df,
        x="Segment",
        y="Count",
        title="Customer Segment Distribution",
        text_auto=True,
        labels={"Count": "Number of Customers", "Segment": "Segment"}
    )

    fig.update_layout(
        title=dict(
            text="Customer Segment Distribution",
            font=dict(size=24, color=label_color)
        ),
        font=dict(family="Segoe UI", size=14),
        xaxis=dict(
            title=dict(text="Segment", font=dict(size=16, color=label_color)),
            tickfont=dict(color=label_color)
        ),
        yaxis=dict(
            title=dict(text="Customer Count", font=dict(size=16, color=label_color)),
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
    st.info("Segment distribution data not available.")

