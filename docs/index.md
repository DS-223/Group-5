# 📊 Welcome to Loyalytics Documentation

Loyalytics is a marketing analytics platform developed for a supermarket chain's **Bonus Card Loyalty Program**. The project addresses declining sales by analyzing customer behavior, segmenting loyalty profiles, and enabling data-driven decision-making.

---

## 🧠 Problem

Despite having a bonus card program, the supermarket has experienced declining sales. The challenge is identifying:

> **"What factors are contributing to the drop in sales among bonus cardholders, and how can segmentation improve retention?"**

---

## ✅ Solution

We implemented an end-to-end analytics platform that:

- Extracts, cleans, and loads transactional and customer data (ETL).
- Builds a **star schema database** to support analytical workloads.
- Performs **RFM segmentation** and **survival analysis** on customer data.
- Visualizes insights via a Streamlit dashboard.
- Deploys services using Docker Compose for full-stack orchestration.

---

## 🎯 Expected Outcomes

- Clear understanding of customer loyalty patterns.
- Identification of high-value vs. at-risk segments.
- Actionable insights through survival modeling and segment summaries.
- A fully reproducible and documented system accessible via:
  - Streamlit UI: [`localhost:8501`](http://localhost:8501)
  - FastAPI Docs: [`localhost:8008/docs`](http://localhost:8008/docs)
  - PgAdmin UI: [`localhost:5050`](http://localhost:5050)
  - GitHub Pages: [https://ds-223.github.io/Group-5/](https://ds-223.github.io/Group-5/)

---

## 📁 Documentation Map

- [`api.md`](api.md) – RESTful API endpoints for predictions and search
- [`app.md`](app.md) - StreamLit, Visualizations, and Email Campaign
- [`database.md`](database.md) – Database schema, ORM models, and raw table loading
- [`model.md`](model.md) – ML logic, RFM pipeline, and survival analysis

