import logging

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from tenacity import RetryError

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

    tile = Tile(zoom=zoom, xcoord=xcoord, ycoord=ycoord)

    with SessionLocal() as db:
        # use session to immediately close after request
        # as we are waiting for the celerytasks to finish
        # and they are also using the database, we could end up in a deadlock
        tile_in_cache_db = tilecache.get_tile(db, tile)
    if not (tile_in_cache_db and tilecache.is_on_disk(tile)):
        celery_app.send_task("app.worker.render_tile", args=[zoom, xcoord, ycoord])

        try:
            await tilecache.wait_for_tile_on_disk(tile)
        except RetryError:
            logger.error(f"Timed out waiting for tile: f{tile}")
            raise HTTPException(status_code=500, detail="Could not render tile")

    with open(tilecache.path_for_tile(tile), "rb") as f:
        tile_image = f.read()

    return Response(content=tile_image, media_type="image/png")
