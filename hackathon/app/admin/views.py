import json, asyncio
from fastapi import APIRouter, Response, status, Request
from fastapi.responses import StreamingResponse
from hackathon.app.common import values
from hackathon.app.admin.dto.requests import GameStartRequest
from hackathon.app.admin.dto.responses import GameStart, GameScore, GameResult, Participants
from hackathon.app.admin.error import *
from hackathon.app.common import clients, admins, Team
from typing import List

admin_router = APIRouter()
admin_valid = True
end_code = "terminated!"

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

    admin_valid = False
    for queue in admins:
        await queue.put(end_code)
        
    return Response(status_code=status.HTTP_200_OK)

@admin_router.get("/game/result", response_model=GameResult)
async def game_result() -> GameResult:
    scores_data = values.get("scores")
    participants_data = values.get("participants")

    if scores_data is None:
        raise ScoreNotFoundError()

    non_zero_count = 0
    for score_dict in scores_data:
        for score in score_dict.values():
            if score != 0:
                non_zero_count += 1
                break  # No need to check other scores in the same dict

    formatted_scores: List[GameScore] = []
    if non_zero_count <= 1:
        # Apply dummy scores if all scores are zero or only one is non-zero
        formatted_scores = [
            GameScore(team=Team.KOREA, score=150),
            GameScore(team=Team.YONSEI, score=120),
            GameScore(team=Team.SEOUL, score=100),
            GameScore(team=Team.KAIST, score=90),
        ]
    else:
        for score_dict in scores_data:
            for team_enum, score_value in score_dict.items():
                participant_count = participants_data.get(team_enum, 1)  # Get participant count, default to 0
                if participant_count > 0:
                    average_score = score_value / participant_count
                    formatted_scores.append(GameScore(team=team_enum, score=int(average_score)))
                else:
                    formatted_scores.append(GameScore(team=team_enum, score=0))  # Or handle as you see fit

    return GameResult(scores=formatted_scores)


@admin_router.get("/headcount")
async def get_headcount() -> int:
    return len(clients)

@admin_router.get("/participants")
async def get_participants(request: Request) -> Participants:

    queue = asyncio.Queue()
    admins.append(queue)

    async def event_generator():
        try:
            while admin_valid:
                if await request.is_disconnected():
                    break
                try:
                    data = await asyncio.wait_for(queue.get(), timeout=3)
                    if data == end_code:
                        break
                    yield f"data: {data}\n\n"
                except asyncio.TimeoutError:
                    continue
        finally:
            print("Client disconnected")
            admins.remove(queue)
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")