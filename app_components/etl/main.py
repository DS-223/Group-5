from db.create_tables import create_tables
from extract_load_raw import run as run_etl
from transform import transform_qarter, transform_store
from load import load_dimcustomer_table
"""
This script orchestrates the ETL (Extract, Transform, Load) process for the project.

Modules:
- `db.create_tables`: Contains the `create_tables` function to set up the database schema.
- `extract_load_raw`: Contains the `run` function to extract and load raw data.
- `transform`: Contains the `transform_qarter` function to process and transform data.
- `load`: Contains the `load_dimcustomer_table` function to load transformed data into the database.

Functions:
- `create_tables()`: Initializes the database by creating necessary tables.
- `run_etl()`: Executes the extraction and loading of raw data into the staging area.
- `transform_qarter()`: Transforms the raw data into a format suitable for loading into the database.
- `load_dimcustomer_table(discount_cards)`: Loads the transformed data into the `dimcustomer` table.

Execution:
- The script first initializes the database schema.
- It then extracts and loads raw data into the staging area.
- The raw data is transformed into a structured format.
- Finally, the transformed data is loaded into the `dimcustomer` table.

Usage:
Run this script as the main module to execute the entire ETL process.

Example:
    $ python main.py

Output:
- Prints "Process completed successfully." upon successful execution of the ETL process.
"""


if __name__ == "__main__":
    create_tables()
    run_etl()
    discount_cards = transform_qarter()
    load_dimcustomer_table(discount_cards)
    cardcode_to_key = dict(zip(discount_cards['CustomerCardCode'], discount_cards['ID']))

    raw_tables = [
        '1masiv', 
        '5rd_masiv', 
        '7rd_masiv', 
        'agoracenter', 
        'malatia', 
        'qanaqer', 
        'raykom', 
        'shengavit'
    ]

    transformed_data = {}

    for table in raw_tables:
        print(f"Transforming table: {table}")
        df = transform_store(table, cardcode_to_key) 
        transformed_data[table] = df
        print(f"Finished transforming {table}. Rows: {len(df)}\n")
        print(df.head())

    print("All store tables transformed successfully.")

