# from utils.rfm_analyzer import RFMAnalyzer

# def main():
#     # RFM Analysis using real data
#     data_filename = 'example_data/transaction_report.csv'
#     analyzer = RFMAnalyzer(data_file=data_filename)

#     analyzer.calculate_rfm()
#     analyzer.score_rfm()
#     rfm = analyzer.segment_customers()

#     # Apply KNN to classify numeric-only segments
#     reclassified = analyzer.classify_unknown_segments(k=5)
#     if not reclassified.empty:
#         print(f"🔁 Reclassified {len(reclassified)} customers using KNN.")

#     segment_analysis = analyzer.analyze_segments()

#     rfm_filename = 'outputs/rfm_results.csv'
#     analyzer.save_results(filename=rfm_filename)
#     print(f"✅ RFM results saved to '{rfm_filename}'.")

#     print("\n📊 RFM Segment Analysis:")
#     print(segment_analysis)


# main.py

from utils.extract_and_save import extract_transaction_data
from utils.rfm_analyzer import RFMAnalyzer

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

if __name__ == "__main__":
    main()
