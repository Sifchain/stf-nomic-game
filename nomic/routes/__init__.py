from fastapi import APIRouter

from .create_game import router as create_game_router
from .home import router as home_router
from .join_game import router as join_game_router
from .login import router as login_router
from .register import router as register_router
from .submit_rule_change import router as submit_rule_change_router
from .vote_rule_change import router as vote_rule_change_router
from .ws import router as ws_router

router = APIRouter()

# Include routers from separate files
router.include_router(home_router)
router.include_router(login_router)
router.include_router(register_router)
router.include_router(ws_router)
router.include_router(create_game_router)
router.include_router(join_game_router)
router.include_router(submit_rule_change_router)
router.include_router(vote_rule_change_router)
