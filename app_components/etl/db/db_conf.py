"""
This module provides the configuration and setup for database operations using SQLAlchemy.

Modules and Libraries:
- sqlalchemy: Core SQLAlchemy library for database interaction.
- sqlalchemy.ext.declarative: Provides the base class for declarative models.
- sqlalchemy.orm: Provides ORM features like session management.
- dotenv: Used to load environment variables from a .env file.
- os: Provides functions to interact with the operating system.

Key Components:
- `get_db`: A generator function that provides a database session and ensures proper cleanup after use.
- `load_dotenv`: Loads environment variables from a .env file to configure the database connection.
- `DATABASE_URL`: The database connection string fetched from environment variables.
- `engine`: The SQLAlchemy engine created using the database URL.
- `Base`: The declarative base class for defining ORM models.
- `SessionLocal`: A configured sessionmaker instance for managing database sessions.

Usage:
1. Define your ORM models by inheriting from `Base`.
2. Use `get_db` to obtain a database session in your application logic.
3. Ensure the `.env` file contains the `DATABASE_URL` variable for proper configuration.
"""

import sqlalchemy as sql
import sqlalchemy.ext.declarative as declarative
import sqlalchemy.orm as orm
from dotenv import load_dotenv
import os


def get_db():
    """
    Function to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Load environment variables from .env file
load_dotenv(".env")

# Get the database URL from environment variables
DATABASE_URL = os.environ.get("DATABASE_URL")

# Create the SQLAlchemy engine
engine = sql.create_engine(DATABASE_URL)

# Base class for declarative models
Base = declarative.declarative_base()

# SessionLocal for database operations
SessionLocal = orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)