import psycopg2
from db.create_tables import create_tables

class TransactionDatabase:
    def __init__(self, host, database, user, password):
        """Initialize the TransactionDatabase with a PostgreSQL connection.

        Args:
            host (str): The host address of the PostgreSQL server.
            database (str): The name of the database to connect to.
            user (str): The username for the PostgreSQL server.
            password (str): The password for the PostgreSQL server.
        """
        self.conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()
        create_tables()

    def insert_date(self, date_key, date, day, month, year, day_of_week, month_name, quarter):
        """Insert a date record into the DimDate table.

        Args:
            date_key (int): The unique key for the date record.
            date (str): The date in 'YYYY-MM-DD' format.
            day (int): The day of the month (1-31).
            month (int): The month of the year (1-12).
            year (int): The year (e.g., 2025).
            day_of_week (int): The day of the week (1-7, where 1 is Monday).
            month_name (str): The name of the month (e.g., 'January').
            quarter (int): The quarter of the year (1-4).
        """
        self.cursor.execute("INSERT INTO DimDate (DateKey, Date, Day, Month, Year, DayOfWeek, MonthName, Quarter) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (DateKey) DO NOTHING",
                           (date_key, date, day, month, year, day_of_week, month_name, quarter))
        self.conn.commit()
        print(f"Date with DateKey {date_key} inserted into DimDate successfully.")

    def insert_customer(self, customer_key, card_code, name, RegistrationDate, birth_date, gender, phone, address):
        """Insert a customer record into the DimCustomer table.

        Args:
            customer_key (int): The unique key for the customer.
            card_code (str): The card code associated with the customer. 
            name (str): The customer's name.
            birth_date (str): The customer's birth date in 'YYYY-MM-DD' format.
            gender (str): The customer's gender (e.g., 'Male', 'Female').
            phone (str): The customer's phone number.
            address (str): The customer's address.
        """
    
        self.cursor.execute('INSERT INTO "DimCustomer" ("CustomerKey", "CustomerCardCode", "Name", "RegistrationDate", "BirthDate", "Gender", "Phone", "Address")' \
        ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT ("CustomerKey") DO NOTHING',
                            (customer_key, card_code, name, RegistrationDate, birth_date, gender, phone, address))
        self.conn.commit()
        print(f"Customer with CustomerKey {customer_key} inserted into DimCustomer successfully.")

    def peek_table_head(self, table_name, limit=5):
        """Fetch the first 5 rows from the table provided.

        Returns:
            list: A list of tuples containing the first 5 rows of the DimCards table.
        """
        query = f"SELECT * FROM {table_name} LIMIT {limit};"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)
        return rows


    def insert_card(self, card_key, card_code, registration_date, card_left_amount):
        """Insert a card record into the DimCards table.

        Args:
            card_key (int): The unique key for the card.
            card_code (str): The card's code (e.g., 'CARD123').
            registration_date (str): The card's registration date in 'YYYY-MM-DD' format.
            card_left_amount (float): The remaining balance on the card.
        """
        self.cursor.execute("INSERT INTO DimCards (CardKey, CardCode, RegistrationDate, CardLeftAmount) VALUES (%s, %s, %s, %s) ON CONFLICT (CardKey) DO NOTHING",
                           (card_key, card_code, registration_date, card_left_amount))
        self.conn.commit()
        print(f"Card with CardKey {card_key} inserted into DimCards successfully.")

    def add_transaction(self, transaction_date_key, customer_key, card_key, amount):
        """Add a new transaction to the FactTransactions table.

        Args:
            transaction_date_key (int): The foreign key referencing DimDate.
            customer_key (int): The foreign key referencing DimCustomer.
            card_key (int): The foreign key referencing DimCards.
            amount (float): The transaction amount.
        """
        self.cursor.execute("INSERT INTO FactTransactions (TransactionDateKey, CustomerKey, CardKey, Amount) VALUES (%s, %s, %s, %s)",
                           (transaction_date_key, customer_key, card_key, amount))
        self.conn.commit()
        print("Transaction added to FactTransaction successfully.")

    def fetch_transactions(self):
        """Fetch all transactions with details from related tables.

        Returns:
            list: A list of tuples containing transaction details, including
                  TransactionDateKey, CustomerKey, CardKey, Amount, Date, Name, and CardCode.
        """
        self.cursor.execute('''
            SELECT ft.TransactionDateKey, ft.CustomerKey, ft.CardKey, ft.Amount, 
                   dd.Date, dc.Name, dca.CardCode
            FROM FactTransactions ft
            JOIN DimDate dd ON ft.TransactionDateKey = dd.DateKey
            JOIN DimCustomer dc ON ft.CustomerKey = dc.CustomerKey
            JOIN DimCards dca ON ft.CardKey = dca.CardKey
        ''')
        transactions = self.cursor.fetchall()
        for transaction in transactions:
            print(f"Transaction on {transaction[4]} by {transaction[5]} using card {transaction[6]}: ${transaction[3]}")
        return transactions

    def update_transaction_amount(self, transaction_date_key, customer_key, card_key, new_amount):
        """Update the amount of an existing transaction in the FactTransactions table.

        Args:
            transaction_date_key (int): The foreign key referencing DimDate.
            customer_key (int): The foreign key referencing DimCustomer.
            card_key (int): The foreign key referencing DimCards.
            new_amount (float): The new transaction amount.
        """
        self.cursor.execute('''
            UPDATE FactTransactions 
            SET Amount = %s 
            WHERE TransactionDateKey = %s AND CustomerKey = %s AND CardKey = %s
        ''', (new_amount, transaction_date_key, customer_key, card_key))
        self.conn.commit()
        print("Transaction amount updated successfully.")

    def delete_transaction(self, transaction_date_key, customer_key, card_key):
        """Delete a transaction from the FactTransactions table.

        Args:
            transaction_date_key (int): The foreign key referencing DimDate.
            customer_key (int): The foreign key referencing DimCustomer.
            card_key (int): The foreign key referencing DimCards.
        """
        self.cursor.execute('''
            DELETE FROM FactTransactions 
            WHERE TransactionDateKey = %s AND CustomerKey = %s AND CardKey = %s
        ''', (transaction_date_key, customer_key, card_key))
        self.conn.commit()
        print("Transaction deleted successfully.")

    def close_connection(self):
        """Close the database connection."""
        self.conn.close()
        print("Database connection closed.")