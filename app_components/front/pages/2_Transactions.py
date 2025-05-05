import streamlit as st

st.set_page_config(page_title="Transaction Analysis", layout="wide")
st.title("Transaction Analysis")

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
