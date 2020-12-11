# -*- coding: utf-8 -*-

"""Tests for retrieve."""

from rest_framework.reverse import reverse

from .base import UsersBaseTest


class TestRetrieveCase(UsersBaseTest):
    """Test cases for retrieve."""

    def retrieve_url(self, pk):
        """Return the retrieve url for a user primary key."""
        return reverse('users:user-detail', args=[pk])

    def test_not_authenticated_401(self):
        """Test return code for retrieve not authenticated."""
        req = self.client.get(self.retrieve_url('me'))
        body = req.json()
        self.assertEqual(req.status_code, 401, body)
        self.assertEqual(body['code'], 'not_authenticated', body)

    def test_not_found_for_other_user_if_not_staff_404(self):
        """Test not found in access to other user if it is not staff."""
        self.client.force_authenticate(self.user)
        req = self.client.get(self.retrieve_url(self.staff_user.id))
        body = req.json()
        self.assertEqual(req.status_code, 404, body)

    def test_access_to_othe_user_if_staff_200(self):
        """Test access 200 to other user if it is staff."""
        self.client.force_authenticate(self.staff_user)
        req = self.client.get(self.retrieve_url(self.user.id))
        body = req.json()
        self.assertEqual(req.status_code, 200, body)
        self.assertEqual(body['id'], self.user.id, body)
