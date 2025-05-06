import pandas as pd
from sqlalchemy import create_engine
import os

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise EnvironmentError("DATABASE_URL not found in environment. Make sure Docker is injecting it.")

engine = create_engine(DATABASE_URL)

def save_csv_to_db(csv_path: str, table_name: str = "RFMResults") -> None:
    """
    Loads a CSV and writes it to a PostgreSQL table.
    If the table already exists, it will be replaced.
    """
    try:
        df = pd.read_csv(csv_path, encoding='utf-8-sig')
        df.to_sql(table_name, engine, index=False, if_exists='replace')
        print(f"✅ CSV saved to DB table '{table_name}' successfully.")
    except Exception as e:
        raise RuntimeError(f"Failed to write to database: {e}")
