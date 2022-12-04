import base64
from pathlib import Path

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.api import deps
from app.core.celery_app import celery_app
from app.schemas.tile_cache import Tile
from app.tile_cache import tilecache

router = APIRouter()


@router.get(
    "/{zoom}/{xcoord}/{ycoord}.png",
    response_class=Response,
    responses={200: {"content": {"image/png": {}}}},
)
def get_tile(zoom: int, xcoord: int, ycoord: int, db: Session = Depends(deps.get_db)):
    """
    Get tile from cache or render
    """

    cached_tile_path = Path("/tiles") / str(zoom) / str(xcoord) / f"{ycoord}.png"
    tile_in_cache_db = tilecache.get_tile(
        db, Tile(zoom=zoom, xcoord=xcoord, ycoord=ycoord)
    )
    if tile_in_cache_db and cached_tile_path.exists():
        with open(cached_tile_path, "rb") as f:
            tile_image = f.read()
    else:
        render_task = celery_app.send_task(
            "app.worker.render_tile", args=[zoom, xcoord, ycoord]
        )
        # TODO: sometimes the task ran into a timeout
        # although execution is successful and fast
        # could not reproduce this error
        tile_image = base64.b64decode(render_task.get(timeout=10))
        cached_tile_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cached_tile_path, "wb") as f:
            f.write(tile_image)

        tilecache.updated_tile(db, Tile(zoom=zoom, xcoord=xcoord, ycoord=ycoord))

    return Response(content=tile_image, media_type="image/png")
