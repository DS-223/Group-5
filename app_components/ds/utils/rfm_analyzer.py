import pandas as pd
from datetime import datetime
from typing import Optional
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

class RFMAnalyzer:
    """
    A class to perform RFM (Recency, Frequency, Monetary) analysis on customer transaction data.
    Supports scoring, segmentation, and optional KNN-based classification of unknown segments.
    """

    def __init__(self, data_file) -> None:
        """
        Initialize the RFMAnalyzer with data from a CSV file.

        Parameters:
        - data_file (str): Path to the input CSV file containing transaction data.
        
        Raises:
        - ValueError: If the CSV is empty, or lacks required columns.
        """
        self.df = pd.read_csv(data_file, encoding='utf-8-sig')
        if self.df.empty:
            raise ValueError(f"Input file '{data_file}' is empty.")
        if 'card_code' not in self.df.columns:
            raise ValueError("CSV must contain a 'card_code' column for customer IDs.")
        self._preprocess_data()
        if 'discount_card' in self.df.columns and self.df['discount_card'].notna().any():
            self.customer_df = self.df[self.df['discount_card'].notna()].copy()
        else:
            self.customer_df = self.df.copy()
        self.customer_df['date'] = pd.to_datetime(self.customer_df['date'], errors='coerce')
        if self.customer_df['date'].isna().all():
            raise ValueError("All 'date' values are NaT after parsing; check your 'date' column format.")
        self.analysis_date = self.customer_df['date'].max() + pd.Timedelta(days=1)
        self.rfm: Optional[pd.DataFrame] = None

    def _preprocess_data(self) -> None:
        """
        Internal method to convert relevant date columns to datetime format.
        Truncates 'date' to only include YYYY-MM-DD.
        """
        for col in ['date', 'issue_date', 'date_of_birth']:
            if col in self.df.columns:
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
        self.df['date'] = self.df['date'].dt.strftime('%Y-%m-%d')

    def calculate_rfm(self) -> pd.DataFrame:
        """
        Calculate Recency, Frequency, and Monetary metrics per customer.

        Returns:
        - pd.DataFrame: DataFrame with 'card_code', 'recency', 'frequency', and 'monetary' columns.
        """
        self.rfm = (
            self.customer_df
            .groupby('card_code')
            .agg(
                recency   = ('date', lambda x: (self.analysis_date - x.max()).days),
                frequency = ('card_code', 'count'),
                monetary  = ('transaction_amount', 'sum')
            )
            .reset_index()
        )
        return self.rfm

    def score_rfm(self) -> pd.DataFrame:
        """
        Assign scores to Recency, Frequency, and Monetary values using fixed intervals.

        Returns:
        - pd.DataFrame: RFM table with added 'r_score', 'f_score', 'm_score', 'rfm_score', and 'rfm_sum'.
        
        Raises:
        - ValueError: If calculate_rfm() has not been run yet.
        """
        if self.rfm is None:
            raise ValueError("Run calculate_rfm() first.")
        def r_score(x): return 5 if x < 5 else 4 if x < 15 else 3 if x < 30 else 2 if x < 60 else 1
        def f_score(x): return 5 if x > 100 else 4 if x > 75 else 3 if x > 40 else 2 if x > 15 else 1
        def m_score(x): return 5 if x > 300_000 else 4 if x > 200_000 else 3 if x > 100_000 else 2 if x > 50_000 else 1

        self.rfm['r_score'] = self.rfm['recency'].apply(r_score)
        self.rfm['f_score'] = self.rfm['frequency'].apply(f_score)
        self.rfm['m_score'] = self.rfm['monetary'].apply(m_score)

        self.rfm['rfm_score'] = (
            self.rfm['r_score'].astype(str)
            + self.rfm['f_score'].astype(str)
            + self.rfm['m_score'].astype(str)
        )
        self.rfm['rfm_sum'] = self.rfm[['r_score', 'f_score', 'm_score']].sum(axis=1, numeric_only=True)
        return self.rfm

    def segment_customers(self) -> pd.DataFrame:
        """
        Assign customers to behavioral segments based on their RFM score.

        Returns:
        - pd.DataFrame: Updated RFM table with customer segment labels.

        Raises:
        - ValueError: If score_rfm() has not been run yet.
        """
        if self.rfm is None:
            raise ValueError("Run score_rfm() first.")

        segment_map = {
            r'555|554|545|455|554|544|445|454|544': 'Champions',
            r'4[4-5][4-5]|[4-5][4-5][4-5]|5[4-5][4-5]': 'Loyal Customers',
            r'3[3-5][3-5]|[3-5][3-5][3-5]|4[2-4][2-4]': 'Potential Loyalists',
            r'2[4-5][4-5]|3[2-4][4-5]|4[1-3][4-5]': 'Big Spenders',
            r'[1-2][1-2][1-3]|2[1-2][1-2]|1[2-3][1-2]': 'Leaving Customers'
        }

        self.rfm['segment'] = (
            self.rfm['rfm_score']
            .replace(segment_map, regex=True)
            .where(lambda s: ~s.str.fullmatch(r'\d{3}'), other=self.rfm['rfm_score'])
        )

        demo = []
        for c in ['gender', 'date_of_birth']:
            if c in self.customer_df.columns:
                demo.append(c)
        if demo:
            details = self.customer_df[['card_code'] + demo].drop_duplicates()
            self.rfm = self.rfm.merge(details, on='card_code', how='left')
            if 'date_of_birth' in demo:
                self.rfm['age'] = ((self.analysis_date - pd.to_datetime(self.rfm['date_of_birth']))
                                    .dt.days // 365)

        self.classify_unknown_segments()
        return self.rfm

    def classify_unknown_segments(self, k: int = 5) -> pd.DataFrame:
        """
        Use KNN to classify customers whose segment is still an RFM numeric code.

        Parameters:
        - k (int): Number of neighbors to use in KNN classifier.

        Returns:
        - pd.DataFrame: DataFrame of the reclassified rows.
        
        Raises:
        - ValueError: If segment_customers() has not been run yet.
        """
        if self.rfm is None:
            raise ValueError("Run segment_customers() first.")
        mask = self.rfm['segment'].str.fullmatch(r'\d{3}')
        if not mask.any():
            return pd.DataFrame(columns=self.rfm.columns)

        known = self.rfm[~mask]
        unknown = self.rfm[mask]
        Xk = known[['r_score','f_score','m_score']]
        yk = known['segment']
        Xu = unknown[['r_score','f_score','m_score']]
        scaler = StandardScaler()
        Xk_s = scaler.fit_transform(Xk)
        Xu_s = scaler.transform(Xu)
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(Xk_s, yk)
        preds = knn.predict(Xu_s)
        self.rfm.loc[mask, 'segment'] = preds
        return self.rfm.loc[mask].copy()

    def analyze_segments(self) -> pd.DataFrame:
        """
        Generate summary statistics for each customer segment.

        Returns:
        - pd.DataFrame: Aggregated metrics including mean R, F, M, age, count, and percentage.
        
        Raises:
        - ValueError: If segment_customers() has not been run yet.
        """
        if self.rfm is None:
            raise ValueError("Run segment_customers() first.")
        result = (
            self.rfm
            .groupby('segment')
            .agg(
                recency   = ('recency','mean'),
                frequency = ('frequency','mean'),
                monetary  = ('monetary','mean'),
                count     = ('card_code','count'),
                age       = ('age','mean')
            )
        )
        result['percentage'] = (result['count']/result['count'].sum())*100
        return result.sort_values('count', ascending=False)

    def save_results(self, filename: str = 'example_data/rfm_results.csv') -> None:
        """
        Save the RFM table with segments to a CSV file.

        Parameters:
        - filename (str): Output file path. Default is 'example_data/rfm_results.csv'.

        Raises:
        - ValueError: If RFM analysis has not been performed yet.
        """
        if self.rfm is None:
            raise ValueError("Nothing to save; run your analysis first.")
        self.rfm.to_csv(filename, index=False, encoding='utf-8-sig')
