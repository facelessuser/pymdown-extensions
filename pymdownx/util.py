"""
General utilities.

MIT license.

Copyright (c) 2017 Isaac Muse <isaacmuse@gmail.com>
"""
from __future__ import unicode_literals
import sys
import copy

PY3 = sys.version_info >= (3, 0)
IS_NARROW = sys.maxunicode == 0xFFFF

if PY3:
    uchr = chr
else:
    uchr = unichr

if IS_NARROW:  # pragma: no cover
    # For ease of supporting, just require uniseq for both narrow and wide PY27.

    def get_code_points(s):
        """Get the Unicode code points."""

        pt = []

        def is_full_point(p, point):
            """
            Check if we have a full code point.

            Surrogates are stored in point.
            """
            v = ord(p)
            if 0xD800 <= v <= 0xDBFF:
                del point[:]
                point.append(p)
                return False
            if point and 0xDC00 <= v <= 0xDFFF:
                point.append(p)
                return True
            del point[:]
            return True

        return [(''.join(pt) if pt else c) for c in s if is_full_point(c, pt)]

    def get_ord(c):
        """Get Unicode ord."""

        if len(c) == 2:
            high, low = [ord(p) for p in c]
            ordinal = (high - 0xD800) * 0x400 + low - 0xDC00 + 0x10000
        else:
            ordinal = ord(c)

        return ordinal

    def get_char(value):
        """Get the Unicode char."""
        if value > 0xFFFF:
            c = ''.join(
                [
                    uchr(int((value - 0x10000) / (0x400)) + 0xD800),
                    uchr((value - 0x10000) % 0x400 + 0xDC00)
                ]
            )
        else:
            c = uchr(value)
        return c

else:
    def get_code_points(s):
        """Get the Unicode code points."""

        return [c for c in s]

    def get_ord(c):
        """Get Unicode ord."""

        return ord(c)

    def get_char(value):
        """Get the Unicode char."""

        return uchr(value)


def escape_chars(md, echrs):
    """
    Add chars to the escape list.

    Don't just append as it modifies the global list permanently.
    Make a copy and extend **that** copy so that only this Markdown
    instance gets modified.
    """

    escaped = copy.copy(md.ESCAPED_CHARS)
    for ec in echrs:
        if ec not in escaped:
            escaped.append(ec)
    md.ESCAPED_CHARS = escaped


class PymdownxDeprecationWarning(UserWarning):
    """Deprecation warning for Pymdownx that is not hidden."""
