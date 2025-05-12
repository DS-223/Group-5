"""
This script orchestrates the ETL (Extract, Transform, Load) process for loading data into a database.

Modules:
- `db.create_tables`: Contains the `create_tables` function to initialize database tables.
- `extract_load_raw`: Contains the `run` function to extract and load raw data.
- `transform`: Contains functions for transforming data:
    - `transform_qarter`: Transforms discount card data.
    - `transform_store`: Transforms store-specific data.
    - `transform_dimdate`: Transforms date-related data.
- `load`: Contains functions for loading data into specific tables:
    - `load_dimcustomer_table`: Loads transformed customer data into the DimCustomer table.
    - `load_dimdate_table`: Loads transformed date data into the DimDate table.
    - `load_facttransaction_table`: Loads transformed transaction data into the FactTransaction table.
- `loguru.logger`: Used for logging information during the ETL process.

Workflow:
1. Initializes database tables by calling `create_tables`.
2. Executes the ETL process to extract and load raw data using `run_etl`.
3. Transforms and loads the DimCustomer table:
    - Transforms discount card data using `transform_qarter`.
    - Loads the transformed data into the DimCustomer table using `load_dimcustomer_table`.
    - Cleans and maps `CustomerCardCode` to `ID` for further transformations.
4. Transforms and loads store-specific data:
    - Iterates through a list of raw table names, transforming each using `transform_store`.
    - Logs the transformation progress and stores the transformed data.
5. Transforms and loads the DimDate table:
    - Transforms date-related data using `transform_dimdate`.
    - Loads the transformed data into the DimDate table using `load_dimdate_table`.
6. Transforms and loads the FactTransaction table:
    - Loads the transformed store and date data into the FactTransaction table using `load_facttransaction_table`.

Execution:
- The script is executed as the main module.
"""

from db.create_tables import create_tables
from extract_load_raw import run as run_etl
from transform import transform_qarter, transform_store, transform_dimdate
from load import load_dimcustomer_table, load_dimdate_table, load_facttransaction_table
from loguru import logger

if __name__ == "__main__":

    create_tables()
    run_etl()

    # --- DimCustomer ---
    discount_cards = transform_qarter()
    load_dimcustomer_table(discount_cards)
    discount_cards['CustomerCardCode'] = (
        discount_cards['CustomerCardCode']
        .astype(str)
        .str.strip()
        .str.replace(r"\.0$", "", regex=True)
    )

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

    # --- Transform all stores ---
    for table in raw_tables:
        logger.info(f"Transforming table: {table}")
        df = transform_store(table, cardcode_to_key)
        transformed_data[table] = df
        logger.info(f"Finished transforming {table}. Rows: {len(df)}\n")
        print(df.head())

    logger.info("All store tables transformed successfully.")

    # --- DimDate ---
    dim_date_df = transform_dimdate(transformed_data)
    print(dim_date_df.head())
    load_dimdate_table(dim_date_df) 

    # --- FactTransaction ---
    load_facttransaction_table(transformed_data, dim_date_df)

    # Signal that ETL is done
    try:
        with open("/shared/etl_done", "w") as f:
            f.write("done")
        logger.info("✅ ETL completed. Signal file created at /shared/etl_done.")
    except Exception as e:
        logger.error(f"❌ Failed to write signal file: {e}")
