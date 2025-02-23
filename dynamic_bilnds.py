import time
import threading

class DynamicBlinds:
    def __init__(self, start_small_blind, start_big_blind, increase_interval, increase_factor):
        """
        Initializes the blind structure with dynamic increases.
        - start_small_blind: Initial Small Blind
        - start_big_blind: Initial Big Blind
        - increase_interval: Time (seconds) after which blinds increase
        - increase_factor: Multiplier to increase blinds each level
        """
        self.small_blind = start_small_blind
        self.big_blind = start_big_blind
        self.increase_interval = increase_interval
        self.increase_factor = increase_factor
        self.running = False

    def start_blind_timer(self):
        """Starts the blind increase timer."""
        self.running = True
        threading.Thread(target=self.increase_blinds, daemon=True).start()

    def increase_blinds(self):
        """Automatically increases blinds at set intervals."""
        while self.running:
            time.sleep(self.increase_interval)  # Wait for the next blind level
            self.small_blind = int(self.small_blind * self.increase_factor)
            self.big_blind = int(self.big_blind * self.increase_factor)
            print(f"🔺 Blinds increased! Small Blind: {self.small_blind}, Big Blind: {self.big_blind}")

    def stop_blinds(self):
        """Stops blind increases (e.g., when tournament ends)."""
        self.running = False

# Example Usage:
blinds = DynamicBlinds(start_small_blind=10, start_big_blind=20, increase_interval=60, increase_factor=1.5)
blinds.start_blind_timer()

# Simulating gameplay for 3 minutes before stopping
time.sleep(180)
blinds.stop_blinds()
print("🏁 Tournament Ended. Final Blind Levels:", blinds.small_blind, blinds.big_blind)
