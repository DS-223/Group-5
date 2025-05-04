import pandas as pd
from loguru import logger
import glob
from os import path
import zipfile
import re
from sqlalchemy import inspect
from db.db_conf import engine
from db.star_schema import DimCustomer, DimDate, FactTransaction

def has_shared_strings(file_path: str) -> bool:
    """
    Checks if an Excel file contains a sharedStrings.xml file.

    This function determines whether the specified Excel file (in .xlsx format)
    includes a sharedStrings.xml file, which is typically used to store shared
    strings in the workbook.

    Args:
        file_path (str): The file path to the Excel file to be checked.

    Returns:
        bool: True if the sharedStrings.xml file exists in the Excel file, 
              False otherwise or if an error occurs while accessing the file.

    Raises:
        None: Any exceptions encountered during file access are caught and 
              result in a return value of False.
    """
    try:
        with zipfile.ZipFile(file_path) as z:
            return 'xl/sharedStrings.xml' in z.namelist()
    except Exception:
        return False

def clean_table_name(name: str) -> str:
    return re.sub(r'\W+', '_', name).lower()

def load_xlsx_to_table(table_name: str, xlsx_path: str) -> bool:
    inspector = inspect(engine)
    try:
        df = pd.read_excel(xlsx_path, engine='openpyxl')
        if df.empty:
            logger.warning(f"Table {table_name} is empty. Skipping.")
            return False
        if inspector.has_table(table_name):
            logger.warning(f"Table {table_name} already exists. Skipping.")
            return False
        df.to_sql(table_name, con=engine, index=False, if_exists="replace")
        logger.info(f"Loaded {df.shape[0]} rows into table: {table_name}")
        return True
    except Exception as e:
        logger.error(f"Failed to load table {table_name}. Error: {e}")
        return False

def load_store_dim_table():
    store_file = "data/Stores.xlsx"
    df = pd.read_excel(store_file)

    df = df.rename(columns={
        'StoreID': 'StoreID',
        'Name': 'Name',
        'Address': 'Address',
        'OpenDate': 'OpenYear',
        'District': 'District',
        'SQM': 'SQM'
    })

    from sqlalchemy import inspect
    inspector = inspect(engine)
    if inspector.has_table('DimStore'):
        logger.warning("DimStore already exists. Skipping reload.")
    else:
        df.to_sql('DimStore', con=engine, index=False, if_exists="append")
        logger.info(f"Loaded DimStore table with {len(df)} rows.")


def run():
    folder_path = "data/*.xlsx"
    files = glob.glob(folder_path)
    logger.info(f"Found {len(files)} XLSX files.")

    success_count = 0
    logger.info(f"Loading Dimstore from Stores.xlsx")
    load_store_dim_table()
    success_count += 1

    for file_path in files:
        table_raw = path.splitext(path.basename(file_path))[0]
        table_name = clean_table_name(table_raw)

        if not has_shared_strings(file_path):
            logger.warning(f"Skipping invalid XLSX file: {file_path} (missing sharedStrings.xml)")
            continue

        elif table_name == "stores":
            continue

        logger.info(f"Loading table: {table_name}")
        if load_xlsx_to_table(table_name, file_path):
            success_count += 1


    logger.info(f"All done. {success_count}/{len(files)} tables loaded successfully.")