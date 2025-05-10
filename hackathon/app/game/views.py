from fastapi import APIRouter
from hackathon.app.common import values

game_router = APIRouter()

@game_router.get("/status")
def get_game():
    return {"game": values["count"]}

@game_router.post("/submit")
def start_game():
    return {"message": "Game started"}