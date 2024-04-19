import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from nomic.database import crud
from nomic.database.models.game_player import GamePlayer
from nomic.database.models.user import User
from nomic.routes.ws import broadcast_message
from nomic.utils.jwt_handler import get_current_user

router = APIRouter()


@router.post("/game/{game_id}/take-action/{rule_id}")
async def take_action(
    game_id: str,
    rule_id: str,
    db: Session = Depends(crud.get_db),
    current_user: User = Depends(get_current_user),
):
    game = crud.get_game_by_id(db, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # Check if the user is part of the game
    game_player = (
        db.query(GamePlayer)
        .filter(GamePlayer.game_id == game.id, GamePlayer.user_id == current_user.id)
        .first()
    )
    if not game_player:
        raise HTTPException(status_code=403, detail="User not part of the game")

    # must be user turn
    if game.current_player_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not your turn")

    rule = crud.get_rule_by_id(db, rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")

    # Verify the rule is active in the game
    if rule.game_id != game.id:
        raise HTTPException(status_code=404, detail="Rule not active in the game")

    crud.take_action(db, game_id, rule_id, str(current_user.id))

    # Create the response detail
    take_action_details = {
        "message": "Action recorded successfully",
        "game_id": game_id,
        "rule_id": rule_id,
        "user_id": str(current_user.id),
    }

    # Broadcast the take action event to all WebSocket clients
    await broadcast_message(
        json.dumps(
            {
                "event_type": "take_action",
                "game_id": game_id,
                "rule_id": rule_id,
                "user_id": str(current_user.id),
            }
        )
    )

    return take_action_details
