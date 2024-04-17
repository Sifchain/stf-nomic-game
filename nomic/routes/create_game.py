import json
from uuid import uuid4

from fastapi import APIRouter, Depends

from nomic.database.models.user import User
from nomic.routes.ws import broadcast_message
from nomic.utils.jwt_handler import get_current_user

router = APIRouter()


@router.post("/create-game")
async def create_game(
    game_name: str, initial_rules: dict, current_user: User = Depends(get_current_user)
):
    game_id = str(uuid4())
    # Implementation for saving to DB here...

    game_details = {
        "message": "Game created successfully",
        "game_id": game_id,
        "game_name": game_name,
        "initial_rules": initial_rules,
        "current_user": current_user,
    }

    # Broadcast the creation of the new game to all WebSocket clients
    await broadcast_message(
        json.dumps(
            {
                "event_type": "create_game",
                "game_name": game_name,
                "game_id": game_id,
                "initial_rules": initial_rules,
            }
        )
    )

    return game_details
