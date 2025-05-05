from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
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
