import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import os

from db_ops.extract_and_save import extract_survival_data
from lifelines import CoxPHFitter, WeibullAFTFitter


class SurvivalAnalyzer:
    """
    A class to perform survival analysis on customer data using 
    Cox Proportional Hazards and Weibull AFT models.

    Data is extracted from a database using extract_survival_data,
    and both model fitting and visualization capabilities are provided.
    """

    def __init__(self, csv_path='outputs/survival_data.csv'):
        """
        Initializes the SurvivalAnalyzer by extracting data and loading it into memory.

        Parameters:
        csv_path (str): Path to the CSV file to store or read survival data.
        """
        extract_survival_data(csv_path)
        self.data = pd.read_csv(csv_path)
        print("Missing values per column:")
        print(self.data[['duration', 'event', 'Age', 'Gender']].isnull().sum())
        self.data = self.data.dropna(subset=['duration', 'event', 'Age', 'Gender'])
        self.models = {}

    def fit_cox_model(self):
        """
        Fits a Cox Proportional Hazards model using duration, event, age, and gender.
        """
        self.data = self.data.dropna(subset=['duration', 'event', 'Age', 'Gender'])
        self.cph = CoxPHFitter()
        self.cph.fit(self.data[['duration', 'event', 'Age', 'Gender']],
                 duration_col='duration', event_col='event')
        self.models['CoxPH'] = self.cph

    def fit_weibull_model(self):
        """
        Fits a Weibull AFT (Accelerated Failure Time) model using duration, event, age, and gender.
        """
        self.data = self.data.dropna(subset=['duration', 'event', 'Age', 'Gender'])
        self.weibull = WeibullAFTFitter()
        self.weibull.fit(self.data[['duration', 'event', 'Age', 'Gender']],
                     duration_col='duration', event_col='event')
        self.models['WeibullAFT'] = self.weibull

    def save_model_summaries(self, output_folder='outputs'):
        """
        Saves model summary tables (coefficients, standard errors, etc.) as CSV files.

        Parameters:
        output_folder (str): Directory where the summary files will be saved.
        """
        os.makedirs(output_folder, exist_ok=True)

        for model_name, model in self.models.items():
            output_path = os.path.join(output_folder, f"{model_name}_summary.csv")
            if hasattr(model, 'summary') and model.summary is not None:
                model.summary.to_csv(output_path, index=False)

    def print_model_summaries(self):
        """
        Prints the summary statistics of the fitted Cox and Weibull models to the console.
        """
        print("📄 Cox Proportional Hazards Summary:")
        self.cph.print_summary()
        print("\n📄 Weibull AFT Summary:")
        self.weibull.print_summary()

    def plot_weibull_survival_function(self,filename='outputs/weibull_survival_curve.png'):
        """
        Plots the Weibull survival function using the median values of covariates 
        and saves it to a file.

        Parameters:
        filename (str): Name of the PNG file to save the plot.
        """
        median_values = self.data[['Age', 'Gender']].median().to_frame().T
        plt.figure()
        self.weibull.predict_survival_function(median_values).plot()
        plt.title('Weibull AFT Survival Curve (Median Covariates)')
        plt.xlabel('Days Since Registration')
        plt.ylabel('Survival Probability')
        plt.grid()
        plt.savefig(filename, bbox_inches='tight')
        plt.close()

    def plot_custom_profiles(self, filename='outputs/weibull_custom_profiles.png'):
        """
        Plots Weibull survival functions for two custom customer profiles 
        (e.g., young male and old female) and saves the plot.

        Parameters:
        filename (str): Name of the PNG file to save the plot.
        """
        profiles = pd.DataFrame([
            {'Age': 25, 'Gender': 0},  # young male
            {'Age': 65, 'Gender': 1},  # old female
        ])

        plt.figure()
        surv_funcs = self.weibull.predict_survival_function(profiles)
        for i, row in profiles.iterrows():
            label = f"Age={row['Age']}, Gender={'Male' if row['Gender']==0 else 'Female'}"
            plt.plot(surv_funcs.index, surv_funcs.iloc[:, i], label=label)

        plt.title("Weibull AFT Survival Curves by Profile")
        plt.xlabel("Days Since Registration")
        plt.ylabel("Survival Probability")
        plt.legend()
        plt.grid()
        plt.savefig(filename, bbox_inches='tight')
        plt.close()
