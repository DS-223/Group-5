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

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date

# schema.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date

class CustomerOut(BaseModel):
    CustomerKey: int
    CustomerCardCode: Optional[str]
    Name: Optional[str]
    RegistrationDate: Optional[datetime]
    BirthDate: Optional[datetime]
    Gender: Optional[str]
    Phone: Optional[str]
    Address: Optional[str]

    class Config:
        from_attributes = True


class CustomerCreate(BaseModel):
    CustomerKey: int
    CustomerCardCode: Optional[str] = Field(None, alias="CustomerCardCode")
    Name: str = Field(..., alias="Name")
    RegistrationDate: Optional[datetime] = Field(None, alias="RegistrationDate")
    BirthDate: Optional[date] = Field(None, alias="BirthDate")
    Gender: Optional[str] = Field(None, alias="Gender")
    Phone: Optional[str] = Field(None, alias="Phone")
    Address: Optional[str] = Field(None, alias="Address")

    class Config:
        populate_by_name = True
