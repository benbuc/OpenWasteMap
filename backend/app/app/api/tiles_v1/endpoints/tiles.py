import base64

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
    render_task = celery_app.send_task(
        "app.worker.render_tile", args=[zoom, xcoord, ycoord]
    )
    image_out = base64.b64decode(render_task.get(timeout=5))

    return Response(content=image_out, media_type="image/png")
