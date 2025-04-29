import streamlit as st

st.set_page_config(page_title="Dashboard", layout="wide")

if 'mode' not in st.session_state:
    st.session_state['mode'] = 'Light Mode'

selected_mode = st.sidebar.radio("Choose Display Mode:", ("Light Mode", "Dark Mode"),
                                 index=0 if st.session_state['mode'] == 'Light Mode' else 1)
st.session_state['mode'] = selected_mode
mode = st.session_state['mode']

if mode == "Light Mode":
    st.markdown("""
        <style>
        .stApp {background-color: #e0f7f9; font-family: 'Segoe UI', sans-serif; color: #006d77;}
        .block-container {padding-top: 1rem; background-color: white; border-radius: 12px; box-shadow: 0px 8px 30px rgba(0, 0, 0, 0.05);}
        section[data-testid="stSidebar"] {background: linear-gradient(to bottom, #a0e9eb, #e0f7f9);}
        section[data-testid="stSidebar"] * {color: #006d77 !important;}
        input[type="text"] {border: 2px solid #00b4d8; border-radius: 8px; padding: 10px; background-color: #f0f9fa; color: #006d77;}
        input[type="text"]:focus {border: 2px solid #00b4d8; background-color: #ffffff;}
        .stAlert {background-color: #c2f2f4 !important; color: #006d77 !important; border: 2px solid #00b4d8; border-radius: 12px; font-weight: 600;}
        .stAlert:hover {box-shadow: 0px 0px 15px #00b4d8;}
        h1, h2, h3 {font-weight: 700; color: #008080;}
        footer {visibility: hidden;}
        header[data-testid="stHeader"] {background: none;}
        div[data-testid="collapsedControl"] svg {
            stroke: #006d77 !important;
            color: #006d77 !important;
            transition: 0.3s ease;
        }
        div[data-testid="collapsedControl"]:hover svg {
            stroke: #00b4d8 !important;
            color: #00b4d8 !important;
            filter: drop-shadow(0 0 7px #00b4d8) drop-shadow(0 0 12px #00b4d8);
            transform: scale(1.2);
            transition: 0.3s ease;
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
        input[type="text"] {border: 2px solid #00f0ff; border-radius: 8px; padding: 10px; background-color: #002222; color: #f0f0f0;}
        input[type="text"]:focus {border: 2px solid #00f0ff; background-color: #001c1c;}
        label, .css-1cpxqw2, .css-1cpxqw2 span {color: #b2ffff !important; font-weight: 500;}
        .stAlert {background-color: #003838 !important; color: #d9fef7 !important; border: 2px solid #00f0ff; border-radius: 12px; font-weight: 600;}
        .stAlert:hover {box-shadow: 0px 0px 15px #00f0ff;}
        h1, h2, h3 {font-weight: 700; color: #f0f0f0;}
        footer {visibility: hidden;}
        header[data-testid="stHeader"] {background: none;}
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

st.title("Welcome to the Dashboard")
st.markdown("Use the sidebar to navigate to different pages")
