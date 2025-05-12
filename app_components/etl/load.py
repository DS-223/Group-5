"""
This module handles the ETL (Extract, Transform, Load) process for loading data into a PostgreSQL database.
Functions:
    load_dimcustomer_table(discount_cards: pd.DataFrame):
        Loads customer data into the DimCustomer table in the database.
        Parameters:
            discount_cards (pd.DataFrame): A DataFrame containing customer data.
    load_dimdate_table(dim_date_df: pd.DataFrame):
        Loads date-related data into the DimDate table in the database.
        Parameters:
            dim_date_df (pd.DataFrame): A DataFrame containing date dimension data.
    load_facttransaction_table(transformed_data: dict, dim_date_df: pd.DataFrame):
        Loads transaction data into the FactTransaction table in the database.
        Parameters:
            transformed_data (dict): A dictionary containing transformed transaction data.
            dim_date_df (pd.DataFrame): A DataFrame containing date dimension data.
Classes:
    TransactionDatabase:
        A helper class for interacting with the database, imported from CRUD_func.
Dependencies:
    - CRUD_func.TransactionDatabase: Handles database operations.
    - dotenv.load_dotenv: Loads environment variables from a .env file.
    - transform.transform_qarter: A transformation function for quarter data.
    - pandas (pd): For handling data in DataFrame format.
    - psycopg2: For connecting to the PostgreSQL database.
    - loguru.logger: For logging information and errors.
Environment Variables:
    - DB_HOST: The database host.
    - DB_NAME: The database name.
    - DB_USER: The database user.
    - DB_PASSWORD: The database password.
Database Tables:
    - DimCustomer: Stores customer-related data.
    - DimDate: Stores date-related data.
    - FactTransaction: Stores transaction-related data.
    - DimStore: Stores store-related data (used for mapping store names to IDs).
Logging:
    - Logs database connection attempts and results.
    - Logs the number of rows loaded into each table.
"""

from CRUD_func import TransactionDatabase
from dotenv import load_dotenv
from transform import transform_qarter
import os
import pandas as pd
import time
import psycopg2
from loguru import logger

load_dotenv()

for attempt in range(5):
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        conn.close()
        logger.info("Database connection successful.")
        break
    except psycopg2.OperationalError as e:
        logger.warning(f"Attempt {attempt + 1}: Database connection failed. Retrying in 3 seconds...")
        time.sleep(3)
else:
    raise Exception("Failed to connect to the database after 5 attempts.")

        
db = TransactionDatabase(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)


def load_dimcustomer_table(discount_cards: pd.DataFrame):
    """
    Loads data into the DimCustomer table from a given DataFrame.
    This function iterates over the rows of the provided DataFrame and inserts
    each row into the DimCustomer table in the database. It also logs the total
    number of rows in the table after the operation.
    Args:
        discount_cards (pd.DataFrame): A pandas DataFrame containing customer data.
            Expected columns:
                - 'ID' (int): Unique identifier for the customer.
                - 'CustomerCardCode' (str): Code of the customer's card.
                - 'Name' (str): Name of the customer.
                - 'RegistrationDate' (datetime or None): Date of registration.
                - 'BirthDate' (datetime or None): Birth date of the customer.
                - 'Gender' (str): Gender of the customer.
                - 'PhoneNumber' (str): Phone number of the customer.
                - 'CustomerAddress' (str): Address of the customer.
                - 'Email' (str): Email address of the customer.
    Returns:
        None
    Logs:
        Logs the total number of rows in the DimCustomer table after the data
        has been loaded.
    """

    for _, row in discount_cards.iterrows():
        db.insert_customer(
            customer_key=int(row['ID']),
            card_code=row['CustomerCardCode'],
            name=row['Name'],
            RegistrationDate=row['RegistrationDate'].strftime('%Y-%m-%d') if pd.notnull(row['RegistrationDate']) else None,
            birth_date=row['BirthDate'].strftime('%Y-%m-%d') if pd.notnull(row['BirthDate']) else None,
            gender=row['Gender'],
            phone=row['PhoneNumber'],
            address=row['CustomerAddress'],
            email=row['Email']
        )
    db.cursor.execute('SELECT COUNT(*) FROM "DimCustomer";')
    row_count = db.cursor.fetchone()[0]
    logger.info(f"Finished loading DimCustomer table. Length: {row_count}")


def load_dimdate_table(dim_date_df: pd.DataFrame):
    """
    Loads data into the DimDate table in the database.
    This function takes a pandas DataFrame containing date dimension data,
    prepares the data for insertion, and inserts it into the "DimDate" table.
    If a record with the same "DateKey" already exists, it will be ignored
    due to the ON CONFLICT DO NOTHING clause.
    Args:
        dim_date_df (pd.DataFrame): A DataFrame containing the following columns:
            - 'DateKey' (int): The unique key for the date.
            - 'Date' (str): The date in string format.
            - 'Day' (int): The day of the
    """
    records = []
    for _, row in dim_date_df.iterrows():
        records.append((
            int(row['DateKey']),
            row['Date'],
            int(row['Day']),
            int(row['Month']),
            int(row['Year']),
            int(row['Quarter']),
            int(row['DayOfWeek']),
            row['DayName'],
            row['MonthName']
        ))

    # Prepare the insert query with ON CONFLICT DO NOTHING
    insert_query = """
        INSERT INTO "DimDate" 
        ("DateKey", "Date", "Day", "Month", "Year", "Quarter", "DayOfWeek", "DayName", "MonthName")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT ("DateKey") DO NOTHING
    """

    # Execute all at once
    db.cursor.executemany(insert_query, records)
    db.conn.commit()

    logger.info(f"Finished loading DimDate table. Rows attempted: {len(records)}")

def load_facttransaction_table(transformed_data, dim_date_df):
    """
    Loads transaction data into the FactTransaction table in the database.
    This function processes transformed transaction data and maps it to the 
    appropriate dimensions (Date, Customer, Store) before inserting it into 
    the FactTransaction table. It ensures that only valid transactions are 
    loaded by performing checks on date, customer, and store mappings.
    Args:
        transformed_data (dict): A dictionary where keys are table names and 
            values are pandas DataFrames containing the transformed transaction 
            data for each table.
        dim_date_df (pandas.DataFrame): A DataFrame containing the Date dimension 
            data, including 'Date' and 'DateKey' columns.
    Raises:
        Exception: If there are issues with date mapping during processing.
    Notes:
        - Transactions with invalid dates, unknown customers, or unmapped stores 
          are skipped.
        - The function logs the progress of loading transactions for each table 
          and the final count of rows in the FactTransaction table.
    Example:
        transformed_data = {
            "Table1": pd.DataFrame([...]),
            "Table2": pd.DataFrame([...])
        }
        dim_date_df = pd.DataFrame([...])
        load_facttransaction_table(transformed_data, dim_date_df)
    """

    store_df = pd.read_sql('SELECT * FROM "DimStore";', db.conn)

    date_to_datekey = dict(zip(dim_date_df['Date'].dt.date, dim_date_df['DateKey']))
    store_name_to_id = dict(zip(store_df['Name'].str.strip(), store_df['StoreID']))
    
    transaction_id = 1

    for table_name, df in transformed_data.items():
        logger.info(f"Loading transactions for {table_name}...")

        for idx, row in df.iterrows():
            transaction_key = transaction_id

            # --- DATE ---
            try:
                date_key = date_to_datekey.get(row['Date'].date())
            except Exception:
                continue  # Skip invalid dates

            if pd.isna(date_key):
                continue

            # --- CUSTOMER ---
            customer_key = int(row['CustomerKey'])
            if customer_key == 0:
                continue  # Skip unknown customers

            # --- STORE ---
            store_key = row['StoreID']
            if pd.isna(store_key):
                continue  # Skip if store not mapped

            amount = float(row['Money Spent'])

            db.add_transaction(
                transaction_key=transaction_key,
                transaction_date_key=int(date_key),
                customer_key=customer_key,
                store_key=int(store_key),
                amount=amount
            )

            transaction_id += 1

    db.cursor.execute('SELECT COUNT(*) FROM "FactTransaction";')
    row_count = db.cursor.fetchone()[0]
    logger.info(f"Finished loading FactTransaction table. Length: {row_count}")