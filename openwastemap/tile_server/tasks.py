"""
Tasks which are executed using celery.
"""

from pathlib import Path

from celery.decorators import task
from django.conf import settings

from .render import TileRenderer


@task(name="tile_async")
def tile_async(zoom, xcoord, ycoord):
    rendered_tile = TileRenderer(zoom, xcoord, ycoord).render()
    out_path = (
        Path(settings.TILES_ROOT) / str(zoom) / str(xcoord) / (str(ycoord) + ".png")
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    rendered_tile.save(out_path)
