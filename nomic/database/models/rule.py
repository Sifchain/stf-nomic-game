import uuid
from datetime import datetime

from sqlalchemy import (UUID, Boolean, Column, DateTime, ForeignKey, Integer,
                        Text)
from sqlalchemy.orm import relationship

from nomic.database import Base


class Rule(Base):
    __tablename__ = "rules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    game_id = Column(UUID(as_uuid=True), ForeignKey("games.id"))
    name = Column(Text)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to Game model
    game = relationship("Game", back_populates="rules")
