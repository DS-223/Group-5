import pandas as pd
import numpy as np
from faker import Faker
from typing import List, Dict
import datetime

class RFMDataGenerator:
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


class SurvivalDataGenerator:
    def __init__(self, n_customers=500, seed=42):
        self.n_customers = n_customers
        self.seed = seed
        self.faker = Faker()
        np.random.seed(self.seed)
        self.today = pd.to_datetime('2025-04-26')

    def generate_customers(self):
        customers = []
        for i in range(self.n_customers):
            customers.append({
                'CustomerKey': i + 1,
                'Name': self.faker.name(),
                'BirthDate': self.faker.date_of_birth(minimum_age=18, maximum_age=80),
                'Gender': np.random.choice(['Male', 'Female']),
                'Phone': self.faker.phone_number(),
                'Address': self.faker.address()
            })
        self.customers = pd.DataFrame(customers)
        return self.customers

    def generate_cards(self):
        cards = []
        start_reg_date = datetime.date(2020, 1, 1)
        end_reg_date = datetime.date(2023, 1, 1)
        for i in range(self.n_customers):
            cards.append({
                'CardKey': i + 1,
                'CardCode': self.faker.bothify(text='????-####'),
                'RegistrationDate': self.faker.date_between(start_date=start_reg_date, end_date=end_reg_date),
                'CardLeftoverAmount': round(np.random.uniform(0, 500), 2)
            })
        self.cards = pd.DataFrame(cards)
        return self.cards

    def generate_transactions(self):
        transactions = []
        for cust_id in self.customers['CustomerKey']:
            n_trans = np.random.poisson(4)
            if n_trans == 0:
                continue
            reg_date = self.cards.loc[self.cards['CardKey'] == cust_id, 'RegistrationDate'].values[0]
            dates = pd.to_datetime(reg_date) + pd.to_timedelta(np.sort(np.random.randint(0, 900, size=n_trans)), unit='D')
            for d in dates:
                if d > self.today:
                    continue
                transactions.append({
                    'CustomerKey': cust_id,
                    'TransactionDate': d,
                    'Amount': round(np.random.uniform(5, 300), 2)
                })
        self.transactions = pd.DataFrame(transactions)
        return self.transactions

    def prepare_survival_data(self):
        last_transaction = self.transactions.groupby('CustomerKey')['TransactionDate'].max().reset_index()
        last_transaction.columns = ['CustomerKey', 'LastTransactionDate']
        
        data = self.customers.merge(self.cards, left_on='CustomerKey', right_on='CardKey')\
                             .merge(last_transaction, on='CustomerKey', how='left')
        
        data['duration'] = (data['LastTransactionDate'].fillna(self.today) - pd.to_datetime(data['RegistrationDate'])).dt.days
        data['duration'] = data['duration'].clip(lower=1)
        data['event'] = np.where((self.today - data['LastTransactionDate']).dt.days > 180, 1, 0)
        data['event'] = data['event'].fillna(1)
        data['Age'] = (self.today - pd.to_datetime(data['BirthDate'])).dt.days // 365
        data['Gender'] = data['Gender'].map({'Male': 0, 'Female': 1})
        
        self.survival_data = data
        return self.survival_data