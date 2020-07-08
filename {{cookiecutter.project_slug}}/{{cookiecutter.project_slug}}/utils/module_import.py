# -*- coding: utf-8 -*-

"""Import functions to be used with different types of input."""

from collections import abc
from functools import singledispatch
from importlib import import_module

from {{ cookiecutter.project_slug }}.utils.exceptions import AttributeDoesNotExistInModule
from {{ cookiecutter.project_slug }}.utils.exceptions import FormatNotValid
from {{ cookiecutter.project_slug }}.utils.exceptions import ImportFailed
from {{ cookiecutter.project_slug }}.utils.exceptions import MalformedStringReference


@singledispatch
def import_modules(ref):
    """Raise an exception because the reference is not recognised."""
    raise FormatNotValid('Format {0} not valid to import modules.'.format(type(ref)))


@import_modules.register(type(None))
def _none(nothing: None):
    """If the input is None, the result is None."""
    return None  # noqa: WPS324


@import_modules.register(str)
def _str(str_ref: str):
    """Import a dotted module path and return the attribute/class designated by the last name in the path.

    Originally developed in https://github.com/django/django/blob/master/django/utils/module_loading.py
    We can't use the original one because we need the distinctions between exceptions to identify the input.

    Args:
        str_ref: the string reference to the module

    Returns:
        The module imported.

    Raises:
        MalformedStringReference: The string is not formed as a module path.
        ImportFailed: It was not possible to import the module.
        AttributeDoesNotExistInModule: The module was imported but the attribute requested does not exist.
    """
    try:
        module_path, class_name = str_ref.rsplit('.', 1)
    except ValueError as malf_err:
        raise MalformedStringReference("{0} doesn't look like a module path".format(str_ref)) from malf_err

    try:
        module = import_module(module_path)
    except (ValueError, TypeError) as fail_err:
        raise ImportFailed('Import of "{0}" failed.'.format(module_path)) from fail_err

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise AttributeDoesNotExistInModule(
            'Module {0} does not define a {1} attribute/class'.format(module_path, class_name),
        ) from err


@import_modules.register(abc.Sequence)
def _seq(seq_refs: abc.Sequence):
    """Return a list of modules."""
    return [import_modules(ele) for ele in seq_refs]
