import asyncio
from fastapi import APIRouter, status, HTTPException, Request
from fastapi.responses import StreamingResponse
from hackathon.app.common import values, clients
from hackathon.app.game.dto import GameStatusResponse, GameSubmitResponse, GameSubmitRequest
from hackathon.app.game.error import GameStartAtNotFoundError, SongLengthNotFoundError
from hackathon.app.game import service

game_router = APIRouter()

@game_router.get("/status", status_code=status.HTTP_200_OK)
async def get_game_status(request: Request):
    queue = asyncio.Queue()
    clients.append(queue)

    async def event_generator():
        try:
            data = await queue.get()
            yield f"data: {data}\n\n"
        finally:
            clients.remove(queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@game_router.post("/submit", response_model=GameSubmitResponse)
async def submit_score(submission: GameSubmitRequest):
    answer_timestamps = values.get('beat_list')

    if answer_timestamps is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Beat list not initialized")

    try:
        score_data = await service.process_submission_and_calculate_score(
            submission.timestamp, answer_timestamps
        )
        return GameSubmitResponse(**score_data)
    except Exception as e:

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Scoring error: {str(e)}")