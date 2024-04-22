import uuid
from datetime import datetime

from sqlalchemy import UUID, Column, DateTime, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship

from nomic.database import Base


class RuleProposal(Base):
    __tablename__ = "rule_proposals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    game_id = Column(UUID(as_uuid=True), ForeignKey("games.id"))
    proposed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    name = Column(Text)
    description = Column(Text, nullable=True)
    status = Column(
        Enum(
            "CREATED",
            "VOTING",
            "PASSED",
            "REJECTED",
            "CANCELLED",
            name="rule_proposal_statuses",
        ),
        default="CREATED",
    )  # type: ignore
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to User model through RuleProposalVote
    votes = relationship("RuleProposalVote", back_populates="rule_proposal")

    # Relationship to Game model
    game = relationship("Game", back_populates="rule_proposals")
