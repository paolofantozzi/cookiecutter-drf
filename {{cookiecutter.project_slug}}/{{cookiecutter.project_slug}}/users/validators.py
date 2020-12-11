# -*- coding: utf-8 -*-

"""Validators for users."""

import re

from localflavor.it.util import ssn_validation
from rest_framework.exceptions import ValidationError


class CfValidator:
    """Validator for italian ssn."""

    def __call__(self, cf):
        """Check if the cf is valid."""
        cf = cf.upper()
        if len(cf) != 16:  # noqa: WPS432 - length of a standard cf
            raise ValidationError('Not valid cf. It should have 16 characters.')
        if re.match(r'[A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z]', cf) is None:
            raise ValidationError('Not valid cf')
        try:
            ssn_validation(cf)
        except ValueError:
            raise ValidationError('Not valid cf')
