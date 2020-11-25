# -*- coding: utf-8 -*-

"""Models for users."""
{%- if cookiecutter.api_only_mode == 'y' %}

from datetime import datetime
{%- endif %}

from django.contrib.auth.models import AbstractUser
from django.db import models
{%- if cookiecutter.api_only_mode == 'n' %}
from django.urls import reverse
{%- endif %}
from django.utils.translation import ugettext_lazy as _
{%- if cookiecutter.api_only_mode == 'y' %}
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
{%- endif %}


class User(AbstractUser):
    """User model."""

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    is_privacy_accepted = models.BooleanField(default=False)
    is_email_validated = models.BooleanField(default=False)

    # Field for identification in Italy
    cf = models.CharField(help_text=_('Codice Fiscale'), max_length=32)
    {%- if cookiecutter.api_only_mode == 'y' %}

    def get_jwt_access_token(self) -> str:
        """Return the current jwt access token."""
        try:
            return self.jwt_access_token
        except AttributeError:
            self._obtain_jwt_tokens()
            return self.jwt_access_token

    def get_jwt_refresh_token(self) -> str:
        """Return the current jwt refresh token."""
        try:
            return self.jwt_refresh_token
        except AttributeError:
            self._obtain_jwt_tokens()
            return self.jwt_refresh_token

    def get_jwt_access_token_expiring_time(self) -> datetime:
        """Return the current jwt refresh token."""
        try:
            return self.access_token_expiring_time
        except AttributeError:
            self._obtain_jwt_tokens()
            return self.access_token_expiring_time

    def get_jwt_refresh_token_expiring_time(self) -> datetime:
        """Return the current jwt refresh token."""
        try:
            return self.refresh_token_expiring_time
        except AttributeError:
            self._obtain_jwt_tokens()
            return self.refresh_token_expiring_time

    def _obtain_jwt_tokens(self):
        access_lifetime = api_settings.ACCESS_TOKEN_LIFETIME
        refresh_lifetime = api_settings.REFRESH_TOKEN_LIFETIME
        refresh = RefreshToken.for_user(self)
        now = datetime.now()
        self.jwt_access_token = str(refresh.access_token)
        self.jwt_refresh_token = str(refresh)
        self.access_token_expiring_time = now + access_lifetime
        self.refresh_token_expiring_time = now + refresh_lifetime
    {%- else %}

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
    {%- endif %}
