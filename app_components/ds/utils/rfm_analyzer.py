# import pandas as pd
# from datetime import datetime

# class RFMAnalyzer:
#     def __init__(self, data_file='synthetic_retail_data.csv'):
#         self.df = pd.read_csv(data_file, encoding='utf-8-sig')
#         self._preprocess_data()
#         self.customer_df = self.df[self.df['discount_card'].notna()].copy()
#         self.analysis_date = self.customer_df['date'].max() + pd.Timedelta(days=1)
#         self.rfm = None
#         self.quantiles = None

#     def _preprocess_data(self):
#         """Convert date columns to datetime."""
#         date_cols = ['date', 'issue_date', 'date_of_birth']
#         for col in date_cols:
#             self.df[col] = pd.to_datetime(self.df[col], dayfirst=True, errors='coerce')

#     def calculate_rfm(self):
#         """Calculate RFM metrics."""
#         self.rfm = self.customer_df.groupby('card_code').agg({
#             'date': lambda x: (self.analysis_date - x.max()).days,
#             'discount_card': 'count',
#             'transaction_amount': 'sum'
#         }).reset_index()
#         self.rfm.columns = ['card_code', 'recency', 'frequency', 'monetary']
#         return self.rfm

#     def score_rfm(self):
#         """Assign RFM scores based on quantiles."""
#         self.quantiles = self.rfm.quantile(q=[0.2, 0.4, 0.6, 0.8])

#         def r_score(x):
#             if x <= self.quantiles['recency'][0.2]: return 5
#             elif x <= self.quantiles['recency'][0.4]: return 4
#             elif x <= self.quantiles['recency'][0.6]: return 3
#             elif x <= self.quantiles['recency'][0.8]: return 2
#             else: return 1

#         def fm_score(x, col):
#             if x <= self.quantiles[col][0.2]: return 1
#             elif x <= self.quantiles[col][0.4]: return 2
#             elif x <= self.quantiles[col][0.6]: return 3
#             elif x <= self.quantiles[col][0.8]: return 4
#             else: return 5

#         self.rfm['r_score'] = self.rfm['recency'].apply(r_score)
#         self.rfm['f_score'] = self.rfm['frequency'].apply(lambda x: fm_score(x, 'frequency'))
#         self.rfm['m_score'] = self.rfm['monetary'].apply(lambda x: fm_score(x, 'monetary'))
#         self.rfm['rfm_score'] = self.rfm['r_score'].astype(str) + self.rfm['f_score'].astype(str) + self.rfm['m_score'].astype(str)
#         self.rfm['rfm_sum'] = self.rfm[['r_score', 'f_score', 'm_score']].sum(axis=1)
#         return self.rfm

#     def segment_customers(self):
#         """Assign customer segments based on RFM scores."""
#         segment_map = {
#             r'555|554|545|455': 'Champions',
#             r'[4-5][4-5][3-5]': 'Loyal Customers',
#             r'[3-4][3-4][3-4]': 'Potential Loyalists',
#             r'[3-5][1-3][1-3]': 'Recent Customers',
#             r'[2-3][2-3][2-3]': 'Needing Attention',
#             r'[1-2][1-2][1-2]': 'At Risk',
#             r'1[1-3][1-3]': 'Hibernating',
#             r'[1-2][1-2][4-5]': 'Cant Lose Them',
#             r'[1-2]5[1-5]': 'Lost'
#         }
#         self.rfm['segment'] = self.rfm['rfm_score'].replace(segment_map, regex=True)
#         self.rfm['segment'] = self.rfm['segment'].fillna('Others')

#         # Merge with customer details
#         customer_details = self.customer_df[['card_code', 'gender', 'date_of_birth']].drop_duplicates()
#         self.rfm = self.rfm.merge(customer_details, on='card_code', how='left')
#         self.rfm['age'] = (self.analysis_date - self.rfm['date_of_birth']).dt.days // 365
#         return self.rfm

#     def analyze_segments(self):
#         """Analyze segments and return summary."""
#         segment_analysis = self.rfm.groupby('segment').agg({
#             'recency': 'mean',
#             'frequency': 'mean',
#             'monetary': 'mean',
#             'card_code': 'count',
#             'age': 'mean'
#         }).rename(columns={'card_code': 'count'})
#         segment_analysis['percentage'] = (segment_analysis['count'] / segment_analysis['count'].sum()) * 100
#         return segment_analysis.sort_values('count', ascending=False)

#     def save_results(self, filename='rfm_results.csv'):
#         """Save RFM results to CSV."""
#         self.rfm.to_csv(filename, index=False, encoding='utf-8-sig')



# rfm_analyzer.py
import pandas as pd
from datetime import datetime
from typing import Optional

class RFMAnalyzer:
    def __init__(self, data_file: str = 'synthetic_retail_data.csv') -> None:
        self.df = pd.read_csv(data_file, encoding='utf-8-sig')
        self._preprocess_data()
        self.customer_df = self.df[self.df['discount_card'].notna()].copy()
        self.analysis_date = self.customer_df['date'].max() + pd.Timedelta(days=1)
        self.rfm: Optional[pd.DataFrame] = None
        self.quantiles: Optional[pd.DataFrame] = None

    def _preprocess_data(self) -> None:
        """Convert relevant columns to datetime."""
        for col in ['date', 'issue_date', 'date_of_birth']:
            self.df[col] = pd.to_datetime(self.df[col], dayfirst=True, errors='coerce')

    def calculate_rfm(self) -> pd.DataFrame:
        """Calculate Recency, Frequency, and Monetary values."""
        self.rfm = self.customer_df.groupby('card_code').agg({
            'date': lambda x: (self.analysis_date - x.max()).days,
            'discount_card': 'count',
            'transaction_amount': 'sum'
        }).reset_index()
        self.rfm.columns = ['card_code', 'recency', 'frequency', 'monetary']
        return self.rfm

    def score_rfm(self) -> pd.DataFrame:
        """Assign RFM scores based on fixed business-defined intervals."""

        def r_score(x: int) -> int:
            if x < 5:
                return 5
            elif x < 15:
                return 4
            elif x < 30:
                return 3
            elif x < 60:
                return 2
            else:
                return 1

        def f_score(x: int) -> int:
            if x > 100:
                return 5
            elif x > 75:
                return 4
            elif x > 40:
                return 3
            elif x > 15:
                return 2
            else:
                return 1

        def m_score(x: float) -> int:
            if x > 300_000:
                return 5
            elif x > 200_000:
                return 4
            elif x > 100_000:
                return 3
            elif x > 50_000:
                return 2
            else:
                return 1

        self.rfm['r_score'] = self.rfm['recency'].apply(r_score)
        self.rfm['f_score'] = self.rfm['frequency'].apply(f_score)
        self.rfm['m_score'] = self.rfm['monetary'].apply(m_score)

        self.rfm['rfm_score'] = (
            self.rfm['r_score'].astype(str) +
            self.rfm['f_score'].astype(str) +
            self.rfm['m_score'].astype(str)
        )

        self.rfm['rfm_sum'] = self.rfm[['r_score', 'f_score', 'm_score']].sum(axis=1)
        return self.rfm


    def segment_customers(self) -> pd.DataFrame:
        """Classify customers into custom segments based on RFM scores."""
        segment_map = {
            r'555|554|545|455|554|544|445|454|544': 'Champions',
            r'4[4-5][4-5]|[4-5][4-5][4-5]|5[4-5][4-5]': 'Loyal Customers',
            r'3[3-5][3-5]|[3-5][3-5][3-5]|4[2-4][2-4]': 'Potential Loyalists',
            r'2[4-5][4-5]|3[2-4][4-5]|4[1-3][4-5]': 'Big Spenders',
            r'[1-2][1-2][1-3]|2[1-2][1-2]|1[2-3][1-2]': 'Leaving Customers'
        }
        self.rfm['segment'] = self.rfm['rfm_score'].replace(segment_map, regex=True)
        self.rfm['segment'] = self.rfm['segment'].fillna('Others')

        customer_details = self.customer_df[['card_code', 'gender', 'date_of_birth']].drop_duplicates()
        self.rfm = self.rfm.merge(customer_details, on='card_code', how='left')
        self.rfm['age'] = (self.analysis_date - self.rfm['date_of_birth']).dt.days // 365
        return self.rfm

    def analyze_segments(self) -> pd.DataFrame:
        """Aggregate metrics by customer segment."""
        segment_analysis = self.rfm.groupby('segment').agg({
            'recency': 'mean',
            'frequency': 'mean',
            'monetary': 'mean',
            'card_code': 'count',
            'age': 'mean'
        }).rename(columns={'card_code': 'count'})
        segment_analysis['percentage'] = (segment_analysis['count'] / segment_analysis['count'].sum()) * 100
        return segment_analysis.sort_values('count', ascending=False)

    def save_results(self, filename: str = 'rfm_results.csv') -> None:
        """Save the RFM results to a CSV file."""
        if self.rfm is not None:
            self.rfm.to_csv(filename, index=False, encoding='utf-8-sig')
