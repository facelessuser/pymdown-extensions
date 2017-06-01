"""Deprecated name for details."""
from __future__ import absolute_import
from __future__ import unicode_literals
from . import details
from .util import PymdownxDeprecationWarning
import warnings


def makeExtension(*args, **kwargs):
    """Return extension."""

    warnings.warn(
        "'Spoilers' has been renamed to 'Details'. Please use 'Details' as 'Spoilers' has been deprecated."
        "\n'Spoilers' will be removed in the future in favor of 'Details'\n",
        PymdownxDeprecationWarning
    )

    return details.DetailsExtension(*args, **kwargs)
