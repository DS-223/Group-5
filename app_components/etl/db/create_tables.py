from db.db_conf import Base, engine
from loguru import logger
from db.star_schema import DimDate, DimCustomer, FactTransaction

def create_tables():
    Base.metadata.create_all(bind=engine)
    logger.info("All tables are created successfully.")