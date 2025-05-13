import streamlit as st
import pandas as pd
import requests
from dotenv import load_dotenv
import os
import plotly.express as px

# Set up the Streamlit page configuration
st.set_page_config(page_title="Revenue Insights", layout="wide")

# Title of the page
st.title("Revenue Insights")

# Custom CSS for styling the page
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

# Load environment variables from .env file
load_dotenv()
API_URL = os.getenv("API_REVENUE_ENDPOINT")  # Fetch the API URL for revenue data

# Define color themes for the visualization
theme_teal = "#008080"
text_color = "#f0f0f0"
bar_color = "#62a6a8"
label_color = "#f0f0f0"

@st.cache_data(show_spinner=True)
def fetch_revenue_data():
    """
    Fetches revenue data from the API, parses it into a DataFrame,
    and prepares it for visualization.

    This function performs the following tasks:
    1. Sends a GET request to the API endpoint specified by `API_REVENUE_ENDPOINT`.
    2. If the request is successful, it parses the returned JSON data into a pandas DataFrame.
    3. It assumes the response data is either a list of lists or a list of dictionaries and adjusts accordingly.
    4. It renames the columns to 'Month' and 'Revenue' and adds a 'Month_dt' column for datetime processing.
    5. The DataFrame is sorted by 'Month_dt' for chronological order.
    
    Returns:
        pd.DataFrame: A DataFrame containing 'Month', 'Revenue', and a parsed 'Month_dt' for sorting.
    """
    try:
        # Send a GET request to the API endpoint
        response = requests.get(API_URL)
        
        # Check if the API call was successful
        if response.status_code == 200:
            data = response.json()  # Parse the JSON response
            
            # Handle cases based on the structure of the returned data
            if isinstance(data, list) and isinstance(data[0], list):
                df = pd.DataFrame(data, columns=["Month", "Revenue"])  # List of lists format
            elif isinstance(data[0], dict):
                df = pd.DataFrame(data)  # List of dictionaries format
                df.rename(columns={"month": "Month", "revenue": "Revenue"}, inplace=True)  # Rename columns
            else:
                st.error("Unexpected API data format.")
                return pd.DataFrame()
            
            # Parse 'Month' column as datetime for proper sorting
            df["Month_dt"] = pd.to_datetime(df["Month"], format="%b %Y")
            df = df.sort_values("Month_dt")  # Sort by datetime column
            
            return df  # Return the cleaned and sorted DataFrame
        else:
            st.error(f"API returned status code: {response.status_code}")  # Handle API errors
            return pd.DataFrame()  # Return an empty DataFrame on error
    except Exception as e:
        st.error(f"Error fetching data from API: {e}")  # Handle any other errors
        return pd.DataFrame()  # Return an empty DataFrame in case of error

# Fetch the revenue data using the above function
df = fetch_revenue_data()

if not df.empty:
    # Create a bar chart using Plotly Express for the revenue data
    fig = px.bar(
        df,
        x="Month",  # X-axis shows the 'Month'
        y="Revenue",  # Y-axis shows the 'Revenue'
        title="Monthly Revenue Overview",  # Chart title
        text_auto=".2s",  # Automatically format the text on the bars
        labels={"Revenue": "Revenue", "Month": "Month"}  # Axis labels
    )

    # Customize layout settings for the chart
    fig.update_layout(
        title=dict(
            text="Monthly Revenue Overview",  # Title of the chart
            font=dict(size=24, color=label_color)  # Title font settings
        ),
        font=dict(family="Segoe UI", size=14),  # Font settings for the labels and tickers
        xaxis=dict(
            title=dict(text="Month", font=dict(size=16, color=label_color)),  # X-axis label
            tickfont=dict(color=label_color)  # X-axis tick label color
        ),
        yaxis=dict(
            title=dict(text="Revenue", font=dict(size=16, color=label_color)),  # Y-axis label
            tickfont=dict(color=label_color)  # Y-axis tick label color
        ),
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent background for the plot area
        paper_bgcolor="rgba(0,0,0,0)",  # Transparent background for the whole chart
        margin=dict(t=60, b=60)  # Set margin for the chart
    )
    
    # Update the bar chart's appearance, setting the bar color and text properties
    fig.update_traces(
        marker_color=bar_color,  # Bar color
        textfont_size=12,  # Text size on the bars
        textfont_color=text_color  # Text color on the bars
    )
    
    # Display the Plotly chart within Streamlit
    st.plotly_chart(fig, use_container_width=True)
else:
    # Show a message if the DataFrame is empty (i.e., no data was fetched)
    st.info("Revenue data not available.")
