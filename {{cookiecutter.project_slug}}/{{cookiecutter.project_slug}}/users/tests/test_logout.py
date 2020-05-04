# -*- coding: utf-8 -*-

"""Tests for logout.

Originally developed by orehush (https://gist.github.com/orehush/667c79b28fdc94f86746bd15694d1167).
"""

from functools import partial

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from {{ cookiecutter.project_slug }}.users.models import User


class TestLogoutCase(APITestCase):
    """Test cases for logout.

    Originally developed by orehush (https://gist.github.com/orehush/667c79b28fdc94f86746bd15694d1167).
    """

    login_url = reverse('users:login')
    refresh_token_url = reverse('users:token_refresh')
    logout_url = reverse('users:logout')

    username = 'test'
    password = 'kah2ie3urh4k'

    def setUp(self):
        """Create a test user."""
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def _login(self):
        data = {
            'username': self.username,
            'password': self.password,
        }
        r = self.client.post(self.login_url, data)
        body = r.json()
        if 'access' in body:
            self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(body['access']))
        return r.status_code, body

    def test_logout_response_204(self):
        """Test return code 204 for logout."""
        _, body = self._login()
        data = {'refresh': body['refresh']}
        r = self.client.post(self.logout_url, data)
        body = r.content
        self.assertEqual(r.status_code, 204, body)
        self.assertFalse(body, body)

    def test_logout_with_bad_refresh_token_response_400(self):
        """Test return code 400 for bad refresh token."""
        self._login()
        data = {'refresh': 'dsf.sdfsdf.sdf'}
        r = self.client.post(self.logout_url, data)
        body = r.json()
        self.assertEqual(r.status_code, 400, body)
        self.assertTrue(body, body)

    def test_logout_refresh_token_in_blacklist(self):
        """Test exception for using blacklisted refresh token."""
        _, body = self._login()
        self.client.post(self.logout_url, body)
        token = partial(RefreshToken, body['refresh'])
        self.assertRaises(TokenError, token)
