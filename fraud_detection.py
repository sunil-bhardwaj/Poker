import numpy as np
import time
import random

class AIFraudDetection:
    def __init__(self):
        """
        Initializes the fraud detection system with thresholds.
        - Chip Dumping: Detects players intentionally losing to another player.
        - Collusion: Detects players sharing hole card information.
        - Bot Behavior: Identifies unnatural or instant decisions.
        """
        self.chip_dump_threshold = 0.8  # If one player wins >80% from another, flag it
        self.collusion_threshold = 0.75  # If players fold together >75%, flag it
        self.bot_reaction_threshold = 0.5  # If reaction times are too consistent, flag it

        self.player_wins = {}  # Track how often one player wins against another
        self.fold_patterns = {}  # Track simultaneous folds
        self.reaction_times = {}  # Track average reaction time per player

    def detect_chip_dumping(self, game_history):
        """
        Detects chip dumping by analyzing win percentages between players.
        """
        for game in game_history:
            winner, loser, amount = game  # (winner_id, loser_id, chip_amount)
            if loser not in self.player_wins:
                self.player_wins[loser] = {}

            self.player_wins[loser][winner] = self.player_wins[loser].get(winner, 0) + 1

        for loser, winners in self.player_wins.items():
            for winner, count in winners.items():
                total_matches = sum(winners.values())
                win_ratio = count / total_matches
                if win_ratio > self.chip_dump_threshold:
                    print(f"🚨 Possible chip dumping detected: {winner} wins {win_ratio*100:.2f}% from {loser}!")

    def detect_collusion(self, fold_history):
        """
        Detects collusion by checking if two players frequently fold together.
        """
        for hand in fold_history:
            players_folded = tuple(sorted(hand))  # (player1, player2, ...)
            self.fold_patterns[players_folded] = self.fold_patterns.get(players_folded, 0) + 1

        for pair, count in self.fold_patterns.items():
            total_hands = sum(self.fold_patterns.values())
            collusion_ratio = count / total_hands
            if collusion_ratio > self.collusion_threshold:
                print(f"🚨 Possible collusion detected: {pair} fold together {collusion_ratio*100:.2f}% of the time!")

    def detect_bot_behavior(self, reaction_times):
        """
        Detects bots based on consistent reaction times.
        """
        for player, times in reaction_times.items():
            avg_time = np.mean(times)
            std_dev = np.std(times)
            if std_dev < self.bot_reaction_threshold:
                print(f"🚨 Possible bot detected: {player} has reaction times too consistent (Avg: {avg_time:.2f}s)")

# Example Usage:
fraud_detector = AIFraudDetection()

# Simulated chip dumping scenario
game_history = [("Player_1", "Player_2", 500), ("Player_1", "Player_2", 700), ("Player_1", "Player_2", 800)]
fraud_detector.detect_chip_dumping(game_history)

# Simulated collusion scenario
fold_history = [("Player_3", "Player_4"), ("Player_3", "Player_4"), ("Player_3", "Player_4")]
fraud_detector.detect_collusion(fold_history)

# Simulated bot behavior scenario
reaction_times = {"Player_5": [0.99, 1.01, 1.02, 1.00, 0.98], "Player_6": [1.5, 2.1, 1.8, 1.4]}
fraud_detector.detect_bot_behavior(reaction_times)
