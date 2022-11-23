"""
Module for rendering a single OWM tile.
"""

import math
from typing import Optional

import numpy as np
from PIL import Image

from app import crud
from app.db.session import SessionLocal

from .parameters import EARTH_RADIUS, SAMPLE_MAX_INFLUENCE, TILE_SIZE
from .utilities import latitude_from_tilename, longitude_from_tilename

# array of rgb colors and their stops from 0 to 1
# in form of (stop, r, g, b)
# stops have to be in order and contain 0 and 1
COLORS = [
    (0.0, 0.0, 255.0, 0.0),
    (0.2, 255.0, 248.0, 0.0),
    (0.30, 255.0, 171.0, 0.0),
    (0.75, 255.0, 0.0, 0.0),
    (0.9, 255.0, 13.0, 111.0),
    (1.0, 166.0, 150.0, 255.0),
]

DATATYPE = np.float32


def get_color_channels_for_waste_levels(waste_levels):
    """
    Convert array of waste levels to arrays for each color channel
    """

    normalized_levels = np.clip((waste_levels / 10.0)[..., None], 0, 1)

    pixels = np.zeros(waste_levels.shape + (3,))

    for col1, col2 in zip(COLORS, COLORS[1:]):
        mix = (normalized_levels - col1[0]) / (col2[0] - col1[0])
        color_section = (normalized_levels >= col1[0]) & (normalized_levels <= col2[0])

        color = np.array(col1[1:]) * (1 - mix) + np.array(col2[1:]) * mix

        pixels = np.where(color_section, color, pixels)

    return pixels


class TileRenderer:  # pylint: disable=too-many-instance-attributes
    """
    Used to render tiles containing the sample overlay.

    This converts the zoom level and x,y tile number to
    a PNG image with transparency.
    This image contains the weighted average for all samples
    which influence every given pixel.
    """

    def __init__(self, zoom, xnum, ynum, owner_id: Optional[int] = None):
        """
        Initialize with zoom level and and x,y tile numbers.
        """

        self.owner_id = owner_id

        self.zoom = zoom
        self.xnum = xnum
        self.ynum = ynum

        self.sample_max_influence = SAMPLE_MAX_INFLUENCE(zoom)

        self.tile_nw = (
            math.degrees(latitude_from_tilename(zoom, ynum)),
            math.degrees(longitude_from_tilename(zoom, xnum)),
        )
        self.tile_se = (
            math.degrees(latitude_from_tilename(zoom, ynum + 1)),
            math.degrees(longitude_from_tilename(zoom, xnum + 1)),
        )

        self.pixels = np.zeros((TILE_SIZE, TILE_SIZE, 4), dtype=DATATYPE)
        self.samples = self.get_samples()

    def get_coordinate_boundaries(self):
        """
        Returns the minimum and maximum latitude / longitude
        of which samples may influence the current tile.
        """
        # TO-DO: has weird behavior at the edges of the coordinate system

        lat_diff = math.degrees(self.sample_max_influence / EARTH_RADIUS)
        min_lat = self.tile_se[0] - lat_diff
        max_lat = self.tile_nw[0] + lat_diff

        # For the longitude difference,
        # use the latitude which is farther away from the equator
        lat_max = math.radians(max(abs(min_lat), abs(max_lat)))

        quotient = math.sin(self.sample_max_influence / (2 * EARTH_RADIUS)) / math.cos(
            lat_max
        )
        lon_diff = abs(math.degrees(2 * math.asin(quotient)))
        min_lon = self.tile_nw[1] - lon_diff
        max_lon = self.tile_se[1] + lon_diff

        return (min_lat, max_lat, min_lon, max_lon)

    def get_samples(self):
        """
        Return a numpy array containing waste samples.

        The numpy array includes all waste samples which influence
        the current tile.
        For each sample it contains the waste level, latitude and longitude.
        """

        min_lat, max_lat, min_lon, max_lon = self.get_coordinate_boundaries()

        with SessionLocal() as db:
            sample_objects = crud.waste_sample.get_multi_in_range(
                db,
                min_lat=min_lat,
                max_lat=max_lat,
                min_lon=min_lon,
                max_lon=max_lon,
                owner_id=self.owner_id,
            )

        samples = np.zeros((len(sample_objects), 3), dtype=DATATYPE)

        for i, sample_object in enumerate(sample_objects):
            sample_object = sample_objects[i]
            samples[i] = (
                sample_object.waste_level,
                sample_object.latitude,
                sample_object.longitude,
            )

        return samples

    def get_pixel_coordinates(self):
        """
        Returns an array mapping each pixel to a lat / lon pair.
        """

        pixel_position_y = np.linspace(
            self.ynum, self.ynum + 1, num=TILE_SIZE, endpoint=False, dtype=DATATYPE
        )
        latitudes = latitude_from_tilename(self.zoom, pixel_position_y)

        west_lon, east_lon = (
            longitude_from_tilename(self.zoom, self.xnum + i) for i in [0, 1]
        )
        longitudes = np.linspace(
            west_lon, east_lon, num=TILE_SIZE, endpoint=False, dtype=DATATYPE
        )

        return np.array(np.meshgrid(latitudes, longitudes)).T

    def get_distance_array(self, pixel_coordinates):
        """
        Returns an array containing the distance from every pixel
        to every sample.
        """

        samples = np.radians(self.samples)

        px_lat = pixel_coordinates[..., 0, None]
        px_lon = pixel_coordinates[..., 1, None]
        sample_lat = samples[..., 1]
        sample_lon = samples[..., 2]

        dlat = px_lat - sample_lat

        # This allows us to use small-angle approximation even at the edges
        # of the coordinate system (longitude around -180 oder 180 degrees)
        # if for a pixel the longitude difference becomes larger than 180 degrees
        # we are simply subtracting 360 degrees.
        # This works with the assumption, that the maximum influence of a sample does
        # not exceed 180 degrees.
        dlon = np.abs(px_lon - sample_lon)
        dlon[dlon > np.pi] -= 2 * np.pi

        # This is a highly optimized version of the Haversine formula
        return EARTH_RADIUS * np.sqrt(
            (dlat**2) + (np.cos(sample_lat) ** 2) * (dlon**2)
        )

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

        confidence_sum = np.sum(confidence_levels, axis=2)
        waste_levels_sum = np.sum(confidence_levels * self.samples[..., 0], axis=2)

        # confidence sums may be zero!
        # so only devide if there is confidence at this pixel
        average_waste_levels = np.divide(
            waste_levels_sum,
            confidence_sum,
            out=np.zeros_like(waste_levels_sum),
            where=confidence_sum != 0,
        )

        return (average_waste_levels, confidence_sum)

    def render(self):
        """
        Render the tile and return the Image.
        """

        if not self.samples.size:
            return Image.new("RGBA", (TILE_SIZE, TILE_SIZE))

        pixel_coordinates = self.get_pixel_coordinates()

        distances = self.get_distance_array(pixel_coordinates)

        confidence_levels = self.get_confidence_levels(distances)

        waste_levels, confidence_sum = self.get_weighted_average(confidence_levels)

        blend = np.clip(confidence_sum, 0, 1) * 0.75
        self.pixels[..., :3] = get_color_channels_for_waste_levels(waste_levels)
        self.pixels[..., 3] = blend * 255

        return Image.fromarray(self.pixels.astype(np.uint8))
