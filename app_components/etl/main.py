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