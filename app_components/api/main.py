from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from columns import FactTransaction, DimDate, DimCustomer, DimStore
from schema import CustomerCreate, CustomerOut
from typing import List, Dict
import pandas as pd
from fastapi.responses import FileResponse
import os


app = FastAPI(title="Customer Management API")


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


@app.get("/transactions/report/download")
def download_transaction_report(db: Session = Depends(get_db)):
    """
    Generates a joined transaction report (date, customer, store, etc.) and exports it as a CSV file for the modeling.
    """
    results = (
        db.query(
            DimDate.Date.label("date"),
            DimCustomer.CustomerCardCode.label("card_code"),
            DimCustomer.CustomerKey.label("customer_key"),
            DimCustomer.Address.label("customer_address"),
            DimCustomer.Phone.label("customer_phone"),
            DimCustomer.RegistrationDate.label("issue_date"),
            DimCustomer.BirthDate.label("date_of_birth"),
            DimCustomer.Gender.label("gender"),
            DimStore.Name.label("store"),
            FactTransaction.Amount.label("transaction_amount"),
        )
        .join(DimDate, FactTransaction.TransactionDateKey == DimDate.DateKey)
        .join(DimCustomer, FactTransaction.CustomerKey == DimCustomer.CustomerKey)
        .join(DimStore, FactTransaction.StoreKey == DimStore.StoreID)
        .all()
    )

    # Debug print
    print(f"✅ Retrieved {len(results)} rows from the joined query")

    if not results:
        return {"message": "No transaction data found to export."}

    # Prepare list of dicts
    data = [
        {
            "date": r.date,
            "store": r.store,
            "card_code": r.card_code,
            "customer_key": r.customer_key,
            "customer_address": r.customer_address,
            "customer_phone": r.customer_phone,
            "issue_date": r.issue_date,
            "date_of_birth": r.date_of_birth,
            "gender": r.gender,
            "transaction_amount": r.transaction_amount
        }
        for r in results
    ]

    # Ensure output folder exists
    export_dir = "exports"
    os.makedirs(export_dir, exist_ok=True)
    file_path = os.path.join(export_dir, "transaction_report.csv")

    # Save to CSV
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False, encoding='utf-8-sig')

    return FileResponse(
        path=file_path,
        filename="transaction_report.csv",
        media_type="text/csv"
    )
