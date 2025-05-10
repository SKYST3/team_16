from fastapi import APIRouter, Response, status
from hackathon.app.common import values
from hackathon.app.admin.dto.requests import GameStartRequest
from hackathon.app.admin.dto.responses import GameStart
from hackathon.app.admin.error import BeatListNotFoundError, SongLengthNotFoundError, GameStartAtNotFoundError

admin_router = APIRouter()

@admin_router.get("/game")
async def get_game() -> GameStart:
    song_length = values.get("song_length")
    if song_length is None:
        raise SongLengthNotFoundError()

    beat_list = values.get("beat_list")
    if beat_list is None:
        raise BeatListNotFoundError()

    return {
        "song_length": song_length,
        "beat_list": beat_list,
    }

@admin_router.post("/game/start")
def start_game(
    req: GameStartRequest,
):
    if values.get("game_started_at") is not None:
        return GameStartAtNotFoundError()
    
    values["game_started_at"] = req.game_started_at

    return Response(status_code=status.HTTP_200_OK)

@admin_router.post("/game/result")
def game_result():
    return {
        "scores": values["scores"],
    }