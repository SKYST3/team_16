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
	"beat_list": [2653, 4606, 6465, 6832, 7274, 7733, 8311, 9269, 10255, 11550, 12007, 13957, 14851, 15810, 16789, 17684, 19638, 20506, 21441, 22789, 23250, 24246, 25132, 26124, 27064, 28867, 30801, 31751, 32638, 34930, 35669, 36423, 37207, 37908, 38661, 39367, 40127, 40878, 41636, 42401, 43157, 43902, 44662, 45297, 45775],
    "scores": [
        {Team.SEOUL: 0},
        {Team.KAIST: 0},
        {Team.YONSEI: 0},
        {Team.KOREA: 0},
	],
    "participants": {
        Team.SEOUL: 0,
        Team.KAIST: 0,
        Team.YONSEI: 0,
        Team.KOREA: 0,
    },

}

clients = []
# admins = []