# -*- coding: utf-8 -*-

"""Context preprocessor."""

from django.conf import settings


def settings_context(_request):
    """Set settings context."""
    return {'settings': settings}
