# -*- coding: utf-8 -*-

"""Exceptions for users."""

from rest_framework.exceptions import APIException


class UserNotActive(APIException):
    """Authentication failed exception with code for user not active."""

    status_code = 401
    default_code = 'user_not_active'
    default_detail = 'User not active. Should be activated.'
