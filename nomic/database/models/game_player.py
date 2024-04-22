from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from nomic.database import Base


class GamePlayer(Base):
    __tablename__ = "game_players"

    game_id = Column(UUID(as_uuid=True), ForeignKey("games.id"), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    score = Column(Integer, default=0)
    joined_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    game = relationship("Game", back_populates="players")
    user = relationship("User", back_populates="games")
