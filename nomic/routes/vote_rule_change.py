import json

from fastapi import APIRouter, Depends

from nomic.routes.ws import broadcast_message
from nomic.utils.jwt_handler import get_current_user

router = APIRouter()


@router.post("/vote-rule-change/{game_id}/{change_id}")
async def vote_rule_change(
    game_id: str,
    change_id: str,
    vote: str,
    current_user: str = Depends(get_current_user),
):
    # update the vote tally in database

    # Create the response detail
    vote_details = {
        "message": "Vote recorded",
        "game_id": game_id,
        "change_id": change_id,
        "vote": vote,
    }

    # Broadcast the vote to all WebSocket clients
    await broadcast_message(
        json.dumps(
            {
                "event_type": "vote_rule_change",
                "game_id": game_id,
                "change_id": change_id,
                "vote": vote,
                "voted_by": current_user,
            }
        )
    )

    return vote_details
