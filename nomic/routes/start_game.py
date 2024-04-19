import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from nomic.database import crud
from nomic.routes.ws import broadcast_message

router = APIRouter()


@router.post("/game/{game_id}/start")
async def start_game(game_id: str, db: Session = Depends(crud.get_db)):
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

    crud.start_game(db, game)

    start_details = {
        "message": "Started the game successfully",
        "game_id": game_id,
        "turn": str(game.turn),
    }

    # Broadcast the game being started to all WebSocket clients
    await broadcast_message(
        json.dumps(
            {
                "event_type": "start_game",
                "game_id": game_id,
                "turn": str(game.turn),
            }
        )
    )

    return start_details
