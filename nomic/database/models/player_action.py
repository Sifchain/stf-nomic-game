import uuid
from datetime import datetime

from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer

from nomic.database import Base


class PlayerAction(Base):
    __tablename__ = "player_actions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    game_id = Column(UUID(as_uuid=True), ForeignKey("games.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    rule_id = Column(UUID(as_uuid=True), ForeignKey("rules.id"))
    turn = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
