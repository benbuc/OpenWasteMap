from fastapi import APIRouter

from app.api.tiles_v1.endpoints import tiles

api_router = APIRouter()
api_router.include_router(tiles.router, tags=["tiles"])
