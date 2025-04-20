import pandas as pd
from loguru import logger
from db.db_conf import engine  # SQLAlchemy engine from the db.py
import glob
from os import path
import zipfile
import re
from sqlalchemy import Inspector

inspector = Inspector.from_engine(engine)


def has_shared_strings(file_path: str) -> bool:
    """Check if the Excel file has a valid sharedStrings.xml (i.e., not malformed)."""
    try:
        with zipfile.ZipFile(file_path) as z:
            return 'xl/sharedStrings.xml' in z.namelist()
    except Exception:
        return False

def clean_table_name(name: str) -> str:
    """Sanitize the table name for use in Postgres (no dashes or spaces)."""
    return re.sub(r'\W+', '_', name).lower()  # e.g., "1-Masiv" → "1_masiv"

def load_xlsx_to_table(table_name: str, xlsx_path: str) -> bool:
    """
    Load data from an XLSX file into a database table.
    Returns True if successful, False if failed.
    """
    try:
        df = pd.read_excel(xlsx_path, engine='openpyxl')
        if df.empty:
            logger.warning(f"Table {table_name} is empty. Skipping.")
            return False
        # Check if the table already exists
        if inspector.has_table(table_name):
            logger.warning(f"Table {table_name} already exists. Skipping.")
            return False
        df.to_sql(table_name, con=engine, index=False, if_exists="replace")
        logger.info(f"Loaded {df.shape[0]} rows into table: {table_name}")
        return True
    except Exception as e:
        logger.error(f"Failed to load table {table_name}. Error: {e}")
        return False

if __name__ == "__main__":
    folder_path = "data/*.xlsx"
    files = glob.glob(folder_path)
    logger.info(f"Found {len(files)} XLSX files.")

    success_count = 0
    for file_path in files:
        table_raw = path.splitext(path.basename(file_path))[0]  # e.g. '1-Masiv.xlsx' → '1-Masiv'
        table_name = clean_table_name(table_raw)

        if not has_shared_strings(file_path):
            logger.warning(f"Skipping invalid XLSX file: {file_path} (missing sharedStrings.xml)")
            continue

        logger.info(f"Loading table: {table_name}")
        if load_xlsx_to_table(table_name, file_path):
            success_count += 1

    logger.info(f"All done. {success_count}/{len(files)} tables loaded successfully.")