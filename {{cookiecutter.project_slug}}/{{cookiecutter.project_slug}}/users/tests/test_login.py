# -*- coding: utf-8 -*-

"""Tests for users' models."""

import pytest

from {{ cookiecutter.project_slug }}.users.models import User

pytestmark = pytest.mark.django_db


def test_user_get_tokens(user: User):
    assert user.get_jwt_access_token()
    assert user.get_jwt_refresh_token()
    assert user.get_jwt_access_token_expiring_time()
    assert user.get_jwt_refresh_token_expiring_time()
