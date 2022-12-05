import asyncio
import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.tiles_v1.api import api_router
from app.core.config import settings
from app.tile_cache.render_outdated import TileCacheRenderOutdated

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.TILES_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.TILES_V1_STR)


@app.on_event("startup")
async def run_mainloop():
    """Adding the mainloop to the asyncio event loop."""
    # https://github.com/tiangolo/fastapi/issues/825

    logger.info("Starting the mainloop")

    current_loop = asyncio.get_running_loop()
    renderer = TileCacheRenderOutdated()
    current_loop.create_task(renderer.mainloop())
