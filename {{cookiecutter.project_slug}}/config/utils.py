# -*- coding: utf-8 -*-

"""Global utils functions.."""

from rest_framework.views import exception_handler


def error_code_exception_handler(exc, context):
    """Fill the error code from exceptions if it is not already present."""
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['code'] = (
            response.get('code', '') or getattr(exc, 'default_code', '')
        )

    return response
