# -*- coding: utf-8 -*-

"""Testing settings."""

import pytest

from {{ cookiecutter.project_slug }}.users.models import User
from {{ cookiecutter.project_slug }}.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    """Set media rott to temporary path."""
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    """Create a user factory."""
    return UserFactory()
{%- if cookiecutter.use_whitenoise == 'y' %}


@pytest.fixture(autouse=True)
def whitenoise_autorefresh(settings):
    """Get rid of whitenoise "No directory at" warning, as it's not helpful when running tests.

    Args:
        settings: settings of the application


    Related:
        - https://github.com/evansd/whitenoise/issues/215
        - https://github.com/evansd/whitenoise/issues/191
        - https://github.com/evansd/whitenoise/commit/4204494d44213f7a51229de8bc224cf6d84c01eb

    """
    settings.WHITENOISE_AUTOREFRESH = True
{%- endif %}
