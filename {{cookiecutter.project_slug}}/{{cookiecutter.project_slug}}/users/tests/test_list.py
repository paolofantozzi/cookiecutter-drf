# -*- coding: utf-8 -*-

"""Tests for list."""

from rest_framework.reverse import reverse

from .base import UsersBaseTest


class TestListCase(UsersBaseTest):
    """Test cases for list."""

    def setUp(self):
        """Reverse used urls."""
        super().setUp()
        self.users_list_url = reverse('users:user-list')

    def test_not_authenticated_401(self):
        """Test return code for list not authenticated."""
        req = self.client.get(self.users_list_url)
        body = req.json()
        self.assertEqual(req.status_code, 401, body)
        self.assertEqual(body['code'], 'not_authenticated', body)

    def test_only_self_in_list_not_staff(self):
        """Test return only self in list if not staff."""
        self.client.force_authenticate(self.user)
        req = self.client.get(self.users_list_url)
        body = req.json()
        self.assertEqual(req.status_code, 200, body)
        self.assertEqual(len(body), 1, body)
        self.assertEqual(body[0]['id'], self.user.id, body)

    def test_many_users_in_list_if_staff(self):
        """Test return many users in list if not staff."""
        self.client.force_authenticate(self.staff_user)
        req = self.client.get(self.users_list_url)
        body = req.json()
        self.assertEqual(req.status_code, 200, body)
        self.assertGreater(len(body), 1, body)
