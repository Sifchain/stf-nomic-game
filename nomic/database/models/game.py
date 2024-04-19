import uuid
from datetime import datetime

from sqlalchemy import UUID, Column, DateTime, Enum, ForeignKey, String, Table
from sqlalchemy.orm import relationship

from nomic.database import Base
from nomic.database.models.rule import Rule  # noqa: F401


class Game(Base):
    __tablename__ = "games"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    status = Column(Enum("CREATED", "STARTED", "ENDED", name="game_statuses"), default="CREATED")  # type: ignore
    turn = Column(UUID(as_uuid=True), nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to User model
    players = relationship("User", secondary="game_players", back_populates="games")

    # Relationship to Rule model
    rules = relationship("Rule", back_populates="game")

    # Relationship to RuleProposal model
    rule_proposals = relationship("RuleProposal", back_populates="game")


# Define the association table for the many-to-many relationship between Games and Users
game_players = Table(
    "game_players",
    Base.metadata,
    Column("game_id", UUID(as_uuid=True), ForeignKey("games.id"), primary_key=True),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True),
)
