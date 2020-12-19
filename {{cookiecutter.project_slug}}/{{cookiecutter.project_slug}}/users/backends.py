# -*- coding: utf-8 -*-

"""Backends for users."""


from django.contrib.auth.backends import ModelBackend

from {{ cookiecutter.project_slug }}.users.exceptions import UserNotActive


class ModelBackendWithNotActiveException(ModelBackend):
    """Add the managing of non active user as a different authentication exception."""

    def user_can_authenticate(self, user):
        """Throw authentication exception for users with is_active=False."""
        is_active = getattr(user, 'is_active', True)
        if not is_active:
            raise UserNotActive()
        return True
