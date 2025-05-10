from pydantic import BaseModel

class GameStartRequest(BaseModel):
    game_started_at: int