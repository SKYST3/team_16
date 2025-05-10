from pydantic import BaseModel
from typing import List

class GameStatusResponse(BaseModel):
    game_start_at: int
    song_length: int

class GameSubmitRequest(BaseModel):
    timestamp: List[int]
    team: str

class GameSubmitResponse(BaseModel):
    normal: int
    good: int
    perfect: int
    score: int

class TeamCountResquest(BaseModel):
    team: str