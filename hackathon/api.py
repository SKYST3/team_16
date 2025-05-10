from fastapi import APIRouter
from hackathon.app.admin import admin_router
from hackathon.app.game import game_router

api_router = APIRouter()

api_router.include_router(admin_router, prefix="/admin", tags=["admin"])
api_router.include_router(game_router, prefix="/game", tags=["game"])
