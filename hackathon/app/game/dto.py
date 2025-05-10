from pydantic import BaseModel

class GameStatusResponse(BaseModel):
    game_start_at: int
    song_length: int