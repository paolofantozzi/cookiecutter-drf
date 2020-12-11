# -*- coding: utf-8 -*-

"""Models for users."""

from django.contrib.auth.models import AbstractUser
from django.db import models
{%- if cookiecutter.api_only_mode == 'n' %}
from django.urls import reverse
{%- endif %}
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    """User model."""

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    is_privacy_accepted = models.BooleanField(default=False)
    privacy_accepted_datetime = models.DateTimeField(null=True)

    is_terms_and_conditions_accepted = models.BooleanField(default=False)
    terms_and_conditions_accepted_datetime = models.DateTimeField(null=True)

    is_marketing_accepted = models.BooleanField(default=False)
    marketing_accepted_datetime = models.DateTimeField(null=True)

    # Field for identification in Italy
    cf = models.CharField(help_text=_('Codice Fiscale'), max_length=32)
    {%- if cookiecutter.api_only_mode == 'n' %}

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
    {%- endif %}
