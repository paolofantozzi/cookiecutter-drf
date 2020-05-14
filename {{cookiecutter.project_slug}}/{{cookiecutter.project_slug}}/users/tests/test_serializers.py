# -*- coding: utf-8 -*-

"""Tests for serializers."""

from factory import Faker
from rest_framework.test import force_authenticate

from ..serializers import UserSerializer
from .base import UsersBaseTest


class TestSerializersCase(UsersBaseTest):
    """Test cases for retrieve."""

    def get_request(self):
        """Create a useless request."""
        request = self.factory.post('/')
        force_authenticate(request, self.user)
        request.user = self.user
        return request

    def test_missing_data(self):
        """Test return code for retrieve not authenticated."""
        request = self.get_request()
        serializer = UserSerializer(data={}, context={'request': request})
        self.assertFalse(serializer.is_valid())

    def test_not_valid_without_cf(self):
        """Test not valid serializer without cf."""
        new_data = self.generate_valid_user_data()
        new_data.pop('cf')
        request = self.get_request()
        serializer = UserSerializer(data=new_data, context={'request': request})
        self.assertFalse(serializer.is_valid())

    def test_not_valid_cf_too_short(self):
        """Test not valid serializer for too short cf."""
        new_data = self.generate_valid_user_data()
        new_data['cf'] = new_data['cf'][:-1]
        request = self.get_request()
        serializer = UserSerializer(data=new_data, context={'request': request})
        self.assertFalse(serializer.is_valid())

    def test_not_valid_cf_random_string(self):
        """Test not valid serializer for random string cf."""
        new_data = self.generate_valid_user_data()
        new_data['cf'] = Faker('pystr', max_chars=16).generate()
        request = self.get_request()
        serializer = UserSerializer(data=new_data, context={'request': request})
        self.assertFalse(serializer.is_valid(), new_data['cf'])

    def test_not_valid_cf_already_existing(self):
        """Test not valid serializer for already_existing cf."""
        new_data = self.generate_valid_user_data()
        new_data['cf'] = self.user.cf
        request = self.get_request()
        serializer = UserSerializer(data=new_data, context={'request': request})
        self.assertFalse(serializer.is_valid())
