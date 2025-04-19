from pydantic import BaseModel
from typing import Optional
from datetime import date

# Customer schemas
class CustomerBase(BaseModel):
    name: str
    gender: Optional[str]
    birth_date: Optional[date]
    location: Optional[str]

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    customer_id: int


# Store schemas
class StoreBase(BaseModel):
    store_name: str
    location: str

class StoreCreate(StoreBase):
    pass

class Store(StoreBase):
    store_id: int


# Card schemas
class CardBase(BaseModel):
    customer_id: int
    card_code: str
    registration_date: date

class CardCreate(CardBase):
    pass

class Card(CardBase):
    card_id: int


# Transaction schemas
class TransactionBase(BaseModel):
    customer_id: int
    card_id: int
    store_id: int
    transaction_date: date
    amount: float

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    transaction_id: int
