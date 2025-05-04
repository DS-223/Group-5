from db.db_conf import Base, engine, SessionLocal 
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship


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

    def __repr__(self):
        return f"<DimDate(DateKey={self.DateKey}, Date={self.Date})>"


class DimCustomer(Base):
    __tablename__ = "DimCustomer"

    CustomerKey = Column(Integer, primary_key=True, autoincrement=True)
    CustomerCardCode = Column(String(20), unique = True)
    Name = Column(String(150))
    RegistrationDate = Column(DateTime)
    BirthDate = Column(DateTime)
    Gender = Column(String(150))
    Phone = Column(String(150))
    Address = Column(String(150))

    def __repr__(self):
        return f"<DimCustomer(CustomerKey={self.CustomerKey}, Name={self.Name})>"


    
class DimStore(Base):
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
    __tablename__ = "FactTransaction"

    TransactionKey = Column(Integer, primary_key=True, autoincrement=True)
    TransactionDateKey = Column(Integer, ForeignKey("DimDate.DateKey"))
    CustomerKey = Column(Integer, ForeignKey("DimCustomer.CustomerKey"))
    StoreKey = Column(Integer, ForeignKey("DimStore.StoreID"), nullable=False)
    Amount = Column(Float, nullable=False)

    def __repr__(self):
        return f"<FactTransaction(TransactionKey={self.TransactionKey}, Amount={self.Amount})>"