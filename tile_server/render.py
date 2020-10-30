"""
Module for rendering a single OWM tile.
"""

import math
import numpy as np
from PIL import Image

from waste_samples.models import WasteSample

# radius (in m) of the samples maximum influence
SAMPLE_MAX_INFLUENCE = lambda zoom: 300.0 * 1.6**(14-zoom)

# earth radius (in m)
EARTH_RADIUS = 6372.7982 * 1000

# the size of each tile in pixels
TILE_SIZE = 256

# array of rgb colors and their stops from 0 to 1
# in form of (stop, r, g, b)
# stops have to be in order and contain 0 and 1
COLORS = [
    (0.0,    0.0, 255.0,   0.0),
    (0.2,  255.0, 248.0,   0.0),
    (0.30, 255.0, 171.0,   0.0),
    (0.75, 255.0,   0.0,   0.0),
    (0.9,  255.0,  13.0, 111.0),
    (1.0,  166.0, 150.0, 255.0)
]

def coordinates_from_tilename(zoom, xnum, ynum):
    """
    Calculate coordinates from tilename

    Calculates latitude and longitude of
    the north-western corner of the tile.
    For the other corners, invoke with xnum+1, ynum+1
    or xnum+1 and ynum+1 respectively
    https://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
    """

    num_tiles   = 2.0 ** zoom
    lon_deg     = xnum / num_tiles * 360.0 - 180.0
    lat_rad     = math.atan(math.sinh(math.pi * (1 - 2 * ynum / num_tiles)))
    lat_deg     = math.degrees(lat_rad)

    return (lat_deg, lon_deg)

def get_color_channels_for_waste_levels(waste_levels):
    """
    Convert array of waste levels to arrays for each color channel
    """

    normalized_levels = np.clip((waste_levels / 10.0)[..., None], 0, 1)

    pixels = np.zeros(waste_levels.shape + (3,))

    for col1, col2 in zip(COLORS, COLORS[1:]):
        mix = (normalized_levels - col1[0]) / (col2[0] - col1[0])
        color_section = (normalized_levels >= col1[0]) & (normalized_levels <= col2[0])

        color = np.array(col1[1:]) * (1-mix) + np.array(col2[1:]) * mix

        pixels = np.where(color_section, color, pixels)

    return pixels

class TileRenderer: # pylint: disable=too-many-instance-attributes
    """
    Used to render tiles containing the sample overlay.

    This converts the zoom level and x,y tile number to
    a PNG image with transparency.
    This image contains the weighted average for all samples
    which influence every given pixel.
    """

    def __init__(self, zoom, xnum, ynum):
        """
        Initialize with zoom level and and x,y tile numbers.
        """

        self.zoom    = zoom
        self.xnum    = xnum
        self.ynum    = ynum

        self.sample_max_influence = SAMPLE_MAX_INFLUENCE(zoom)

        self.tile_nw = coordinates_from_tilename(self.zoom, self.xnum, self.ynum)
        self.tile_se = coordinates_from_tilename(self.zoom, self.xnum+1, self.ynum+1)

        self.pixels  = np.zeros((TILE_SIZE, TILE_SIZE, 4))
        self.samples = self.get_samples()

    def get_coordinate_boundaries(self):
        """
        Returns the minimum and maximum latitude / longitude
        of which samples may influence the current tile.
        """
        # TO-DO: has weird behavior at the edges of the coordinate system

        lat_diff = math.degrees(self.sample_max_influence / EARTH_RADIUS)
        min_lat  = self.tile_se[0] - lat_diff
        max_lat  = self.tile_nw[0] + lat_diff

        # For the longitude difference,
        # use the latitude which is farther away from the equator
        lat_max  = math.radians(max(abs(min_lat), abs(max_lat)))

        quotient = math.sin(self.sample_max_influence / (2 * EARTH_RADIUS)) / math.cos(lat_max)
        lon_diff = abs(math.degrees(2 * math.asin(quotient)))
        min_lon  = self.tile_nw[1] - lon_diff
        max_lon   = self.tile_se[1] + lon_diff

        return (min_lat, max_lat, min_lon, max_lon)

    def get_samples(self):
        """
        Return a numpy array containing waste samples.

        The numpy array includes all waste samples which influence
        the current tile.
        For each sample it contains the waste level, latitude and longitude.
        """

        min_lat, max_lat, min_lon, max_lon = self.get_coordinate_boundaries()

        sample_objects = WasteSample.objects.filter(
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
                sample_object.longitude
            )

        return samples

    def get_pixel_coordinates(self):
        """
        Returns an array mapping each pixel to a lat / lon pair.
        """
        # TO-DO: we can not use linear interpolation for smaller zoom levels!

        latitudes  = np.linspace(self.tile_nw[0], self.tile_se[0], num=TILE_SIZE)
        longitudes = np.linspace(self.tile_nw[1], self.tile_se[1], num=TILE_SIZE)

        return np.array(np.meshgrid(latitudes, longitudes)).T

    def get_distance_array(self, pixel_coordinates):
        """
        Returns an array containing the distance from every pixel
        to every sample.
        """

        pixel_coordinates, samples = map(np.radians, [pixel_coordinates, self.samples])

        px_lat     = pixel_coordinates[..., 0, None]
        px_lon     = pixel_coordinates[..., 1, None]
        sample_lat = samples[..., 1]
        sample_lon = samples[..., 2]

        dlat       = px_lat - sample_lat
        dlon       = px_lon - sample_lon

        radicand   = np.sin(dlat/2.0)**2 + \
                     np.cos(px_lat) * np.cos(sample_lat) * np.sin(dlon/2.0)**2

        return 2 * EARTH_RADIUS * np.arcsin(np.sqrt(radicand))

    def get_confidence_levels(self, distances):
        """
        Returns an array containing the confidence for
        every sample at every pixel.
        """

        # clip values to range
        distances = np.clip(distances, 0, self.sample_max_influence)

        # calculate confidence levels
        return 1.0 - (distances / self.sample_max_influence)

    def get_weighted_average(self, confidence_levels):
        """
        Returns weighted average waste level for every pixel
        and the sum of confidence levels for every pixel.
        """

        confidence_sum   = np.sum(confidence_levels, axis=2)
        waste_levels_sum = np.sum(confidence_levels * self.samples[..., 0], axis=2)

        # confidence sums may be zero!
        # so only devide if there is confidence at this pixel
        average_waste_levels = np.divide(waste_levels_sum, confidence_sum,
            out=np.zeros_like(waste_levels_sum),
            where=confidence_sum!=0
        )

        return (average_waste_levels, confidence_sum)

    def render(self):
        """
        Render the tile and return the Image.
        """

        if not self.samples.size:
            return Image.new('RGBA', (TILE_SIZE, TILE_SIZE))

        pixel_coordinates = self.get_pixel_coordinates()

        distances = self.get_distance_array(pixel_coordinates)

        confidence_levels = self.get_confidence_levels(distances)

        waste_levels, confidence_sum = self.get_weighted_average(confidence_levels)

        blend = np.clip(confidence_sum, 0, 1) * 0.75
        self.pixels[..., :3] = get_color_channels_for_waste_levels(waste_levels)
        self.pixels[..., 3] = blend*255

        return Image.fromarray(self.pixels.astype(np.uint8))
