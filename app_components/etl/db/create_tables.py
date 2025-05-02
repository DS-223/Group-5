from db.db_conf import Base, engine
from db.star_schema import DimDate, DimCustomer, FactTransaction

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("All tables are created successfully.")