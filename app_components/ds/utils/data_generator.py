# import pandas as pd
# import numpy as np
# from faker import Faker
# # from datetime import datetime, timedelta

# class DataGenerator:
#     def __init__(self, num_customers=150, num_transactions=1000, seed=42):
#         self.num_customers = num_customers
#         self.num_transactions = num_transactions
#         self.fake = Faker()
#         np.random.seed(seed)
#         Faker.seed(seed)
#         self.stores = ['Շենգավիթ', 'Քանաքեռ', 'Կենտրոն', 'Աջափնյակ', 'Ավան', 'Նոր Նորք', 'Էրեբունի']
#         self.customers = []

#     def generate_customers(self):
#         """Generate customer data."""
#         for i in range(self.num_customers):
#             gender = np.random.choice(['Женский', 'Мужской'], p=[0.6, 0.4])
#             first_name = self.fake.first_name_female() if gender == 'Женский' else self.fake.first_name_male()
#             last_name = self.fake.last_name()
            
#             self.customers.append({
#                 'card_code': 2719000000000 + i,
#                 'full_name': f"{first_name} {last_name}",
#                 'phone': '0' + ''.join(np.random.choice(list('123456789'), size=8)),
#                 'issue_date': self.fake.date_between(start_date='-4y', end_date='-3m'),
#                 'date_of_birth': self.fake.date_of_birth(minimum_age=18, maximum_age=85),
#                 'gender': gender,
#                 'address': f"г. {self.fake.city()}, ул. {self.fake.street_name()}, д. {self.fake.building_number()}" if np.random.random() < 0.2 else None
#             })
#         return self.customers

#     def generate_transactions(self):
#         """Generate transaction data."""
#         transactions = []
#         for _ in range(self.num_transactions):
#             if np.random.random() < 0.25:  # 25% no card
#                 transactions.append({
#                     'date': self.fake.date_time_between(start_date='-2y', end_date='now').strftime('%d.%m.%Y %H:%M:%S'),
#                     'discount_card': None,
#                     'store': np.random.choice(self.stores),
#                     'product_name': None,
#                     'card_code': None,
#                     'customer_address': None,
#                     'customer_phone': None,
#                     'issue_date': None,
#                     'date_of_birth': None,
#                     'gender': None,
#                     'transaction_amount': round(np.random.gamma(shape=1.5, scale=800), 2)
#                 })
#             else:
#                 customer = np.random.choice(self.customers)
#                 transactions.append({
#                     'date': self.fake.date_time_between(start_date='-2y', end_date='now').strftime('%d.%m.%Y %H:%M:%S'),
#                     'discount_card': f"{customer['card_code']} ({customer['full_name']})",
#                     'store': np.random.choice(self.stores),
#                     'product_name': None,
#                     'card_code': customer['card_code'],
#                     'customer_address': customer['address'] if np.random.random() < 0.1 else None,
#                     'customer_phone': customer['phone'],
#                     'issue_date': customer['issue_date'].strftime('%d.%m.%Y'),
#                     'date_of_birth': customer['date_of_birth'].strftime('%d.%m.%Y') if np.random.random() < 0.8 else None,
#                     'gender': customer['gender'],
#                     'transaction_amount': round(np.random.gamma(shape=2, scale=600), 2)
#                 })
#         return pd.DataFrame(transactions)

#     def save_data(self, filename='synthetic_retail_data.csv'):
#         """Save generated data to CSV."""
#         self.generate_customers()
#         df = self.generate_transactions()
#         print("Null percentages:")
#         print(df.isnull().mean())
#         print("\nSample data:")
#         print(df.head())
#         df.to_csv(filename, index=False, encoding='utf-8-sig')
#         return df



# data_generator.py
import pandas as pd
import numpy as np
from faker import Faker
from typing import List, Dict

class DataGenerator:
    def __init__(self, num_customers: int = 150, num_transactions: int = 1000, seed: int = 42) -> None:
        self.num_customers = num_customers
        self.num_transactions = num_transactions
        self.fake = Faker()
        np.random.seed(seed)
        Faker.seed(seed)
        self.stores = ['Շենգավիթ', 'Քանաքեռ', 'Կենտրոն', 'Աջափնյակ', 'Ավան', 'Նոր Նորք', 'Էրեբունի']
        self.customers: List[Dict] = []

    def generate_customers(self) -> List[Dict]:
        """Generate synthetic customers."""
        for i in range(self.num_customers):
            gender = np.random.choice(['Женский', 'Мужской'], p=[0.6, 0.4])
            first_name = self.fake.first_name_female() if gender == 'Женский' else self.fake.first_name_male()
            last_name = self.fake.last_name()
            
            self.customers.append({
                'card_code': 2719000000000 + i,
                'full_name': f"{first_name} {last_name}",
                'phone': '0' + ''.join(np.random.choice(list('123456789'), size=8)),
                'issue_date': self.fake.date_between(start_date='-4y', end_date='-3m'),
                'date_of_birth': self.fake.date_of_birth(minimum_age=18, maximum_age=85),
                'gender': gender,
                'address': f"г. {self.fake.city()}, ул. {self.fake.street_name()}, д. {self.fake.building_number()}" if np.random.random() < 0.2 else None
            })
        return self.customers

    def generate_transactions(self) -> pd.DataFrame:
        """Generate synthetic transactions."""
        transactions = []
        for _ in range(self.num_transactions):
            if np.random.rand() < 0.25:
                transactions.append({
                    'date': self.fake.date_time_between(start_date='-2y', end_date='now').strftime('%d.%m.%Y %H:%M:%S'),
                    'discount_card': None,
                    'store': np.random.choice(self.stores),
                    'product_name': None,
                    'card_code': None,
                    'customer_address': None,
                    'customer_phone': None,
                    'issue_date': None,
                    'date_of_birth': None,
                    'gender': None,
                    'transaction_amount': round(np.random.gamma(1.5, 800), 2)
                })
            else:
                customer = np.random.choice(self.customers)
                transactions.append({
                    'date': self.fake.date_time_between(start_date='-2y', end_date='now').strftime('%d.%m.%Y %H:%M:%S'),
                    'discount_card': f"{customer['card_code']} ({customer['full_name']})",
                    'store': np.random.choice(self.stores),
                    'product_name': None,
                    'card_code': customer['card_code'],
                    'customer_address': customer['address'] if np.random.rand() < 0.1 else None,
                    'customer_phone': customer['phone'],
                    'issue_date': customer['issue_date'].strftime('%d.%m.%Y'),
                    'date_of_birth': customer['date_of_birth'].strftime('%d.%m.%Y') if np.random.rand() < 0.8 else None,
                    'gender': customer['gender'],
                    'transaction_amount': round(np.random.gamma(2, 600), 2)
                })
        return pd.DataFrame(transactions)

    def save_data(self, filename: str = 'synthetic_retail_data.csv') -> pd.DataFrame:
        """Generate and save data."""
        self.generate_customers()
        df = self.generate_transactions()
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        return df
