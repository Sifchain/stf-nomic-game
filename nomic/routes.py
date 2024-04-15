from fastapi import APIRouter
from . import app

router = APIRouter()

@router.get("/")
async def home():
    return {"message": "Welcome to the Nomic game!"}

@router.get("/game")
async def game():
    return {"message": "Game functionalities under development"}

app.include_router(router)
