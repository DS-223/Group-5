# from utils.data_generator import RFMDataGenerator, SurvivalDataGenerator
# from utils.rfm_analyzer import RFMAnalyzer
# from utils.survival_analyzer import SurvivalAnalyzer

# def main():
#     # RFM Analysis
#     data_filename = 'outputs/synthetic_retail_data.csv'
#     rfm_generator = RFMDataGenerator()
#     rfm_generator.generate_customers()
#     df = rfm_generator.save_data(filename=data_filename)
#     print(f"✅ Synthetic data saved to '{data_filename}'.")

#     analyzer = RFMAnalyzer(data_file=data_filename)
#     analyzer.calculate_rfm()
#     analyzer.score_rfm()
#     rfm = analyzer.segment_customers()
#     segment_analysis = analyzer.analyze_segments()

#     rfm_filename = 'outputs/rfm_results.csv'
#     analyzer.save_results(filename=rfm_filename)
#     print(f"✅ RFM results saved to '{rfm_filename}'.")

#     print("\n📊 RFM Segment Analysis:")
#     print(segment_analysis)

#     # recommender = Recommender()
#     # recommendations = recommender.get_recommendations(segment_analysis.index)

#     # print("\n💡 Marketing Recommendations:")
#     # for rec in recommendations:
#     #     print(f"- {rec}")

#     # ------------------------------------------------------------------------

#     # Survival Analysis
#     survival_generator = SurvivalDataGenerator()
#     customers = survival_generator.generate_customers()
#     cards = survival_generator.generate_cards()
#     transactions = survival_generator.generate_transactions()
#     survival_data = survival_generator.prepare_survival_data()

#     # Survival Analysis
#     analyzer = SurvivalAnalyzer(survival_data)

#     # Fit and save Kaplan-Meier plot
#     analyzer.fit_kaplan_meier()
#     analyzer.save_kaplan_meier_plot(filename='outputs/kaplan_meier_curve.png')

#     # Fit Cox model
#     analyzer.fit_cox_model()
#     analyzer.print_cox_summary()

#     # Fit additional models
#     analyzer.fit_additional_models()

#     # Save all model summaries into a CSV
#     analyzer.save_model_summaries()



# if __name__ == "__main__":
#     main()

from utils.rfm_analyzer import RFMAnalyzer
from utils.survival_analyzer import SurvivalAnalyzer
from utils.data_generator import SurvivalDataGenerator

def main():
    # RFM Analysis using real data
    data_filename = 'example_data/transaction_report.csv'
    analyzer = RFMAnalyzer(data_file=data_filename)

    analyzer.calculate_rfm()
    analyzer.score_rfm()
    rfm = analyzer.segment_customers()

    # Apply KNN to classify numeric-only segments
    reclassified = analyzer.classify_unknown_segments(k=5)
    if not reclassified.empty:
        print(f"🔁 Reclassified {len(reclassified)} customers using KNN.")

    segment_analysis = analyzer.analyze_segments()

    rfm_filename = 'outputs/rfm_results.csv'
    analyzer.save_results(filename=rfm_filename)
    print(f"✅ RFM results saved to '{rfm_filename}'.")

    print("\n📊 RFM Segment Analysis:")
    print(segment_analysis)


    # Survival Analysis (optional, still uses synthetic data)
    survival_generator = SurvivalDataGenerator()
    customers = survival_generator.generate_customers()
    cards = survival_generator.generate_cards()
    transactions = survival_generator.generate_transactions()
    survival_data = survival_generator.prepare_survival_data()

    analyzer = SurvivalAnalyzer(survival_data)
    analyzer.fit_kaplan_meier()
    analyzer.save_kaplan_meier_plot(filename='outputs/kaplan_meier_curve.png')
    analyzer.fit_cox_model()
    analyzer.print_cox_summary()
    analyzer.fit_additional_models()
    analyzer.save_model_summaries()

if __name__ == "__main__":
    main()
