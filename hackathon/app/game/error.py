from fastapi import HTTPException, status

class GameStartAtNotFoundError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="game_start_at not found."
        )

class SongLengthNotFoundError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="song_length not found."
        )