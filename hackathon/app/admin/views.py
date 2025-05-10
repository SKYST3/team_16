import json, asyncio
from fastapi import APIRouter, Response, status
from fastapi.responses import StreamingResponse
from hackathon.app.common import values
from hackathon.app.admin.dto.requests import GameStartRequest
from hackathon.app.admin.dto.responses import GameStart, GameScore, GameResult, Participants
from hackathon.app.admin.error import *
from hackathon.app.common import clients
from typing import List

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
        "song_length" : values["song_length"],
        "beat_list" : values["beat_list"]
    }
    response = json.dumps(response)

    for queue in clients:
        await queue.put(response)
        
    return Response(status_code=status.HTTP_200_OK)

@admin_router.post("/game/result", response_model=GameResult)
async def game_result() -> GameResult:
    scores_data = values.get("scores")
    if scores_data is None:
        raise ScoreNotFoundError()

    formatted_scores: list[GameScore] = []
    for score_dict in scores_data:
        for team_enum, score_value in score_dict.items():
            formatted_scores.append(GameScore(team=team_enum, score=score_value))

    return GameResult(scores=formatted_scores)


@admin_router.get("/game/headcount")
async def get_headcount() -> int:
    return len(clients)

@admin_router.get("/game/queue")
async def get_queue() -> int:
    return len(clients)

@admin_router.get("/game/participants")
async def get_participants() -> Participants:

    queue = asyncio.Queue()
    clients.append(queue)

    async def event_generator():
        try:
            data = await queue.get()
            yield f"data: {data}\n\n"
        finally:
            clients.remove(queue)
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")