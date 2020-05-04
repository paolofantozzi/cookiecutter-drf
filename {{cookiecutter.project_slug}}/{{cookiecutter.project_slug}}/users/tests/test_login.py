# -*- coding: utf-8 -*-

"""Tests for login."""

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from {{ cookiecutter.project_slug }}.users.models import User


class TestLoginCase(APITestCase):
    """Test cases for logout."""

    login_url = reverse('users:login')
    refresh_token_url = reverse('users:token_refresh')
    my_profile_url = reverse('users:user-detail', kwargs={'pk': 'me'})

    username = 'test'
    password = 'kah2ie3urh4k'

    def setUp(self):
        """Create a test user."""
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.login_post_data = {
            'username': self.username,
            'password': self.password,
        }

    def test_login_return_code_200(self):
        """Test return code for login."""
        r = self.client.post(self.login_url, self.login_post_data)
        body = r.json()
        self.assertEqual(r.status_code, 200, body)

    def test_wrong_login_return_code_401(self):
        """Test return code for login."""
        r = self.client.post(self.login_url, {'username': 'no', 'password': 'no'})
        body = r.json()
        self.assertEqual(r.status_code, 401, body)

    def test_login_response_fields(self):
        """Test response fields for login."""
        r = self.client.post(self.login_url, self.login_post_data)
        body = r.json()
        self.assertIn('access', body, body)
        self.assertIn('refresh', body, body)

    def test_refresh_token_response_fields(self):
        """Test response fields for refresh token."""
        r = self.client.post(self.login_url, self.login_post_data)
        body = r.json()
        r = self.client.post(self.refresh_token_url, {'refresh': body['refresh']})
        body = r.json()
        self.assertIn('access', body, body)

    def test_refresh_token_return_code_200(self):
        """Test return code for refresh token."""
        r = self.client.post(self.login_url, self.login_post_data)
        body = r.json()
        r = self.client.post(self.refresh_token_url, {'refresh': body['refresh']})
        body = r.json()
        self.assertEqual(r.status_code, 200, body)

    def test_wrong_refresh_token_return_code_401(self):
        """Test return code for refresh token."""
        r = self.client.post(self.refresh_token_url, {'refresh': 'no'})
        body = r.json()
        self.assertEqual(r.status_code, 401, body)

    def test_wrong_refresh_token_error_code(self):
        """Test error code for refresh token."""
        r = self.client.post(self.refresh_token_url, {'refresh': 'no'})
        body = r.json()
        self.assertEqual(r.status_code, 401, body)
        self.assertEqual(body['code'], 'token_not_valid', body)

    def test_not_authenticated_request_return_code_403(self):
        """Test return code for not authenticated."""
        r = self.client.get(self.my_profile_url)
        body = r.json()
        self.assertEqual(r.status_code, 403, body)

    def test_authenticated_request_return_code_200(self):
        """Test return code for authenticated."""
        r = self.client.post(self.login_url, self.login_post_data)
        body = r.json()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(body['access']))
        r = self.client.get(self.my_profile_url)
        body = r.json()
        self.assertEqual(r.status_code, 200, body)
