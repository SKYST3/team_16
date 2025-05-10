from fastapi import APIRouter, status
from hackathon.app.common import values
from hackathon.app.game.dto import GameStatusResponse
from hackathon.app.game.error import GameStartAtNotFoundError, SongLengthNotFoundError
from hackathon.app.game.service import test

game_router = APIRouter()

@game_router.get("/status", status_code=status.HTTP_200_OK)
def get_game():
    test()
    # # game_start_at 있는지 확인
    # game_start_at = values.get('game_started_at')
    # if game_start_at is None:
    #     raise GameStartAtNotFoundError()

    # # song_length 없으면 에러 반환환
    # song_length = values.get('song_length')
    # if song_length is None:
    #     raise SongLengthNotFoundError()

    # # 값 반환
    # return GameStatusResponse(
    #     game_start_at = game_start_at,
    #     song_length = song_length
    # )

@game_router.post("/submit")
def start_game():
    return {"message": "Game started"}