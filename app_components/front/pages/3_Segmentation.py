import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Customer Segmentation", layout="wide")
st.title("🧬 Customer Segmentation (RFM)")

try:
    df = pd.read_csv("rfm_analysis_results.csv")
except FileNotFoundError:
    st.error("❌ 'rfm_analysis_results.csv' not found. Please upload the file.")
    st.stop()

st.markdown("### 📊 Segment Distribution")

if "segment" in df.columns:
    pie_data = df["segment"].value_counts().reset_index()
    pie_data.columns = ["Segment", "Count"]

    fig1 = px.pie(
        pie_data, 
        values="Count", 
        names="Segment", 
        title="Customer Segment Distribution",
        hole=0.4
    )
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("Column 'segment' not found.")

st.markdown("### 📈 Frequency vs Monetary Value")

if all(col in df.columns for col in ["frequency", "monetary", "segment"]):
    fig2 = px.scatter(
        df,
        x="frequency",
        y="monetary",
        color="segment",
        hover_data=["recency"],
        title="Customer Spread by Segment"
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("Missing one or more of: 'frequency', 'monetary', 'segment' columns.")
