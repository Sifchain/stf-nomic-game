import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from nomic.database import crud
from nomic.database.models.game_player import GamePlayer
from nomic.database.models.user import User
from nomic.routes.ws import broadcast_message
from nomic.utils.jwt_handler import get_current_user

router = APIRouter()


@router.post("/game/{game_id}/end-turn")
async def end_turn(
    game_id: str,
    db: Session = Depends(crud.get_db),
    current_user: User = Depends(get_current_user),
):
    game = crud.get_game_by_id(db, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    # must be user turn
    if game.current_player_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not your turn")

    # retrieve game player
    game_player = (
        db.query(GamePlayer)
        .filter(GamePlayer.game_id == game.id, GamePlayer.user_id == current_user.id)
        .first()
    )

    _, _, score = crud.end_turn(db, game, game_player)

    details = {
        "message": "Turn ended and votes processed",
        "game_id": game_id,
        "old_player_id": f"{current_user.id}",
        "new_player_id": f"{game.current_player_id}",
        "new_score": game_player.score,
        "dice_score": score,
    }

    # Broadcast the end turn event to all WebSocket clients
    await broadcast_message(
        json.dumps(
            {
                "event_type": "end_turn",
                "game_id": game_id,
                "old_player_id": f"{current_user.id}",
                "new_player_id": f"{game.current_player_id}",
                "new_score": game_player.score,
                "dice_score": score,
            }
        )
    )

    return details
