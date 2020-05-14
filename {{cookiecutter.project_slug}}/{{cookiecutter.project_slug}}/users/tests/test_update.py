# -*- coding: utf-8 -*-

"""Tests for update."""

from rest_framework.reverse import reverse

from .base import UsersBaseTest


class TestUpdateCase(UsersBaseTest):
    """Test cases for update."""

    def generate_update_data(self):
        """Generate new user data for update."""
        new_data = self.generate_valid_user_data()
        new_data.pop('username')  # username can't be changed with standard flow
        new_data.pop('email')  # email can't be changed with standard flow
        new_data.pop('password')  # password can't be changed with standard flow
        return new_data

    def update_url(self, pk):
        """Return the retrieve url for a user primary key."""
        return reverse('users:user-detail', kwargs={'pk': pk})

    def test_not_authenticated_401(self):
        """Test return code for update not authenticated."""
        new_data = self.generate_update_data()
        req = self.client.put(self.update_url(self.user.id), new_data)
        body = req.json()
        self.assertEqual(req.status_code, 401, body)
        self.assertEqual(body['code'], 'not_authenticated', body)

    def test_not_found_for_other_user_if_not_staff_404(self):
        """Test not found in access to other user if it is not staff."""
        self.client.force_authenticate(self.user)
        new_data = self.generate_update_data()
        req = self.client.put(self.update_url(self.staff_user.id), new_data)
        body = req.json()
        self.assertEqual(req.status_code, 404, body)

    def test_update_to_other_user_if_staff_200(self):
        """Test update 200 to other user if it is staff."""
        self.client.force_authenticate(self.staff_user)
        new_data = self.generate_update_data()
        req = self.client.put(self.update_url(self.user.id), new_data)
        body = req.json()
        self.assertEqual(req.status_code, 200, body)
        self.assertEqual(body['id'], self.user.id, body)
        for key, update_value in new_data.items():
            self.assertEqual(body[key], update_value.strip(), body)

    def test_update_self_200(self):
        """Test update 200 to self."""
        self.client.force_authenticate(self.user)
        new_data = self.generate_update_data()
        req = self.client.put(self.update_url(self.user.id), new_data)
        body = req.json()
        self.assertEqual(req.status_code, 200, body)
        self.assertEqual(body['id'], self.user.id, body)
        for key, update_value in new_data.items():
            self.assertEqual(body[key], update_value.strip(), body)

    def test_patch_not_authenticated_401(self):
        """Test return code for update not authenticated."""
        new_data = self.generate_update_data()
        req = self.client.patch(self.update_url(self.user.id), new_data)
        body = req.json()
        self.assertEqual(req.status_code, 401, body)
        self.assertEqual(body['code'], 'not_authenticated', body)

    def test_patch_not_found_for_other_user_if_not_staff_404(self):
        """Test not found in access to other user if it is not staff."""
        self.client.force_authenticate(self.user)
        new_data = self.generate_update_data()
        req = self.client.patch(self.update_url(self.staff_user.id), new_data)
        body = req.json()
        self.assertEqual(req.status_code, 404, body)

    def test_patch_update_to_other_user_if_staff_200(self):
        """Test update 200 to other user if it is staff."""
        self.client.force_authenticate(self.staff_user)
        new_data = self.generate_update_data()
        req = self.client.patch(self.update_url(self.user.id), new_data)
        body = req.json()
        self.assertEqual(req.status_code, 200, body)
        self.assertEqual(body['id'], self.user.id, body)
        for key, update_value in new_data.items():
            self.assertEqual(body[key], update_value.strip(), body)

    def test_patch_update_self_200(self):
        """Test update 200 to self."""
        self.client.force_authenticate(self.user)
        new_data = self.generate_update_data()
        req = self.client.patch(self.update_url(self.user.id), new_data)
        body = req.json()
        self.assertEqual(req.status_code, 200, body)
        self.assertEqual(body['id'], self.user.id, body)
        for key, update_value in new_data.items():
            self.assertEqual(body[key], update_value.strip(), body)
