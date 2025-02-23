import random

class PokerGameVariant:
    def __init__(self, variant="Texas Hold'em"):
        """
        Initialize the game variant.
        Supported variants: Texas Hold'em, Omaha, Short Deck, Five-Card Draw
        """
        self.variant = variant
        self.deck = self.create_deck()
        random.shuffle(self.deck)

    def create_deck(self):
        """Creates a deck based on the poker variant."""
        ranks = "23456789TJQKA"
        suits = "♠♥♦♣"
        deck = [r + s for r in ranks for s in suits]

        if self.variant == "Short Deck":
            deck = [c for c in deck if c[0] not in "2345"]  # Remove 2,3,4,5

        return deck

    def deal_hole_cards(self):
        """Deals hole cards based on the poker variant."""
        if self.variant == "Texas Hold'em":
            return [self.deck.pop(), self.deck.pop()]
        elif self.variant == "Omaha":
            return [self.deck.pop() for _ in range(4)]
        elif self.variant == "Five-Card Draw":
            return [self.deck.pop() for _ in range(5)]
        elif self.variant == "Short Deck":
            return [self.deck.pop(), self.deck.pop()]

    def deal_community_cards(self):
        """Deals community cards (Flop, Turn, River) for shared-board variants."""
        if self.variant in ["Texas Hold'em", "Omaha", "Short Deck"]:
            return [self.deck.pop() for _ in range(5)]
        return []

# Example Usage:
game = PokerGameVariant(variant="Omaha")
hole_cards = game.deal_hole_cards()
community_cards = game.deal_community_cards()

print(f"🃏 Variant: {game.variant}")
print(f"👤 Hole Cards: {hole_cards}")
print(f"🏆 Community Cards: {community_cards}")
