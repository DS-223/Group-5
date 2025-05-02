import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Customer Segmentation", layout="wide")
st.title("Customer Segmentation")

if 'mode' not in st.session_state:
    st.session_state['mode'] = 'Light Mode'

mode = st.session_state['mode']

df = pd.DataFrame({
    "Recency": np.random.randint(1, 50, 100),
    "Frequency": np.random.randint(1, 20, 100),
    "Monetary": np.random.randint(50, 500, 100),
    "Segment": np.random.choice(["Low", "Medium", "High"], 100)
})

fig = px.scatter(
    df,
    x="Frequency",
    y="Monetary",
    color="Segment",
    size="Recency",
    title="RFM Segmentation",
    color_discrete_sequence=["#00e0e0", "#00cfcf", "#00baba"]
)

if mode == "Light Mode":
    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        font_color="#222831",
        title_font_color="#222831",
        legend_title_font_color="#222831",
        legend_font_color="#222831",
        xaxis_title_font=dict(color="#222831"),
        yaxis_title_font=dict(color="#222831"),
        xaxis_tickfont=dict(color="#222831"),
        yaxis_tickfont=dict(color="#222831"),
    )
else:
    fig.update_layout(
        plot_bgcolor="#001c1c",
        paper_bgcolor="#001c1c",
        font_color="#f0f0f0",
        title_font_color="#f0f0f0",
        legend_title_font_color="#f0f0f0",
        legend_font_color="#f0f0f0",
        xaxis_title_font=dict(color="#f0f0f0"),
        yaxis_title_font=dict(color="#f0f0f0"),
        xaxis_tickfont=dict(color="#f0f0f0"),
        yaxis_tickfont=dict(color="#f0f0f0"),
    )

st.plotly_chart(fig, use_container_width=True)

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
