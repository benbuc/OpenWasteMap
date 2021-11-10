"""
Tasks which can be executed using celery.
"""

from pathlib import Path

from celery.decorators import task
from django.conf import settings

from .render import TileRenderer
from .utilities import tiles_affected_by_sample


@task(name="render_tile")
def render_tile(zoom, xcoord, ycoord):
    rendered_tile = TileRenderer(zoom, xcoord, ycoord).render()
    if not settings.DEBUG or settings.CHECK_TILE_CACHE_HIT:
        out_path = (
            Path(settings.TILES_ROOT) / str(zoom) / str(xcoord) / (str(ycoord) + ".png")
        )
        out_path.parent.mkdir(parents=True, exist_ok=True)
        rendered_tile.save(out_path)
    return rendered_tile


@task(name="invalidate_tiles")
def invalidate_tiles(latitude, longitude):
    """
    Invalidate all tiles which are affected
    by a sample at the given coordinates.
    """

    for (zoom, xnum, ynum) in tiles_affected_by_sample(latitude, longitude):
        (
            Path(settings.TILES_ROOT) / str(zoom) / str(xnum) / (str(ynum) + ".png")
        ).unlink(missing_ok=True)
