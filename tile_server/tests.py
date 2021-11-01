"""
Tests for the Tile Server App.
"""

import numpy as np
import PIL
from django.test import TestCase
from django.urls import reverse

import tile_server.render as r
from waste_samples.models import WasteSample


class TileServerTests(TestCase):
    """
    Test the Tile Server.
    """

    def test_server_accessible(self):
        """
        Test whether the tile server index can be loaded.
        """

        response = self.client.get(reverse("tile_server:index"))

        self.assertEqual(response.status_code, 200)

    def test_can_download_tiles(self):
        """
        Test that accessing a tile returns a png image.
        """

        response = self.client.get(
            reverse(
                "tile_server:tile",
                kwargs={
                    "zoom": 0,
                    "xcoord": 0,
                    "ycoord": 0,
                },
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["content-type"], "image/png")


class TileRenderTests(TestCase):
    """
    Test functions of tile rendering.
    """

    def setUp(self):
        """
        Set up test case by creating some samples.
        """

        self.tile = (13, 4407, 2686)
        WasteSample.objects.create(
            waste_level=0, latitude=52.521226, longitude=13.684172, user=None
        )

        self.renderer = r.TileRenderer(*self.tile)

    def test_color_channels_have_correct_shape(self):
        """
        Test that waste level to color conversion returns the correct shape.
        """

        levels = np.ones((r.TILE_SIZE, r.TILE_SIZE))
        colors = r.get_color_channels_for_waste_levels(levels)

        self.assertEqual(colors.shape, (r.TILE_SIZE, r.TILE_SIZE, 3))

    def test_found_samples(self):
        """
        Test that the sample was found in the rectangle.
        """

        self.assertGreater(len(self.renderer.samples), 0)

    def test_render_returns_image(self):
        """
        The render function has to return a PNG image.
        """

        rendered_image = self.renderer.render()
        self.assertIsInstance(rendered_image, PIL.Image.Image)

    def test_rendering_is_green(self):
        """
        The rendered images included the waste sample with level 0.
        """

        rendered_image = np.array(self.renderer.render())
        self.assertTrue((rendered_image[..., 0] == 0).all())
        self.assertTrue((rendered_image[..., 1] == 255).any())
        self.assertTrue((rendered_image[..., 2] == 0).all())
