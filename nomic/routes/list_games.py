from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from nomic.database import crud
from nomic.database.models.game import Game

router = APIRouter()


@router.get("/games")
async def list_games(db: Session = Depends(crud.get_db)):
    """
    Retrieve and display all games with brief details.
    """
    games = db.query(Game).all()
    return [
        {
            "game_id": str(game.id),
            "game_name": game.name,
            "status": game.status,
            "players": [
                {"id": player.user_id, "name": player.user.username}
                for player in game.players
            ],
            "current_player_id": (
                str(game.current_player_id)
                if game.current_player_id
                else "Game not started yet"
            ),
            "current_turn": game.current_turn,
            "winner_id": (
                str(game.winner_id) if game.winner_id else "Game not ended yet"
            ),
            "rules": game.rules,
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
            "created_by": game.created_by,
            "created_at": game.created_at,
            "updated_at": game.updated_at,
        }
        for game in games
    ]
