import base64
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import Response

from app.core.celery_app import celery_app

router = APIRouter()


@router.get(
    "/{zoom}/{xcoord}/{ycoord}.png",
    response_class=Response,
    responses={200: {"content": {"image/png": {}}}},
)
def get_tile(
    zoom: int,
    xcoord: int,
    ycoord: int,
):
    """
    Get tile from cache or render
    """

    cached_tile_path = Path("/tiles") / str(zoom) / str(xcoord) / f"{ycoord}.png"
    try:
        # try loading file from cache
        with open(cached_tile_path, "rb") as f:
            tile_image = f.read()
    except FileNotFoundError:
        # when no cached file found, recreate tile and store to cache
        render_task = celery_app.send_task(
            "app.worker.render_tile", args=[zoom, xcoord, ycoord]
        )
        tile_image = base64.b64decode(render_task.get(timeout=5))
        cached_tile_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cached_tile_path, "wb") as f:
            f.write(tile_image)

    return Response(content=tile_image, media_type="image/png")
