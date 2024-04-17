import uuid

from sqlalchemy import UUID, Column, Integer, String
from sqlalchemy.orm import relationship

from nomic.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    score = Column(Integer, default=0)

    # Link to games through the game_players association table
    games = relationship("Game", secondary="game_players", back_populates="players")
