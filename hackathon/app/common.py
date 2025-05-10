from enum import Enum

class Team(str, Enum):
    SEOUL = "SEOUL"
    KAIST = "KAIST"
    YONSEI = "YONSEI"
    KOREA = "KOREA"

values = {
    "count": 1,
    "game_started_at": 0,
    "song_length": 30,
	"beat_list": [0.0, 0.5, 1.0, 1.5, 2.0, 8.0],
    "scores": [
		{"team": Team.SEOUL, "score": 0},
		{"team": Team.KAIST, "score": 0},
		{"team": Team.YONSEI, "score": 0},
		{"team": Team.KOREA, "score": 0},
	]
}
