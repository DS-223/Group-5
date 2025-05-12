from db_ops.extract_and_save import extract_transaction_data
from db_ops.db_writer import save_csv_to_db
from utils.rfm_analyzer import RFMAnalyzer
from utils.survival_analyzer import SurvivalAnalyzer

def main():
    # Step 1: Extract data from DB and save to CSV
    extract_transaction_data(csv_path="customer_transactions.csv")

    # Step 2: Initialize RFM Analyzer
    analyzer = RFMAnalyzer("customer_transactions.csv")

    # Step 3: Run full RFM analysis
    analyzer.calculate_rfm()
    analyzer.score_rfm()
    analyzer.segment_customers()

    # Step 4: Analyze and print segment summary
    segment_summary = analyzer.analyze_segments()
    print("\n--- Customer Segment Summary ---")
    print(segment_summary)

    # Step 5: Save detailed results
    analyzer.save_results("outputs/rfm_results.csv")
    print("\nRFM results saved to 'outputs/rfm_results.csv'.")

    # Save RFM results to DB
    save_csv_to_db("example_data/rfm_results.csv", table_name="RFMResults")

    #-----------------------------------------------------------------------------

    survival_analyzer = SurvivalAnalyzer()

    survival_analyzer.fit_cox_model()
    survival_analyzer.fit_weibull_model()

    survival_analyzer.print_model_summaries()
    survival_analyzer.save_model_summaries()

    survival_analyzer.plot_weibull_survival_function()
    survival_analyzer.plot_custom_profiles()


if __name__ == "__main__":
    main()
