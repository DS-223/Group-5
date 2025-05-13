import streamlit as st

st.set_page_config(page_title="Dashboard", layout="wide")

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
    input[type="text"] {
        border: 2px solid #00f0ff;
        border-radius: 8px;
        padding: 10px;
        background-color: #002222;
        color: #f0f0f0;
    }
    input[type="text"]:focus {
        border: 2px solid #00f0ff;
        background-color: #001c1c;
    }
    label, .css-1cpxqw2, .css-1cpxqw2 span {
        color: #b2ffff !important;
        font-weight: 500;
    }
    .stAlert {
        background-color: #003838 !important;
        color: #d9fef7 !important;
        border: 2px solid #00f0ff;
        border-radius: 12px;
        font-weight: 600;
    }
    .stAlert:hover {
        box-shadow: 0px 0px 15px #00f0ff;
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
    div[data-testid="collapsedControl"] svg {
        stroke: #f0f0f0 !important;
        color: #f0f0f0 !important;
        transition: 0.3s ease;
    }
    div[data-testid="collapsedControl"]:hover svg {
        stroke: #00f0ff !important;
        color: #00f0ff !important;
        filter: drop-shadow(0 0 7px #00f0ff) drop-shadow(0 0 12px #00f0ff);
        transform: scale(1.2);
        transition: 0.3s ease;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Loyalitics")
st.markdown("Use the sidebar to navigate to different pages")