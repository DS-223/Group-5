# from utils.data_generator import DataGenerator
# from utils.rfm_analyzer import RFMAnalyzer
# from utils.recommender import Recommender

# def main():
#     # Generate data
#     generator = DataGenerator()
#     df = generator.save_data()

#     # Perform RFM analysis
#     analyzer = RFMAnalyzer()
#     analyzer.calculate_rfm()
#     analyzer.score_rfm()
#     rfm = analyzer.segment_customers()
#     segment_analysis = analyzer.analyze_segments()
#     analyzer.save_results()

#     # Print segment analysis
#     print("RFM Segment Analysis:")
#     print(segment_analysis)

#     # Get recommendations
#     recommender = Recommender()
#     recommendations = recommender.get_recommendations(segment_analysis.index)
#     print("\nMarketing Recommendations:")
#     for rec in recommendations:
#         print(rec)

# if __name__ == "__main__":
#     main()


from utils.data_generator import DataGenerator
from utils.rfm_analyzer import RFMAnalyzer
from utils.recommender import Recommender

def main():
    # === Step 1: Generate and Save Synthetic Data ===
    data_filename = 'synthetic_retail_data.csv'
    generator = DataGenerator()
    generator.generate_customers()
    df = generator.save_data(filename=data_filename)
    print(f"✅ Synthetic data saved to '{data_filename}'.")

    # === Step 2: Perform RFM Analysis ===
    analyzer = RFMAnalyzer(data_file=data_filename)
    analyzer.calculate_rfm()
    analyzer.score_rfm()
    rfm = analyzer.segment_customers()
    segment_analysis = analyzer.analyze_segments()

    # Save RFM results
    rfm_filename = 'rfm_results.csv'
    analyzer.save_results(filename=rfm_filename)
    print(f"✅ RFM results saved to '{rfm_filename}'.")

    # === Step 3: Print Segment Analysis ===
    print("\n📊 RFM Segment Analysis:")
    print(segment_analysis)

    # === Step 4: Get and Print Marketing Recommendations ===
    recommender = Recommender()
    recommendations = recommender.get_recommendations(segment_analysis.index)

    print("\n💡 Marketing Recommendations:")
    for rec in recommendations:
        print(f"- {rec}")

if __name__ == "__main__":
    main()
