# -*- coding: utf-8 -*-

"""Global utils functions.."""

import types

from rest_framework import status
from rest_framework.views import exception_handler

# Similar to a frozendict
STATUS_ERROR_CODES = types.MappingProxyType({
    status.HTTP_404_NOT_FOUND: 'not_found',
})


def error_code_exception_handler(exc, context):
    """Fill the error code from exceptions if it is not already present."""
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is None:
        return None

    # first of all check the original response
    code = response.get('code', '')

    # if there is no code check the exception code
    code = code or getattr(exc, 'default_code', '')

    # if there is still no code then try the fixed codes otherwise empty string
    code = code or STATUS_ERROR_CODES.get(response.status_code, '')

    response.data['code'] = code
    return response
