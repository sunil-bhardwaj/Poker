import random

class TexasHoldemGame:
    def __init__(self):
        self.players = {}
        self.community_cards = []
        self.pot = 0

    def process_action(self, player_id, action):
        if action["action"] == "bet":
            amount = action["amount"]
            self.pot += amount
            return f"💰 {player_id} bets {amount} chips!"
        
        elif action["action"] == "fold":
            return f"🃏 {player_id} folds."
        
        elif action["action"] == "showdown":
            return self.determine_winner()

    def determine_winner(self):
        winner = random.choice(list(self.players.keys()))
        return f"🏆 {winner} wins {self.pot} chips!"
