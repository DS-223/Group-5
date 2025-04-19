from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Customers
class CustomerDB(Base):
    __tablename__ = "customers"
    customer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    gender = Column(String)
    birth_date = Column(Date)
    location = Column(String)

    transactions = relationship("TransactionDB", back_populates="customer")
    bonus_cards = relationship("CardDB", back_populates="customer")

# Transactions
class TransactionDB(Base):
    __tablename__ = "transactions"
    transaction_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    card_id = Column(Integer, ForeignKey("cards.card_id"))
    store_id = Column(Integer, ForeignKey("stores.store_id"))
    transaction_date = Column(Date)
    amount = Column(Float)

    customer = relationship("CustomerDB", back_populates="transactions")

# Stores
class StoreDB(Base):
    __tablename__ = "stores"
    store_id = Column(Integer, primary_key=True, index=True)
    store_name = Column(String)
    location = Column(String)

# Bonus Cards
class CardDB(Base):
    __tablename__ = "cards"
    card_id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    card_code = Column(String)
    registration_date = Column(Date)

    customer = relationship("CustomerDB", back_populates="bonus_cards")
