# from pydantic import BaseModel
# from typing import Optional
# from datetime import date

# # Customer schemas
# class CustomerBase(BaseModel):
#     name: str
#     gender: Optional[str]
#     birth_date: Optional[date]
#     location: Optional[str]

# class CustomerCreate(CustomerBase):
#     pass

# class Customer(CustomerBase):
#     customer_id: int


# # Store schemas
# class StoreBase(BaseModel):
#     store_name: str
#     location: str

# class StoreCreate(StoreBase):
#     pass

# class Store(StoreBase):
#     store_id: int


# # Card schemas
# class CardBase(BaseModel):
#     customer_id: int
#     card_code: str
#     registration_date: date

# class CardCreate(CardBase):
#     pass

# class Card(CardBase):
#     card_id: int


# # Transaction schemas
# class TransactionBase(BaseModel):
#     customer_id: int
#     card_id: int
#     store_id: int
#     transaction_date: date
#     amount: float

# class TransactionCreate(TransactionBase):
#     pass

# class Transaction(TransactionBase):
#     transaction_id: int


# --- schema.py ---

from pydantic import BaseModel
from typing import Optional
from datetime import date

# --- Customer Models ---

class CustomerBase(BaseModel):
    Name: str
    BirthDate: Optional[date] = None
    Gender: Optional[str] = None
    Phone: Optional[str] = None
    Address: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class Customer(CustomerBase):
    CustomerKey: int

    class Config:
        orm_mode = True

# --- Transaction Models ---

class TransactionBase(BaseModel):
    TransactionDateKey: int
    CustomerKey: int
    CardKey: Optional[int] = None
    Amount: float
    StoreName: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    TransactionKey: int

    class Config:
        orm_mode = True

# --- Top Customers Model ---

# class TopCustomer(BaseModel):
#     Name: str
#     TotalAmount: float
