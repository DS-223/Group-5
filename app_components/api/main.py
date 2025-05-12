from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks  
from sqlalchemy.orm import Session
from database import get_db, engine
from columns import (FactTransaction, 
                     DimDate, DimCustomer, 
                     DimStore, 
                     RFMResults)
from schema import (CustomerCreate, 
                    CustomerOut, 
                    MonthlyRevenue, 
                    CustomerTransactionOut, 
                    GenderCount, 
                    StoreTransactionSum, 
                    CustomerSegmentOut,
                    StoreMonthlyTransaction)
from typing import List, Dict
from sqlalchemy import func, cast, String, BigInteger
from datetime import datetime
import pandas as pd
from fastapi.responses import FileResponse, JSONResponse
import os
from sqlalchemy import inspect
from email_utils import EmailCampaignManager



app = FastAPI(title="Customer Management API")

#------------------------------------------------------------------------------------------------------
#--------------------------------------By Customers----------------------------------------------------
#------------------------------------------------------------------------------------------------------
@app.post("/customers/", response_model=CustomerOut)
async def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    """
    Creates a new customer record in the DimCustomer table.
    """
    db_customer = DimCustomer(**customer.dict(by_alias=True))
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer



@app.get("/customers/{customer_id}", response_model=CustomerOut)
async def get_customer(customer_id: int, db: Session = Depends(get_db)):
    """
    Returns the customer with the specified CustomerKey.
    """
    customer = db.query(DimCustomer).filter(DimCustomer.CustomerKey == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return customer 



@app.put("/customers/{customer_id}", response_model=CustomerOut)
async def update_customer(customer_id: int, updated_data: CustomerCreate, db: Session = Depends(get_db)):
    """
    Updates an existing customer record in the DimCustomer table.
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
    Deletes a customer record from the DimCustomer table.
    """
    customer = db.query(DimCustomer).filter(DimCustomer.CustomerKey == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    db.delete(customer)
    db.commit()
    return {"message": "Customer deleted successfully"}



@app.get("/analytics/customer-count-by-gender", response_model=List[GenderCount])
def get_customer_count_by_gender(db: Session = Depends(get_db)):
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
    Returns all transactions made by a specific customer.
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
    Returns monthly transaction totals for each store.
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
#------------------------------By Customer Segment-----------------------------------------------------
#------------------------------------------------------------------------------------------------------
@app.get("/analytics/customers-by-segment/{segment}", response_model=List[CustomerSegmentOut])
def get_customers_by_segment(segment: str, db: Session = Depends(get_db)):
    """
    Returns customers who belong to a given RFM segment.
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
    Returns total segment distribution.
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
    Returns segment distribution for males only.
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
    Returns segment distribution for females only.
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
    mgr = EmailCampaignManager(segment, engine, 'hayk_nalchajyan@edu.aua.am', 'uclr rwxq annw rksa')
    count = mgr.fetch_emails()
    if count == 0:
        raise HTTPException(404, f"No addresses found for segment '{segment}'")

    background.add_task(mgr.send_emails)
    return {"detail": f"Queued {count} e-mails for segment '{segment}'"}
