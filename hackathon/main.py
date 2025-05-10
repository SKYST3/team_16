from fastapi import FastAPI, Request
from hackathon.api import api_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import asyncio
import time
from hackathon.app.common import clients

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/game")
async def game_stream(request: Request):
    queue = asyncio.Queue()
    clients.append(queue)

    async def event_generator():
        try:
            data = await queue.get()
            yield f"data: {data}\n\n"
        finally:
            clients.remove(queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")