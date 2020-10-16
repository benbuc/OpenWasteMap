"""
Test cases for the Accounts app.
"""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import authenticate, get_user_model

class UserSessionTests(TestCase):
    """
    Test the ability for authenticated users to use the site.
    """

    def setUp(self):
        """
        Sets up the UserSessionTests by creating a new user.
        """

        self.credentials = {
            'username'  : 'testuser',
            'email'     : 'mail@example.com',
            'password'  : 'MySup3erSecretK3Y',
        }
        user = get_user_model().objects.create_user(
            username=self.credentials['username'],
            email=self.credentials['email']
        )
        user.set_password(self.credentials['password'])
        user.save()

    def test_user_can_authenticate(self):
        """
        Test whether existing users can authenticate.
        """
        user = authenticate(
            username=self.credentials['username'],
            password=self.credentials['password'],
        )

        self.assertIsNotNone(user)
        self.assertTrue(user.is_authenticated)

    def test_wrong_password_cant_authenticate(self):
        """
        Test whether existing users can not authenticate with wrong passwords.
        """
        user = authenticate(
            username=self.credentials['username'],
            password=self.credentials['password']+"lalala",
        )

        self.assertIsNone(user)

    def test_login_page_accessible(self):
        """
        The login page is accessible.
        """
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form")

    def test_can_login_using_view(self):
        """
        Test whether users can log in using the login view.
        """
        response = self.client.post(reverse('accounts:login'), {
            'username': self.credentials['username'],
            'password': self.credentials['password'],
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('accounts:profile'))

    def test_restricted_access(self):
        """
        Using shall not be able to access the profile page without logging in.
        """
        profile_not_logged_in = self.client.get(reverse('accounts:profile'))

        self.assertEqual(profile_not_logged_in.status_code, 302)
        self.assertIn(reverse('accounts:login'), profile_not_logged_in.url)

        logged_in = self.client.login(
            username=self.credentials['username'],
            password=self.credentials['password'],
        )
        self.assertTrue(logged_in)

        profile_logged_in = self.client.get(reverse('accounts:profile'))
        self.assertEqual(profile_logged_in.status_code, 200)
        self.assertContains(profile_logged_in, self.credentials['username'])

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
        num_users_before = get_user_model().objects.count()
        response = self.client.post(reverse('accounts:register'), self.credentials)
        num_users_after = get_user_model().objects.count()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            get_user_model().objects.filter(username=self.credentials['username']).exists()
        )
        self.assertGreater(num_users_after, num_users_before)

    def test_existing_username_gives_error_message(self):
        """
        Registering with an existing username must return an error message.
        """
        self.client.post(reverse('accounts:register'), self.credentials)
        num_users_before = get_user_model().objects.count()

        credentials = self.credentials
        credentials["email"] = "anothermail@example.com"
        user_two = self.client.post(reverse('accounts:register'), credentials)
        num_users_after = get_user_model().objects.count()

        self.assertEqual(user_two.status_code, 200)
        self.assertContains(user_two, "already exists")
        self.assertEqual(num_users_before, num_users_after)

    def test_register_with_valid_mail(self):
        """
        Users must only be allowed to register with an email address.
        """

        num_users_before = get_user_model().objects.count()

        credentials = self.credentials
        credentials["email"] = "testmail"

        response = self.client.post(reverse('accounts:register'), credentials)
        num_users_after = get_user_model().objects.count()

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
        user = get_user_model().objects.get(username=credentials['username'])

        self.assertEqual(user.email, credentials['email'])
        self.assertEqual(user.first_name, credentials['first_name'])
        self.assertEqual(user.last_name, credentials['last_name'])
