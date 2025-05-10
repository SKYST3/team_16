from fastapi import APIRouter, status, HTTPException
from hackathon.app.common import values
from hackathon.app.game.dto import GameStatusResponse, GameSubmitResponse, GameSubmitRequest
from hackathon.app.game.error import GameStartAtNotFoundError, SongLengthNotFoundError
from hackathon.app.game import service

game_router = APIRouter()

@game_router.get("/status", status_code=status.HTTP_200_OK)
async def get_game():
    # game_start_at 있는지 확인
    game_start_at = values.get('game_started_at')
    if game_start_at is None:
        raise GameStartAtNotFoundError()

    # song_length 없으면 에러 반환환
    song_length = values.get('song_length')
    if song_length is None:
        raise SongLengthNotFoundError()

    # 값 반환
    return GameStatusResponse(
        game_start_at = game_start_at,
        song_length = song_length
    )

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