import json

from fastapi import APIRouter, Depends

from nomic.database.models.user import User
from nomic.routes.ws import broadcast_message
from nomic.utils.jwt_handler import get_current_user

router = APIRouter()


@router.post("/game/{game_id}/vote-rule-change/{change_id}")
async def vote_rule_change(
    game_id: str,
    change_id: str,
    vote: str,
    current_user: User = Depends(get_current_user),
):
    # update the vote tally in database

    # Create the response detail
    vote_details = {
        "message": "Vote recorded",
        "game_id": game_id,
        "change_id": change_id,
        "vote": vote,
        "voted_by": str(current_user.id),
    }

    # Broadcast the vote to all WebSocket clients
    await broadcast_message(
        json.dumps(
            {
                "event_type": "vote_rule_change",
                "game_id": game_id,
                "change_id": change_id,
                "vote": vote,
                "voted_by": str(current_user.id),
            }
        )
    )

    return vote_details
