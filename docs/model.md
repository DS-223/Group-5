# Model Service

The `ds` service is responsible for performing advanced data analytics, including customer segmentation (via RFM analysis) and customer retention modeling (via survival analysis). It uses preprocessed transaction and customer data from the ETL pipeline and produces insights that are stored in the database and visualized in the frontend.

---

## 🧱 Architecture Overview

The model pipeline is built with:

- **SQLAlchemy & pandas**: For database interaction and data manipulation
- **scikit-learn**: For segmentation (KNN for unknown segment classification)
- **lifelines**: For survival analysis (Cox Proportional Hazards, Weibull AFT)
- **matplotlib**: For visualization
- **Python + Docker**: For containerized execution

---

## 📦 Input & Output Files

| File Path                     | Purpose                                 |
|------------------------------|-----------------------------------------|
| `outputs/customer_transactions.csv` | Extracted customer transaction data |
| `outputs/rfm_results.csv`    | Output of the RFM analysis              |
| `outputs/survival_data.csv`  | Prepared survival data                  |
| `outputs/*.png`              | Survival plots                          |
| `outputs/*.csv`              | Model summaries                         |

---

## 🔍 Components

### 1. **Data Extraction**

Module: `db_ops/extract_and_save.py`

- **`extract_transaction_data()`**: Joins FactTransaction, DimCustomer, and DimDate tables for RFM analysis.
- **`extract_survival_data()`**: Constructs a survival dataset with event and duration variables.

---

### 2. **RFM Analysis**

Module: `utils/rfm_analyzer.py`

- **`calculate_rfm()`**: Computes recency, frequency, and monetary values per customer.
- **`score_rfm()`**: Assigns 1–5 scores for each metric.
- **`segment_customers()`**: Classifies customers into segments such as:
  - Champions
  - Loyal Customers
  - Potential Loyalists
  - Big Spenders
  - Leaving Customers
- **`classify_unknown_segments()`**: Uses KNN classifier to assign a segment to previously unclassified customers.
- **`analyze_segments()`**: Produces aggregated statistics per segment.
- **`save_results()`**: Saves the detailed results to CSV.

---

### 3. **Survival Analysis**

Module: `utils/survival_analyzer.py`

- Uses `lifelines` to fit:
  - **Cox Proportional Hazards Model**
  - **Weibull AFT Model**
- Key Methods:
  - **`fit_cox_model()`**
  - **`fit_weibull_model()`**
  - **`print_model_summaries()`**
  - **`save_model_summaries()`**
  - **`plot_weibull_survival_function()`**
  - **`plot_custom_profiles()`**

---

## 🧪 Output Tables in Database

| Table                | Description                                     |
|---------------------|-------------------------------------------------|
| `RFMResults`         | RFM scores, segments, and demographic details   |
| `SurvivalData`       | Raw data used for survival modeling             |
| `CoxPHSummary`       | Summary of Cox PH model coefficients            |
| `WeibullAFTSummary`  | Summary of Weibull AFT model coefficients       |

---

## 🐳 Docker Execution

The `ds` service uses a `wait-for-etl.sh` script to ensure ETL has completed before running. It then launches:

```
python ds_main.py
```

Main entrypoint script: `ds_main.py`, which calls the full analytics pipeline sequentially.

---
