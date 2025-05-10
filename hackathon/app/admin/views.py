from fastapi import APIRouter
from hackathon.app.common import values

admin_router = APIRouter()

@admin_router.get("/game")
async def get_game():
    d = values["count"]
    values["count"] += 1
    return {"game": d}

@admin_router.post("/game/start")
def start_game():
    return {"message": "Game started"}

@admin_router.post("/game/result")
def game_result():
    return {"message": "Game result submitted"}