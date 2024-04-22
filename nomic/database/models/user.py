import uuid

from sqlalchemy import UUID, Column, String
from sqlalchemy.orm import relationship

from nomic.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    # Link to games through the game_players association table
    games = relationship("GamePlayer", back_populates="user")

    # Relationship to RuleProposalVote model
    rule_proposal_votes = relationship("RuleProposalVote", back_populates="user")
