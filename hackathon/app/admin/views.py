import json
from fastapi import APIRouter, Response, status
from hackathon.app.common import values
from hackathon.app.admin.dto.requests import GameStartRequest
from hackathon.app.admin.dto.responses import GameStart, GameScore
from hackathon.app.admin.error import *
from hackathon.app.common import clients

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
    values["game_started_at"] = req.game_started_at
    
    response = {
        "game_started_at" : values["game_started_at"],
        "song_length" : values["song_length"]
    }
    response = json.dumps(response)

    for queue in clients:
        await queue.put(response)
        
    return Response(status_code=status.HTTP_200_OK)

@admin_router.post("/game/result")
async def game_result() -> GameScore:
    if values.get("scores") is None:
        return ScoreNotFoundError()
    return {
        "scores": values["scores"],
    }

@admin_router.get("/game/queue")
async def get_queue() -> int:
    return len(clients)