'''
This file defines the Pydantic data models (schemas) used for request validation and API responses in the Customer 
Loyalty & Analytics system built with FastAPI.

Each class maps to a specific use case within the application, ensuring type-safe communication 
between the backend and frontend or external clients.

Core Purpose:
Validation: Ensures incoming data (e.g., customer creation) matches expected structure.
Serialization: Converts database models into clean, readable JSON responses.
Documentation: Helps auto-generate OpenAPI (Swagger) docs with clear field types and descriptions.

Overview of Key Models:
CustomerCreate, CustomerOut: For creating and retrieving customer profiles.
MonthlyRevenue: Represents revenue figures per calendar month.
CustomerTransactionOut: Details a single customer transaction with time, store, and amount.
GenderCount: Used in demographic breakdowns.
StoreTransactionSum, StoreMonthlyTransaction: Aggregate store-based revenue stats.
CustomerSegmentOut: Represents customers filtered by RFM segment (Recency, Frequency, Monetary).
RFMSegmentBlock: Summary stats per segment for segmentation matrices.
SurvivalCurvePoint: Represents data points used in Kaplan-Meier survival analysis.
ScorecardMetric: Represents the metrics that are shown by scorecards
'''


from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date

class CustomerOut(BaseModel):
    """
    Response model for returning customer details from the database.

    Includes optional demographic and contact information, suitable for frontend display.
    """
    CustomerKey: int
    CustomerCardCode: Optional[str]
    Name: Optional[str]
    RegistrationDate: Optional[datetime]
    BirthDate: Optional[datetime]
    Gender: Optional[str]
    Phone: Optional[str]
    Address: Optional[str]
    Email: Optional[str]                    

    class Config:
        from_attributes = True


class CustomerCreate(BaseModel):
    """
    Request model for creating or updating customer records.

    Includes required and optional customer fields with aliases for clean field mapping.
    """
    CustomerKey: int
    CustomerCardCode: Optional[str] = Field(None, alias="CustomerCardCode")
    Name: str = Field(..., alias="Name")
    RegistrationDate: Optional[datetime] = Field(None, alias="RegistrationDate")
    BirthDate: Optional[date] = Field(None, alias="BirthDate")
    Gender: Optional[str] = Field(None, alias="Gender")
    Phone: Optional[str] = Field(None, alias="Phone")
    Address: Optional[str] = Field(None, alias="Address")
    Email: Optional[str] = Field(None, alias="Email")                

    class Config:
        populate_by_name = True


class MonthlyRevenue(BaseModel):
    """
    Model representing monthly revenue data.

    Attributes:
        - month: Human-readable string like "Mar 2024"
        - revenue: Total revenue for that month
    """
    month: str  # Example: "Mar 2024"
    revenue: float


class CustomerTransactionOut(BaseModel):
    """
    Response model for displaying customer transaction details.

    Includes transaction ID, date, store name, and amount.
    """
    transaction_id: int
    date: datetime
    store: str
    amount: float

    class Config:
        from_attributes = True


class GenderCount(BaseModel):
    """
    Model for aggregating customer counts by gender.
    """
    gender: str
    count: int


class StoreTransactionSum(BaseModel):
    """
    Model showing total transaction value per store across all time.
    """
    store: str
    total_amount: float


class CustomerSegmentOut(BaseModel):
    """
    Response model for retrieving customers filtered by RFM segment.

    Includes segment label, RFM score, demographics, and identifiers.
    """
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
    """
    Monthly aggregated transaction totals for a specific store.

    Includes store name, month (e.g., "Mar 2024"), and total revenue.
    """
    store: str
    month: str  # Example: "Mar 2024"
    total_amount: float


class RFMSegmentBlock(BaseModel):
    """
    Aggregated statistics for a single RFM segment block.

    Includes user count, percentage, average monetary value,
    and maximum recency/frequency scores within the segment.
    """
    segment: str
    user_count: int
    user_percent: float
    avg_monetary: float
    recency_score: int
    frequency_score: int


class SurvivalCurvePoint(BaseModel):
    """
    A single point on the survival curve for Kaplan-Meier analysis.

    Includes time, survival probability, and optional confidence interval bounds.
    """
    time: float
    survival_prob: float
    ci_lower: Optional[float] = None
    ci_upper: Optional[float] = None


class ScorecardMetric(BaseModel):
    """
    Represents a single scorecard metric with a label and value.
    Used for frontend visualizations like KPI cards.
    """
    label: str
    value: float | int
