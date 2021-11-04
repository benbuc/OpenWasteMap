"""
Tests for the Waste Samples App.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from utilities.test_utilities import get_testuser

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
        testuser = get_user_model().objects.create_user(username="testuser")
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


class WasteSampleRestrictedAccessTest(TestCase):
    """
    Protected areas shall not be accessed by unauthenticated users.
    """

    def test_index_shows_no_username(self):
        """
        The waste sample index page does not show a username.
        """

        user = get_user_model().objects.create_user(
            "testuser", "test@test.org", "temppw"
        )
        create_sample(2, 3.1415, 2.71, user)

        response = self.client.get(reverse("waste_samples:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(2))
        self.assertContains(response, str(3.1415))
        self.assertContains(response, str(2.71))
        self.assertNotContains(response, user.username)

    def test_access_sample_creation_without_login(self):
        """
        People may not be able to access the creation view
        without a valid session.
        """

        response = self.client.get(reverse("waste_samples:create"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)


class WasteSampleCreationViewTest(TestCase):
    """
    Logged in users can create Waste Samples
    through the creation view.
    """

    def setUp(self):
        """
        Set Up test by creating a test user and logging in.
        """

        self.user, self.credentials = get_testuser()
        self.client.login(**self.credentials)

    def test_creation_view_accessible(self):
        """
        The view for creating a Waste Sample can be accessed.
        """

        response = self.client.get(reverse("waste_samples:create"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form")

    def test_can_create_sample(self):
        """
        Posted data to the view can be read from the database.
        """

        sample_data = {
            "waste_level": 7,
            "latitude": 42.8,
            "longitude": 43.3,
        }

        total_before = WasteSample.objects.count()
        response = self.client.post(reverse("waste_samples:create"), sample_data)
        total_after = WasteSample.objects.count()

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            WasteSample.objects.filter(waste_level=sample_data["waste_level"]).exists()
        )
        self.assertGreater(total_after, total_before)
        self.assertTrue(
            self.user.wastesample_set.filter(waste_level=sample_data["waste_level"])
        )
