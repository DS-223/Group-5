'''
This Python file defines the core FastAPI application for a Customer Loyalty and Analytics system. 
It exposes RESTful API endpoints that interact with PostgreSQL tables using SQLAlchemy ORM,
perform segmentation, calculate RFM scores, generate survival curves, and send email campaigns.

Key Functional Areas:
- Customer Management
create_customer, get_customer, update_customer, delete_customer
CRUD operations on customer records in the DimCustomer table.
-Analytics & Reporting

- Revenue and transaction endpoints:
/revenue/monthly - Total revenue per month
/customers/{customer_id}/transactions - All transactions for a customer
/analytics/transactions-by-store-month - Monthly store-wise revenue
/analytics/transaction-amount-by-store - Store-wise cumulative revenue

- RFM Segmentation
Returns customer data segmented by behavior:
/analytics/customers-by-segment/{segment} - Customers in a specific segment
/analytics/segment-distribution/{all|male|female} - Segment size breakdown

- Email Campaign Management
/campaigns/{segment} - Launches background email campaign to selected RFM segment
/analytics/segments_for_button - Supports frontend dropdown for available segments


RFM Matrix Overview
/analytics/rfm-matrix - Returns data for matrix visualizations including segment size, avg. monetary value, and scores

Customer Survival Analysis
/analytics/survival-curve - Generates Kaplan-Meier survival curve using SurvivalData, modeling customer churn over time

Scorecards with filtering 
/analytics/summary-scorecards - Returns data for scorecards
/dropdowns/stores - Allows to choose a store
/dropdowns/segments - Allows to choose a segment
/dropdowns/date-range - Allows to choose a date range


Technologies & Dependencies:
FastAPI - API framework
SQLAlchemy - ORM for database interaction
Pydantic - Request/response schema validation
Lifelines - Kaplan-Meier survival curve analysis
PostgreSQL - Database backend
BackgroundTasks - Async email dispatch
This is the central service layer of the system, providing ready-to-use data and insights to drive dashboards, retention campaigns, and reporting tools.
'''

from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks  
from sqlalchemy.orm import Session
from database import get_db, engine
from columns import (FactTransaction, 
                     DimDate, DimCustomer, 
                     DimStore, 
                     RFMResults, 
                     SurvivalData)
from schema import (CustomerCreate, 
                    CustomerOut, 
                    MonthlyRevenue, 
                    CustomerTransactionOut, 
                    GenderCount, 
                    StoreTransactionSum, 
                    CustomerSegmentOut,
                    StoreMonthlyTransaction, 
                    RFMSegmentBlock, 
                    SurvivalCurvePoint, 
                    ScorecardMetric)
from typing import List, Dict, Optional
from sqlalchemy import func, cast, BigInteger
from datetime import datetime
import pandas as pd
from fastapi.responses import JSONResponse
import os
from email_utils import EmailCampaignManager

from lifelines import KaplanMeierFitter


app = FastAPI(title="Customer Management API")

#------------------------------------------------------------------------------------------------------
#--------------------------------------By Customers----------------------------------------------------
#------------------------------------------------------------------------------------------------------
@app.post("/customers/", response_model=CustomerOut)
async def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    """
    Creates a new customer entry in the DimCustomer table.
    Accepts customer data and returns the newly created customer record.
    """
    db_customer = DimCustomer(**customer.dict(by_alias=True))
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer



@app.get("/customers/{customer_id}", response_model=CustomerOut)
async def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Fetches a customer record by CustomerKey.
    Raises 404 if the customer is not found.
    """
    customer = db.query(DimCustomer).filter(DimCustomer.CustomerKey == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return customer 



@app.put("/customers/{customer_id}", response_model=CustomerOut)
async def update_customer(customer_id: int, updated_data: CustomerCreate, db: Session = Depends(get_db)):
    """
    Updates an existing customer record with new values.
    Returns the updated customer or raises 404 if not found.
    """
    customer = db.query(DimCustomer).filter(DimCustomer.CustomerKey == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    for key, value in updated_data.dict(by_alias=True).items():
        setattr(customer, key, value)

    db.commit()
    db.refresh(customer)
    return customer



@app.delete("/customers/{customer_id}")
async def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Deletes a customer by CustomerKey.
    Returns a success message or raises 404 if the customer doesn't exist.
    """
    customer = db.query(DimCustomer).filter(DimCustomer.CustomerKey == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    db.delete(customer)
    db.commit()
    return {"message": "Customer deleted successfully"}



@app.get("/analytics/customer-count-by-gender", response_model=List[GenderCount])
def get_customer_count_by_gender(db: Session = Depends(get_db)):
    """
    Returns the number of customers grouped by gender.
    Useful for demographic analysis.
    """
    results = (
        db.query(
            DimCustomer.Gender.label("gender"),
            func.count(DimCustomer.CustomerKey).label("count")
        )
        .group_by(DimCustomer.Gender)
        .all()
    )
    return results

#------------------------------------------------------------------------------------------------------
#------------------------------Transations/Revenue-----------------------------------------------------
#------------------------------------------------------------------------------------------------------
@app.get("/revenue/monthly", response_model=List[MonthlyRevenue])
def get_monthly_revenue(db: Session = Depends(get_db)):
    """
    Returns monthly revenue totals.
    Format: [{"month": "Mar 2024", "revenue": 12345.67}, ...]
    """
    results = (
        db.query(
            DimDate.Month,
            DimDate.Year,
            func.sum(FactTransaction.Amount).label("total_revenue")
        )
        .join(FactTransaction, DimDate.DateKey == FactTransaction.TransactionDateKey)
        .group_by(DimDate.Year, DimDate.Month)
        .order_by(DimDate.Year, DimDate.Month)
        .all()
    )

    return [
        MonthlyRevenue(
            month=datetime(year, month, 1).strftime("%b %Y"),
            revenue=round(total, 2)
        )
        for month, year, total in results
    ]


@app.get("/customers/{customer_id}/transactions", response_model=List[CustomerTransactionOut])
def get_customer_transactions(customer_id: int, db: Session = Depends(get_db)):
    """
    Retrieves all transactions made by a specific customer, ordered by date.
    """
    results = (
        db.query(
            FactTransaction.TransactionKey.label("transaction_id"),
            DimDate.Date.label("date"),
            DimStore.Name.label("store"),
            FactTransaction.Amount.label("amount"),
        )
        .join(DimDate, FactTransaction.TransactionDateKey == DimDate.DateKey)
        .join(DimStore, FactTransaction.StoreKey == DimStore.StoreID)
        .filter(FactTransaction.CustomerKey == customer_id)
        .order_by(DimDate.Date)
        .all()
    )

    return results


@app.get("/analytics/transactions-by-store-month", response_model=List[StoreMonthlyTransaction])
def transactions_by_store(db: Session = Depends(get_db)):
    """
    Returns monthly total transaction amounts for each store.
    Used for store-level revenue breakdowns.
    """
    results = (
        db.query(
            DimStore.Name.label("store"),
            DimDate.Year,
            DimDate.Month,
            func.sum(FactTransaction.Amount).label("total_amount")
        )
        .join(FactTransaction, FactTransaction.StoreKey == DimStore.StoreID)
        .join(DimDate, FactTransaction.TransactionDateKey == DimDate.DateKey)
        .group_by(DimStore.Name, DimDate.Year, DimDate.Month)
        .order_by(DimStore.Name, DimDate.Year, DimDate.Month)
        .all()
    )

    return [
        StoreMonthlyTransaction(
            store=store,
            month=datetime(year, month, 1).strftime("%b %Y"),
            total_amount=round(amount or 0, 2)
        )
        for store, year, month, amount in results
    ]



@app.get("/analytics/transaction-amount-by-store", response_model=List[StoreTransactionSum])
def get_transaction_amount_by_store(db: Session = Depends(get_db)):
    """
    Returns total transaction amounts aggregated by store across all time.
    """
    results = (
        db.query(
            DimStore.Name.label("store"),
            func.sum(FactTransaction.Amount).label("total_amount")
        )
        .join(FactTransaction, FactTransaction.StoreKey == DimStore.StoreID)
        .group_by(DimStore.Name)
        .all()
    )
    return results

#------------------------------------------------------------------------------------------------------
#------------------------------By Customer Segment RFM-------------------------------------------------
#------------------------------------------------------------------------------------------------------
@app.get("/analytics/customers-by-segment/{segment}", response_model=List[CustomerSegmentOut])
def get_customers_by_segment(segment: str, db: Session = Depends(get_db)):
    """
    Returns a list of customers belonging to a specific RFM segment.
    """
    results = (
        db.query(
            DimCustomer.CustomerKey,
            DimCustomer.CustomerCardCode,
            DimCustomer.Name,
            RFMResults.segment,
            RFMResults.rfm_sum,
            RFMResults.age,
            RFMResults.gender
        )
        .join(
            RFMResults,
            RFMResults.card_code == cast(DimCustomer.CustomerCardCode, BigInteger)
        )
        .filter(func.lower(RFMResults.segment) == segment.lower())
        .all()
    )

    if not results:
        raise HTTPException(status_code=404, detail=f"No customers found for segment '{segment}'")

    return results


@app.get("/analytics/segment-distribution/all")
def get_segment_distribution_all(db: Session = Depends(get_db)):
    """
    Returns the overall count of customers per RFM segment.
    """
    results = (
        db.query(
            RFMResults.segment,
            func.count(RFMResults.card_code).label("count")
        )
        .group_by(RFMResults.segment)
        .all()
    )

    return JSONResponse(content={segment: count for segment, count in results})


@app.get("/analytics/segment-distribution/male")
def get_segment_distribution_male(db: Session = Depends(get_db)):
    """
    Returns count of customers per segment for males only.
    """
    results = (
        db.query(
            RFMResults.segment,
            func.count(RFMResults.card_code).label("count")
        )
        .filter(func.lower(RFMResults.gender) == "male")
        .group_by(RFMResults.segment)
        .all()
    )

    return JSONResponse(content={segment: count for segment, count in results})


@app.get("/analytics/segment-distribution/female")
def get_segment_distribution_female(db: Session = Depends(get_db)):
    """
    Returns count of customers per segment for females only.
    """
    results = (
        db.query(
            RFMResults.segment,
            func.count(RFMResults.card_code).label("count")
        )
        .filter(func.lower(RFMResults.gender) == "female")
        .group_by(RFMResults.segment)
        .all()
    )

    return JSONResponse(content={segment: count for segment, count in results})

#------------------------------------------------------------------------------------------------------
#-----------------------------------Sending Emails-----------------------------------------------------
#------------------------------------------------------------------------------------------------------
@app.get("/analytics/segments_for_button", response_model=list[str])
def list_segments(db: Session = Depends(get_db)):
    rows = db.query(RFMResults.segment).distinct().all()
    return [r[0] for r in rows]


@app.post("/campaigns/{segment}")
def launch_campaign(
    segment: str,
    background: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """
    Launches an email campaign for customers in the given RFM segment.

    Emails are queued and sent asynchronously using BackgroundTasks.
    Raises 404 if no email addresses are found for the segment.
    """
    mgr = EmailCampaignManager(segment, engine, 'hayk_nalchajyan@edu.aua.am', 'uclr rwxq annw rksa')
    count = mgr.fetch_emails()
    if count == 0:
        raise HTTPException(404, f"No addresses found for segment '{segment}'")

    background.add_task(mgr.send_emails)
    return {"detail": f"Queued {count} e-mails for segment '{segment}'"}



#------------------------------------------------------------------------------------------------------
#-----------------------------------Segments Block Visual----------------------------------------------
#------------------------------------------------------------------------------------------------------
@app.get("/analytics/rfm-matrix", response_model=list[RFMSegmentBlock])
def rfm_matrix(db: Session = Depends(get_db)):
    """
    Returns data for RFM segment matrix:
    - segment name
    - user count + %
    - avg monetary value
    - recency + frequency score
    """

    # Step 1: Get total user count
    total_users = db.query(func.count(RFMResults.card_code)).scalar()

    # Step 2: Query all blocks
    results = (
        db.query(
            RFMResults.segment,
            func.count(RFMResults.card_code).label("user_count"),
            func.avg(RFMResults.monetary).label("avg_monetary"),
            func.max(RFMResults.r_score).label("recency_score"),
            func.max(RFMResults.f_score).label("frequency_score"),
        )
        .group_by(RFMResults.segment)
        .all()
    )

    # Step 3: Format response
    response = []
    for row in results:
        response.append(RFMSegmentBlock(
            segment=row.segment,
            user_count=row.user_count,
            user_percent=round((row.user_count / total_users) * 100, 2),
            avg_monetary=round(row.avg_monetary or 0, 2),
            recency_score=row.recency_score,
            frequency_score=row.frequency_score
        ))

    return response



#------------------------------------------------------------------------------------------------------
#--------------------------------------------RFM Analysis----------------------------------------------
#------------------------------------------------------------------------------------------------------
@app.get("/analytics/survival-curve", response_model=List[SurvivalCurvePoint])
def get_survival_curve(db: Session = Depends(get_db)):
    """
    Performs Kaplan-Meier survival analysis using duration and event columns.
    Returns survival probabilities and confidence intervals over time.
    """
    # Load duration and event from DB
    data = db.query(SurvivalData.duration, SurvivalData.event).filter(
        SurvivalData.duration.isnot(None),
        SurvivalData.event.isnot(None)
    ).all()

    durations = [d[0] for d in data]
    events = [d[1] for d in data]

    if not durations or not events:
        raise HTTPException(status_code=404, detail="No survival data available.")

    # Fit Kaplan-Meier estimator
    kmf = KaplanMeierFitter()
    kmf.fit(durations, event_observed=events)

    # Build response
    results = []
    for t, s, l, u in zip(
        kmf.survival_function_.index,
        kmf.survival_function_["KM_estimate"],
        kmf.confidence_interval_["KM_estimate_lower_0.95"],
        kmf.confidence_interval_["KM_estimate_upper_0.95"]
    ):
        results.append(SurvivalCurvePoint(
            time=float(t),
            survival_prob=float(s),
            ci_lower=float(l),
            ci_upper=float(u)
        ))

    return results


#------------------------------------------------------------------------------------------------------
#---------------------------------------Scorecard Metrics----------------------------------------------
#------------------------------------------------------------------------------------------------------
@app.get("/analytics/summary-scorecards", response_model=List[ScorecardMetric])
def get_summary_scorecards(
    store_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    segment: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Returns 3 metrics for dashboard scorecards:
    - Total Revenue
    - Total Orders
    - Total Customers
    Filters (optional):
    - store_id (int)
    - start_date (datetime)
    - end_date (datetime)
    - segment (str)
    """
    query = db.query(FactTransaction)

    if start_date or end_date:
        query = query.join(DimDate, FactTransaction.TransactionDateKey == DimDate.DateKey)
    if segment:
        query = query.join(DimCustomer, FactTransaction.CustomerKey == DimCustomer.CustomerKey)
        query = query.join(RFMResults, RFMResults.card_code == cast(DimCustomer.CustomerCardCode, BigInteger))

    if store_id is not None:
        query = query.filter(FactTransaction.StoreKey == store_id)
    if start_date is not None:
        query = query.filter(DimDate.Date >= start_date)
    if end_date is not None:
        query = query.filter(DimDate.Date <= end_date)
    if segment is not None:
        query = query.filter(func.lower(RFMResults.segment) == segment.lower())

    total_amount = query.with_entities(func.sum(FactTransaction.Amount)).scalar() or 0.0
    total_orders = query.with_entities(func.count(FactTransaction.TransactionKey)).scalar() or 0
    total_customers = query.with_entities(FactTransaction.CustomerKey).distinct().count()

    return [
        ScorecardMetric(label="Total Revenue", value=round(total_amount, 2)),
        ScorecardMetric(label="Total Orders", value=total_orders),
        ScorecardMetric(label="Total Customers", value=total_customers)
    ]


#------------------------------------------------------------------------------------------------------
#------------------------------------Dropdowns for scorecards------------------------------------------
#------------------------------------------------------------------------------------------------------
@app.get("/dropdowns/stores", response_model=List[Dict[str, str]])
def get_store_dropdown(db: Session = Depends(get_db)):
    """
    Returns available stores for dropdown selection.
    """
    stores = db.query(DimStore.StoreID, DimStore.Name).all()
    return [{"value": str(sid), "label": name} for sid, name in stores]


@app.get("/dropdowns/segments", response_model=List[str])
def get_segment_dropdown(db: Session = Depends(get_db)):
    """
    Returns available RFM segments for dropdown.
    """
    segments = db.query(RFMResults.segment).distinct().all()
    return [s[0] for s in segments if s[0] is not None]


@app.get("/dropdowns/date-range", response_model=Dict[str, str])
def get_date_range(db: Session = Depends(get_db)):
    """
    Returns min/max transaction dates for optional filtering.
    """
    result = (
        db.query(func.min(DimDate.Date), func.max(DimDate.Date))
        .join(FactTransaction, FactTransaction.TransactionDateKey == DimDate.DateKey)
        .first()
    )
    min_date, max_date = result
    return {
        "min_date": min_date.strftime("%Y-%m-%d") if min_date else None,
        "max_date": max_date.strftime("%Y-%m-%d") if max_date else None
    }
