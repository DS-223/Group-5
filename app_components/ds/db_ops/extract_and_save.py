import pandas as pd
from sqlalchemy import create_engine
import os

# Expect DATABASE_URL to come from environment (injected by Docker Compose)
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise EnvironmentError("DATABASE_URL not found in environment. Make sure Docker is injecting it.")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

def extract_transaction_data(csv_path: str = "customer_transactions.csv") -> None:
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
    print(f"✅ Data successfully saved to '{csv_path}'")
