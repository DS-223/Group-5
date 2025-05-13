# Database Documentation

This service manages the **PostgreSQL database** for the ETL pipeline and analytics platform. It uses SQLAlchemy ORM to define and interact with the star schema that powers the reporting and machine learning workflows.

---

## 📐 Star Schema Design

The schema follows a classic star structure with the following tables:

- `DimDate`: Stores date-related attributes.
- `DimCustomer`: Contains customer metadata (e.g., name, birthdate, gender, email).
- `DimStore`: Information about store branches including location and size.
- `FactTransaction`: The central fact table that records every customer transaction.

Each `FactTransaction` entry references:

- a customer (`CustomerKey` from `DimCustomer`),
- a store (`StoreKey` from `DimStore`),
- and a transaction date (`DateKey` from `DimDate`).

---

## ⚙️ ORM Models

The ORM classes in `db/star_schema.py` define the schema as Python classes.

- All models inherit from a common `Base` defined in `db_conf.py`.
- The `create_tables()` function initializes the schema in the target PostgreSQL database.

```python
Base.metadata.create_all(bind=engine)
```

---

## 🧠 Business Logic Layer

The class `TransactionDatabase` in `CRUD_func.py` wraps direct database interactions such as:

- Inserting customers, dates, and transactions
- Updating or deleting records
- Fetching data for reporting or debugging

---

## 🔁 ETL Integration

The ETL pipeline loads data into the star schema in multiple phases:

1. **Extract & Load Raw XLSX**:
   - Excel files are ingested into raw tables using Pandas and `to_sql()`.
   - Raw file names are cleaned into table names.

2. **Transform**:
   - Data is cleaned and standardized (e.g., phone/email formatting, gender unification).
   - Invalid records are dropped.

3. **Load to Star Schema**:
   - Dimension tables are filled using `load_dimcustomer_table()` and `load_dimdate_table()`.
   - Transaction data is processed and inserted using `load_facttransaction_table()`.

---

## 🧪 Data Validations

- Dates must follow `YYYY-MM-DD` and be logically consistent.
- CustomerCardCodes are filtered to 13-character strings.
- Phone and address fields are validated for structure and length.
- Store names are mapped to known clean values using `STORE_NAME_MAPPING`.

---

## 🛠️ Dependencies

The ETL database logic requires:

- `SQLAlchemy`
- `psycopg2-binary`
- `pandas`
- `loguru`
- `dotenv`

---

## 🔐 Configuration

Database credentials are loaded from a `.env` file:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/maindb
DB_USER=postgres
DB_HOST=postgres-db
DB_PASSWORD=postgres
DB_NAME=maindb
PGADMIN_EMAIL=admin@admin.com 
PGADMIN_PASSWORD=admin
```

---

## 📂 Related Files

| File | Description |
|------|-------------|
| `/db` | SQLAlchemy Setup: Engine, Base, Session, General Database Configuration|
| `CRUD_func.py` | Class wrapping SQL queries |
| `extract_load_raw.py` | Extracts all XLSX files, does validation and dumps them in the DB |
| `transform.py` | Takes raw tables and does transformation, cleaning and validation |
| `load.py` | Takes clean tables and sequentially loads into DB, row-by-row (FactTransaction, DimCustomer) or by batch |
| `main.py` | Entry point that orchestrates ETL and signals completion |
