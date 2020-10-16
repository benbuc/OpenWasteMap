"""
Tests for the Waste Samples App.
"""

from django.test import TestCase
from django.contrib.auth.models import User

from .models import WasteSample

def create_sample(waste_level=5, latitude=12.345, longitude=23.456, user=None):
    """
    Create WasteSample with the given parameters.
    """
    return WasteSample.objects.create(
        waste_level=waste_level,
        latitude=latitude,
        longitude=longitude,
        user=user,
    )

class WasteSampleModelTests(TestCase):
    """
    Test for the Waste Sample model.
    """

    def test_can_create_sample(self):
        """
        Test whether samples can be created.
        """
        sample = create_sample(waste_level=1)

        self.assertEqual(sample.waste_level, 1)

    def test_string_representation_with_user(self):
        """
        Test whether the string representation contains the waste level and username.
        """
        testuser = User.objects.create_user(username="testuser")
        sample = create_sample(waste_level=2, user=testuser)

        self.assertIn(str(2), str(sample))
        self.assertIn(testuser.username, str(sample))

    def test_string_representation_no_user(self):
        """
        Test whether the string representation contains the waste level and 'Null'.
        """
        sample = create_sample(waste_level=2)

        self.assertIn(str(2), str(sample))
        self.assertIn("Null", str(sample))
