from db.create_tables import create_tables
from extract_load_raw import run as run_etl
from transform import transform_qarter as transform

if __name__ == "__main__":
    create_tables()
    run_etl()
    transform()
    print("ETL process completed successfully.")
