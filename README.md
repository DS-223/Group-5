# 🧠 Loyalytics – Marketing Analytics Project

### 📈 Overview
Loyalytics is an end-to-end marketing analytics platform designed to help supermarkets retain customers and boost loyalty. By analyzing transaction data from bonus card holders, the system performs behavioral segmentation, RFM analysis, and survival modeling to uncover actionable insights.

---

## 🔍 Problem Statement
**“What factors are contributing to the drop in sales among bonus cardholders, and how can we use segmentation to improve customer retention and loyalty?”**

Despite a bonus card system, customer activity and sales have declined. This platform helps the company investigate behavioral data, segment customers, and improve targeting efforts.

---

## ⚙️ Technologies Used
- **FastAPI** – REST API for backend
- **Python** – Core language for ETL, modeling, and APIs
- **Pandas, Scikit-learn, Lifelines** – Data processing, ML & survival analysis
- **SQLAlchemy, PostgreSQL** – ORM and relational database
- **Streamlit** – Interactive front-end dashboard
- **Docker & Docker Compose** – Containerized orchestration
- **pgAdmin** – GUI for managing PostgreSQL
- **MkDocs** – Project documentation (📄 [GitHub Pages Site](https://ds-223.github.io/Group-5/))

---

## 🚀 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/DS-223/Group-5.git
cd Group-5/app_components
```

### 2. Build and Launch the Application
```bash
docker-compose up --build
```

All services will spin up: ETL, API, Streamlit, PostgreSQL, and pgAdmin.

---

## 🌐 Access Services
- 📊 Streamlit Front-End: [http://localhost:8501](http://localhost:8501)
- 🧪 FastAPI Docs: [http://localhost:8008/docs](http://localhost:8008/docs)
- 🛠️ pgAdmin UI: [http://localhost:5050](http://localhost:5050)

## For the Streamlit Personalized Search and Transaction History Search, try CustomerID: 70444
## For the Streamlit Main page, set the dates (today's date is added automatically), real data range is **01/09/2024 - 14/04/2025**
## For the FastApi customer-related calls, try CustomerID: 70444

### First Time pgAdmin Setup
1. Go to [http://localhost:5050](http://localhost:5050)
2. Login:
   - Email: `admin@admin.com`
   - Password: `admin`
3. Create a new server connection:
   - Name: anything (e.g., `postgres-db`)
   - Host: `db`
   - Port: `5432`
   - Username: `postgres`
   - Password: `postgres`
   - Database: `maindb`

---

## 🧪 ERD – Entity Relationship Diagram
The project’s star schema includes:
- **FactTransaction**
- **DimCustomer**
- **DimDate**
- **DimStore**

📄 View full ERD in [`ERD.pdf`](ERD.pdf)

---

## 🧬 Project Structure

```
app_components/
├── api/                → FastAPI service
│   ├── __init__.py
│   ├── columns.py
│   ├── database.py
│   ├── email_utils.py
│   ├── main.py
│   ├── schema.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env
│
├── ds/                 → ML & analytics (RFM, survival)
│   ├── ds_main.py
│   ├── wait-for-etl.sh
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env
│   ├── db_ops/
│   │   ├── __init__.py
│   │   ├── db_writer.py
│   │   ├── extract_and_save.py
│   ├── utils/
│       ├── __init__.py
│       ├── rfm_analyzer.py
│       ├── survival_analyzer.py
│   ├── outputs/
│
├── etl/                → ETL pipeline
│   ├── main.py
│   ├── CRUD_func.py
│   ├── extract_load_raw.py
│   ├── load.py
│   ├── transform.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .dockerignore
│   ├── data/
│   ├── db/
│       ├── create_tables.py
│       ├── db_conf.py
│       ├── star_schema.py
│
├── front/              → Streamlit dashboard
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env
│   ├── pages/
│       ├── 1_Revenue.py
│       ├── 2_Transactions.py
│       ├── 3_Segmentation.py
│       ├── 4_Personalized_search.py
│       ├── 5_Transaction_history.py
│
├── postgres_data/      → PostgreSQL volume
├── pgadmin_data/       → pgAdmin volume
├── docker-compose.yml
├── .env

docs/
├── index.md
├── api.md
├── app.md
├── database.md
├── model.md
├── mkdocs.yml

feedback/
├── Milestone 1 Feedback.pdf
├── Milestone 2 Feedback.pdf
├── Milestone 3 Feedback.pdf

LICENSE
README.md
ERD.pdf
Website_skeleton.pdf
requirements.txt
mkdocs_requirements.txt
demo.md
```

---

## 👥 Team Members
- **Product/Project Manager:** Albert Simonyan
- **Data Scientist:** Hayk Nalchajyan  
- **Backend Developer:** Gayane Hovsepyan  
- **Frontend Developer:** Mariam Mezhlumyan  
- **Database Engineer:** Narek Ghukasyan 

---

## 📅 Milestones
- **Milestone 1:** Problem definition, roadmap, UI prototype
- **Milestone 2:** Database, ETL, model logic implementation
- **Milestone 3:** Integrated dashboard, deployment, final report
