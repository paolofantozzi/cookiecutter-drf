# -*- coding: utf-8 -*-

"""Tests for logout.

Originally developed by orehush (https://gist.github.com/orehush/667c79b28fdc94f86746bd15694d1167).
"""

from functools import partial

from rest_framework.reverse import reverse
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .base import UsersBaseTest


class TestLogoutCase(UsersBaseTest):
    """Test cases for logout.

    Originally developed by orehush (https://gist.github.com/orehush/667c79b28fdc94f86746bd15694d1167).
    """

    def setUp(self):
        """Reverse used urls."""
        super().setUp()
        self.login_url = reverse('users:jwt-create')
        self.refresh_token_url = reverse('users:jwt-refresh')
        self.logout_url = reverse('users:jwt-logout')

    def test_logout_need_authentication(self):
        """Test logout needs to be authenticated."""
        req = self.client.post(self.login_url, self.login_post_data)
        body = req.json()
        req = self.client.post(self.logout_url, {'refresh': body['refresh']})
        body = req.json()
        self.assertEqual(req.status_code, 401, body)
        self.assertEqual(body['code'], 'not_authenticated', body)

    def test_logout_response_200(self):
        """Test return code 200 for logout."""
        req = self.client.post(self.login_url, self.login_post_data)
        body = req.json()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(body['access']))
        req = self.client.post(self.logout_url, {'refresh': body['refresh']})
        body = req.json()
        self.assertEqual(req.status_code, 200, body)

    def test_logout_with_bad_refresh_token_response_400(self):
        """Test return code 400 for bad refresh token."""
        req = self.client.post(self.login_url, self.login_post_data)
        body = req.json()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(body['access']))
        req = self.client.post(self.logout_url, {'refresh': 'dsf.sdfsdf.sdf'})
        body = req.json()
        self.assertEqual(req.status_code, 400, body)

    def test_logout_refresh_token_in_blacklist(self):
        """Test exception for using blacklisted refresh token."""
        req = self.client.post(self.login_url, self.login_post_data)
        body = req.json()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(body['access']))
        self.client.post(self.logout_url, {'refresh': body['refresh']})
        token = partial(RefreshToken, body['refresh'])
        self.assertRaises(TokenError, token)

    def test_refresh_token_in_blacklist(self):
        """Test refresh token in blacklist."""
        req = self.client.post(self.login_url, self.login_post_data)
        body = req.json()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(body['access']))
        self.client.post(self.logout_url, {'refresh': body['refresh']})
        req = self.client.post(self.refresh_token_url, {'refresh': body['refresh']})
        body = req.json()
        self.assertEqual(req.status_code, 401, body)
        self.assertEqual(body['code'], 'token_not_valid', body)
