import pandas as pd
from sqlalchemy import create_engine
import os

# Expect DATABASE_URL to come from environment (injected by Docker Compose)
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise EnvironmentError("DATABASE_URL not found in environment. Make sure Docker is injecting it.")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

def extract_transaction_data(csv_path: str = "outputs/customer_transactions.csv") -> None:
    """
    Extracts transaction, customer, and date data from the database,
    joins them, and saves to a CSV for RFM analysis.
    """
    query = """
        SELECT 
            dc."CustomerCardCode" AS card_code,
            ft."Amount" AS transaction_amount,
            dd."Date" AS date,
            dc."BirthDate" AS date_of_birth,
            dc."Gender" AS gender
        FROM "FactTransaction" ft
        JOIN "DimCustomer" dc ON ft."CustomerKey" = dc."CustomerKey"
        JOIN "DimDate" dd ON ft."TransactionDateKey" = dd."DateKey"
        WHERE dc."CustomerCardCode" IS NOT NULL
    """
    try:
        df = pd.read_sql(query, engine)
    except Exception as e:
        raise RuntimeError(f"Failed to query database: {e}")

    if df.empty:
        raise ValueError("No data found in the query. Check the DB content.")

    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"Data successfully saved to '{csv_path}'")

def extract_survival_data(csv_path: str = "outputs/survival_data.csv") -> None:
    """
    Extracts survival analysis data from the database,
    calculates duration and event, and saves to a CSV file.
    """
    query = """
            WITH last_txn AS (
                SELECT 
                    dc."CustomerCardCode",
                    MAX(dd."Date") AS "LastTransactionDate"
                FROM "FactTransaction" ft
                JOIN "DimDate" dd ON ft."TransactionDateKey" = dd."DateKey"
                JOIN "DimCustomer" dc ON ft."CustomerKey" = dc."CustomerKey"
                GROUP BY dc."CustomerCardCode"
            ),
            survival_data AS (
                SELECT 
                    dc."CustomerCardCode",
                    dc."Name",
                    dc."RegistrationDate",
                    dc."BirthDate",
                    dc."Gender",
                    COALESCE(lt."LastTransactionDate", CURRENT_DATE) AS "LastTransactionDate",
                    GREATEST(DATE_PART('day', COALESCE(lt."LastTransactionDate", CURRENT_DATE) - dc."RegistrationDate"), 1) AS "duration",
                    CASE 
                        WHEN lt."LastTransactionDate" IS NULL THEN 1
                        WHEN CURRENT_DATE - lt."LastTransactionDate" > INTERVAL '180 days' THEN 1
                        ELSE 0
                    END AS "event",
                    FLOOR(DATE_PART('year', AGE(CURRENT_DATE, dc."BirthDate"))) AS "Age"
                FROM "DimCustomer" dc
                LEFT JOIN last_txn lt ON dc."CustomerCardCode" = lt."CustomerCardCode"
            )
            SELECT 
                "CustomerCardCode",
                "Name",
                "RegistrationDate",
                "BirthDate",
                "Gender",
                "Age",
                "duration",
                "event"
            FROM survival_data;
    """
    try:
        df = pd.read_sql(query, engine)
    except Exception as e:
        raise RuntimeError(f"Failed to query database: {e}")

    if df.empty:
        raise ValueError("No data found in the query. Check the DB content.")

    # Optional: encode Gender
    df['Gender'] = df['Gender'].map({'Male': 0, 'Female': 1})

    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"Survival data successfully saved to '{csv_path}'")
