import streamlit as st
import pandas as pd
import requests
from dotenv import load_dotenv
import os
import plotly.graph_objects as go

# Set up Streamlit page configuration
st.set_page_config(page_title="Survival Analysis", layout="wide")

# Page title and styling
st.title("Survival Analysis")
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
    h1, h2, h3 {
        font-weight: 700;
        color: #f0f0f0;
    }
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {background: none;}
    </style>
""", unsafe_allow_html=True)

# Load environment variables from a .env file
load_dotenv()
API_URL = os.getenv("API_SURVIVAL_ENDPOINT")  # API URL for fetching survival curve data

def fetch_survival_curve_data():
    """
    Fetches the survival curve data from the API endpoint.

    This function sends a GET request to the API endpoint and attempts to 
    retrieve the Survival curve data, including survival 
    probabilities and confidence intervals. If the request is successful, 
    the data is returned as a JSON object. If there is any error during 
    the request, an error message is displayed using Streamlit.

    Returns:
        list: A list of dictionaries containing time, survival probabilities, 
              and confidence intervals for each point on the survival curve.
    """
    try:
        response = requests.get(API_URL)  # Send GET request to API
        response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)
        return response.json()  # Return the JSON response if successful
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")  # Display HTTP error
    except Exception as err:
        st.error(f"Other error occurred: {err}")  # Display general error
    return []  # Return an empty list in case of failure

# Fetch survival curve data
data = fetch_survival_curve_data()

if data:
    # Extract data points for time, survival probabilities, and confidence intervals
    times = [point['time'] for point in data]
    survival_probs = [point['survival_prob'] for point in data]
    ci_lower = [point['ci_lower'] for point in data]
    ci_upper = [point['ci_upper'] for point in data]

    # Create a Plotly figure
    fig = go.Figure()

    # Add the survival curve to the figure
    fig.add_trace(go.Scatter(
        x=times, y=survival_probs,
        mode='lines', name='Survival Curve',
        line=dict(color='#1c79c0')  # Brighter blue color for the survival curve
    ))

    # Add the confidence interval as a shaded area
    fig.add_trace(go.Scatter(
        x=times + times[::-1],  # Concatenate times for confidence interval
        y=ci_upper + ci_lower[::-1],  # Reverse lower confidence interval
        fill='toself', fillcolor='rgba(28, 121, 192, 0.3)',  # Lighter transparent blue for confidence interval
        line=dict(color='rgba(255,255,255,0)'),  # No border line for the confidence interval
        name='95% Confidence Interval'
    ))

    # Update layout settings for the figure
    fig.update_layout(
        title="Survival Curve",  # Title of the plot
        title_font=dict(family="Segoe UI", size=16, color="white"),  # Title font settings
        xaxis_title="Time",  # Label for x-axis
        yaxis_title="Survival Probability",  # Label for y-axis
        plot_bgcolor='#002424',  # Darker background for the plot area
        paper_bgcolor='#002424',  # Dark background for the whole figure
        font=dict(family="Segoe UI", size=12, color="white"),  # Font settings for axis and labels
        height=600  # Set the height of the plot
    )

    # Display the Plotly chart in the Streamlit app
    st.plotly_chart(fig)
else:
    # Display a message if no data is available
    st.info("No survival curve data available.")
