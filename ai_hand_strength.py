import random
import numpy as np
from itertools import combinations
from poker import evaluate_hand, deck

def estimate_hand_strength(hole_cards, community_cards, num_simulations=1000):
    """
    Estimates hand strength using Monte Carlo simulations.
    
    Args:
        hole_cards (list): The player's hole cards.
        community_cards (list): The known community cards.
        num_simulations (int): Number of simulations to run.
    
    Returns:
        float: Estimated probability of winning.
    """
    remaining_deck = [card for card in deck if card not in hole_cards + community_cards]
    wins = 0

    for _ in range(num_simulations):
        random.shuffle(remaining_deck)
        opponent_hole = remaining_deck[:2]
        remaining_community = community_cards + remaining_deck[2:7 - len(community_cards)]

        my_hand_score = evaluate_hand(hole_cards + remaining_community)
        opponent_hand_score = evaluate_hand(opponent_hole + remaining_community)

        if my_hand_score > opponent_hand_score:
            wins += 1

    return wins / num_simulations

# Example Usage:
hole_cards = ['Ah', 'Kh']  # Ace of hearts, King of hearts
community_cards = ['Qs', 'Jd', '9h']  # Some community cards
win_probability = estimate_hand_strength(hole_cards, community_cards)

print(f"Estimated win probability: {win_probability:.2%}")
