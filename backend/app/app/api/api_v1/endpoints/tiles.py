import io

from fastapi import APIRouter
from fastapi.responses import Response
from PIL import Image

router = APIRouter()


@router.get(
    "/{x}/{y}/{z}.png",
    response_class=Response,
    responses={200: {"content": {"image/png": {}}}},
)
def get_tile(x: int, y: int, z: int):
    im = Image.new("RGBA", (256, 256))
    image_out = io.BytesIO()
    im.save(image_out, format="png")

    return Response(content=image_out.getvalue(), media_type="image/png")
