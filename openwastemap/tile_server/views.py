"""
Views from the Tile Server App.
"""

from pathlib import Path

from django.conf import settings
from django.http.response import HttpResponse

from .tasks import render_tile


def index(request):
    """Return empty response"""
    return HttpResponse()


def tile(request, zoom, xcoord, ycoord):
    """Return the Tile at requested coordinates."""

    if not settings.IS_TEST and settings.CHECK_TILE_CACHE_HIT:
        tile_path = (
            Path(settings.TILES_ROOT) / str(zoom) / str(xcoord) / (str(ycoord) + ".png")
        )  # TODO: this is written twice (tasks.py)

        if tile_path.exists():
            with open(tile_path, "rb") as tile_image:
                return HttpResponse(tile_image.read(), content_type="image/png")

    response = HttpResponse(content_type="image/png")
    render_tile.run(zoom, xcoord, ycoord).save(response, "PNG")
    return response
