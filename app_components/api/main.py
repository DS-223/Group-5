from fastapi import FastAPI, HTTPException
from typing import List
from schema import (
    Customer, CustomerCreate,
    Store, StoreCreate,
    Card, CardCreate,
    Transaction, TransactionCreate
)

app = FastAPI(title="Loyalty Mock API")

# ---------------------------
# Mock Data Stores
# ---------------------------
from database import mock_customers, mock_stores, mock_cards, mock_transactions

# ---------------------------
# CUSTOMER ROUTES
# ---------------------------

# POST Request - Create a new customer
@app.post("/customers/", response_model=Customer)
async def create_customer(customer: CustomerCreate):
    """
    Create a new customer.

    **Parameters:**
    - `customer (CustomerCreate)`: The customer data to create.

    **Returns:**
    - `Customer`: The newly created customer.
    """
    new_customer = Customer(customer_id=len(mock_customers)+1, **customer.dict())
    mock_customers.append(new_customer)
    return new_customer


# GET Request - List all customers
@app.get("/customers/", response_model=List[Customer])
async def list_customers():
    """
    Retrieve all customers.

    **Returns:**
    - `List[Customer]`: A list of all customers.
    """
    return mock_customers


# GET Request - Retrieve a customer by ID
@app.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int):
    """
    Retrieve a customer by their customer ID.

    **Parameters:**
    - `customer_id (int)`: The unique identifier for the customer.

    **Returns:**
    - `Customer`: The customer's details.

    **Raises:**
    - `HTTPException: 404`: If the customer is not found.
    """
    for c in mock_customers:
        if c.customer_id == customer_id:
            return c
    raise HTTPException(status_code=404, detail="Customer not found")


# PUT Request - Update a customer by ID
@app.put("/customers/{customer_id}", response_model=Customer)
async def update_customer(customer_id: int, updated: CustomerCreate):
    """
    Update a customer by their ID.

    **Parameters:**
    - `customer_id (int)`: ID of the customer to update.
    - `updated (CustomerCreate)`: Updated customer data.

    **Returns:**
    - `Customer`: The updated customer.

    **Raises:**
    - `HTTPException: 404`: If the customer is not found.
    """
    for i, c in enumerate(mock_customers):
        if c.customer_id == customer_id:
            updated_customer = Customer(customer_id=customer_id, **updated.dict())
            mock_customers[i] = updated_customer
            return updated_customer
    raise HTTPException(status_code=404, detail="Customer not found")


# DELETE Request - Delete a customer by ID
@app.delete("/customers/{customer_id}")
async def delete_customer(customer_id: int):
    """
    Delete a customer by their ID.

    **Parameters:**
    - `customer_id (int)`: ID of the customer to delete.

    **Returns:**
    - `dict`: Success message.

    **Raises:**
    - `HTTPException: 404`: If the customer is not found.
    """
    for i, c in enumerate(mock_customers):
        if c.customer_id == customer_id:
            mock_customers.pop(i)
            return {"message": "Customer deleted"}
    raise HTTPException(status_code=404, detail="Customer not found")

# ---------------------------
# STORE ROUTES
# ---------------------------

# POST Request - Create a new store
@app.post("/stores/", response_model=Store)
async def create_store(store: StoreCreate):
    """
    Create a new store.

    **Parameters:**
    - `store (StoreCreate)`: Store data to create.

    **Returns:**
    - `Store`: The newly created store.
    """
    new_store = Store(store_id=len(mock_stores)+1, **store.dict())
    mock_stores.append(new_store)
    return new_store


# GET Request - List all stores
@app.get("/stores/", response_model=List[Store])
async def list_stores():
    """
    Retrieve all stores.

    **Returns:**
    - `List[Store]`: A list of all stores.
    """
    return mock_stores


# PUT Request - Update a store by ID
@app.put("/stores/{store_id}", response_model=Store)
async def update_store(store_id: int, updated: StoreCreate):
    """
    Update a store by its ID.

    **Parameters:**
    - `store_id (int)`: ID of the store to update.
    - `updated (StoreCreate)`: Updated store data.

    **Returns:**
    - `Store`: The updated store.

    **Raises:**
    - `HTTPException: 404`: If the store is not found.
    """
    for i, store in enumerate(mock_stores):
        if store.store_id == store_id:
            updated_store = Store(store_id=store_id, **updated.dict())
            mock_stores[i] = updated_store
            return updated_store
    raise HTTPException(status_code=404, detail="Store not found")


# DELETE Request - Delete a store by ID
@app.delete("/stores/{store_id}")
async def delete_store(store_id: int):
    """
    Delete a store by its ID.

    **Parameters:**
    - `store_id (int)`: ID of the store to delete.

    **Returns:**
    - `dict`: Success message.

    **Raises:**
    - `HTTPException: 404`: If the store is not found.
    """
    for i, store in enumerate(mock_stores):
        if store.store_id == store_id:
            mock_stores.pop(i)
            return {"message": "Store deleted successfully"}
    raise HTTPException(status_code=404, detail="Store not found")


# ---------------------------
# BONUS CARD ROUTES
# ---------------------------

# POST Request - Create a new bonus card
@app.post("/cards/", response_model=Card)
async def create_card(card: CardCreate):
    """
    Create a new bonus card.

    **Parameters:**
    - `card (CardCreate)`: Card data to create.

    **Returns:**
    - `Card`: The newly created bonus card.
    """
    new_card = Card(card_id=len(mock_cards)+1, **card.dict())
    mock_cards.append(new_card)
    return new_card


# GET Request - List all bonus cards
@app.get("/cards/", response_model=List[Card])
async def list_cards():
    """
    Retrieve all bonus cards.

    **Returns:**
    - `List[Card]`: A list of all bonus cards.
    """
    return mock_cards


# DELETE Request - Delete a bonus card by ID
@app.delete("/cards/{card_id}")
async def delete_card(card_id: int):
    """
    Delete a bonus card by its ID.

    **Parameters:**
    - `card_id (int)`: ID of the card to delete.

    **Returns:**
    - `dict`: Success message.

    **Raises:**
    - `HTTPException: 404`: If the card is not found.
    """
    for i, card in enumerate(mock_cards):
        if card.card_id == card_id:
            mock_cards.pop(i)
            return {"message": "Card deleted successfully"}
    raise HTTPException(status_code=404, detail="Card not found")


# ---------------------------
# TRANSACTION ROUTES
# ---------------------------

# POST Request - Create a new transaction
@app.post("/transactions/", response_model=Transaction)
async def create_transaction(tx: TransactionCreate):
    """
    Create a new transaction.

    **Parameters:**
    - `tx (TransactionCreate)`: Transaction data to create.

    **Returns:**
    - `Transaction`: The newly created transaction.
    """
    new_tx = Transaction(transaction_id=len(mock_transactions)+1, **tx.dict())
    mock_transactions.append(new_tx)
    return new_tx


# GET Request - List all transactions
@app.get("/transactions/", response_model=List[Transaction])
async def list_transactions():
    """
    Retrieve all transactions.

    **Returns:**
    - `List[Transaction]`: A list of all transactions.
    """
    return mock_transactions
