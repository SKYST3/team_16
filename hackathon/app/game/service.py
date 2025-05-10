from fastapi import APIRouter

game_router = APIRouter()

@game_router.get("/status")
def get_game():
    return {"game": "status"}

@game_router.post("/submit")
def start_game():
    return {"message": "Game started"}