import json

from fastapi import APIRouter, Depends

from nomic.database.models.user import User
from nomic.routes.ws import broadcast_message
from nomic.utils.jwt_handler import get_current_user

router = APIRouter()


@router.post("/join-game/{game_id}")
async def join_game(game_id: str, current_user: User = Depends(get_current_user)):
    # Check if the game exists and add the player to the game

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
