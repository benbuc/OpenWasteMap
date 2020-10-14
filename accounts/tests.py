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
        num_users_before = User.objects.count()
        response = self.client.post(reverse('accounts:register'), self.credentials)
        num_users_after = User.objects.count()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username=self.credentials['username']).exists())
        self.assertGreater(num_users_after, num_users_before)

    def test_existing_username_gives_error_message(self):
        """
        Registering with an existing username must return an error message.
        """
        self.client.post(reverse('accounts:register'), self.credentials)
        num_users_before = User.objects.count()

        credentials = self.credentials
        credentials["email"] = "anothermail@example.com"
        user_two = self.client.post(reverse('accounts:register'), credentials)
        num_users_after = User.objects.count()

        self.assertEqual(user_two.status_code, 200)
        self.assertContains(user_two, "already exists")
        self.assertEqual(num_users_before, num_users_after)

    def test_register_with_valid_mail(self):
        """
        Users must only be allowed to register with an email address.
        """

        num_users_before = User.objects.count()

        credentials = self.credentials
        credentials["email"] = "testmail"

        response = self.client.post(reverse('accounts:register'), credentials)
        num_users_after = User.objects.count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(num_users_before, num_users_after)

    def test_user_can_register_full_name(self):
        """
        Test whether a user could enter a full name and all data can be read.
        """

        credentials = self.credentials
        credentials['first_name'] = "Obi-Wan"
        credentials['last_name']  = "Kenobi"

        response = self.client.post(reverse('accounts:register'), credentials)

        self.assertEqual(response.status_code, 200)
        user = User.objects.get(username=credentials['username'])

        self.assertEqual(user.email, credentials['email'])
        self.assertEqual(user.first_name, credentials['first_name'])
        self.assertEqual(user.last_name, credentials['last_name'])
