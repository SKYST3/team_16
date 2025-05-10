from fastapi import APIRouter, status
from hackathon.app.common import values
from hackathon.app.game.dto import GameStatusResponse, GameSubmitResponse, GameSubmitRequest
from hackathon.app.game.error import GameStartAtNotFoundError, SongLengthNotFoundError

game_router = APIRouter()

@game_router.get("/status", status_code=status.HTTP_200_OK)
def get_game():
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

@game_router.post("/submit", response = GameSubmitResponse)
def submit_score(submission: GameSubmitRequest):
    answer_timestamp = values.get('beat_list')

    normal_count = 0
    good_count = 0
    perfect_count = 0
    total_score = 0

    submitted_timestamps = submission.timestamp

    # Need function to extract closest submitted_timestamp to answer key

    # Function that calculates the perfect, good, misses

    return GameSubmitResponse(
        normal=normal_count,
        good=good_count,
        perfect=perfect_count,
        score=total_score
    )