import streamlit as st

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("Welcome to the Dashboard")
st.markdown("Use the sidebar to navigate to different pages")

import streamlit as st

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