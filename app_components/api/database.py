"""
Mock in-memory database module for the Loyalty API.
This file simulates a database by storing data in Python lists.
"""

from typing import List
from schema import Customer, Store, Card, Transaction

# Mock data stores (these act like tables in a real DB)
mock_customers: List[Customer] = []
mock_stores: List[Store] = []
mock_cards: List[Card] = []
mock_transactions: List[Transaction] = []


# --- database.py ---

# import os
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from dotenv import load_dotenv

# # Load environment variables from .env
# load_dotenv()

# # Read DATABASE_URL from .env file
# DATABASE_URL = os.getenv("DATABASE_URL")

# # Create SQLAlchemy engine
# engine = create_engine(DATABASE_URL)

# # Create session factory
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Dependency to get a session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
