import asyncio, json
from fastapi import APIRouter, status, HTTPException, Request, Response
from fastapi.responses import StreamingResponse
from hackathon.app.common import values, clients, Team
from hackathon.app.game.dto import GameStatusResponse, GameSubmitResponse, GameSubmitRequest, TeamCountResquest
from hackathon.app.game.error import GameStartAtNotFoundError, SongLengthNotFoundError
from hackathon.app.game import service

game_router = APIRouter()

@game_router.get("/status", status_code=status.HTTP_200_OK)
async def get_game_status(request: Request):
    queue = asyncio.Queue()
    clients.append(queue)

    async def event_generator():
        try:
            data = await queue.get()
            yield f"data: {data}\n\n"
        finally:
            clients.remove(queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@game_router.post("/submit", response_model=GameSubmitResponse)
async def submit_score(submission: GameSubmitRequest):
    answer_timestamps = values.get('beat_list')

    updated_timestamps = []
    if submission.timestamp:
        for timestamp in submission.timestamp:
            updated_timestamps.append(timestamp - values.get('game_started_at'))
            # print(f"game_started_at: {values.get('game_started_at')}")

    if answer_timestamps is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Beat list not initialized")

    # print(updated_timestamps)

    try:
        score_data = await service.process_submission_and_calculate_score(
            updated_timestamps, answer_timestamps, submission.team
        )
        print(submission.team, score_data)
        return GameSubmitResponse(**score_data)
    except Exception as e:

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Scoring error: {str(e)}")
    
@game_router.post("/select_team")
async def select_team(selection: TeamCountResquest):
    team_str = selection.team
    participants = values.get("participants")
    if participants is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Participants data not initialized on the server",
        )

    try:
        selected_team = Team(team_str)
        if selected_team in participants:
            values["participants"][selected_team] += 1
            resp = {
                "team": selected_team,
                "count": values["participants"][selected_team],
            }
            # for queue in admins:
            #     await queue.put(json.dumps(resp))
            print(f"Team {selected_team} joined")
            return Response(status_code=status.HTTP_200_OK)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid team: {team_str}"
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid team format: {team_str}"
        )