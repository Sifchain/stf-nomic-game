import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from nomic.database import crud
from nomic.database.models.game_player import GamePlayer
from nomic.database.models.rule_proposal import RuleProposal
from nomic.database.models.rule_proposal_vote import RuleProposalVote
from nomic.database.models.user import User
from nomic.routes.ws import broadcast_message
from nomic.utils.jwt_handler import get_current_user

router = APIRouter()


@router.post("/game/{game_id}/vote-rule-proposal/{rule_proposal_id}/{vote_type}")
async def vote_rule_proposal(
    game_id: str,
    rule_proposal_id: str,
    vote_type: str,
    db: Session = Depends(crud.get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Endpoint to vote on a rule proposal with 'yes' or 'no'.
    """
    if vote_type not in ["yes", "no"]:
        raise HTTPException(
            status_code=400, detail="Invalid vote type. Choose 'yes' or 'no'."
        )
    try:
        game = crud.get_game_by_id(db, game_id)
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")

        # Check if the user is part of the game
        game_player = (
            db.query(GamePlayer)
            .filter(
                GamePlayer.game_id == game.id, GamePlayer.user_id == current_user.id
            )
            .first()
        )
        if not game_player:
            raise HTTPException(status_code=403, detail="User not part of the game")

        rule_proposal = db.query(RuleProposal).filter_by(id=rule_proposal_id).first()
        if not rule_proposal:
            raise HTTPException(status_code=404, detail="Rule proposal not found")

        if rule_proposal.status != "VOTING":
            raise HTTPException(
                status_code=400,
                detail="Voting is not allowed on this rule proposal at the current stage.",
            )

        # Check if the user has already voted
        existing_vote = (
            db.query(RuleProposalVote)
            .filter_by(rule_proposal_id=rule_proposal_id, user_id=current_user.id)
            .first()
        )
        if existing_vote:
            raise HTTPException(
                status_code=400,
                detail="User has already cast a vote on this rule proposal",
            )

        rule_proposal = crud.vote_rule_proposal(
            db, rule_proposal_id, str(current_user.id), vote_type
        )

        # Create the response detail
        vote_details = {
            "message": "Vote recorded successfully",
            "game_id": game_id,
            "rule_proposal_id": str(rule_proposal.id),
            "vote_type": vote_type,
            "voted_by": str(current_user.id),
        }

        # Broadcast the vote to all WebSocket clients
        await broadcast_message(
            json.dumps(
                {
                    "event_type": "vote_rule_change",
                    "game_id": game_id,
                    "rule_proposal_id": str(rule_proposal.id),
                    "vote_type": vote_type,
                    "voted_by": str(current_user.id),
                }
            )
        )

        return vote_details

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
