from django.test import TestCase
from django.urls import reverse
from django.core import mail
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
import re

User = get_user_model()

class AccountEndpointsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            're_password': 'testpassword123'
        }

    def test_user_registration_and_verification(self):
        # Test registration
        url = '/api/v1/auth/users/'
        response = self.client.post(url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the user exists but is not active
        user = User.objects.get(username=self.user_data['username'])
        self.assertFalse(user.is_active)

        # Check that an email was sent
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.to, [self.user_data['email']])

        # Extract activation link from email
        activation_link = re.search(r'http://\S+', email.body).group()
        uid = activation_link.split('/')[-2]
        token = activation_link.split('/')[-1]

        # Activate the user
        activation_url = "/api/v1/auth/users/activation/"
        activation_data = {'uid': uid, 'token': token}
        response = self.client.post(activation_url, activation_data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check that the user is now active
        user.refresh_from_db()
        self.assertTrue(user.is_active)

    def test_user_login_before_verification(self):
        # Register a user
        url = '/api/v1/auth/users/'
        self.client.post(url, self.user_data)

        # Try to login before verification
        login_url = reverse('accounts:v1:jwt-create')
        response = self.client.post(login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_login_after_verification(self):
        # Register and verify a user
        self.test_user_registration_and_verification()

        # Now try to login
        login_url = reverse('accounts:v1:jwt-create')
        response = self.client.post(login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_profile(self):
        # Register and verify a user
        self.test_user_registration_and_verification()

        # Login
        login_url = reverse('accounts:v1:jwt-create')
        login_response = self.client.post(login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        access_token = login_response.data['access']

        # Get user profile
        url = "/api/v1/auth/users/me/"
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user_data['username'])
        self.assertEqual(response.data['email'], self.user_data['email'])

    def test_password_reset_request(self):
        # Register and verify a user
        self.test_user_registration_and_verification()

        # Clear the outbox
        mail.outbox = []

        url = "/api/v1/auth/users/reset_password/"
        response = self.client.post(url, {'email': self.user_data['email']})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check that a password reset email was sent
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.to, [self.user_data['email']])

    def test_user_logout(self):
        # Register, verify, and login a user
        self.test_user_registration_and_verification()
        login_url = reverse('accounts:v1:jwt-create')
        login_response = self.client.post(login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        refresh_token = login_response.data['refresh']

        # Now test logout
        url = "/api/v1/auth/token/blacklist/"
        response = self.client.post(url, {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Try to use the refresh token after logout
        url = reverse('accounts:v1:jwt-refresh')
        response = self.client.post(url, {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh(self):
        # Register, verify, and login a user
        self.test_user_registration_and_verification()
        login_url = reverse('accounts:v1:jwt-create')
        login_response = self.client.post(login_url, {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        refresh_token = login_response.data['refresh']

        # Now test token refresh
        url = reverse('accounts:v1:jwt-refresh')
        response = self.client.post(url, {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)