# -*- coding: utf-8 -*-

"""Tests for create."""

from rest_framework.reverse import reverse

from .base import UsersBaseTest


class TestCreateCase(UsersBaseTest):
    """Test cases for create."""

    def setUp(self):
        """Reverse used urls."""
        super().setUp()
        self.user_create_url = reverse('users:user-list')
        self.create_data = self.generate_valid_user_data()
        self.read_only_fields = [
            'id',
            'is_email_validated',
            'access',
            'refresh',
            'access_token_expiring_time',
            'refresh_token_expiring_time',
        ]

    def test_create_201(self):
        """Test return code for create."""
        req = self.client.post(self.user_create_url, self.create_data)
        body = req.json()
        self.assertEqual(req.status_code, 201, body)
        for field, field_value in self.create_data.items():
            if field == 'password':
                continue
            self.assertEqual(body[field], field_value.strip(), body)

        for read_only_field in self.read_only_fields:
            self.assertIn(read_only_field, body, body)

    def test_create_staff_by_non_staff_error_400(self):
        """Test error for create a staff user if self is not staff."""
        self.client.force_authenticate(self.user)
        req = self.client.post(self.user_create_url, {**self.create_data, 'is_staff': True})
        body = req.json()
        self.assertEqual(req.status_code, 400, body)

    def test_create_staff_by_staff_error_201(self):
        """Test create a staff user if self is staff."""
        self.client.force_authenticate(self.staff_user)
        req = self.client.post(self.user_create_url, {**self.create_data, 'is_staff': True})
        body = req.json()
        self.assertEqual(req.status_code, 201, body)
