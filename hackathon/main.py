from fastapi import FastAPI, Request
from hackathon.api import api_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import asyncio
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

clients = []

@app.get("/game")
async def game_stream(request: Request):
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue()

    # 클라이언트 등록
    clients.append(queue)

    async def event_generator():
        try:
            while True:
                if await request.is_disconnected():
                    break
                data = await queue.get()
                yield f"data: {data}\n\n"
        finally:
            # 연결 종료 시 클라이언트 제거
            clients.remove(queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")