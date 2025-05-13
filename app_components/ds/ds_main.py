from db_ops.extract_and_save import extract_transaction_data
from db_ops.db_writer import save_csv_to_db
from utils.rfm_analyzer import RFMAnalyzer
from utils.survival_analyzer import SurvivalAnalyzer

def main():
    """
    Main pipeline to perform customer RFM analysis and survival analysis.

    This function executes the following steps:
    1. Extracts transaction data from the database and saves it as a CSV.
    2. Runs full RFM (Recency, Frequency, Monetary) analysis:
        - Calculates RFM metrics
        - Scores each customer
        - Segments customers based on scores
    3. Prints and saves RFM segment summaries to both CSV and the database.
    4. Performs survival analysis using Cox PH and Weibull AFT models:
        - Fits models
        - Prints and saves summaries
        - Plots survival curves and custom profiles
        - Saves outputs to the database
    """

    # Step 1: Extract data from DB and save to CSV
    extract_transaction_data(csv_path="outputs/customer_transactions.csv")

    # Step 2: Initialize RFM Analyzer with the extracted data
    analyzer = RFMAnalyzer("outputs/customer_transactions.csv")

    # Step 3: Run full RFM analysis
    analyzer.calculate_rfm()         # Compute Recency, Frequency, Monetary values
    analyzer.score_rfm()             # Assign scores to each metric
    analyzer.segment_customers()     # Assign customer segments based on RFM scores

    # Step 4: Analyze and print segment summary
    segment_summary = analyzer.analyze_segments()
    print("\n--- Customer Segment Summary ---")
    print(segment_summary)

    # Step 5: Save detailed RFM results to CSV
    analyzer.save_results("outputs/rfm_results.csv")
    print("\nRFM results saved to 'outputs/rfm_results.csv'.")

    # Step 6: Save RFM results to the database
    save_csv_to_db("outputs/rfm_results.csv", table_name="RFMResults")

    # -------------------------------------------------------------------------

    # Step 7: Initialize and run survival analysis
    survival_analyzer = SurvivalAnalyzer()

    # Fit both Cox Proportional Hazards and Weibull AFT models
    survival_analyzer.fit_cox_model()
    survival_analyzer.fit_weibull_model()

    # Display and save model summaries
    survival_analyzer.print_model_summaries()
    survival_analyzer.save_model_summaries()

    # Step 8: Generate survival plots
    survival_analyzer.plot_weibull_survival_function()
    survival_analyzer.plot_custom_profiles()

    # Step 9: Save survival analysis results to the database
    save_csv_to_db("outputs/survival_data.csv", table_name="SurvivalData")
    save_csv_to_db("outputs/CoxPH_summary.csv", table_name="CoxPHSummary")
    save_csv_to_db("outputs/WeibullAFT_summary.csv", table_name="WeibullAFTSummary")


if __name__ == "__main__":
    main()
