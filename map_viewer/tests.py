"""
Test cases for the Map Viewer app.
"""

from django.test import TestCase
from django.urls import reverse

class MapViewerTests(TestCase):
    """
    Test the Map Viewer app.
    """

    def test_index_accessible(self):
        """
        Check if the index can be accessed.
        """

        response = self.client.get(reverse('map_viewer:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Map Viewer")
