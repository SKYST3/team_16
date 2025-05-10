from fastapi import APIRouter

admin_router = APIRouter()

@admin_router.get("/game")
def get_game():
    return {"game": "Game data"}

@admin_router.post("/game/start")
def start_game():
    return {"message": "Game started"}

@admin_router.post("/game/result")
def game_result():
    return {"message": "Game result submitted"}