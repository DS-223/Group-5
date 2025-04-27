import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set up app
st.set_page_config(page_title="Transaction Analysis", layout="wide")
st.title("Transaction Analysis")

# Mode selection
mode = st.sidebar.radio("Choose Display Mode:", ("Light Mode", "Dark Mode"))

# Sample Data
dates = pd.date_range(start="2024-01-01", periods=12, freq='M')
districts = ["North", "South", "East", "West", "Central"]

df = pd.DataFrame({
    "Date": np.tile(dates, len(districts)),
    "District": np.repeat(districts, len(dates)),
    "Transactions": np.random.randint(100, 1000, len(dates) * len(districts))
})

# Line plot
fig = px.line(
    df, 
    x="Date", 
    y="Transactions", 
    color="District", 
    title="Monthly Transactions by District",
    color_discrete_map={
        "North": "#00b4d8",   # Bright turquoise
        "South": "#90e0ef",   # Light turquoise
        "East": "#0077b6",    # Deep turquoise
        "West": "#48cae4",    # Sky blue turquoise
        "Central": "#0096c7"  # Fresh strong turquoise
    }
)

# Dynamic plot background and text based on mode
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

# Show plot
st.plotly_chart(fig, use_container_width=True)

# Dynamic page styling
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
        label, .css-1cpxqw2, .css-1cpxqw2 span {
            color: #006d77 !important;
            font-weight: 500;
        }
        input[type="text"] {
            border: 2px solid #00b4d8;
            border-radius: 8px;
            padding: 10px;
            background-color: #f0f9fa;
            color: #006d77;
        }
        input[type="text"]:focus {
            border: 2px solid #00b4d8;
            background-color: #ffffff;
        }
        .stAlert {
            background-color: #c2f2f4 !important;
            color: #006d77 !important;
            border: 2px solid #00b4d8;
            border-radius: 12px;
            font-weight: 600;
        }
        .stAlert:hover {
            box-shadow: 0px 0px 15px #00b4d8;
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
        label, .css-1cpxqw2, .css-1cpxqw2 span {
            color: #f0f0f0 !important;
            font-weight: 500;
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
        .stAlert {
            background-color: #003838 !important;
            color: #f0f0f0 !important;
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
        footer {visibility: hidden;}
        header[data-testid="stHeader"] { background: none; }
        </style>
    """, unsafe_allow_html=True)
