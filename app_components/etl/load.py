"""
This script is responsible for loading data into the database as part of the ETL process.
Modules:
    - CRUD_func: Contains the `TransactionDatabase` class for database operations.
    - dotenv: Used to load environment variables from a `.env` file.
    - transform: Contains the `transform_qarter` function for data transformation.
    - os: Provides functions to interact with the operating system.
    - pandas: Used for data manipulation and analysis.
    - time: Provides time-related functions.
    - psycopg2: PostgreSQL database adapter for Python.
Environment Variables:
    - DB_HOST: The hostname of the database server.
    - DB_NAME: The name of the database.
    - DB_USER: The username for database authentication.
    - DB_PASSWORD: The password for database authentication.
Functions:
    - load_dimcustomer_table(discount_cards: pd.DataFrame):
        Loads customer data into the `DimCustomer` table in the database.
        Iterates through a DataFrame of customer data and inserts each record into the database.
        Parameters:
            discount_cards (pd.DataFrame): A DataFrame containing customer data with the following columns:
                - ID: Unique identifier for the customer.
                - Name: Name of the customer.
                - BirthDate: Birth date of the customer (optional).
                - Gender: Gender of the customer.
                - PhoneNumber: Phone number of the customer.
                - CustomerAddress: Address of the customer.
        Prints:
            - A message indicating the completion of the loading process.
            - The head of the `DimCustomer` table for verification.
Database Connection:
    - Attempts to establish a connection to the database up to 5 times.
    - If the connection fails after 5 attempts, raises an exception.
    - Prints a success message upon successful connection.
Classes:
    - TransactionDatabase: Used to interact with the database, including inserting records and peeking at table data.
"""
from CRUD_func import TransactionDatabase
from dotenv import load_dotenv
from transform import transform_qarter
import os
import pandas as pd
import time
import psycopg2

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
        print("Database connection successful.")
        break
    except psycopg2.OperationalError as e:
        print(f"Attempt {attempt + 1}: Database connection failed. Retrying in 3 seconds...")
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
    for _, row in discount_cards.iterrows():
        db.insert_customer(
            customer_key=int(row['ID']),
            card_code=row['CustomerCardCode'],
            name=row['Name'],
            RegistrationDate=row['RegistrationDate'].strftime('%Y-%m-%d') if pd.notnull(row['RegistrationDate']) else None,
            birth_date=row['BirthDate'].strftime('%Y-%m-%d') if pd.notnull(row['BirthDate']) else None,
            gender=row['Gender'],
            phone=row['PhoneNumber'],
            address=row['CustomerAddress']
        )
    db.cursor.execute('SELECT COUNT(*) FROM "DimCustomer";')
    row_count = db.cursor.fetchone()[0]
    print(f"Finished loading DimCustomer table. Length: {row_count}")