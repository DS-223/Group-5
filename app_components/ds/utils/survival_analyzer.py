import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import os

from db_ops.extract_and_save import extract_survival_data
from lifelines import (
    KaplanMeierFitter, CoxPHFitter
)

class SurvivalAnalyzer:
    def __init__(self, csv_path='survival_data.csv'):
        # Extract and load data from SQL
        extract_survival_data(csv_path)
        self.data = pd.read_csv(csv_path)
        self.models = {}

    def fit_non_personalized_model(self):
        # Kaplan-Meier (non-personalized)
        self.kmf = KaplanMeierFitter()
        self.kmf.fit(self.data['duration'], event_observed=self.data['event'])
        self.models['KaplanMeier'] = self.kmf

    def save_kaplan_meier_plot(self, filename='kaplan_meier_curve.png'):
        plt.figure()
        self.kmf.plot_survival_function()
        plt.title('Non-Personalized Survival Curve (Kaplan-Meier)')
        plt.xlabel('Days Since Registration')
        plt.ylabel('Survival Probability')
        plt.grid()
        plt.savefig(filename, bbox_inches='tight')
        plt.close()

    def fit_personalized_model(self):
        # Cox Proportional Hazards (personalized)
        self.cph = CoxPHFitter()
        self.cph.fit(self.data[['duration', 'event', 'Age', 'Gender']],
                     duration_col='duration', event_col='event')
        self.models['CoxPH'] = self.cph

    def save_model_summaries(self, output_folder='outputs'):
        os.makedirs(output_folder, exist_ok=True)

        for model_name, model in self.models.items():
            output_path = os.path.join(output_folder, f"{model_name}_summary.csv")

            if hasattr(model, 'summary') and model.summary is not None:
                df = model.summary.copy()
                df.to_csv(output_path, index=False)
            elif model_name == 'KaplanMeier':
                df = model.survival_function_.reset_index()
                df.to_csv(output_path, index=False)

    def print_cox_summary(self):
        self.cph.print_summary()

