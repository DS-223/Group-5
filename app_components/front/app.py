import streamlit as st
import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# Set page configuration for the Streamlit app
st.set_page_config(page_title="Dashboard", layout="wide")

# Custom CSS styles to format the app's appearance
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

# Load environment variables from a .env file
load_dotenv()

# Fetch endpoints from .env variables for API communication
API_STORES_ENDPOINT = os.getenv("API_STORES_ENDPOINT")
API_SEGMENTS_ENDPOINT = os.getenv("API_SEGMENTS_ENDPOINT")
API_DATERANGE_ENDPOINT = os.getenv("API_DATERANGE_ENDPOINT")
API_SCORECARDS_ENDPOINT = os.getenv("API_SCORECARDS_ENDPOINT")

# Utility functions to fetch data from external APIs

def get_store_options():
    """
    Fetch available store options from the API endpoint.
    Returns a list of store options (or an empty list if an error occurs).
    """
    try:
        response = requests.get(API_STORES_ENDPOINT)
        response.raise_for_status()  # Raises HTTPError if the response code is 4xx or 5xx
        return response.json()  # Return the JSON response containing store options
    except Exception as e:
        st.error(f"Failed to load stores: {e}")
        return []  # Return an empty list if the request fails

def get_segment_options():
    """
    Fetch available segment options from the API endpoint.
    Returns a list of segment options (or an empty list if an error occurs).
    """
    try:
        response = requests.get(API_SEGMENTS_ENDPOINT)
        response.raise_for_status()  # Check if the response status is valid
        return response.json()  # Return the segment data as a JSON response
    except Exception as e:
        st.error(f"Failed to load segments: {e}")
        return []  # Return an empty list if the request fails

def get_date_range():
    """
    Fetch the date range (min and max dates) from the API endpoint.
    Returns a dictionary containing 'min_date' and 'max_date' (or default values if an error occurs).
    """
    try:
        response = requests.get(API_DATERANGE_ENDPOINT)
        response.raise_for_status()  # Ensure the response is valid
        return response.json()  # Return the date range data as JSON
    except Exception as e:
        st.error(f"Failed to load date range: {e}")
        return {"min_date": None, "max_date": None}  # Return default values if the request fails

def get_scorecards(store_id, start_date, end_date, segment):
    """
    Fetch scorecard data based on selected store, date range, and segment.
    Args:
    - store_id (str): The selected store's unique identifier
    - start_date (str): The start date for the scorecard data (in 'YYYY-MM-DD' format)
    - end_date (str): The end date for the scorecard data (in 'YYYY-MM-DD' format)
    - segment (str): The selected segment for filtering the scorecard data

    Returns:
    - list: The scorecards data in JSON format (or an empty list if an error occurs)
    """
    try:
        params = {
            "store_id": store_id,
            "start_date": start_date,
            "end_date": end_date,
            "segment": segment
        }
        response = requests.get(API_SCORECARDS_ENDPOINT, params=params)  # Send GET request with parameters
        response.raise_for_status()  # Check if the response status is valid
        return response.json()  # Return scorecards data in JSON format
    except Exception as e:
        st.error(f"Failed to load scorecards: {e}")
        return []  # Return an empty list if the request fails

# Fetch options for stores, segments, and date range
stores = get_store_options()
segments = get_segment_options()
date_range = get_date_range()

# UI elements for interacting with the app (filters, date range, etc.)
st.title("Loyalitics")
st.markdown("Use the sidebar to navigate to different pages")

st.subheader("Filter Options")

# Create columns for the two filters (store and segment)
col1, col2 = st.columns(2)

# Selectbox for choosing a store
with col1:
    selected_store = st.selectbox(
        "Select Store",
        options=stores,  # Populate options with stores fetched from the API
        format_func=lambda x: x['label'] if isinstance(x, dict) else x,  # Display store labels
        index=0 if stores else None,  # Default to first store if available
        key="store_selectbox"
    )

# Selectbox for choosing a segment
with col2:
    selected_segment = st.selectbox(
        "Select Segment",
        options=segments,  # Populate options with segments fetched from the API
        index=0 if segments else None,  # Default to first segment if available
        key="segment_selectbox"
    )

# Display the available date range based on API response
st.markdown("### Available Date Range")
st.info(
    f"**From:** `{date_range.get('min_date', 'N/A')}` &nbsp;&nbsp;&nbsp; "
    f"**To:** `{date_range.get('max_date', 'N/A')}`"
)

# Date inputs for selecting the start and end dates for filtering
start_date = st.date_input("Start Date", min_value=datetime(2020, 1, 1), max_value=datetime.today())
end_date = st.date_input("End Date", min_value=start_date, max_value=datetime.today())

# Fetch and display scorecards when the button is clicked
if st.button("Fetch Scorecards"):
    store_id = selected_store['value']  # Extract store id from the selected store (assumed to be a dictionary)
    segment = selected_segment  # Selected segment

    # Format the selected start and end dates as strings
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")

    # Fetch the scorecards data based on the selected filters
    scorecards = get_scorecards(store_id, start_date_str, end_date_str, segment)

    # Display the fetched scorecard metrics
    if scorecards:
        st.subheader("Summary Scorecards")
        for metric in scorecards:
            st.metric(label=metric['label'], value=metric['value'])  # Display each scorecard metric
