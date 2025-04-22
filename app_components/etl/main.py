from db.create_tables import create_tables
from etl_process import run as run_etl

if __name__ == "__main__":
    create_tables()
    run_etl()