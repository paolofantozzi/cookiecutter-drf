# -*- coding: utf-8 -*-

"""Global utils functions.."""

from rest_framework import status
from rest_framework.views import exception_handler


def error_code_exception_handler(exc, context):
    """Fill the error code from exceptions if it is not already present."""
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # If it is a 400 error then each code is a field
    if response is not None and response.status_code != status.HTTP_400_BAD_REQUEST:
        response.data['code'] = response.get('code', '') or getattr(exc, 'default_code', '')  # noqa: WPS221

    return response
