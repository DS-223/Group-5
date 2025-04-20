class Recommender:
    def __init__(self):
        self.recommendations = {
            'Champions': "Reward them. Offer loyalty programs and exclusive previews",
            'Loyal Customers': "Upsell higher value products. Ask for reviews",
            'Potential Loyalists': "Offer membership/subscription or give them early access to new products",
            'Recent Customers': "Provide onboarding support and special offers to encourage repeat purchases",
            'Needing Attention': "Re-engage with email campaigns and recommendations based on past purchases",
            'At Risk': "Send personalized emails to win them back, offer discounts",
            'Hibernating': "Win them back with reactivation campaigns or surveys",
            'Cant Lose Them': "Make limited time offers and get feedback",
            'Lost': "Revive interest with reach out campaigns or ignore if not profitable"
        }

    def get_recommendations(self, segments):
        """Return recommendations for given segments."""
        result = []
        for segment in segments:
            if segment in self.recommendations:
                result.append(f"{segment}: {self.recommendations[segment]}")
        return result