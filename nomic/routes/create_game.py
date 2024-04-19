import json

from fastapi import APIRouter, Depends
from fastapi.param_functions import Form
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from nomic.database import crud
from nomic.database.models.user import User
from nomic.routes.ws import broadcast_message
from nomic.utils.jwt_handler import get_current_user


class CreateGameInput:
    def __init__(
        self, game_name: Annotated[str, Form()], initial_rules: Annotated[list, Form()]
    ):
        self.game_name = game_name
        self.initial_rules = initial_rules


router = APIRouter()


@router.post("/game/create")
async def create_game(
    form_data: CreateGameInput = Depends(),
    db: Session = Depends(crud.get_db),
    current_user: User = Depends(get_current_user),
):
    game = crud.create_game(db, form_data.game_name, current_user)

    game_details = {
        "message": "Game created successfully",
        "game_id": str(game.id),
        "game_name": game.name,
        "initial_rules": form_data.initial_rules,
        "created_by": str(current_user.id),
    }

    # Broadcast the creation of the new game to all WebSocket clients
    await broadcast_message(
        json.dumps(
            {
                "event_type": "create_game",
                "game_name": form_data.game_name,
                "game_id": str(game.id),
                "initial_rules": form_data.initial_rules,
                "created_by": str(current_user.id),
            }
        )
    )

    return game_details
