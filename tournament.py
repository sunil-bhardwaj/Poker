import time
import threading

class PokerTournament:
    def __init__(self, name, buy_in, num_players, blind_structure):
        """
        Initializes a tournament with buy-in, number of players, and blind levels.
        """
        self.name = name
        self.buy_in = buy_in
        self.num_players = num_players
        self.players = {f"Player_{i+1}": buy_in for i in range(num_players)}
        self.blind_structure = blind_structure  # List of (time, small_blind, big_blind)
        self.current_blinds = (blind_structure[0][1], blind_structure[0][2])
        self.running = False

    def start_tournament(self):
        """Starts the poker tournament."""
        print(f"🏆 Tournament '{self.name}' started with {self.num_players} players!")
        self.running = True
        threading.Thread(target=self.increase_blinds, daemon=True).start()

    def increase_blinds(self):
        """Increases the blinds based on the blind structure over time."""
        for level in self.blind_structure:
            time.sleep(level[0])  # Wait for the blind duration
            self.current_blinds = (level[1], level[2])
            print(f"🔺 Blinds increased: {self.current_blinds}")

            if not self.running:
                break

    def player_eliminated(self, player_id):
        """Handles player elimination."""
        if player_id in self.players:
            del self.players[player_id]
            print(f"💀 {player_id} eliminated! {len(self.players)} players left.")

        if len(self.players) == 1:
            self.end_tournament()

    def end_tournament(self):
        """Ends the tournament and declares a winner."""
        winner = list(self.players.keys())[0]
        print(f"🏅 Tournament '{self.name}' Winner: {winner}")
        self.running = False

# Example Usage:
blind_structure = [(60, 10, 20), (120, 20, 40), (180, 50, 100)]  # (Time in seconds, SB, BB)
tournament = PokerTournament(name="Texas Hold'em Championship", buy_in=1000, num_players=5, blind_structure=blind_structure)
tournament.start_tournament()

# Simulating player eliminations
time.sleep(10)
tournament.player_eliminated("Player_3")
time.sleep(10)
tournament.player_eliminated("Player_1")
