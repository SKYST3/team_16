from pydantic import BaseModel
from hackathon.app.common import Team

class GameStart(BaseModel):
    song_length: int
    beat_list: list[float]

class GameScore(BaseModel):
    team: Team
    score: int

class GameResult(BaseModel):
    scores: list[GameScore]

class Participants(BaseModel):
    SEOUL: int
    KAIST: int
    KOREA: int
    YONSEI: int