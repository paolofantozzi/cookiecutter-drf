# -*- coding: utf-8 -*-

"""Base classes for tests."""

from django.urls import include
from django.urls import path
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework.test import URLPatternsTestCase

from .. import urls
from .factories import UserFactory


class UsersBaseTest(APITestCase, URLPatternsTestCase):
    """Base test case for users."""

    urlpatterns = [
        path('', include(urls, namespace='users')),
    ]
    factory = APIRequestFactory()

    def setUp(self):
        """Create a test user."""
        psw = UserFactory.get_random_password()
        self.user = UserFactory(password=psw)
        self.login_post_data = {
            'username': self.user.username,
            'password': psw,
        }

        psw = UserFactory.get_random_password()
        self.staff_user = UserFactory(password=psw, is_staff=True)
        self.staff_login_post_data = {
            'username': self.staff_user.username,
            'password': psw,
        }

    def generate_valid_user_data(self):
        """Return new valid data for user."""
        return UserFactory.as_dict()
