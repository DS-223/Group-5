from utils.data_generator import DataGenerator
from utils.rfm_analyzer import RFMAnalyzer
from utils.recommender import Recommender

def main():
    # Generate data
    generator = DataGenerator()
    df = generator.save_data()

    # Perform RFM analysis
    analyzer = RFMAnalyzer()
    analyzer.calculate_rfm()
    analyzer.score_rfm()
    rfm = analyzer.segment_customers()
    segment_analysis = analyzer.analyze_segments()
    analyzer.save_results()

    # Print segment analysis
    print("RFM Segment Analysis:")
    print(segment_analysis)

    # Get recommendations
    recommender = Recommender()
    recommendations = recommender.get_recommendations(segment_analysis.index)
    print("\nMarketing Recommendations:")
    for rec in recommendations:
        print(rec)

if __name__ == "__main__":
    main()