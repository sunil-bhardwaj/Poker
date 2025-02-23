import numpy as np

class RakebackSystem:
    def __init__(self):
        self.tiers = {
            "Bronze": {"min_rake": 0, "percent": 5},
            "Silver": {"min_rake": 500, "percent": 10},
            "Gold": {"min_rake": 2000, "percent": 15},
            "Platinum": {"min_rake": 5000, "percent": 20}
        }

    def calculate_rakeback(self, player_id, total_rake):
        """Calculates AI-enhanced rakeback based on VIP tier."""
        tier = "Bronze"
        for t, details in self.tiers.items():
            if total_rake >= details["min_rake"]:
                tier = t

        rakeback_percent = self.tiers[tier]["percent"]
        
        # AI Model: Predict additional rewards based on playing style
        additional_reward = self.ai_predict_bonus(total_rake)

        rakeback_amount = (rakeback_percent / 100) * total_rake + additional_reward
        return {"player_id": player_id, "tier": tier, "rakeback": rakeback_amount}

    def ai_predict_bonus(self, total_rake):
        """Simulated AI model to reward frequent players dynamically."""
        # Using a sigmoid function to predict bonus rewards
        return round(50 * (1 / (1 + np.exp(-0.001 * (total_rake - 2500)))), 2)

# Example Usage:
rakeback_system = RakebackSystem()
player_rakeback = rakeback_system.calculate_rakeback("Player_1", 3000)
print(player_rakeback)
