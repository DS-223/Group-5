'''
This file defines the SQLAlchemy ORM models for the database schema used in the Customer Loyalty and Analytics system. 
Each class corresponds to a database table and specifies the structure, relationships, and primary keys.

Key Components:

DimDate: A dimension table for calendar-related metadata (date, day, month, etc.).
DimCustomer: Stores customer demographics and contact details.
DimStore: Contains information about physical store locations.
FactTransaction: A fact table that logs all customer transactions, linked to date, customer, and store.
RFMResults: Holds precomputed Recency-Frequency-Monetary (RFM) scores and segmentation data for customer profiling.
SurvivalData: Stores processed records used for survival analysis, particularly tracking customer lifecycle duration and churn events.
These models support analytical queries, API responses, and dashboard visualizations used throughout the application.
'''


from sqlalchemy import Column, Integer, String, Float, DateTime, Date, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from database import Base

class DimDate(Base):
    __tablename__ = "DimDate"

    DateKey = Column(Integer, primary_key=True, autoincrement=True)
    Date = Column(DateTime, nullable=False)
    Day = Column(Integer, nullable=False)
    Month = Column(Integer, nullable=False)
    Year = Column(Integer, nullable=False)
    Quarter = Column(Integer, nullable=False)
    DayOfWeek = Column(Integer, nullable=False)
    DayName = Column(String(20), nullable=False)
    MonthName = Column(String(20), nullable=False)

    transactions = relationship("FactTransaction", back_populates="date")


class DimCustomer(Base):
    __tablename__ = "DimCustomer"
    __table_args__ = {'extend_existing': True}

    CustomerKey = Column(Integer, primary_key=True, autoincrement=True)
    CustomerCardCode = Column(String(20), unique=True)
    Name = Column(String(150))
    RegistrationDate = Column(DateTime)
    BirthDate = Column(DateTime)
    Gender = Column(String(150))
    Phone = Column(String(150))
    Address = Column(String(150))
    Email = Column(String(255), nullable=True)          
    
    transactions = relationship("FactTransaction", back_populates="customer")



class DimStore(Base):
    __tablename__ = "DimStore"

    StoreID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(50), nullable=False)
    Address = Column(String(150), nullable=False)
    OpenYear = Column(Integer, nullable=False)
    District = Column(String(50), nullable=False)
    SQM = Column(Integer, nullable=False)

    transactions = relationship("FactTransaction", back_populates="store")


class FactTransaction(Base):
    __tablename__ = "FactTransaction"

    TransactionKey = Column(Integer, primary_key=True, autoincrement=True)
    TransactionDateKey = Column(Integer, ForeignKey("DimDate.DateKey"))
    CustomerKey = Column(Integer, ForeignKey("DimCustomer.CustomerKey"))
    StoreKey = Column(Integer, ForeignKey("DimStore.StoreID"))
    Amount = Column(Float, nullable=False)

    date = relationship("DimDate", back_populates="transactions")
    customer = relationship("DimCustomer", back_populates="transactions")
    store = relationship("DimStore", back_populates="transactions")


class RFMResults(Base):
    __tablename__ = "RFMResults"

    card_code = Column(String(50), primary_key=True)
    recency = Column(Integer)
    frequency = Column(Integer)
    monetary = Column(Float)
    r_score = Column(Integer)
    f_score = Column(Integer)
    m_score = Column(Integer)
    rfm_score = Column(String(3))
    rfm_sum = Column(Integer)
    segment = Column(String(50))
    gender = Column(String(10))
    date_of_birth = Column(Date)
    age = Column(Integer)


class SurvivalData(Base):
    __tablename__ = "SurvivalData"
    
    CustomerCardCode = Column(BigInteger, primary_key=True)
    Name = Column(String)
    RegistrationDate = Column(String)
    BirthDate = Column(String)
    Gender = Column(Float)
    Age = Column(Float)
    duration = Column(Float)
    event = Column(BigInteger)