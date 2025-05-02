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
    Name = Column(String(150))
    BirthDate = Column(DateTime)
    Gender = Column(String(150))
    Phone = Column(String(150))
    Address = Column(String(150))

    def __repr__(self):
        return f"<DimCustomer(CustomerKey={self.CustomerKey}, Name={self.Name})>"


class DimCards(Base):
    __tablename__ = "DimCards"

    CardKey = Column(Integer, primary_key=True, autoincrement=True)
    CardCode = Column(String(20))
    RegistrationDate = Column(DateTime)
    CardLeftoverAmount = Column(Float, nullable=False)

    def __repr__(self):
        return f"<DimCards(CardKey={self.CardKey}, CardCode={self.CardCode})>"


class FactTransaction(Base):
    __tablename__ = "FactTransaction"

    TransactionKey = Column(Integer, primary_key=True, autoincrement=True)
    TransactionDateKey = Column(Integer, ForeignKey("DimDate.DateKey"))
    CustomerKey = Column(Integer, ForeignKey("DimCustomer.CustomerKey"))
    CardKey = Column(Integer, ForeignKey("DimCards.CardKey"))
    Amount = Column(Float, nullable=False)
    StoreName = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<FactTransaction(TransactionKey={self.TransactionKey}, Amount={self.Amount})>"