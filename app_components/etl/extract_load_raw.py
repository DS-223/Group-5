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
    """
    Convert a string into a lowercase, underscore-separated table name by replacing non-alphanumeric characters.
    """

    return re.sub(r'\W+', '_', name).lower()

def load_xlsx_to_table(table_name: str, xlsx_path: str) -> bool:
    """
    Loads data from an Excel (.xlsx) file into a database table.
    This function reads data from the specified Excel file and attempts to load it
    into a database table with the given name. If the table already exists or the
    Excel file is empty, the operation is skipped.
    Args:
        table_name (str): The name of the database table to load data into.
        xlsx_path (str): The file path to the Excel (.xlsx) file.
    Returns:
        bool: True if the data was successfully loaded into the table, False otherwise.
    Raises:
        Exception: Logs an error message if any exception occurs during the process.
    Notes:
        - The function uses the `openpyxl` engine to read the Excel file.
        - If the table already exists in the database, the function logs a warning
          and skips the operation.
        - If the Excel file is empty, the function logs a warning and skips the operation.
        - The data is written to the database using the `replace` mode, which overwrites
          any existing data in the table.
    """

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
    """
    Loads data from an Excel file into a database table named 'DimStore'.
    This function reads store data from an Excel file, processes it, and loads it into the 
    'DimStore' table in the database. If the table already exists and contains data, the 
    function skips reloading the data. If the table exists but is empty, it appends the data. 
    If the table does not exist, it creates the table and loads the data.
    Steps:
    1. Reads the Excel file 'data/Stores.xlsx' into a pandas DataFrame.
    2. Renames the columns of the DataFrame to match the database schema.
    3. Checks if the 'DimStore' table exists in the database using SQLAlchemy's inspector.
    4. If the table exists and contains data, logs a warning and skips loading.
    5. If the table exists but is empty, appends the data and logs the operation.
    6. If the table does not exist, creates the table and loads the data.
    Logging:
    - Logs a warning if the table already exists and contains data.
    - Logs an info message when data is successfully loaded.
    Dependencies:
    - pandas (pd)
    - sqlalchemy (inspect, engine)
    - logger (for logging messages)
    Raises:
    - Any exceptions raised by pandas or SQLAlchemy during file reading or database operations.
    Note:
    Ensure that the database engine (`engine`) and logger (`logger`) are properly configured 
    before calling this function.
    """

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
        row_count = pd.read_sql('SELECT COUNT(*) FROM "DimStore";', engine).iloc[0, 0]
        if row_count > 0:
            logger.warning("DimStore already exists and has data. Skipping reload.")
        else:
            df.to_sql('DimStore', con=engine, index=False, if_exists="append")
            logger.info(f"DimStore existed but was empty. Loaded {len(df)} rows.")
    else:
        df.to_sql('DimStore', con=engine, index=False, if_exists="replace")
        logger.info(f"DimStore did not exist. Loaded {len(df)} rows.")
        
def run():
    """
    Executes the ETL process to load data from XLSX files into database tables.
    This function performs the following steps:
    1. Searches for all XLSX files in the "data" folder.
    2. Logs the number of files found.
    3. Loads the Dimstore table from a specific "Stores.xlsx" file.
    4. Iterates through the found XLSX files, cleans their names, and determines
       whether they are valid for processing.
    5. Skips invalid files or files with specific names (e.g., "stores").
    6. Loads valid XLSX files into their respective database tables.
    7. Logs the number of successfully loaded tables.
    Logging and warnings are provided for invalid files or skipped files.
    Note:
        - The function assumes the presence of helper functions such as:
          `load_store_dim_table`, `clean_table_name`, `has_shared_strings`,
          and `load_xlsx_to_table`.
        - The logger object is used for logging messages.
    Raises:
        Any exceptions raised by the helper functions are not handled here
        and will propagate to the caller.
    """

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