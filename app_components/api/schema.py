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


class MonthlyRevenue(BaseModel):
    month: str  # Example: "Mar 2024"
    revenue: float

class CustomerTransactionOut(BaseModel):
    transaction_id: int
    date: datetime
    store: str
    amount: float

    class Config:
        from_attributes = True


class GenderCount(BaseModel):
    gender: str
    count: int


class StoreTransactionSum(BaseModel):
    store: str
    total_amount: float


class CustomerSegmentOut(BaseModel):
    CustomerKey: int
    CustomerCardCode: str
    Name: Optional[str]
    segment: str
    rfm_sum: Optional[int]
    age: Optional[int]
    gender: Optional[str]

    class Config:
        from_attributes = True


class StoreMonthlyTransaction(BaseModel):
    store: str
    month: str  # Example: "Mar 2024"
    total_amount: float