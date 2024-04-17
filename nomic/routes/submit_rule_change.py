import json
from uuid import uuid4

from fastapi import APIRouter, Depends

from nomic.database.models.user import User
from nomic.routes.ws import broadcast_message
from nomic.utils.jwt_handler import get_current_user

router = APIRouter()


@router.post("/game/{game_id}/submit-rule-change")
async def submit_rule_change(
    game_id: str, rule_change: dict, current_user: User = Depends(get_current_user)
):
    change_id = str(uuid4())  # Generate a unique change ID
    # save the rule change proposal to database

    # Create the response detail
    rule_change_details = {
        "message": "Rule change proposal submitted",
        "game_id": game_id,
        "change_id": change_id,
        "rule_change": rule_change,
        "submitted_by": str(current_user.id),
    }

    # Broadcast the rule change proposal to all WebSocket clients
    await broadcast_message(
        json.dumps(
            {
                "event_type": "submit_rule_change",
                "game_id": game_id,
                "change_id": change_id,
                "rule_change": rule_change,
                "submitted_by": str(current_user.id),
            }
        )
    )

    return rule_change_details
