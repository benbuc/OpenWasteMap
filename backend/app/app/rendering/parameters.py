"""
Parameters and constants which effect tile rendering.
"""

# radius (in m) of the samples maximum influence
SAMPLE_MAX_INFLUENCE = lambda zoom: 300.0 * 1.6 ** (14 - zoom)  # noqa: E731

# earth radius (in m)
EARTH_RADIUS = 6372.7982 * 1000

# the size of each tile in pixels
TILE_SIZE = 256
