"""
Tests for the Tile Server App.
"""

from django.test import TestCase
from django.urls import reverse


class TileServerTests(TestCase):
    """
    Test the Tile Server.
    """

    def test_server_accessible(self):
        """
        Test whether the tile server index can be loaded.
        """

        response = self.client.get(reverse('tile_server:index'))

        self.assertEqual(response.status_code, 200)

    def test_can_download_tiles(self):
        """
        Test that accessing a tile returns a png image.
        """

        response = self.client.get(reverse('tile_server:tile', kwargs={
            'zoom'      : 0,
            'xcoord'    : 0,
            'ycoord'    : 0,
        }))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], "image/png")
