from db.db_conf import Base, engine
from loguru import logger
from db.star_schema import DimDate, DimCustomer, FactTransaction

def create_tables():
    """
    Creates all tables defined in the SQLAlchemy ORM models by binding them to the database engine.
    This function uses the SQLAlchemy `Base.metadata.create_all` method to create the tables
    in the database if they do not already exist. It also logs a message indicating the successful
    creation of the tables.
    Returns:
        None
    """

    Base.metadata.create_all(bind=engine)
    logger.info("All raw and empty tables are created successfully.")