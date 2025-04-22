import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Revenue Insights", layout="wide")
st.title("Revenue Insights")

df = pd.DataFrame({
    "Month": pd.date_range("2024-01-01", periods=12, freq="M"),
    "Revenue": np.random.randint(5000, 20000, 12)
})

fig = px.bar(df, x="Month", y="Revenue", title="Monthly Revenue Overview")
st.plotly_chart(fig, use_container_width=True)

# style
st.markdown("""
    <style>
    /* Whole app background */
    .stApp {
        background-image: linear-gradient(to right, #e0eafc, #cfdef3);
        background-attachment: fixed;
        background-size: cover;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Glass effect on widgets */
    .block-container {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem 2rem;
        border-radius: 15px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.1);
        backdrop-filter: blur(6px);
        -webkit-backdrop-filter: blur(6px);
    }

    /* Sidebar design */
    section[data-testid="stSidebar"] {
        background: linear-gradient(to bottom, #e4eaf0, #ffffff);
        color: #000000;
    }

    /* Sidebar text */
    .css-1d391kg {
        font-size: 1rem;
    }

    /* Make headers prettier */
    h1, h2, h3 {
        font-weight: 600;
        color: #222831;
    }

    /* Hide the Streamlit branding footer */
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)