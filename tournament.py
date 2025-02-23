import time
import random
import threading

class PokerTournament:
    def __init__(self, name, starting_chips, blind_structure, min_players=2, max_players=100):
        """
        Initializes a poker tournament.
        - name: Tournament name
        - starting_chips: Initial stack for players
        - blind_structure: List of (small_blind, big_blind, duration_seconds)
        - min_players: Minimum required players
        - max_players: Maximum allowed players
        """
        self.name = name
        self.starting_chips = starting_chips
        self.blind_structure = blind_structure
        self.min_players = min_players
        self.max_players = max_players
        self.players = {}
        self.running = False
        self.current_blind_level = 0

    def register_player(self, player_id):
        """Registers a player if the tournament hasn't started."""
        if self.running or len(self.players) >= self.max_players:
            return f"🚫 Registration closed for {self.name}."
        self.players[player_id] = self.starting_chips
        return f"✅ {player_id} joined {self.name}."

    def start_tournament(self):
        """Starts the tournament if enough players have joined."""
        if len(self.players) < self.min_players:
            return "⚠️ Not enough players to start."
        
        self.running = True
        print(f"🏆 {self.name} has started with {len(self.players)} players!")
        
        # Start blind level increases
        threading.Thread(target=self.increase_blinds, daemon=True).start()
        return "🃏 Tournament in progress..."

    def increase_blinds(self):
        """Increases blinds at set intervals based on blind structure."""
        for level, (small_blind, big_blind, duration) in enumerate(self.blind_structure):
            if not self.running:
                break
            self.current_blind_level = level
            print(f"🔺 Blinds increased! Small Blind: {small_blind}, Big Blind: {big_blind}")
            time.sleep(duration)

        print("🏁 Tournament blinds complete.")

    def eliminate_player(self, player_id):
        """Eliminates a player when they lose all chips."""
        if player_id in self.players:
            del self.players[player_id]
            print(f"❌ {player_id} has been eliminated.")
            if len(self.players) == 1:
                winner = list(self.players.keys())[0]
                print(f"🎉 {winner} wins {self.name}!")
                self.running = False

# Example Usage:
blind_structure = [(10, 20, 60), (20, 40, 60), (50, 100, 120)]  # (SB, BB, duration in sec)
tournament = PokerTournament(name="Sunday Major", starting_chips=1500, blind_structure=blind_structure)

print(tournament.register_player("Player_1"))
print(tournament.register_player("Player_2"))

print(tournament.start_tournament())

# Simulate gameplay
time.sleep(130)  # Let blinds increase
tournament.eliminate_player("Player_1")
tournament.eliminate_player("Player_2")
