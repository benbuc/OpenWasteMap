import io

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.api import deps
from app.rendering.render import TileRenderer

router = APIRouter()


@router.get(
    "/{zoom}/{xcoord}/{ycoord}.png",
    response_class=Response,
    responses={200: {"content": {"image/png": {}}}},
)
def get_tile(
    zoom: int, xcoord: int, ycoord: int, db: Session = Depends(deps.get_db),
):
    image_out = io.BytesIO()
    rendered_tile = TileRenderer(zoom, xcoord, ycoord, db).render()
    rendered_tile.save(image_out, "png")

    return Response(content=image_out.getvalue(), media_type="image/png")
