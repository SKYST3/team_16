from fastapi import APIRouter, Response, status
from hackathon.app.common import values
from hackathon.app.admin.dto.requests import GameStartRequest
from hackathon.app.admin.dto.responses import GameStart

admin_router = APIRouter()

@admin_router.get("/game")
async def get_game() -> GameStart:
    return {
        "song_length": values["song_length"],
        "beat_list": values["beat_list"],
    }

@admin_router.post("/game/start")
def start_game(
    req: GameStartRequest,
):
    values["game_started_at"] = req.game_started_at
    return Response(status_code=status.HTTP_200_OK)

@admin_router.post("/game/result")
def game_result():
    return {
        "scores": values["scores"],
    }