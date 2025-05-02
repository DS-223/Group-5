import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import os

from lifelines import (
    KaplanMeierFitter, CoxPHFitter,
    NelsonAalenFitter, WeibullFitter, ExponentialFitter, LogLogisticFitter
)

class SurvivalAnalyzer:
    def __init__(self, survival_data):
        self.data = survival_data
        self.models = {}

    def fit_kaplan_meier(self):
        self.kmf = KaplanMeierFitter()
        self.kmf.fit(self.data['duration'], event_observed=self.data['event'])
        self.models['KaplanMeier'] = self.kmf

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
        self.models['CoxPH'] = self.cph

    def fit_additional_models(self):
        naf = NelsonAalenFitter()
        naf.fit(self.data['duration'], event_observed=self.data['event'])
        self.models['NelsonAalen'] = naf

        wf = WeibullFitter()
        wf.fit(self.data['duration'], event_observed=self.data['event'])
        self.models['Weibull'] = wf

        ef = ExponentialFitter()
        ef.fit(self.data['duration'], event_observed=self.data['event'])
        self.models['Exponential'] = ef

        llf = LogLogisticFitter()
        llf.fit(self.data['duration'], event_observed=self.data['event'])
        self.models['LogLogistic'] = llf


    def save_model_summaries(self, output_folder='outputs'):
        os.makedirs(output_folder, exist_ok=True)

        for model_name, model in self.models.items():
            output_path = os.path.join(output_folder, f"{model_name}_summary.csv")

            if hasattr(model, 'summary') and model.summary is not None:
                # Save parametric model summary
                df = model.summary.copy()
                df.to_csv(output_path, index=False)

            elif model_name == 'KaplanMeier':
                # Save Kaplan-Meier survival function
                df = model.survival_function_.reset_index()
                df.to_csv(output_path, index=False)

            elif model_name == 'NelsonAalen':
                # Save Nelson-Aalen cumulative hazard
                df = model.cumulative_hazard_.reset_index()
                df.to_csv(output_path, index=False)

            else:
                # Skip models with no appropriate output
                continue


    def print_cox_summary(self):
        self.cph.print_summary()
