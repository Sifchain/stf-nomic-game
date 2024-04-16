import uuid
from datetime import datetime

from sqlalchemy import JSON, UUID, Column, DateTime
from sqlalchemy.orm import relationship

from nomic.database import Base


class Game(Base):
    __tablename__ = "games"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    state = Column(JSON)  # Stores game state like turn number, scores, etc.
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to User model
    players = relationship("User", secondary="game_players", back_populates="games")

    # Relationship to Rule model
    rules = relationship("Rule", back_populates="game")
