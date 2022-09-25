from fastapi import APIRouter

from app.api.api_v1.endpoints import admin, login, tiles, users, utils, waste_samples

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(
    waste_samples.router, prefix="/waste-samples", tags=["waste_samples"]
)
api_router.include_router(tiles.router, prefix="/tiles", tags=["tiles"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
