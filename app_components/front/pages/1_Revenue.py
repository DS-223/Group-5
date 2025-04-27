import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Revenue Insights", layout="wide")
st.title("Revenue Insights")

mode = st.sidebar.radio("Choose Display Mode:", ("Light Mode", "Dark Mode"))

df = pd.DataFrame({
    "Month": pd.date_range("2024-01-01", periods=12, freq="M")
})
df["Revenue"] = np.random.randint(5000, 20000, size=len(df))

fig = px.bar(
    df,
    x="Month",
    y="Revenue",
    title="Monthly Revenue Overview",
    color_discrete_sequence=["#00b4d8"]
)

if mode == "Light Mode":
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_color="#222831",
        title_font_color="#222831",
        xaxis_title_font=dict(color="#222831"),
        yaxis_title_font=dict(color="#222831"),
        xaxis_tickfont=dict(color="#222831"),
        yaxis_tickfont=dict(color="#222831"),
    )
else:
    fig.update_layout(
        plot_bgcolor="#001c1c",
        paper_bgcolor="#001c1c",
        font_color="#d9fef7",
        title_font_color="#d9fef7",
        xaxis_title_font=dict(color="#d9fef7"),
        yaxis_title_font=dict(color="#d9fef7"),
        xaxis_tickfont=dict(color="#d9fef7"),
        yaxis_tickfont=dict(color="#d9fef7"),
    )

st.plotly_chart(fig, use_container_width=True)

if mode == "Light Mode":
    st.markdown("""
        <style>
        .stApp {
            background-color: #e0f7f9;
            font-family: 'Segoe UI', sans-serif;
            color: #006d77;
        }
        .block-container {
            padding-top: 1rem;
            background-color: white;
            border-radius: 12px;
            box-shadow: 0px 8px 30px rgba(0, 0, 0, 0.05);
        }
        section[data-testid="stSidebar"] {
            background: linear-gradient(to bottom, #a0e9eb, #e0f7f9);
        }
        section[data-testid="stSidebar"] * {
            color: #006d77 !important;
        }
        h1, h2, h3 {
            font-weight: 700;
            color: #008080;
        }
        footer {visibility: hidden;}
        header[data-testid="stHeader"] { background: none; }
        </style>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
        <style>
        .stApp {
            background-color: #001c1c;
            font-family: 'Segoe UI', sans-serif;
            color: #d9fef7;
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
            color: #d9fef7 !important;
        }
        h1, h2, h3 {
            font-weight: 700;
            color: #aefeff;
        }
        footer {visibility: hidden;}
        header[data-testid="stHeader"] { background: none; }
        </style>
    """, unsafe_allow_html=True)
