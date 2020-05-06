# -*- coding: utf-8 -*-

"""App for users."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = '{{ cookiecutter.project_slug }}.users'
    verbose_name = _('Users')

    def ready(self):
        """Configure module when ready."""
        try:
            import {{ cookiecutter.project_slug }}.users.signals  # noqa: F401,WPS433,WPS301
        except ImportError:
            pass  # noqa: WPS420
