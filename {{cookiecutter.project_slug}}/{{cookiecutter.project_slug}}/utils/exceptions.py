# -*- coding: utf-8 -*-

"""Exceptions raised from functions in utils."""


class FormatNotValid(ImportError):
    """The format of data passed to import function cannot be parsed."""


class MalformedStringReference(ImportError):
    """The string is not a valid representation of a module."""


class ImportFailed(ImportError):
    """The trying to import is failed."""


class AttributeDoesNotExistInModule(ImportError):
    """The attribute requested does not exist in the module."""
