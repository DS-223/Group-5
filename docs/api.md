# 🚀 API Documentation

This service exposes the **REST API layer** for the Customer Loyalty & Analytics system. It powers the dashboard, segmentation visualizations, survival models, and automated email campaigns.

Built with **FastAPI**, the API provides endpoints for querying customer data, analyzing transactions, generating RFM segments, and sending retention emails.

---

## ⚙️ Tech Stack

- **FastAPI** – Lightweight, fast web framework for REST endpoints
- **SQLAlchemy** – ORM for interacting with PostgreSQL
- **Pydantic** – Request validation & API response schemas
- **Lifelines** – Kaplan-Meier survival analysis
- **BackgroundTasks** – Async email dispatching

---

## 👤 Customer Endpoints

Manage customer profiles stored in `DimCustomer`:

- `POST /customers/` – Create a new customer  
- `GET /customers/{id}` – Retrieve customer details  
- `PUT /customers/{id}` – Update customer profile  
- `DELETE /customers/{id}` – Remove a customer record

Also includes:

- `GET /analytics/customer-count-by-gender` – Gender-wise demographic distribution

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

Each template includes personalized subject lines and discount codes. See logic in `EmailCampaignManager`.

---

## 📈 Survival Analysis

Use Kaplan-Meier to visualize customer churn over time:

- `GET /analytics/survival-curve` – Returns survival probability at each time step using `SurvivalData`

Supports visualization of customer retention lifecycle.

---

## 🛠️ Example Schema: `CustomerCreate`

```json
{
  "CustomerKey": 123,
  "CustomerCardCode": "BNS1234567890",
  "Name": "Jane Doe",
  "RegistrationDate": "2020-01-01T00:00:00",
  "BirthDate": "1990-05-10",
  "Gender": "Female",
  "Phone": "(555) 123-4567",
  "Address": "123 Loyalty St.",
  "Email": "jane.doe@example.com"
}
```

---

## 🔐 Security & Config

Sensitive credentials like DB URLs or Gmail credentials are stored in a `.env` file. Email logic uses OAuth-friendly app passwords.

---

## 📂 Related Files

| File | Description |
|------|-------------|
| `main.py` | FastAPI app with all endpoints |
| `schema.py` | Pydantic models for request/response |
| `email_utils.py` | Email template logic and SMTP sending |
| `columns.py` | SQLAlchemy table mappings |
| `Dockerfile` | FastAPI container setup |
| `requirements.txt` | All dependencies (e.g., lifelines, fastapi, sqlalchemy) |

---

## 🧪 Testing

Test endpoints locally using:

- Swagger UI: [`localhost:8000/docs`](http://localhost:8000/docs)  
- ReDoc: [`localhost:8000/redoc`](http://localhost:8000/redoc)

---

## ✅ Status

- 📬 Email logic tested for all segments
- 📈 Survival curve rendered correctly
- ✅ Endpoints verified via Swagger
- 🐳 Works with Docker Compose stack

---

For more information, explore [index.md](index.md), [database.md](database.md), and [model.md](model.md).
