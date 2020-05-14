# -*- coding: utf-8 -*-

"""Tests for delete."""

from rest_framework.reverse import reverse

from ..models import User
from .base import UsersBaseTest


class TestDestroyCase(UsersBaseTest):
    """Test cases for destroy."""

    def destroy_url(self, pk):
        """Return the destroy url for a user primary key."""
        return reverse('users:user-detail', kwargs={'pk': pk})

    def test_not_authenticated_401(self):
        """Test return code for delete not authenticated."""
        req = self.client.delete(self.destroy_url('me'))
        body = req.json()
        self.assertEqual(req.status_code, 401, body)
        self.assertEqual(body['code'], 'not_authenticated', body)

    def test_not_found_for_other_user_if_not_staff_404(self):
        """Test not found in access to other user if it is not staff."""
        self.client.force_authenticate(self.user)
        req = self.client.delete(self.destroy_url(self.staff_user.id))
        body = req.json()
        self.assertEqual(req.status_code, 404, body)

    def test_access_to_other_user_if_staff_204(self):
        """Test access 200 to other user if it is staff."""
        self.client.force_authenticate(self.staff_user)
        req = self.client.delete(self.destroy_url(self.user.id))
        self.assertEqual(req.status_code, 204, req)
        user_on_db = User.objects.get(pk=self.user.id)
        self.assertFalse(user_on_db.is_active, req)
