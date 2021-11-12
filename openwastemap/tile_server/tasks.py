"""
Tasks which can be executed using celery.
"""


from celery.decorators import task
from django.conf import settings

from .render import TileRenderer
from .utilities import get_tile_cache_path, tiles_affected_by_sample


@task(name="render_tile")
def render_tile(zoom, xcoord, ycoord):
    rendered_tile = TileRenderer(zoom, xcoord, ycoord).render()
    if not settings.IS_TEST and (not settings.DEBUG or settings.CHECK_TILE_CACHE_HIT):
        out_path = get_tile_cache_path(zoom, xcoord, ycoord)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        rendered_tile.save(out_path)
    return rendered_tile


@task(name="invalidate_tiles")
def invalidate_tiles(latitude, longitude):
    """
    Invalidate all tiles which are affected
    by a sample at the given coordinates.
    """
    if settings.IS_TEST or (settings.DEBUG and not settings.CHECK_TILE_CACHE_HIT):
        return

    for (zoom, xnum, ynum) in tiles_affected_by_sample(latitude, longitude):
        get_tile_cache_path(zoom, xnum, ynum).unlink(missing_ok=True)
