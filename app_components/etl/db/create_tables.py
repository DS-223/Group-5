from db.db_conf import Base, engine
from db.columns import DimDate, DimCustomer, DimCards, FactTransaction

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("All tables are created successfully.")