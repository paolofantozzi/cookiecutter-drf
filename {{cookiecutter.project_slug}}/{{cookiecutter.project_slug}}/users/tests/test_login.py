# -*- coding: utf-8 -*-

"""Tests for login."""

from rest_framework.reverse import reverse

from .base import UsersBaseTest


class TestLoginCase(UsersBaseTest):
    """Test cases for login."""

    def setUp(self):
        """Reverse used urls."""
        super().setUp()
        self.login_url = reverse('users:jwt-create')
        self.refresh_token_url = reverse('users:jwt-refresh')
        self.my_profile_url = reverse('users:user-me')

    def test_login_return_code_200(self):
        """Test return code for login."""
        req = self.client.post(self.login_url, self.login_post_data)
        body = req.json()
        self.assertEqual(req.status_code, 200, body)

    def test_wrong_login_return_code_401(self):
        """Test return code for login."""
        req = self.client.post(self.login_url, {'username': 'no', 'password': 'no'})
        body = req.json()
        self.assertEqual(req.status_code, 401, body)
        self.assertEqual(body['code'], 'authentication_failed', body)

    def test_login_response_fields(self):
        """Test response fields for login."""
        req = self.client.post(self.login_url, self.login_post_data)
        body = req.json()
        self.assertIn('access', body, body)
        self.assertIn('refresh', body, body)

    def test_refresh_token_response_fields(self):
        """Test response fields for refresh token."""
        req = self.client.post(self.login_url, self.login_post_data)
        body = req.json()
        req = self.client.post(self.refresh_token_url, {'refresh': body['refresh']})
        body = req.json()
        self.assertIn('access', body, body)
        self.assertNotIn('refresh', body, body)

    def test_refresh_token_return_code_200(self):
        """Test return code for refresh token."""
        req = self.client.post(self.login_url, self.login_post_data)
        body = req.json()
        req = self.client.post(self.refresh_token_url, {'refresh': body['refresh']})
        body = req.json()
        self.assertEqual(req.status_code, 200, body)

    def test_wrong_refresh_token_return_code_401(self):
        """Test return code for refresh token."""
        req = self.client.post(self.refresh_token_url, {'refresh': 'no'})
        body = req.json()
        self.assertEqual(req.status_code, 401, body)
        self.assertEqual(body['code'], 'token_not_valid', body)

    def test_wrong_refresh_token_error_code(self):
        """Test error code for refresh token."""
        req = self.client.post(self.refresh_token_url, {'refresh': 'no'})
        body = req.json()
        self.assertEqual(req.status_code, 401, body)
        self.assertEqual(body['code'], 'token_not_valid', body)

    def test_not_authenticated_request_return_code_401(self):
        """Test return code for not authenticated."""
        req = self.client.get(self.my_profile_url)
        body = req.json()
        self.assertEqual(req.status_code, 401, body)
        self.assertEqual(body['code'], 'not_authenticated', body)

    def test_authenticated_request_return_code_200(self):
        """Test return code for authenticated."""
        req = self.client.post(self.login_url, self.login_post_data)
        body = req.json()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(body['access']))
        req = self.client.get(self.my_profile_url)
        body = req.json()
        self.assertEqual(req.status_code, 200, body)

    def test_authenticated_with_wrong_token_request_return_code_401(self):
        """Test return code for wrong authenticated."""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format('wrongtoken'))
        req = self.client.get(self.my_profile_url)
        body = req.json()
        self.assertEqual(req.status_code, 401, body)
        self.assertEqual(body['code'], 'token_not_valid', body)
