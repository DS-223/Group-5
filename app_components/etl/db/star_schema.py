"""
This module defines the star schema for a database using SQLAlchemy ORM. 
It includes dimension tables and a fact table to support analytical queries.
Classes:
    DimDate:
        Attributes:
            DateKey (int): Primary key for the date dimension.
            Date (datetime): The actual date.
            Day (int): Day of the month.
            Month (int): Month of the year.
            Year (int): Year.
            Quarter (int): Quarter of the year.
            DayOfWeek (int): Day of the week as an integer.
            DayName (str): Name of the day (e.g., Monday).
            MonthName (str): Name of the month (e.g., January).
    DimCustomer:
        Attributes:
            CustomerKey (int): Primary key for the customer dimension.
            CustomerCardCode (str): Unique card code for the customer.
            Name (str): Name of the customer.
            RegistrationDate (datetime): Date when the customer registered.
            BirthDate (datetime): Customer's birth date.
            Gender (str): Gender of the customer.
            Phone (str): Phone number of the customer.
            Address (str): Address of the customer.
            Email (str): Email address of the customer.
    DimStore:
        Attributes:
            StoreID (int): Primary key for the store dimension.
            Name (str): Name of the store.
            Address (str): Address of the store.
            OpenYear (int): Year the store was opened.
            District (str): District where the store is located.
            SQM (int): Size of the store in square meters.
    FactTransaction:
        Attributes:
            TransactionKey (int): Primary key for the transaction fact table.
            TransactionDateKey (int): Foreign key referencing DimDate.DateKey.
            CustomerKey (int): Foreign key referencing DimCustomer.CustomerKey.
            StoreKey (int): Foreign key referencing DimStore.StoreID.
            Amount (float): Transaction amount.
"""

from db.db_conf import Base, engine, SessionLocal 
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class DimDate(Base):
    """
    Represents the DimDate table in the star schema for date-related dimensions.
    """

    __tablename__ = "DimDate"

    DateKey = Column(Integer, primary_key=True)
    Date = Column(DateTime, nullable=False)
    Day = Column(Integer, nullable=False)
    Month = Column(Integer, nullable=False)
    Year = Column(Integer, nullable=False)
    Quarter = Column(Integer, nullable=False)
    DayOfWeek = Column(Integer, nullable=False)
    DayName = Column(String(20), nullable=False)
    MonthName = Column(String(20), nullable=False)

    def __repr__(self):
        return f"<DimDate(DateKey={self.DateKey}, Date={self.Date})>"


class DimCustomer(Base):
    """
    Represents the DimCustomer table in the star schema, storing customer-related information.
    """

    __tablename__ = "DimCustomer"

    CustomerKey = Column(Integer, primary_key=True, autoincrement=True)
    CustomerCardCode = Column(String(20), unique = True)
    Name = Column(String(150))
    RegistrationDate = Column(DateTime)
    BirthDate = Column(DateTime)
    Gender = Column(String(150))
    Phone = Column(String(150))
    Address = Column(String(150))
    Email = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<DimCustomer(CustomerKey={self.CustomerKey}, Name={self.Name})>"


    
class DimStore(Base):
    """
    Represents the DimStore table in the star schema, storing information about stores.
    """

    __tablename__ = "DimStore"

    StoreID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(50), nullable=False)
    Address = Column(String(150), nullable=False)
    OpenYear = Column(Integer, nullable=False)
    District = Column(String(50), nullable=False)
    SQM = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<DimStore(StoreID={self.StoreID}, StoreName={self.Name})>"


class FactTransaction(Base):
    """
    Represents a fact table for transactions in a star schema database.
    """

    __tablename__ = "FactTransaction"

    TransactionKey = Column(Integer, primary_key=True, autoincrement=True)
    TransactionDateKey = Column(Integer, ForeignKey("DimDate.DateKey"))
    CustomerKey = Column(Integer, ForeignKey("DimCustomer.CustomerKey"))
    StoreKey = Column(Integer, ForeignKey("DimStore.StoreID"), nullable=False)
    Amount = Column(Float, nullable=False)

    def __repr__(self):
        return f"<FactTransaction(TransactionKey={self.TransactionKey}, Amount={self.Amount})>"