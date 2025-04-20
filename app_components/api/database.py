"""
Mock in-memory database module for the Loyalty API.
This file simulates a database by storing data in Python lists.
"""

from typing import List
from schema import Customer, Store, Card, Transaction

# Mock data stores (these act like tables in a real DB)
mock_customers: List[Customer] = []
mock_stores: List[Store] = []
mock_cards: List[Card] = []
mock_transactions: List[Transaction] = []
