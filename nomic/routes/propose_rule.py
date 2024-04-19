import json

from fastapi import APIRouter, Depends, HTTPException
from fastapi.param_functions import Form
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from nomic.database import crud
from nomic.database.models.user import User
from nomic.routes.ws import broadcast_message
from nomic.utils.jwt_handler import get_current_user


class ProposeRuleInput:
    def __init__(
        self,
        rule_name: Annotated[str, Form()],
        rule_description: Annotated[str, Form()],
    ):
        self.rule_name = rule_name
        self.rule_description = rule_description


router = APIRouter()


@router.post("/game/{game_id}/propose-rule")
async def propose_rule(
    game_id: str,
    form_data: ProposeRuleInput = Depends(),
    db: Session = Depends(crud.get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Endpoint to propose a new rule.
    """
    game = crud.get_game_by_id(db, game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    if current_user not in game.players:
        raise HTTPException(status_code=403, detail="User not part of the game")

    rule_proposal = crud.create_rule_proposal(
        db,
        game_id,
        str(current_user.id),
        form_data.rule_name,
        form_data.rule_description,
    )

    # Create the response detail
    rule_proposal_details = {
        "message": "Rule proposed successfully",
        "game_id": game_id,
        "rule_proposal_id": str(rule_proposal.id),
        "rule_name": form_data.rule_name,
        "rule_description": form_data.rule_description,
        "proposed_by": str(current_user.id),
    }

    # Broadcast the rule change proposal to all WebSocket clients
    await broadcast_message(
        json.dumps(
            {
                "event_type": "submit_rule_change",
                "game_id": game_id,
                "rule_proposal_id": str(rule_proposal.id),
                "rule_name": form_data.rule_name,
                "rule_description": form_data.rule_description,
                "submitted_by": str(current_user.id),
            }
        )
    )

    return rule_proposal_details
