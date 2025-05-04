import psycopg2
from db.create_tables import create_tables

class TransactionDatabase:
    def __init__(self, host, database, user, password):
        """Initialize the TransactionDatabase with a PostgreSQL connection."""
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()
        create_tables()

    def insert_date(self, date_key, date, day, month, year, day_of_week, month_name, day_name, quarter):
        """Insert a date record into the DimDate table."""
        self.cursor.execute("""
            INSERT INTO "DimDate" ("DateKey", "Date", "Day", "Month", "Year", "DayOfWeek", "MonthName", "DayName", "Quarter")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT ("DateKey") DO NOTHING
        """, (date_key, date, day, month, year, day_of_week, month_name, day_name, quarter))
        self.conn.commit()
        # print(f"Date with DateKey {date_key} inserted into DimDate successfully.")

    def insert_customer(self, customer_key, card_code, name, RegistrationDate, birth_date, gender, phone, address):
        """Insert a customer record into the DimCustomer table."""
        self.cursor.execute("""
            INSERT INTO "DimCustomer"
            ("CustomerKey", "CustomerCardCode", "Name", "RegistrationDate", "BirthDate", "Gender", "Phone", "Address")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT ("CustomerKey") DO NOTHING
        """, (customer_key, card_code, name, RegistrationDate, birth_date, gender, phone, address))
        self.conn.commit()
        # print(f"Customer with CustomerKey {customer_key} inserted into DimCustomer successfully.")

    def peek_table_head(self, table_name, limit=5):
        """Fetch the first 5 rows from the table provided."""
        query = f'SELECT * FROM "{table_name}" LIMIT {limit};'
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)
        return rows
    
    def add_transaction(self, transaction_key, transaction_date_key, customer_key, store_key, amount):
        """Add a new transaction to the FactTransactions table."""
        self.cursor.execute("""
            INSERT INTO FactTransactions (TransactionKey, TransactionDateKey, CustomerKey, StoreKey, Amount)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (TransactionKey) DO NOTHING
        """, (transaction_key, transaction_date_key, customer_key, store_key, amount))
        self.conn.commit()
        print("Transaction added to FactTransaction successfully.")

    def fetch_transactions(self):
        """Fetch all transactions with details from related tables."""
        self.cursor.execute("""
            SELECT ft.TransactionKey, ft.TransactionDateKey, ft.CustomerKey, ft.Amount, 
                dd.Date, dc.Name
            FROM FactTransactions ft
            JOIN DimDate dd ON ft.TransactionDateKey = dd.DateKey
            JOIN DimCustomer dc ON ft.CustomerKey = dc.CustomerKey
        """)
        transactions = self.cursor.fetchall()
        for transaction in transactions:
            print(f"Transaction {transaction[0]} on {transaction[4]} by {transaction[5]}: ${transaction[3]}")
        return transactions

    def update_transaction_amount(self, transaction_key, new_amount):
        """Update the amount of an existing transaction."""
        self.cursor.execute("""
            UPDATE FactTransactions 
            SET Amount = %s 
            WHERE TransactionKey = %s
        """, (new_amount, transaction_key))
        self.conn.commit()
        print("Transaction amount updated successfully.")

    def delete_transaction(self, transaction_key):
        """Delete a transaction."""
        self.cursor.execute("""
            DELETE FROM FactTransactions 
            WHERE TransactionKey = %s
        """, (transaction_key,))
        self.conn.commit()
        print("Transaction deleted successfully.")

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()
        print("Database connection closed.")