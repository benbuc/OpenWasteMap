"""
Tasks which are executed using celery.
"""

import itertools
import math
from pathlib import Path

from celery.decorators import task
from django.conf import settings

from .render import (
    EARTH_RADIUS,
    SAMPLE_MAX_INFLUENCE,
    TileRenderer,
    tile_xnum_from_longitude,
    tile_ynum_from_latitude,
)


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
    # TODO: Behaviour at edges of the coordinate system

    latitude = math.radians(latitude)
    longitude = math.radians(longitude)

    for zoom in range(19):
        max_distance = SAMPLE_MAX_INFLUENCE(zoom)

        # from the optimized Haversine with dlat / dlon = 0 respectively
        # we are calculating the bounding box of sample influence
        dlat = max_distance / EARTH_RADIUS
        # longitude depends on latitude and it is better to overestimate here
        overestimated_lat = latitude + dlat if latitude > 0 else latitude - dlat
        dlon = max_distance / (EARTH_RADIUS * math.cos(overestimated_lat))

        north_west = (latitude + dlat, longitude - dlon)
        south_east = (latitude - dlat, longitude + dlon)

        min_xy = (
            int(tile_xnum_from_longitude(zoom, north_west[1])),
            int(tile_ynum_from_latitude(zoom, north_west[0])),
        )
        max_xy = (
            int(tile_xnum_from_longitude(zoom, south_east[1])),
            int(tile_ynum_from_latitude(zoom, south_east[0])),
        )

        for x, y in itertools.product(
            range(min_xy[0], max_xy[0] + 1), range(min_xy[1], max_xy[1] + 1)
        ):
            out_path = (
                Path(settings.TILES_ROOT) / str(zoom) / str(x) / (str(y) + ".png")
            )
            out_path.unlink(missing_ok=True)
