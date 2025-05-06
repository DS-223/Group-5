# extract_and_save.py

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Load env vars and create engine
load_dotenv(".env")
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def extract_transaction_data(csv_path: str = "customer_transactions.csv") -> None:
    query = """
        SELECT 
            dc.CustomerCardCode AS card_code,
            ft.Amount AS transaction_amount,
            dd.Date AS date,
            dc.BirthDate AS date_of_birth,
            dc.Gender AS gender
        FROM FactTransaction ft
        JOIN DimCustomer dc ON ft.CustomerKey = dc.CustomerKey
        JOIN DimDate dd ON ft.TransactionDateKey = dd.DateKey
        WHERE dc.CustomerCardCode IS NOT NULL
    """
    df = pd.read_sql(query, engine)
    df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    print(f"Data successfully saved to {csv_path}")
