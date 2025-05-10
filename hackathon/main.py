from fastapi import FastAPI
from hackathon.api import api_router

app = FastAPI()

app.include_router(api_router, prefix="/api")
