"""
Test cases for the Accounts app.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserRegistrationTests(TestCase):
    """
    Test the ability for users to register on the site.
    """
    def setUp(self):
        "Setup User Registration Test Case"
        self.credentials = {
            'username': 'testuser',
            'email': 'mymail@example.com',
            'password1': 'MySup3erSecretK3Y',
            'password2': 'MySup3erSecretK3Y',
        }

    def test_registration_form_is_accessible(self):
        """
        The registration form can be loaded.
        """
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form")

    def test_can_create_user(self):
        """
        Test whether new users can be created.
        """
        response = self.client.post(reverse('accounts:register'), self.credentials)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username=self.credentials['username']).exists())