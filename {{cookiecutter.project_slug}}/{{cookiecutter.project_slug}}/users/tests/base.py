# -*- coding: utf-8 -*-

"""Base classes for tests."""

from django.urls import include
from django.urls import path
from rest_framework.test import APITestCase
from rest_framework.test import URLPatternsTestCase

from .. import urls
from ..models import User


class UsersBaseTest(APITestCase, URLPatternsTestCase):
    """Base test case for users."""

    urlpatterns = [
        path('', include(urls, namespace='users')),
    ]

    def setUp(self):
        """Create a test user."""
        self.username = 'test'
        self.password = 'kah2ie3urh4k'

        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.login_post_data = {
            'username': self.username,
            'password': self.password,
        }

        self.staff_username = 'staff_test'
        self.staff_password = 'jhoda8adfkja'

        self.staff_user = User.objects.create_user(
            username=self.staff_username,
            password=self.staff_password,
            is_staff=True,
        )
        self.staff_login_post_data = {
            'username': self.staff_username,
            'password': self.staff_password,
        }
