import numpy as np
import datetime
from collections import defaultdict

class FraudDetection:
    def __init__(self):
        self.player_stats = defaultdict(lambda: {"total_bets": 0, "wins": 0, "losses": 0, "suspicious_transfers": 0})
        self.bet_timestamps = defaultdict(list)

    def track_bet(self, player_id, amount, timestamp=None):
        """Track bets to detect suspicious patterns."""
        timestamp = timestamp or datetime.datetime.now()
        self.bet_timestamps[player_id].append(timestamp)
        self.player_stats[player_id]["total_bets"] += amount

    def track_win_loss(self, player_id, won=True):
        """Track win/loss ratios to detect chip dumping."""
        if won:
            self.player_stats[player_id]["wins"] += 1
        else:
            self.player_stats[player_id]["losses"] += 1

    def detect_chip_dumping(self, player_id):
        """Detects if a player is intentionally losing to another."""
        losses = self.player_stats[player_id]["losses"]
        bets = self.player_stats[player_id]["total_bets"]
        if losses > 10 and bets > 1000 and (losses / bets) > 0.8:
            return f"🚨 Player {player_id} is suspected of chip dumping!"
        return None

    def detect_collusion(self, player1, player2):
        """Detects if two players are frequently betting against each other in a suspicious way."""
        timestamps1 = np.array([t.timestamp() for t in self.bet_timestamps[player1]])
        timestamps2 = np.array([t.timestamp() for t in self.bet_timestamps[player2]])
        if len(timestamps1) > 5 and len(timestamps2) > 5:
            time_diff = np.abs(timestamps1[:, None] - timestamps2)
            if (time_diff < 2).sum() > 5:  # If 5+ bets happen within 2 seconds
                return f"🚨 Players {player1} and {player2} might be colluding!"
        return None

    def detect_bot_behavior(self, player_id):
        """Detects if a player is acting like a bot (predictable, repetitive play)."""
        timestamps = np.array([t.timestamp() for t in self.bet_timestamps[player_id]])
        if len(timestamps) > 10:
            avg_time_between_bets = np.mean(np.diff(timestamps))
            if avg_time_between_bets < 1.5:  # If player is betting too fast
                return f"🚨 Player {player_id} is playing like a bot!"
        return None

# Example Usage:
fraud_detector = FraudDetection()
fraud_detector.track_bet("player1", 100)
fraud_detector.track_win_loss("player1", won=False)
fraud_detector.track_bet("player2", 200)
fraud_detector.track_win_loss("player2", won=True)

print(fraud_detector.detect_chip_dumping("player1"))
print(fraud_detector.detect_collusion("player1", "player2"))
print(fraud_detector.detect_bot_behavior("player1"))
