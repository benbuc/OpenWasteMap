"""
Module for rendering a single OWM tile.
"""

import math
import numpy as np
from PIL import Image

from waste_samples.models import WasteSample

# radius (in m) of the samples maximum influence
SAMPLE_MAX_INFLUENCE = 250.0

# earth radius (in m)
EARTH_RADIUS = 6372.7982 * 1000

def coord_from_tilename(zoom, xcoord, ycoord):
    """
    Calculate coordinates from tilename

    Returns (latitude, longitude) of the north-western corner of the tile.
    Coordinates are returned in degrees
    https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
    """

    z_pot   = 2.0 ** zoom
    lon     = xcoord / z_pot * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ycoord / z_pot)))
    lat     = math.degrees(lat_rad)

    return (lat, lon)

def get_samples(tile_nw, tile_se):
    """
    Get samples from rectangle and border.

    Returns all samples within the given rectangle
    plus the samples which may influence the given rectangle.
    """

    # TO-DO: has weird behavior at the edges of the coordinate system
    lat_diff    = math.degrees(SAMPLE_MAX_INFLUENCE / EARTH_RADIUS)
    min_lat     = tile_se[0] - lat_diff
    max_lat     = tile_nw[0] + lat_diff

    # for the longitude difference
    # use the latitude which is farther away from the equator
    if abs(max_lat) > abs(min_lat):
        lat = max_lat
    else:
        lat = min_lat

    quotient = math.sin(SAMPLE_MAX_INFLUENCE / (2 * EARTH_RADIUS)) / math.cos(lat)
    lon_diff_rad = 2 * math.asin(quotient)
    lon_diff = math.degrees(lon_diff_rad)
    min_lon  = tile_nw[1] - lon_diff
    max_lon  = tile_se[1] + lon_diff

    sample_objects  = WasteSample.objects.filter(
        latitude__gte=min_lat,
        latitude__lte=max_lat,
        longitude__gte=min_lon,
        longitude__lte=max_lon,
    )

    samples = np.zeros((len(sample_objects), 3))

    for i, sample_object in enumerate(sample_objects):
        sample_object = sample_objects[i]
        samples[i] = (
            sample_object.waste_level,
            sample_object.latitude,
            sample_object.longitude,
        )

    return samples

def haversine_2d(pxLat, pxLon, samLat, samLon):

    pxLat, pxLon, samLat, samLon = map(np.radians, [pxLat, pxLon, samLat, samLon])
    pxLat = pxLat[..., None]
    pxLon = pxLon[..., None]

    dlat = pxLat - samLat
    dlon = pxLon - samLon

    # Great circle distance
    a = np.sin(dlat/2.0)**2 + np.cos(pxLat) * np.cos(samLat) * np.sin(dlon/2.0)**2
    #a = (dlat/2.0)**2 + np.cos(pxLat) * np.cos(samLat) * (dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))

    return c * 6367000

def render_tile(zoom, xcoord, ycoord):
    """
    Render the tile with the given name.
    """

    tile_nw = coord_from_tilename(zoom, xcoord, ycoord)
    tile_se = coord_from_tilename(zoom, xcoord+1, ycoord+1)

    tile    = Image.new('RGBA', (256,256))
    pixels  = np.array(tile)
    samples = get_samples(tile_nw, tile_se)

    if (len(samples) == 0):
        return tile

    # create array mapping each pixel coordinate to a lat / lon pair
    lats = np.linspace(tile_nw[0], tile_se[0], num=256)
    lons = np.linspace(tile_nw[1], tile_se[1], num=256)
    px_loc = np.array(np.meshgrid(lats, lons)).T

    # array containing every pixels distance to every sample
    d = haversine_2d(px_loc[..., 0], px_loc[..., 1], samples[..., 1], samples[..., 2])
    # clip values to range
    d = np.clip(d, 0, SAMPLE_MAX_INFLUENCE)
    # array containing the confidence levels for every sample at every pixel
    c = 1.0 - (d / SAMPLE_MAX_INFLUENCE)
    # array containing the sum of confidence levels of every sample at every pixel
    sc = np.sum(c, axis=2)

    # array containing the sum of weighted waste levels for every pixel
    sw = np.sum(c * samples[..., 0], axis=2)

    # array containing waste levels (weighted average of samples) for every pixel
    wl = np.divide(sw, sc, out=np.zeros_like(sw), where=sc!=0)

    blend = np.clip(sc, 0, 1) * 0.75
    wl *= 25

    # update channel color
    pixels[..., 0] = wl
    pixels[..., 1] = (255-wl)
    pixels[..., 2] = 0
    pixels[..., 3] = blend*255

    tile = Image.fromarray(pixels.astype(np.uint8))

    return tile

def get_tile(zoom, xcoord, ycoord):
    """
    Return the tile with the given name.
    """

    return render_tile(zoom, xcoord, ycoord)
