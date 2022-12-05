import asyncio
import logging
import time
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.core.celery_app import celery_app
from app.db.session import SessionLocal
from app.schemas.tile_cache import Tile
from app.tile_cache import tilecache

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.get(
    "/{zoom}/{xcoord}/{ycoord}.png",
    response_class=Response,
    responses={200: {"content": {"image/png": {}}}},
)
async def get_tile(zoom: int, xcoord: int, ycoord: int):
    """
    Get tile from cache or render
    """

    cached_tile_path = Path("/tiles") / str(zoom) / str(xcoord) / f"{ycoord}.png"
    with SessionLocal() as db:
        # use session to immediately close after request
        # as we are waiting for the celerytasks to finish
        # and they are also using the database, we could end up in a deadlock
        tile_in_cache_db = tilecache.get_tile(
            db, Tile(zoom=zoom, xcoord=xcoord, ycoord=ycoord)
        )
    if not (tile_in_cache_db and cached_tile_path.exists()):
        render_task = celery_app.send_task(
            "app.worker.render_tile", args=[zoom, xcoord, ycoord]
        )

        start_time = time.time()
        timed_out = True
        while time.time() - start_time < 10:
            if render_task.state == "SUCCESS":
                timed_out = False
                break
            elif render_task.state == "FAILURE":
                logger.error(f"Failed to render tile {zoom}/{xcoord}/{ycoord}")
                raise HTTPException(status_code=500, detail="Failed to render tile")
            else:
                await asyncio.sleep(0.1)
        if timed_out:
            logger.error(f"Timed out while rendering tile {zoom}/{xcoord}/{ycoord}")
            raise HTTPException(status_code=500, detail="Failed to render tile")

    with open(cached_tile_path, "rb") as f:
        tile_image = f.read()

    return Response(content=tile_image, media_type="image/png")
