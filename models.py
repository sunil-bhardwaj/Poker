from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

# ---- USER & WALLET SYSTEM ----

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    balance = Column(Float, default=0.0)
    total_winnings = Column(Float, default=0.0)
    total_rake_contributed = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    transactions = relationship("Transaction", back_populates="user")
    player_sessions = relationship("Player", back_populates="user")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    type = Column(String)  # deposit, withdrawal, rakeback
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transactions")

# ---- POKER TABLE & GAME MODELS ----

class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    max_players = Column(Integer, default=9)
    small_blind = Column(Float, default=1.0)
    big_blind = Column(Float, default=2.0)
    rake_percentage = Column(Float, default=5.0)  # House rake percentage
    is_active = Column(Boolean, default=True)

    players = relationship("Player", back_populates="table")
    games = relationship("Game", back_populates="table")

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    table_id = Column(Integer, ForeignKey("tables.id"))
    seat_number = Column(Integer)
    chips = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    is_dealer = Column(Boolean, default=False)
    is_small_blind = Column(Boolean, default=False)
    is_big_blind = Column(Boolean, default=False)

    user = relationship("User", back_populates="player_sessions")
    table = relationship("Table", back_populates="players")
    hands = relationship("Hand", back_populates="player")
    bets = relationship("Bet", back_populates="player")

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, ForeignKey("tables.id"))
    status = Column(Enum("waiting", "pre-flop", "flop", "turn", "river", "showdown"), default="waiting")
    pot_size = Column(Float, default=0.0)
    community_cards = Column(String, default="")  # Store as comma-separated values
    created_at = Column(DateTime, default=datetime.utcnow)

    table = relationship("Table", back_populates="games")
    hands = relationship("Hand", back_populates="game")
    bets = relationship("Bet", back_populates="game")
    pots = relationship("Pot", back_populates="game")

class Hand(Base):
    __tablename__ = "hands"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    player_id = Column(Integer, ForeignKey("players.id"))
    hole_cards = Column(String, default="")  # Store as comma-separated values
    is_winner = Column(Boolean, default=False)
    winnings = Column(Float, default=0.0)

    game = relationship("Game", back_populates="hands")
    player = relationship("Player", back_populates="hands")

class Bet(Base):
    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    player_id = Column(Integer, ForeignKey("players.id"))
    amount = Column(Float, default=0.0)
    bet_type = Column(Enum("fold", "call", "raise", "all-in", "check"), default="call")
    created_at = Column(DateTime, default=datetime.utcnow)

    game = relationship("Game", back_populates="bets")
    player = relationship("Player", back_populates="bets")

# ---- POTS & SIDE POTS ----

class Pot(Base):
    __tablename__ = "pots"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    amount = Column(Float, default=0.0)
    winner_id = Column(Integer, ForeignKey("players.id"), nullable=True)  # Side pots

    game = relationship("Game", back_populates="pots")
    winner = relationship("Player")

# ---- RAKE & RAKEBACK SYSTEM ----

class Rakeback(Base):
    __tablename__ = "rakebacks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_rake = Column(Float, default=0.0)
    rakeback_percentage = Column(Float, default=10.0)  # Cashback percentage
    last_payout = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
