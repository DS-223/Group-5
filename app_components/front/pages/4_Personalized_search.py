import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Personalized Search", layout="wide")
st.title("Personalized Customer Search")

df = pd.DataFrame({
    "Customer ID": [f"{i:013d}" for i in range(1, 101)],
    "First name": np.random.choice(["Anna", "Liam", "Sara", "John", "Hayk", "Gayane", "Mariam", "Albert", "Narek"], 100),
    "Last name":np.random.choice(["Smith", "Porter", "Doe", "Grenger", "Nalchajyan", "Hovsepyan", "Mezhlumyan", "Simonyan", "Ghukasyan"]),
    "Email": [f"user{i}@mail.com" for i in range(1, 101)],
    "Value": np.random.randint(100, 1000, 100)
})

cust_id = st.text_input("Enter Customer ID (e.g., 0000000000005)")

if cust_id:
    result = df[df["Customer ID"] == cust_id.upper()]
    if not result.empty:
        st.success("Customer found:")
        st.dataframe(result)
    else:
        st.warning("No customer found.")

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
