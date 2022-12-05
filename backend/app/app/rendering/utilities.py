import itertools

import numpy as np

from app.schemas.tile_cache import Tile

from .parameters import EARTH_RADIUS, SAMPLE_MAX_INFLUENCE


def num_tiles(zoom):
    "Number of tiles in an axis for a zoom level"
    return 2.0**zoom


# Calculate coordinates from tilename
#
# Calculates latitude and longitude of
# the north-western corner of the tile.
# For the other corners, invoke with xnum+1, ynum+1
# or xnum+1 and ynum+1 respectively
# https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
def latitude_from_tilename(zoom, ynum):
    return np.arctan(np.sinh(np.pi * (1 - 2 * ynum / num_tiles(zoom))))


def tile_ynum_from_latitude(zoom, latitude):
    return (1 - np.arcsinh(np.tan(latitude)) / np.pi) / 2 * num_tiles(zoom)


def longitude_from_tilename(zoom, xnum):
    return xnum / num_tiles(zoom) * 2.0 * np.pi - np.pi


def tile_xnum_from_longitude(zoom, longitude):
    return (longitude + np.pi) / (2 * np.pi) * num_tiles(zoom)


def tiles_affected_by_sample(latitude, longitude):
    """
    Generator returns (zoom, xnum, ynum) for all tiles which
    are affected by a sample at the given coordinates.
    """
    # TODO: Behaviour at edges of the coordinate system

    latitude, longitude = np.radians((latitude, longitude))

    for zoom in range(19):
        max_distance = SAMPLE_MAX_INFLUENCE(zoom)

        # from the optimized Haversine with dlat / dlon = 0 respectively
        # we are calculating the bounding box of sample influence
        dlat = max_distance / EARTH_RADIUS
        # longitude depends on latitude and it is better to overestimate here
        overestimated_lat = latitude + dlat if latitude > 0 else latitude - dlat
        dlon = max_distance / (EARTH_RADIUS * np.cos(overestimated_lat))

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
            yield Tile(zoom=zoom, xcoord=x, ycoord=y)
