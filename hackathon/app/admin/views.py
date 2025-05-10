from fastapi import APIRouter, Response, status
from hackathon.app.common import values
from hackathon.app.admin.dto.requests import GameStartRequest
from hackathon.app.admin.dto.responses import GameStart, GameScore
from hackathon.app.admin.error import *

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
async def start_game(
    req: GameStartRequest,
) -> Response:
    if values.get("game_started_at") is None:
        return GameStartAtNotFoundError()
    
    values["game_started_at"] = req.game_started_at

    return Response(status_code=status.HTTP_200_OK)

@admin_router.post("/game/result")
async def game_result() -> GameScore:
    if values.get("scores") is None:
        return ScoreNotFoundError()
    return {
        "scores": values["scores"],
    }