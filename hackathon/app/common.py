from enum import Enum

class Team(str, Enum):
    SEOUL = "SEOUL"
    KAIST = "KAIST"
    YONSEI = "YONSEI"
    KOREA = "KOREA"

values = {
    "count": 1,
    "game_started_at": 0,
    "song_length": 50,
	"beat_list": [2.653, 4.606, 6.465, 6.832, 7.274, 7.733, 8.311, 9.269, 10.255, 11.55, 12.007, 13.957, 14.851, 15.81, 16.789, 17.684, 19.638, 20.506, 21.441, 22.789, 23.25, 24.246, 25.132, 26.124, 27.064, 28.867, 30.801, 31.751, 32.638, 34.93, 35.669, 36.423, 37.207, 37.908, 38.661, 39.367, 40.127, 40.878, 41.636, 42.401, 43.157, 43.902, 44.662, 45.297, 45.775],
    "scores": [
		{"team": Team.SEOUL, "score": 0},
		{"team": Team.KAIST, "score": 0},
		{"team": Team.YONSEI, "score": 0},
		{"team": Team.KOREA, "score": 0},
	]
}
