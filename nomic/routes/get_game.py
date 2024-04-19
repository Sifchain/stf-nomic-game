from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from nomic.database import crud

router = APIRouter()


@router.get("/game/{game_id}")
async def get_game(game_id: str, db: Session = Depends(crud.get_db)):
    """
    Retrieve and display information about a specific game, including its status.
    """
    game = crud.get_game_by_id(db, game_id)

    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    return {
        "game_id": str(game.id),
        "game_name": game.name,
        "status": game.status,
        "created_at": game.created_at,
        "updated_at": game.updated_at,
        "players": [
            {"player_id": str(player.id), "username": player.username}
            for player in game.players
        ],
        "turn": str(game.turn) if game.turn else "Game not started yet",
        "rules": [
            {
                "rule_id": str(rule.id),
                "name": rule.name,
                "description": rule.description,
            }
            for rule in game.rules
        ],
        "rule_proposals": [
            {
                "rule_proposal_id": str(rule_proposal.id),
                "name": rule_proposal.name,
                "description": rule_proposal.description,
                "status": rule_proposal.status,
                "proposed_by": str(rule_proposal.proposed_by),
                "votes": rule_proposal.votes,
            }
            for rule_proposal in game.rule_proposals
        ],
    }
