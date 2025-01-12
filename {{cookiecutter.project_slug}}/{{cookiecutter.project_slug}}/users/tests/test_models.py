# -*- coding: utf-8 -*-

"""Tests for users' models."""

import pytest

from {{ cookiecutter.project_slug }}.users.models import User


def test_user_get_absolute_url(user: User):
    assert user.get_absolute_url() == f"/users/{user.username}/"
