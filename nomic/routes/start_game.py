import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from nomic.database import crud
from nomic.database.models.user import User
from nomic.routes.ws import broadcast_message
from nomic.utils.jwt_handler import get_current_user

router = APIRouter()


@router.post("/game/{game_id}/start")
async def start_game(
    game_id: str,
    db: Session = Depends(crud.get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Update the status of the game to 'STARTED'.
    """
    game = crud.get_game_by_id(db, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    if game.status != "CREATED":
        raise HTTPException(
            status_code=400,
            detail="Game cannot be started. It is not in the 'CREATED' state.",
        )

    # prevent game to start if no players
    if len(game.players) == 0:
        raise HTTPException(
            status_code=400,
            detail="Game cannot be started. There are no players in the game.",
        )

    # game can only be started by the creator
    if game.created_by != current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Game cannot be started. Only the creator can start the game.",
        )

    crud.start_game(db, game)

    start_details = {
        "message": "Started the game successfully",
        "game_id": game_id,
        "current_player_id": str(game.current_player_id),
    }

    # Broadcast the game being started to all WebSocket clients
    await broadcast_message(
        json.dumps(
            {
                "event_type": "start_game",
                "game_id": game_id,
                "current_player_id": str(game.current_player_id),
            }
        )
    )

    return start_details
