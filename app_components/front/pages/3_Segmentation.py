import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from dotenv import load_dotenv
import os

# ---------------------- Page Config ----------------------
st.set_page_config(page_title="Customer Segmentation", layout="wide")
st.title("Customer Segmentation")

# ---------------------- Mode Handling ----------------------
# Set up dark mode if not set in session state
if 'mode' not in st.session_state:
    st.session_state['mode'] = 'Dark Mode'  # Set default to dark mode

mode = st.session_state['mode']

# Apply dark mode styles if 'Dark Mode' is selected
if mode == "Dark Mode":
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

# ---------------------- Theme Variables ----------------------
# Define the colors for dark mode
theme_teal = "#008080"
theme_dark_text = "#f0f0f0"
bar_color = "#62a6a8"
text_color = theme_dark_text
label_color = theme_dark_text

# ---------------------- Load Environment Variables ----------------------
# Load the API URLs from the .env file
load_dotenv()
API_URL = os.getenv("API_SEGMENTATION_ENDPOINT")
SEGMENT_API = os.getenv("API_RFM_SEGMENTS_BUTTON")
EMAIL_API_BASE = os.getenv("API_LAUNCH_CAMPAIGN_BASE")
API_MATRIX = os.getenv("API_SEGMENTATION_ENDPOINT_MATRIX")

# ---------------------- Fetch Segment Distribution ----------------------
@st.cache_data(show_spinner=True)
def fetch_segment_distribution():
    """
    Fetch the customer segment distribution from the provided API endpoint.
    
    Returns:
        pd.DataFrame: A sorted DataFrame of segments and their customer counts.
    """
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(list(data.items()), columns=["Segment", "Count"])
            return df.sort_values("Count", ascending=False)
        else:
            st.error(f"API returned status code: {response.status_code}")
    except Exception as e:
        st.error(f"Error fetching segment data: {e}")
    return pd.DataFrame()

# ---------------------- Plot Segment Distribution ----------------------
df = fetch_segment_distribution()

if not df.empty:
    fig = px.bar(
        df, x="Segment", y="Count", text_auto=True,
        labels={"Count": "Number of Customers", "Segment": "Segment"}
    )

    fig.update_layout(
        title=dict(text="Customer Segment Distribution", font=dict(size=24, color=label_color)),
        font=dict(family="Segoe UI", size=14),
        xaxis=dict(title=dict(text="Segment", font=dict(size=16, color=label_color)), tickfont=dict(color=label_color)),
        yaxis=dict(title=dict(text="Customer Count", font=dict(size=16, color=label_color)), tickfont=dict(color=label_color)),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=60, b=60)
    )

    fig.update_traces(marker_color=bar_color, textfont_size=12, textfont_color=text_color)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Segment distribution data not available.")

# ---------------------- Fetch RFM Matrix ----------------------
@st.cache_data(show_spinner=True)
def fetch_rfm_matrix():
    """
    Fetch the RFM (Recency, Frequency, Monetary) matrix from the provided API endpoint.

    Returns:
        pd.DataFrame: A DataFrame of the RFM matrix with customer details.
    """
    try:
        response = requests.get(API_MATRIX)
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            st.error(f"Failed to fetch RFM matrix: {response.status_code}")
    except Exception as e:
        st.error(f"Error fetching RFM matrix: {e}")
    return pd.DataFrame()

# ---------------------- Plot RFM Matrix ----------------------
st.subheader("RFM Matrix Heatmap")
rfm_df = fetch_rfm_matrix()

if not rfm_df.empty:
    rfm_df["recency_score"] = rfm_df["recency_score"].astype(int)
    rfm_df["frequency_score"] = rfm_df["frequency_score"].astype(int)
    rfm_df["hover"] = (
        "Segment: " + rfm_df["segment"] +
        "<br>Users: " + rfm_df["user_count"].astype(str) +
        "<br>Avg Monetary: $" + rfm_df["avg_monetary"].astype(str) +
        "<br>User %: " + rfm_df["user_percent"].astype(str) + "%"
    )

    fig_matrix = px.density_heatmap(
        rfm_df,
        x="recency_score", y="frequency_score", z="user_count",
        text_auto=True, hover_name="hover",
        color_continuous_scale="Teal",
        labels={"user_count": "Users"},
    )

    fig_matrix.update_layout(
        title=dict(text="RFM Segmentation Matrix (Recency vs Frequency)", font=dict(size=22, color=label_color)),
        xaxis_title="Recency Score",
        yaxis_title="Frequency Score",
        font=dict(family="Segoe UI", size=13, color=label_color),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=60, b=60)
    )

    st.plotly_chart(fig_matrix, use_container_width=True)
else:
    st.info("RFM matrix data not available.")

# ---------------------- Segment Selection & Campaign Launch ----------------------
segments = []
if SEGMENT_API:
    try:
        response = requests.get(SEGMENT_API)
        response.raise_for_status()
        segments = response.json()
    except Exception as e:
        st.error(f"Could not load segments: {e}")
else:
    st.warning("API_RFM_SEGMENTS_BUTTON not set in .env")

if segments:
    st.subheader("Select a Segment to Send Emails")
    selected_segment = st.selectbox("RFM Segment", segments)

    if selected_segment:
        st.success(f"Segment selected: **{selected_segment}**")

        if st.button("Launch Email Campaign"):
            if EMAIL_API_BASE:
                try:
                    segment_api_friendly = selected_segment.replace(" ", "")
                    api_url = EMAIL_API_BASE.replace("{segment}", segment_api_friendly)

                    st.write(f"Launching campaign for segment: {selected_segment}")
                    st.write(f"API URL: {api_url}")

                    response = requests.post(api_url)
                    response.raise_for_status()
                    detail = response.json().get("detail", "")
                    st.success(f"Campaign Launched! {detail}")
                except requests.exceptions.HTTPError as http_err:
                    st.error(f"HTTP error occurred: {http_err}")
                except Exception as e:
                    st.error(f"Failed to send campaign: {e}")
            else:
                st.error("API_LAUNCH_CAMPAIGN_BASE not set in .env")
else:
    st.info("No segments available to display.")