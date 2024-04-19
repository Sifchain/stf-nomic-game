from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from nomic.database import crud
from nomic.database.models.user import User
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
    if game.turn != current_user.id:
        raise HTTPException(status_code=400, detail="Not your turn")

    crud.end_turn(db, game)

    db.commit()

    details = {
        "message": "Turn ended and votes processed",
        "game_id": game_id,
        "old_turn": f"{current_user.id}",
        "new_turn": f"{game.turn}",
    }

    return details
