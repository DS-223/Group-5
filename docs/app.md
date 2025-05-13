# 🎛️ Streamlit App Documentation

This app is the **frontend dashboard** for the Loyalytics platform, built using **Streamlit**. It connects to the REST API to visualize customer loyalty metrics, transactions, revenue trends, RFM segmentation, and survival probabilities.

---

## 📦 Features & Pages

### 🧮 Dashboard
- Filterable by **store**, **segment**, and **date range**
- Displays **scorecards**: Total Revenue, Total Orders, and Total Customers
- Fetches live data via `/dropdowns` and `/analytics/summary-scorecards`

### 💰 Revenue Insights
- Visualizes monthly revenue using a **Plotly bar chart**
- Pulls data from `/revenue/monthly`
- Cached for fast repeat loads
- Dark-themed UI with stylish customization

### 💳 Transaction Analysis
- Bar chart: Transaction totals by store (`/analytics/transaction-amount-by-store`)
- Line chart: Monthly trends per store (`/analytics/transactions-by-store-month`)
- Helps identify store-level purchase behavior

### 🧠 Customer Segmentation
- Segment distribution bar chart (`/analytics/segment-distribution/all`)
- Heatmap from RFM Matrix (`/analytics/rfm-matrix`)
- RFM-based campaign launcher with email triggers (`/campaigns/{segment}`)
- Dynamic dropdowns from `/analytics/segments_for_button`

### 🕵️‍♂️ Customer Search
- Enter a customer ID to view their profile
- Data pulled via `/customers/{id}`
- Highlights missing or malformed results

### 💼 Transaction Search
- Enter a customer ID to see all their purchases
- Data pulled via `/customers/{id}/transactions`

### ⏳ Survival Analysis
- Fetches Weibull survival curve (`/analytics/survival-curve`)
- Visualizes customer retention over time
- Shaded 95% confidence intervals

---

## 🔐 API Integration

All endpoints are managed through `.env` file keys:

| Env Key | Description |
|---------|-------------|
| `API_REVENUE_ENDPOINT` | Revenue data |
| `API_CUSTOMER_ENDPOINT` | Customer profile fetch |
| `API_TRANSACTIONS_ENDPOINT` | Customer transactions |
| `API_SEGMENTATION_ENDPOINT` | Segment distribution |
| `API_RFM_SEGMENTS_BUTTON` | Segment dropdowns |
| `API_LAUNCH_CAMPAIGN_BASE` | Launch email campaigns |
| `API_TRANSACTIONS_BYSTORE_ENDPOINT` | Store-level totals |
| `API_TRANSACTIONS_MONTH_ENDPOINT` | Store-level monthly trends |
| `API_SEGMENTATION_ENDPOINT_MATRIX` | RFM matrix |
| `API_SURVIVAL_ENDPOINT` | Survival curve |
| `API_STORES_ENDPOINT` | Store dropdown |
| `API_SEGMENTS_ENDPOINT` | Segment dropdown |
| `API_DATERANGE_ENDPOINT` | Min/Max dates |
| `API_SCORECARDS_ENDPOINT` | Scorecard data |

---

## 🛠️ Style & Theming

- Full dark mode with consistent typography and layout
- Responsive sidebar and headers
- Styled metric boxes and input elements
- Plotly for all charts
- Custom CSS blocks embedded per-page

---

## 🐳 Docker Support

The app is deployed via Docker. Configuration:

```Dockerfile
# Dockerfile snippet
FROM python:3.10-slim-bullseye
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.headless=true", "--server.runOnSave=true"]
```

---

## 📦 Requirements

Installed via `requirements.txt`:

- `streamlit`, `requests`, `plotly`, `dotenv`, `SQLAlchemy`, `psycopg2-binary`
- Other visualization and dependency libraries (see full file)

---

## ✅ Status

- 🧪 Fully tested with API backend
- 📊 Dashboards live and connected
- 💌 Email integration active
- 🐳 Dockerized and production-ready

---

## 📂 Related Files

| File | Purpose |
|------|---------|
| `app.py` | Streamlit entry point |
| `/pages` | Streamlit web pages |
| `.env` | Stores environment variables |
| `Dockerfile` | Streamlit Docker image |
| `requirements.txt` | Python dependencies |

