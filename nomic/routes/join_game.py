import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from nomic.database import crud
from nomic.database.models.user import User
from nomic.routes.ws import broadcast_message
from nomic.utils.jwt_handler import get_current_user

router = APIRouter()


@router.post("/game/{game_id}/join")
async def join_game(
    game_id: str,
    db: Session = Depends(crud.get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Add the current user to the game with the provided game_id.
    """

    # Check if the game exists and add the player to the game
    game = crud.get_game_by_id(db, game_id)

    if not game:
        return {"message": "Game not found"}

    if crud.check_player_in_game(game, current_user):
        raise HTTPException(
            status_code=400, detail="Cannot join game, as you are already in the game."
        )

    if game.status != "CREATED":
        raise HTTPException(
            status_code=400, detail="Cannot join game, as it is not in CREATED status."
        )

    crud.join_game(db, game, current_user)

    join_details = {
        "message": "Joined the game successfully",
        "game_id": game_id,
        "user_id": str(current_user.id),
    }

    # Broadcast the player joining the game to all WebSocket clients
    await broadcast_message(
        json.dumps(
            {
                "event_type": "join_game",
                "game_id": game_id,
                "user_id": str(current_user.id),
            }
        )
    )

    return join_details
