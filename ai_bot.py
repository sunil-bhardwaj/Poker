import random
from ai_hand_strength import estimate_hand_strength

class PokerBot:
    def __init__(self, name="AI_Bot", difficulty="medium"):
        self.name = name
        self.difficulty = difficulty  # "easy", "medium", "hard"
        self.aggression = {"easy": 0.3, "medium": 0.6, "hard": 0.9}[difficulty]

    def make_decision(self, hole_cards, community_cards, pot, min_bet, current_bet):
        """
        AI bot makes a decision based on hand strength and aggression level.
        """
        win_prob = estimate_hand_strength(hole_cards, community_cards)
        action = "fold"

        if win_prob > 0.8 or random.random() < self.aggression:
            action = "raise"
            bet = min(max(current_bet * 2, min_bet), pot // 2)
        elif win_prob > 0.5:
            action = "call"
            bet = current_bet
        else:
            action = "fold"
            bet = 0

        return action, bet

# Example Usage:
bot = PokerBot(difficulty="hard")
hole_cards = ['Ah', 'Kh']
community_cards = ['Qs', 'Jd', '9h']
pot = 500
min_bet = 20
current_bet = 50

action, bet = bot.make_decision(hole_cards, community_cards, pot, min_bet, current_bet)
print(f"AI Bot action: {action}, Bet: {bet}")
