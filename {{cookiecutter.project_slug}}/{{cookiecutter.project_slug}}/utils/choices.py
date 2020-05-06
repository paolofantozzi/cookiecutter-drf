# -*- coding: utf-8 -*-

"""Utility functions for choices in serializers."""


def choices_help_text(choices):
    """Return a clear text for choices.

    Args:
        choices: list of tuples (value, label)

    Returns:
        a text in the form:
            enum1: label1
            enum2: label2

    """
    choises_str = ('{enum}: {label}'.format(enum=choice[0], label=choice[1]) for choice in choices)
    return '\n'.join(choises_str)
