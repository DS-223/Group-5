import pandas as pd
import numpy as np
import datetime
from faker import Faker

import matplotlib
matplotlib.use('Agg')  # 🔥 ADD THIS 🔥
import matplotlib.pyplot as plt

from lifelines import KaplanMeierFitter, CoxPHFitter


class DataGenerator:
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


class SurvivalAnalyzer:
    def __init__(self, survival_data):
        self.data = survival_data

    def fit_kaplan_meier(self):
        self.kmf = KaplanMeierFitter()
        self.kmf.fit(self.data['duration'], event_observed=self.data['event'])

    def save_kaplan_meier_plot(self, filename='kaplan_meier_curve.png'):
        plt.figure()
        self.kmf.plot_survival_function()
        plt.title('Customer Card Survival Curve')
        plt.xlabel('Days Since Card Registration')
        plt.ylabel('Survival Probability')
        plt.grid()
        plt.savefig(filename, bbox_inches='tight')
        plt.close()

    def fit_cox_model(self):
        self.cph = CoxPHFitter()
        self.cph.fit(self.data[['duration', 'event', 'Age', 'Gender', 'CardLeftoverAmount']],
                     duration_col='duration', event_col='event')

    def print_cox_summary(self):
        self.cph.print_summary()

# Data Generation
generator = DataGenerator()
customers = generator.generate_customers()
cards = generator.generate_cards()
transactions = generator.generate_transactions()
survival_data = generator.prepare_survival_data()

# Survival Analysis
analyzer = SurvivalAnalyzer(survival_data)
analyzer.fit_kaplan_meier()
analyzer.save_kaplan_meier_plot(filename='kaplan_meier_curve.png')
analyzer.fit_cox_model()
analyzer.print_cox_summary()
