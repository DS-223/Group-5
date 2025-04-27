import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Personalized Search", layout="wide")

mode = st.sidebar.radio("Choose Display Mode:", ("Light Mode", "Dark Mode"))

st.title("Personalized Customer Search")

df = pd.DataFrame({
    "Customer ID": [f"{i:013d}" for i in range(1, 101)],
    "First name": np.random.choice(["Anna", "Liam", "Sara", "John", "Hayk", "Gayane", "Mariam", "Albert", "Narek"], 100),
    "Last name": np.random.choice(["Smith", "Porter", "Doe", "Grenger", "Nalchajyan", "Hovsepyan", "Mezhlumyan", "Simonyan", "Ghukasyan"], 100),
    "Email": [f"user{i}@mail.com" for i in range(1, 101)],
    "Value": np.random.randint(100, 1000, 100)
})

def generate_html_table(dataframe, mode):
    bg_color = "#001c1c" if mode == "Dark Mode" else "white"
    text_color = "#f0f0f0" if mode == "Dark Mode" else "#006d77"
    header_bg = "#003838" if mode == "Dark Mode" else "#e0f7f9"

    table_html = f"""
    <div style="overflow-x:auto; margin-top: 1rem;">
    <table style="border-collapse: collapse; width: 100%;">
    <thead style="background-color:{header_bg}; color:{text_color};">
      <tr>
    """
    for col in dataframe.columns:
        table_html += f"<th style='padding: 10px; text-align: center; border-bottom: 2px solid {text_color};'>{col}</th>"
    table_html += "</tr></thead><tbody>"

    for _, row in dataframe.iterrows():
        table_html += "<tr>"
        for cell in row:
            table_html += f"<td style='padding: 10px; background-color:{bg_color}; color:{text_color}; text-align: center; border-bottom: 1px solid {header_bg};'>{cell}</td>"
        table_html += "</tr>"

    table_html += "</tbody></table></div>"
    return table_html

cust_id = st.text_input("Enter Customer ID (e.g., 0000000000005)")

if cust_id:
    result = df[df["Customer ID"] == cust_id.upper()]
    if not result.empty:
        st.markdown(f"""
        <div style='background-color: #003838; padding: 10px; border-radius: 8px; margin-top:10px;'>
            <h4 style='color: #f0f0f0; margin:0;'>Customer found:</h4>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(generate_html_table(result, mode), unsafe_allow_html=True)
    else:
        not_found_color = "#5a2b2b" if mode == "Dark Mode" else "#ffecec"
        text_color = "#f0f0f0" if mode == "Dark Mode" else "#b30000"
        st.markdown(f"""
        <div style='background-color: {not_found_color}; padding: 10px; border-radius: 8px; margin-top:10px;'>
            <h4 style='color: {text_color}; margin:0;'>No customer found.</h4>
        </div>
        """, unsafe_allow_html=True)

if mode == "Light Mode":
    st.markdown("""
        <style>
        /* LIGHT MODE */
        .stApp {background-color: #e0f7f9; font-family: 'Segoe UI', sans-serif; color: #006d77;}
        .block-container {padding-top: 1rem; background-color: white; border-radius: 12px; box-shadow: 0px 8px 30px rgba(0, 0, 0, 0.05);}
        section[data-testid="stSidebar"] {background: linear-gradient(to bottom, #a0e9eb, #e0f7f9);}
        section[data-testid="stSidebar"] * {color: #006d77 !important;}
        label, .css-1cpxqw2, .css-1cpxqw2 span {color: #006d77 !important; font-weight: 500;}
        input[type="text"] {
            border: 1px solid #00b4d8;
            border-radius: 8px;
            padding: 10px;
            background-color: #f0f9fa;
            color: #006d77;
            caret-color: black;
        }
        input[type="text"]:focus {
            border: 1px solid #00b4d8;
            background-color: #ffffff;
        }
        h1, h2, h3, h4 {font-weight: 700; color: #008080;}
        footer {visibility: hidden;}
        header[data-testid="stHeader"] {background: none;}
        </style>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
        <style>
        /* DARK MODE */
        .stApp {background-color: #001c1c; font-family: 'Segoe UI', sans-serif; color: #f0f0f0;}
        .block-container {padding-top: 1rem; background-color: #002424; border-radius: 12px; box-shadow: 0px 8px 30px rgba(255, 255, 255, 0.05);}
        section[data-testid="stSidebar"] {background: linear-gradient(to bottom, #002929, #001c1c);}
        section[data-testid="stSidebar"] * {color: #f0f0f0 !important;}
        label, .css-1cpxqw2, .css-1cpxqw2 span {color: #f0f0f0 !important; font-weight: 500;}
        input[type="text"] {
            border: 1px solid #00f0ff;
            border-radius: 8px;
            padding: 10px;
            background-color: #002222;
            color: #f0f0f0;
            caret-color: white;
        }
        input[type="text"]:focus {
            border: 1px solid #00f0ff;
            background-color: #001c1c;
        }
        h1, h2, h3, h4 {font-weight: 700; color: #f0f0f0;}
        footer {visibility: hidden;}
        header[data-testid="stHeader"] {background: none;}
        </style>
    """, unsafe_allow_html=True)
