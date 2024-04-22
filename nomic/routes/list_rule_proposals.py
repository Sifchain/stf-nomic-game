from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from nomic.database import crud
from nomic.database.models.rule_proposal import RuleProposal

router = APIRouter()


@router.get("/game/{game_id}/rule-proposals")
async def list_rule_proposals(game_id: str, db: Session = Depends(crud.get_db)):
    """
    Retrieve and display all rule proposals for a specific game.
    """
    game = crud.get_game_by_id(db, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    rule_proposals = (
        db.query(RuleProposal).filter(RuleProposal.game_id == game_id).all()
    )
    return [
        {
            "rule_proposal_id": str(rule.id),
            "name": rule.name,
            "description": rule.description,
            "status": rule.status,
            "votes": rule.votes,
        }
        for rule in rule_proposals
    ]
