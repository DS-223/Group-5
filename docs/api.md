# 🚀 API Documentation

This service exposes the **REST API layer** for the Customer Loyalty & Analytics system. It powers the dashboard, segmentation visualizations, survival models, and automated email campaigns.

Built with **FastAPI**, the API provides endpoints for querying customer data, analyzing transactions, generating RFM segments, launching email campaigns, and dashboard filters.

---

## ⚙️ Tech Stack

- **FastAPI** – Lightweight, fast web framework for REST endpoints
- **SQLAlchemy** – ORM for interacting with PostgreSQL
- **Pydantic** – Request validation & API response schemas
- **Lifelines** – Weibull AFT survival analysis
- **BackgroundTasks** – Async email dispatching

---

## 👤 Customer Endpoints

Manage customer profiles stored in `DimCustomer`:

- `POST /customers/` – Create a new customer  
- `GET /customers/{id}` – Retrieve customer details  
- `PUT /customers/{id}` – Update customer profile  
- `DELETE /customers/{id}` – Remove a customer record  
- `GET /analytics/customer-count-by-gender` – Gender-wise customer distribution

---

## 💰 Transaction & Revenue Analytics

Explore sales data using joins over the star schema:

- `GET /revenue/monthly` – Monthly revenue totals  
- `GET /customers/{id}/transactions` – Full transaction history of a customer  
- `GET /analytics/transactions-by-store-month` – Monthly revenue by store  
- `GET /analytics/transaction-amount-by-store` – Lifetime revenue by store  

---

## 📊 RFM Segmentation

Provides data on **Recency-Frequency-Monetary segments**:

- `GET /analytics/customers-by-segment/{segment}` – List of customers in a specific segment  
- `GET /analytics/segment-distribution/{all|male|female}` – Distribution of segments overall or by gender  
- `GET /analytics/rfm-matrix` – RFM matrix for segment summaries  

---

## 📧 Email Campaigns

Launch targeted retention campaigns via segment-specific email templates:

- `GET /analytics/segments_for_button` – List of all segments for frontend dropdowns  
- `POST /campaigns/{segment}` – Asynchronously send emails to all users in a segment using **BackgroundTasks**  

---

## 📈 Survival Analysis

Uses **Weibull AFT** to model customer churn over time:

- `GET /analytics/survival-curve` – Survival probability over time using `SurvivalData` with Age and Gender as covariates

---

## 🧮 Scorecard Metrics

Returns KPIs used for dashboard summary tiles:

- `GET /analytics/summary-scorecards` – Returns revenue, orders, and unique customer count  
  Filters: `store_id`, `start_date`, `end_date`, `segment`

---

## 🧩 Dashboard Dropdowns

Provides values for dynamic filter controls:

- `GET /dropdowns/stores` – List of store IDs and names  
- `GET /dropdowns/segments` – All available RFM segments  
- `GET /dropdowns/date-range` – Minimum and maximum transaction dates  

---

## 🧪 Testing

Test endpoints locally using:

- Swagger UI: [`localhost:8000/docs`](http://localhost:8000/docs)  
- ReDoc: [`localhost:8000/redoc`](http://localhost:8000/redoc)

---

## 📂 Related Files

| File | Description |
|------|-------------|
| `main.py` | FastAPI app with all endpoints |
| `schema.py` | Pydantic models for request/response |
| `email_utils.py` | Email template logic and SMTP sending |
| `columns.py` | SQLAlchemy table mappings |
| `Dockerfile` | FastAPI container setup |
| `requirements.txt` | Python dependencies |

---

## ✅ Status

- 📬 Email logic verified for all segments  
- 📈 Weibull survival curve implemented  
- ✅ Swagger-tested endpoints  
- 🐳 Docker Compose ready  

---

For more information, explore [index.md](index.md), [database.md](database.md), [app.md](app.md) and [model.md].
