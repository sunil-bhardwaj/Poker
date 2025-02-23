import random
import numpy as np

class AIPokerBot:
    def __init__(self, name="AI_Bot", aggression=0.5, bluff_factor=0.3):
        """
        Initializes the AI poker bot.
        - aggression: Likelihood of aggressive plays (0.0 - 1.0)
        - bluff_factor: Probability of bluffing (0.0 - 1.0)
        """
        self.name = name
        self.aggression = aggression
        self.bluff_factor = bluff_factor

    def evaluate_hand(self, hole_cards, community_cards):
        """
        Basic hand strength evaluation (simplified for bot play).
        Returns a score from 0 to 1.
        """
        all_cards = hole_cards + community_cards
        unique_ranks = {card[0] for card in all_cards}
        unique_suits = {card[1] for card in all_cards}

        # Basic hand evaluation: Pair, Flush, Straight detection
        score = 0.1 * len(unique_ranks)  # More unique ranks = weaker hand
        if len(unique_ranks) <= 4:  # Pair or better
            score += 0.3
        if len(unique_suits) == 1:  # Flush possibility
            score += 0.3

        return min(score, 1.0)  # Normalize to 0-1 range

    def make_decision(self, hole_cards, community_cards, pot_odds):
        """
        AI decision-making based on hand strength, pot odds, and aggression level.
        """
        hand_strength = self.evaluate_hand(hole_cards, community_cards)
        decision = "fold"

        # AI Adjusted Decision Logic
        if hand_strength > 0.7 or random.random() < self.aggression:
            decision = "raise" if random.random() > self.bluff_factor else "bluff"
        elif hand_strength > 0.4 or pot_odds > 0.5:
            decision = "call"
        
        return decision

# Example Usage:
ai_bot = AIPokerBot(name="Bot_1", aggression=0.6, bluff_factor=0.2)

hole_cards = ["A♠", "K♦"]
community_cards = ["Q♠", "J♣", "10♥"]

decision = ai_bot.make_decision(hole_cards, community_cards, pot_odds=0.4)
print(f"🤖 {ai_bot.name} Decision: {decision}")
