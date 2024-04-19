from sqlalchemy import Column, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from nomic.database import Base


class RuleProposalVote(Base):
    __tablename__ = "rule_proposal_votes"

    rule_proposal_id = Column(
        UUID(as_uuid=True), ForeignKey("rule_proposals.id"), primary_key=True
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    vote_type = Column(Enum("yes", "no", name="vote_types"), nullable=False)  # type: ignore

    # Explicit relationships
    user = relationship("User", back_populates="rule_proposal_votes")
    rule_proposal = relationship("RuleProposal", back_populates="votes")
