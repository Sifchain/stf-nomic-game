from fastapi import APIRouter

from .create_game import router as create_game_router
from .end_turn import router as end_turn_router
from .get_game import router as get_game_router
from .home import router as home_router
from .join_game import router as join_game_router
from .list_games import router as list_games_router
from .list_rule_proposals import router as list_rule_proposals_router
from .login import router as login_router
from .propose_rule import router as propose_rule_router
from .register import router as register_router
from .start_game import router as start_game_router
from .vote_rule_proposal import router as vote_rule_proposal_router
from .ws import router as ws_router

router = APIRouter()

# Include routers from separate files
router.include_router(home_router)
router.include_router(login_router)
router.include_router(register_router)
router.include_router(list_games_router)
router.include_router(get_game_router)
router.include_router(create_game_router)
router.include_router(start_game_router)
router.include_router(join_game_router)
router.include_router(list_rule_proposals_router)
router.include_router(propose_rule_router)
router.include_router(vote_rule_proposal_router)
router.include_router(end_turn_router)

router.include_router(ws_router)
