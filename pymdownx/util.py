"""
General utilities.

MIT license.

Copyright (c) 2017 Isaac Muse <isaacmuse@gmail.com>
"""
from __future__ import annotations
from markdown import __version_info__
from markdown import Markdown
from markdown.inlinepatterns import InlineProcessor
import xml.etree.ElementTree as etree
from collections import deque
import sys
import copy
import re
import html
from urllib.request import pathname2url, url2pathname
from urllib.parse import urlparse
from functools import wraps
import warnings
from typing import Sequence, Callable, Any, cast

if sys.platform.startswith('win'):
    _PLATFORM = "windows"
elif sys.platform == "darwin":  # pragma: no cover
    _PLATFORM = "osx"
else:
    _PLATFORM = "linux"

PY39 = (3, 9) <= sys.version_info
PY314 = (3, 14) <= sys.version_info

# TODO: Remove from main when Python Markdown releases https://github.com/Python-Markdown/markdown/commit/152a16f.
MD_FAST = __version_info__[:3] > (3, 10, 3)


def clamp(value: float, mn: float, mx: float) -> float:
    """Clamp the value to the given minimum and maximum."""

    if mn is not None and mx is not None:
        return max(min(value, mx), mn)
    elif mn is not None:
        return max(value, mn)
    elif mx is not None:
        return min(value, mx)
    else:
        return value


def is_win() -> bool:  # pragma: no cover
    """Is Windows."""

    return _PLATFORM == "windows"


def is_linux() -> bool:  # pragma: no cover
    """Is Linux."""

    return _PLATFORM == "linux"


def is_mac() -> bool:  # pragma: no cover
    """Is macOS."""

    return _PLATFORM == "osx"


RE_WIN_DRIVE_LETTER = re.compile(r"^[A-Za-z]$")
RE_WIN_DRIVE_PATH = re.compile(r"^[A-Za-z]:(?:\\.*)?$")
RE_URL = re.compile('(http|ftp)s?|data|mailto|tel|news')
RE_WIN_DEFAULT_PROTOCOL = re.compile(r"^///[A-Za-z]:(?:/.*)?$")


def url2path(path: str) -> str:
    """Path to URL."""

    return url2pathname(path)


def path2url(url: str) -> str:
    """URL to path."""

    path = pathname2url(url)
    # If on windows, replace the notation to use a default protocol `///` with nothing.
    if is_win() and RE_WIN_DEFAULT_PROTOCOL.match(path):
        path = path.replace('///', '', 1)
    if PY314:
        path = path.replace('///', '/')
    return path


def get_code_points(s: str) -> list[str]:
    """Get the Unicode code points."""

    return list(s)


def get_ord(c: str) -> int:
    """Get Unicode ord."""

    return ord(c)


def get_char(value: int) -> str:
    """Get the Unicode char."""

    return chr(value)


def escape_chars(md: Markdown, echrs: Sequence[str]) -> None:
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


def parse_url(url: str) -> tuple[str, str, str, str, str, str, bool, bool]:
    """
    Parse the URL.

    Try to determine if the following is a file path or
    (as we will call anything else) a URL.

    We return it slightly modified and combine the path parts.

    We also assume if we see something like c:/ it is a Windows path.
    We don't bother checking if this **is** a Windows system, but
    'nix users really shouldn't be creating weird names like c: for their folder.
    """

    is_url = False
    is_absolute = False
    scheme, netloc, path, params, query, fragment = urlparse(html.unescape(url))

    if RE_URL.match(scheme):
        # Clearly a URL
        is_url = True
    elif scheme == '' and netloc == '' and path == '':
        # Maybe just a URL fragment
        is_url = True
    elif scheme == 'file' and (RE_WIN_DRIVE_PATH.match(netloc)):
        # file://c:/path or file://c:\path
        path = '/' + (netloc + path).replace('\\', '/')
        netloc = ''
        is_absolute = True
    elif scheme == 'file' and netloc.startswith('\\'):
        # file://\c:\path or file://\\path
        path = (netloc + path).replace('\\', '/')
        netloc = ''
        is_absolute = True
    elif scheme == 'file':
        # file:///path
        is_absolute = True
    elif RE_WIN_DRIVE_LETTER.match(scheme):
        # c:/path
        path = '/{}:{}'.format(scheme, path.replace('\\', '/'))
        scheme = 'file'
        netloc = ''
        is_absolute = True
    elif scheme == '' and netloc != '' and url.startswith('//'):
        # //file/path
        path = '//' + netloc + path
        scheme = 'file'
        netloc = ''
        is_absolute = True
    elif scheme != '' and netloc != '':
        # A non-file path or strange URL
        is_url = True
    elif path.startswith(('/', '\\')):
        # /root path
        is_absolute = True

    return (scheme, netloc, path, params, query, fragment, is_url, is_absolute)


# Unicode punctuation and symbols `\p{P}\p{S}`. These should be placed in regex character class `fr"[{PUNCT}]"`.
PUNCT = (
    b'!-/:-@\\[-`{-\\~\xc2\xa1-\xc2\xa9\xc2\xab-\xc2\xac\xc2\xae-\xc2\xb1\xc2\xb4\xc2\xb6-\xc2\xb8\xc2\xbb\xc2\xbf\xc3'
    b'\x97\xc3\xb7\xcb\x82-\xcb\x85\xcb\x92-\xcb\x9f\xcb\xa5-\xcb\xab\xcb\xad\xcb\xaf-\xcb\xbf\xcd\xb5\xcd\xbe\xce\x84'
    b'-\xce\x85\xce\x87\xcf\xb6\xd2\x82\xd5\x9a-\xd5\x9f\xd6\x89-\xd6\x8a\xd6\x8d-\xd6\x8f\xd6\xbe\xd7\x80\xd7\x83\xd7'
    b'\x86\xd7\xb3-\xd7\xb4\xd8\x86-\xd8\x8f\xd8\x9b\xd8\x9d-\xd8\x9f\xd9\xaa-\xd9\xad\xdb\x94\xdb\x9e\xdb\xa9\xdb\xbd'
    b'-\xdb\xbe\xdc\x80-\xdc\x8d\xdf\xb6-\xdf\xb9\xdf\xbe-\xdf\xbf\xe0\xa0\xb0-\xe0\xa0\xbe\xe0\xa1\x9e\xe0\xa2\x88'
    b'\xe0\xa5\xa4-\xe0\xa5\xa5\xe0\xa5\xb0\xe0\xa7\xb2-\xe0\xa7\xb3\xe0\xa7\xba-\xe0\xa7\xbb\xe0\xa7\xbd\xe0\xa9\xb6'
    b'\xe0\xab\xb0-\xe0\xab\xb1\xe0\xad\xb0\xe0\xaf\xb3-\xe0\xaf\xba\xe0\xb1\xb7\xe0\xb1\xbf\xe0\xb2\x84\xe0\xb5\x8f'
    b'\xe0\xb5\xb9\xe0\xb7\xb4\xe0\xb8\xbf\xe0\xb9\x8f\xe0\xb9\x9a-\xe0\xb9\x9b\xe0\xbc\x81-\xe0\xbc\x97\xe0\xbc\x9a-'
    b'\xe0\xbc\x9f\xe0\xbc\xb4\xe0\xbc\xb6\xe0\xbc\xb8\xe0\xbc\xba-\xe0\xbc\xbd\xe0\xbe\x85\xe0\xbe\xbe-\xe0\xbf\x85'
    b'\xe0\xbf\x87-\xe0\xbf\x8c\xe0\xbf\x8e-\xe0\xbf\x9a\xe1\x81\x8a-\xe1\x81\x8f\xe1\x82\x9e-\xe1\x82\x9f\xe1\x83\xbb'
    b'\xe1\x8d\xa0-\xe1\x8d\xa8\xe1\x8e\x90-\xe1\x8e\x99\xe1\x90\x80\xe1\x99\xad-\xe1\x99\xae\xe1\x9a\x9b-\xe1\x9a\x9c'
    b'\xe1\x9b\xab-\xe1\x9b\xad\xe1\x9c\xb5-\xe1\x9c\xb6\xe1\x9f\x94-\xe1\x9f\x96\xe1\x9f\x98-\xe1\x9f\x9b\xe1\xa0\x80'
    b'-\xe1\xa0\x8a\xe1\xa5\x80\xe1\xa5\x84-\xe1\xa5\x85\xe1\xa7\x9e-\xe1\xa7\xbf\xe1\xa8\x9e-\xe1\xa8\x9f\xe1\xaa\xa0'
    b'-\xe1\xaa\xa6\xe1\xaa\xa8-\xe1\xaa\xad\xe1\xad\x8e-\xe1\xad\x8f\xe1\xad\x9a-\xe1\xad\xaa\xe1\xad\xb4-\xe1\xad'
    b'\xbf\xe1\xaf\xbc-\xe1\xaf\xbf\xe1\xb0\xbb-\xe1\xb0\xbf\xe1\xb1\xbe-\xe1\xb1\xbf\xe1\xb3\x80-\xe1\xb3\x87\xe1\xb3'
    b'\x93\xe1\xbe\xbd\xe1\xbe\xbf-\xe1\xbf\x81\xe1\xbf\x8d-\xe1\xbf\x8f\xe1\xbf\x9d-\xe1\xbf\x9f\xe1\xbf\xad-\xe1\xbf'
    b'\xaf\xe1\xbf\xbd-\xe1\xbf\xbe\xe2\x80\x90-\xe2\x80\xa7\xe2\x80\xb0-\xe2\x81\x9e\xe2\x81\xba-\xe2\x81\xbe\xe2\x82'
    b'\x8a-\xe2\x82\x8e\xe2\x82\xa0-\xe2\x83\x80\xe2\x84\x80-\xe2\x84\x81\xe2\x84\x83-\xe2\x84\x86\xe2\x84\x88-\xe2'
    b'\x84\x89\xe2\x84\x94\xe2\x84\x96-\xe2\x84\x98\xe2\x84\x9e-\xe2\x84\xa3\xe2\x84\xa5\xe2\x84\xa7\xe2\x84\xa9\xe2'
    b'\x84\xae\xe2\x84\xba-\xe2\x84\xbb\xe2\x85\x80-\xe2\x85\x84\xe2\x85\x8a-\xe2\x85\x8d\xe2\x85\x8f\xe2\x86\x8a-\xe2'
    b'\x86\x8b\xe2\x86\x90-\xe2\x90\xa9\xe2\x91\x80-\xe2\x91\x8a\xe2\x92\x9c-\xe2\x93\xa9\xe2\x94\x80-\xe2\x9d\xb5\xe2'
    b'\x9e\x94-\xe2\xad\xb3\xe2\xad\xb6-\xe2\xae\x95\xe2\xae\x97-\xe2\xaf\xbf\xe2\xb3\xa5-\xe2\xb3\xaa\xe2\xb3\xb9-'
    b'\xe2\xb3\xbc\xe2\xb3\xbe-\xe2\xb3\xbf\xe2\xb5\xb0\xe2\xb8\x80-\xe2\xb8\xae\xe2\xb8\xb0-\xe2\xb9\x9d\xe2\xba\x80-'
    b'\xe2\xba\x99\xe2\xba\x9b-\xe2\xbb\xb3\xe2\xbc\x80-\xe2\xbf\x95\xe2\xbf\xb0-\xe2\xbf\xbf\xe3\x80\x81-\xe3\x80\x84'
    b'\xe3\x80\x88-\xe3\x80\xa0\xe3\x80\xb0\xe3\x80\xb6-\xe3\x80\xb7\xe3\x80\xbd-\xe3\x80\xbf\xe3\x82\x9b-\xe3\x82\x9c'
    b'\xe3\x82\xa0\xe3\x83\xbb\xe3\x86\x90-\xe3\x86\x91\xe3\x86\x96-\xe3\x86\x9f\xe3\x87\x80-\xe3\x87\xa5\xe3\x87\xaf'
    b'\xe3\x88\x80-\xe3\x88\x9e\xe3\x88\xaa-\xe3\x89\x87\xe3\x89\x90\xe3\x89\xa0-\xe3\x89\xbf\xe3\x8a\x8a-\xe3\x8a\xb0'
    b'\xe3\x8b\x80-\xe3\x8f\xbf\xe4\xb7\x80-\xe4\xb7\xbf\xea\x92\x90-\xea\x93\x86\xea\x93\xbe-\xea\x93\xbf\xea\x98\x8d'
    b'-\xea\x98\x8f\xea\x99\xb3\xea\x99\xbe\xea\x9b\xb2-\xea\x9b\xb7\xea\x9c\x80-\xea\x9c\x96\xea\x9c\xa0-\xea\x9c\xa1'
    b'\xea\x9e\x89-\xea\x9e\x8a\xea\xa0\xa8-\xea\xa0\xab\xea\xa0\xb6-\xea\xa0\xb9\xea\xa1\xb4-\xea\xa1\xb7\xea\xa3\x8e'
    b'-\xea\xa3\x8f\xea\xa3\xb8-\xea\xa3\xba\xea\xa3\xbc\xea\xa4\xae-\xea\xa4\xaf\xea\xa5\x9f\xea\xa7\x81-\xea\xa7\x8d'
    b'\xea\xa7\x9e-\xea\xa7\x9f\xea\xa9\x9c-\xea\xa9\x9f\xea\xa9\xb7-\xea\xa9\xb9\xea\xab\x9e-\xea\xab\x9f\xea\xab\xb0'
    b'-\xea\xab\xb1\xea\xad\x9b\xea\xad\xaa-\xea\xad\xab\xea\xaf\xab\xef\xac\xa9\xef\xae\xb2-\xef\xaf\x82\xef\xb4\xbe-'
    b'\xef\xb5\x8f\xef\xb7\x8f\xef\xb7\xbc-\xef\xb7\xbf\xef\xb8\x90-\xef\xb8\x99\xef\xb8\xb0-\xef\xb9\x92\xef\xb9\x94-'
    b'\xef\xb9\xa6\xef\xb9\xa8-\xef\xb9\xab\xef\xbc\x81-\xef\xbc\x8f\xef\xbc\x9a-\xef\xbc\xa0\xef\xbc\xbb-\xef\xbd\x80'
    b'\xef\xbd\x9b-\xef\xbd\xa5\xef\xbf\xa0-\xef\xbf\xa6\xef\xbf\xa8-\xef\xbf\xae\xef\xbf\xbc-\xef\xbf\xbd\xf0\x90\x84'
    b'\x80-\xf0\x90\x84\x82\xf0\x90\x84\xb7-\xf0\x90\x84\xbf\xf0\x90\x85\xb9-\xf0\x90\x86\x89\xf0\x90\x86\x8c-\xf0\x90'
    b'\x86\x8e\xf0\x90\x86\x90-\xf0\x90\x86\x9c\xf0\x90\x86\xa0\xf0\x90\x87\x90-\xf0\x90\x87\xbc\xf0\x90\x8e\x9f\xf0'
    b'\x90\x8f\x90\xf0\x90\x95\xaf\xf0\x90\xa1\x97\xf0\x90\xa1\xb7-\xf0\x90\xa1\xb8\xf0\x90\xa4\x9f\xf0\x90\xa4\xbf'
    b'\xf0\x90\xa9\x90-\xf0\x90\xa9\x98\xf0\x90\xa9\xbf\xf0\x90\xab\x88\xf0\x90\xab\xb0-\xf0\x90\xab\xb6\xf0\x90\xac'
    b'\xb9-\xf0\x90\xac\xbf\xf0\x90\xae\x99-\xf0\x90\xae\x9c\xf0\x90\xb5\xae\xf0\x90\xb6\x8e-\xf0\x90\xb6\x8f\xf0\x90'
    b'\xba\xad\xf0\x90\xbd\x95-\xf0\x90\xbd\x99\xf0\x90\xbe\x86-\xf0\x90\xbe\x89\xf0\x91\x81\x87-\xf0\x91\x81\x8d\xf0'
    b'\x91\x82\xbb-\xf0\x91\x82\xbc\xf0\x91\x82\xbe-\xf0\x91\x83\x81\xf0\x91\x85\x80-\xf0\x91\x85\x83\xf0\x91\x85\xb4-'
    b'\xf0\x91\x85\xb5\xf0\x91\x87\x85-\xf0\x91\x87\x88\xf0\x91\x87\x8d\xf0\x91\x87\x9b\xf0\x91\x87\x9d-\xf0\x91\x87'
    b'\x9f\xf0\x91\x88\xb8-\xf0\x91\x88\xbd\xf0\x91\x8a\xa9\xf0\x91\x8f\x94-\xf0\x91\x8f\x95\xf0\x91\x8f\x97-\xf0\x91'
    b'\x8f\x98\xf0\x91\x91\x8b-\xf0\x91\x91\x8f\xf0\x91\x91\x9a-\xf0\x91\x91\x9b\xf0\x91\x91\x9d\xf0\x91\x93\x86\xf0'
    b'\x91\x97\x81-\xf0\x91\x97\x97\xf0\x91\x99\x81-\xf0\x91\x99\x83\xf0\x91\x99\xa0-\xf0\x91\x99\xac\xf0\x91\x9a\xb9'
    b'\xf0\x91\x9c\xbc-\xf0\x91\x9c\xbf\xf0\x91\xa0\xbb\xf0\x91\xa5\x84-\xf0\x91\xa5\x86\xf0\x91\xa7\xa2\xf0\x91\xa8'
    b'\xbf-\xf0\x91\xa9\x86\xf0\x91\xaa\x9a-\xf0\x91\xaa\x9c\xf0\x91\xaa\x9e-\xf0\x91\xaa\xa2\xf0\x91\xac\x80-\xf0\x91'
    b'\xac\x89\xf0\x91\xaf\xa1\xf0\x91\xb1\x81-\xf0\x91\xb1\x85\xf0\x91\xb1\xb0-\xf0\x91\xb1\xb1\xf0\x91\xbb\xb7-\xf0'
    b'\x91\xbb\xb8\xf0\x91\xbd\x83-\xf0\x91\xbd\x8f\xf0\x91\xbf\x95-\xf0\x91\xbf\xb1\xf0\x91\xbf\xbf\xf0\x92\x91\xb0-'
    b'\xf0\x92\x91\xb4\xf0\x92\xbf\xb1-\xf0\x92\xbf\xb2\xf0\x96\xa9\xae-\xf0\x96\xa9\xaf\xf0\x96\xab\xb5\xf0\x96\xac'
    b'\xb7-\xf0\x96\xac\xbf\xf0\x96\xad\x84-\xf0\x96\xad\x85\xf0\x96\xb5\xad-\xf0\x96\xb5\xaf\xf0\x96\xba\x97-\xf0\x96'
    b'\xba\x9a\xf0\x96\xbf\xa2\xf0\x9b\xb2\x9c\xf0\x9b\xb2\x9f\xf0\x9c\xb0\x80-\xf0\x9c\xb3\xaf\xf0\x9c\xb4\x80-\xf0'
    b'\x9c\xba\xb3\xf0\x9c\xbd\x90-\xf0\x9c\xbf\x83\xf0\x9d\x80\x80-\xf0\x9d\x83\xb5\xf0\x9d\x84\x80-\xf0\x9d\x84\xa6'
    b'\xf0\x9d\x84\xa9-\xf0\x9d\x85\xa4\xf0\x9d\x85\xaa-\xf0\x9d\x85\xac\xf0\x9d\x86\x83-\xf0\x9d\x86\x84\xf0\x9d\x86'
    b'\x8c-\xf0\x9d\x86\xa9\xf0\x9d\x86\xae-\xf0\x9d\x87\xaa\xf0\x9d\x88\x80-\xf0\x9d\x89\x81\xf0\x9d\x89\x85\xf0\x9d'
    b'\x8c\x80-\xf0\x9d\x8d\x96\xf0\x9d\x9b\x81\xf0\x9d\x9b\x9b\xf0\x9d\x9b\xbb\xf0\x9d\x9c\x95\xf0\x9d\x9c\xb5\xf0'
    b'\x9d\x9d\x8f\xf0\x9d\x9d\xaf\xf0\x9d\x9e\x89\xf0\x9d\x9e\xa9\xf0\x9d\x9f\x83\xf0\x9d\xa0\x80-\xf0\x9d\xa7\xbf'
    b'\xf0\x9d\xa8\xb7-\xf0\x9d\xa8\xba\xf0\x9d\xa9\xad-\xf0\x9d\xa9\xb4\xf0\x9d\xa9\xb6-\xf0\x9d\xaa\x83\xf0\x9d\xaa'
    b'\x85-\xf0\x9d\xaa\x8b\xf0\x9e\x85\x8f\xf0\x9e\x8b\xbf\xf0\x9e\x97\xbf\xf0\x9e\xa5\x9e-\xf0\x9e\xa5\x9f\xf0\x9e'
    b'\xb2\xac\xf0\x9e\xb2\xb0\xf0\x9e\xb4\xae\xf0\x9e\xbb\xb0-\xf0\x9e\xbb\xb1\xf0\x9f\x80\x80-\xf0\x9f\x80\xab\xf0'
    b'\x9f\x80\xb0-\xf0\x9f\x82\x93\xf0\x9f\x82\xa0-\xf0\x9f\x82\xae\xf0\x9f\x82\xb1-\xf0\x9f\x82\xbf\xf0\x9f\x83\x81-'
    b'\xf0\x9f\x83\x8f\xf0\x9f\x83\x91-\xf0\x9f\x83\xb5\xf0\x9f\x84\x8d-\xf0\x9f\x86\xad\xf0\x9f\x87\xa6-\xf0\x9f\x88'
    b'\x82\xf0\x9f\x88\x90-\xf0\x9f\x88\xbb\xf0\x9f\x89\x80-\xf0\x9f\x89\x88\xf0\x9f\x89\x90-\xf0\x9f\x89\x91\xf0\x9f'
    b'\x89\xa0-\xf0\x9f\x89\xa5\xf0\x9f\x8c\x80-\xf0\x9f\x9b\x97\xf0\x9f\x9b\x9c-\xf0\x9f\x9b\xac\xf0\x9f\x9b\xb0-\xf0'
    b'\x9f\x9b\xbc\xf0\x9f\x9c\x80-\xf0\x9f\x9d\xb6\xf0\x9f\x9d\xbb-\xf0\x9f\x9f\x99\xf0\x9f\x9f\xa0-\xf0\x9f\x9f\xab'
    b'\xf0\x9f\x9f\xb0\xf0\x9f\xa0\x80-\xf0\x9f\xa0\x8b\xf0\x9f\xa0\x90-\xf0\x9f\xa1\x87\xf0\x9f\xa1\x90-\xf0\x9f\xa1'
    b'\x99\xf0\x9f\xa1\xa0-\xf0\x9f\xa2\x87\xf0\x9f\xa2\x90-\xf0\x9f\xa2\xad\xf0\x9f\xa2\xb0-\xf0\x9f\xa2\xbb\xf0\x9f'
    b'\xa3\x80-\xf0\x9f\xa3\x81\xf0\x9f\xa4\x80-\xf0\x9f\xa9\x93\xf0\x9f\xa9\xa0-\xf0\x9f\xa9\xad\xf0\x9f\xa9\xb0-\xf0'
    b'\x9f\xa9\xbc\xf0\x9f\xaa\x80-\xf0\x9f\xaa\x89\xf0\x9f\xaa\x8f-\xf0\x9f\xab\x86\xf0\x9f\xab\x8e-\xf0\x9f\xab\x9c'
    b'\xf0\x9f\xab\x9f-\xf0\x9f\xab\xa9\xf0\x9f\xab\xb0-\xf0\x9f\xab\xb8\xf0\x9f\xac\x80-\xf0\x9f\xae\x92\xf0\x9f\xae'
    b'\x94-\xf0\x9f\xaf\xaf'
).decode('utf-8')


class DelimiterProcessor(InlineProcessor):
    """Processor for handling complex nested patterns such as strong and em matches."""

    SPACE = re.compile(r'\s')

    def __init__(
        self,
        token: str,
        tags: str,
        md: Markdown | None = None,
        no_space: bool = False,
        smart: bool = False,
        double: bool = False
    ) -> None:
        """
        Initialize.

        Arguments:
            `token`: should be a single character.

            `tags`: should be specified as a single tag or two tags with the one that requires
                    repeated tokens first.

            `md`: the Markdown object.

            `no_space`: The "no space" option should be enabled only for Pandoc style spans that require
                        spaces to be escaped (e.g. subscript and superscript). This logic is only applied
                        to single token spans.

            `smart`: enable if intelligent word logic should be applied.

            `double`: if only one tag is specified, indicate whether it requires repeated tokens.

        """

        self.regions: list[tuple[int, int, int, int, int]] = []
        self.stack: deque[tuple[int, int, bool, int]] = deque()
        self.cache_index = 0
        self.cache_pos = 0
        self.cache_legacy_pos = -1

        self.double = len(tags) != 2 and double
        self.single = len(tags) != 2 and not double
        self.no_space = no_space and not self.double
        self.smart = smart
        self.tags = tags.split(',')
        super().__init__(self._build_patterns(token), md)

    def reset(self) -> None:
        """Reset."""

        # Cache info
        self.regions.clear()
        self.stack.clear()
        self.cache_index = 0
        self.cache_pos = 0
        self.cache_legacy_pos = -1

    def _build_patterns(self, token: str) -> str:
        """Build regular expression patterns."""

        # Build up patterns
        self.token = token
        etoken = re.escape(token)
        # Avoid at start and end
        xstart = fr'(?:(?<=_)|(?<![\w{etoken}]))' if token != '_' else fr'(?<![\w{etoken}])'
        xend = fr'(?:(?=_)|(?![\w{etoken}]))' if token != '_' else fr'(?![\w{etoken}])'
        # Regex Unicode punctuation and symbols. Must be inserted in `[]`
        self.max_size = 2
        if len(self.tags) != 2 and not self.double:
            self.max_size = 1

        # Python Markdown uses `STX` (`\0x2`) and `ETX` (`\0x3`) for placeholders.
        # Include handling for these characters in addition to CommonMark rules.
        stx, etx = '\x02', '\x03'

        # Patterns for when the larger delimiter is "smart" and the smaller is "dumb".
        if self.smart and self.no_space and len(self.tags) == 2:
            self.boundary = re.compile(
                fr'''(?x)
                (?:
                    (?P<ambiguous3>
                        (?<!^)(?<![\s{etoken}{PUNCT}]){etoken}{{3,}}(?![\s{etoken}{PUNCT}])(?!$)|
                        (?<!^)(?<=[{PUNCT}{etx}])(?<!{etoken}){etoken}{{3,}}(?!{etoken})(?=[{stx}{PUNCT}])(?!$)
                    )|
                    (?P<end3>
                        (?<!^)(?<![\s{etoken}{PUNCT}]){etoken}{{3,}}|
                        (?<=[{PUNCT}])(?<!{etoken}){etoken}{{3,}}(?!{etoken})(?=[\s{stx}{PUNCT}]|$)
                    )|
                    (?P<start3>
                        {etoken}{{3,}}(?![\s{etoken}{PUNCT}])(?!$)|
                        (?:(?<=[\s{etx}{PUNCT}])|^)(?<!{etoken}){etoken}{{3,}}(?!{etoken})(?=[{PUNCT}])
                    )
                )|
                (?:
                    (?P<ambiguous2>
                        (?<!^)(?<![\s{etoken}{PUNCT}]){xstart}{etoken}{{2}}{xend}(?![\s{etoken}{PUNCT}])(?!$)|
                        (?<!^)(?<=[{PUNCT}{etx}])(?<!{etoken}){etoken}{{2}}(?!{etoken})(?=[{stx}{PUNCT}])(?!$)
                    )|
                    (?P<end2>
                        (?<!^)(?<![\s{etoken}{PUNCT}]){etoken}{{2}}{xend}|
                        (?<=[{PUNCT}])(?<!{etoken}){etoken}{{2}}(?!{etoken})(?=[\s{stx}{PUNCT}]|$)
                    )|
                    (?P<start2>
                        {xstart}{etoken}{{2}}(?![\s{etoken}{PUNCT}])(?!$)|
                        (?:(?<=[\s{etx}{PUNCT}])|^)(?<!{etoken}){etoken}{{2}}(?!{etoken})(?=[{PUNCT}])
                    )
                )|
                (?:
                    (?P<ambiguous1>
                        (?<!^)(?<![\s{etoken}{PUNCT}]){etoken}{{1}}(?![\s{etoken}{PUNCT}])(?!$)|
                        (?<!^)(?<=[{PUNCT}{etx}])(?<!{etoken}){etoken}{{1}}(?!{etoken})(?=[{stx}{PUNCT}])(?!$)
                    )|
                    (?P<end1>
                        (?<!^)(?<![\s{etoken}{PUNCT}]){etoken}{{1}}|
                        (?<=[{PUNCT}])(?<!{etoken}){etoken}{{1}}(?!{etoken})(?=[\s{stx}{PUNCT}]|$)
                    )|
                    (?P<start1>
                        {etoken}{{1}}(?![\s{etoken}{PUNCT}])(?!$)|
                        (?:(?<=[\s{etx}{PUNCT}])|^)(?<!{etoken}){etoken}{{1}}(?!{etoken})(?=[{PUNCT}])
                    )
                )
                ''',
                flags=re.UNICODE
            )
        # Patterns for "smart" cases.
        elif self.smart:
            self.boundary = re.compile(
                fr'''(?x)
                (?P<ambiguous>
                    (?<!^)(?<![\s{etoken}{PUNCT}]){xstart}{etoken}{{1,}}{xend}(?![\s{etoken}{PUNCT}])(?!$)|
                    (?<!^)(?<=[{PUNCT}{etx}])(?<!{etoken}){etoken}{{1,}}(?!{etoken})(?=[{PUNCT}{stx}])(?!$)
                )|
                (?P<end>
                    (?<!^)(?<![\s{etoken}{PUNCT}]){etoken}{{1,}}{xend}|
                    (?<=[{PUNCT}])(?<!{etoken}){etoken}{{1,}}(?!{etoken})(?=[\s{stx}{PUNCT}]|$)
                )|
                (?P<start>
                    {xstart}{etoken}{{1,}}(?![\s{etoken}{PUNCT}])(?!$)|
                    (?:(?<=[\s{etx}{PUNCT}])|^)(?<!{etoken}){etoken}{{1,}}(?!{etoken})(?=[{PUNCT}])
                )
                ''',
                flags=re.UNICODE
            )
        # Patterns for "dumb" cases.
        else:
            self.boundary = re.compile(
                fr'''(?x)
                (?P<ambiguous>
                    (?<!^)(?<![\s{etoken}{PUNCT}]){etoken}{{1,}}(?![\s{etoken}{PUNCT}])(?!$)|
                    (?<!^)(?<=[{PUNCT}{etx}])(?<!{etoken}){etoken}{{1,}}(?!{etoken})(?=[{PUNCT}{stx}])(?!$)
                )|
                (?P<end>
                    (?<!^)(?<![\s{etoken}{PUNCT}]){etoken}{{1,}}|
                    (?<=[{PUNCT}])(?<!{etoken}){etoken}{{1,}}(?!{etoken})(?=[\s{stx}{PUNCT}]|$)
                )|
                (?P<start>
                    {etoken}{{1,}}(?![\s{etoken}{PUNCT}])(?!$)|
                    (?:(?<=[\s{etx}{PUNCT}])|^)(?<!{etoken}){etoken}{{1,}}(?!{etoken})(?=[{PUNCT}])
                )
                ''',
                flags=re.UNICODE
            )

        self.bad = re.compile(fr'{etoken}+')
        return fr'{etoken}'

    def _build_element(
        self,
        data: str,
        start: int = 0,
        offset: int = 0
    ) -> tuple[etree.Element, int]:
        """Element builder."""

        regions = self.regions
        el: etree.Element | None = None
        last: Any = None
        previous: Any = None
        greater: Any = None
        lesser: Any = None

        outer: list[etree.Element] = []
        outer_r: list[tuple[int, int, int, int, int]] = []

        if len(self.tags) == 2:
            greater, lesser = self.tags
        elif self.double:
            greater = self.tags[0]
            lesser = None
        else:
            lesser = self.tags[0]
            greater = None

        # Iterate regions creating the elements they represent
        end = len(regions)
        idx = 0
        for idx, i in enumerate(range(start, end), 1):
            r = regions[i]
            # Not contained within region
            if idx and r[0] >= regions[start][3]:
                idx -= 1
                break
            # Get the appropriate element(s)
            if r[4] == 2:
                el1 = etree.Element(greater)
            else:
                el1 = etree.Element(lesser)

            # Populate the elements with their text
            if idx > 1:
                if last.text is None:
                    if previous[2] < r[0]:
                        last.text = data[previous[1]+offset:previous[2]+offset]
                    else:
                        last.text = data[previous[1]+offset:r[0]+offset]
                if last is not outer[-1] and last.tail is None:
                    if r[0] < outer_r[-1][3]:
                        last.tail = data[previous[3]+offset:r[0]+offset]
                    else:
                        last.tail = data[previous[3]+offset:outer_r[-1][2]+offset]
                        outer[-1].tail = data[outer_r[-1][3]+offset:r[0]+offset]

            # First element
            if el is None:
                el = el1
                last = el
                outer.append(el)
                outer_r.append(r)

            # Subsequent elements
            else:
                # Is the current outer element no longer wrapping this one?
                while len(outer_r) > 1 and r[3] > outer_r[-1][3]:
                    outer.pop()
                    outer_r.pop()

                # Non-nested
                else:
                    outer[-1].append(el1)

                # Is this element wrapping the next?
                if i + 1 < end:
                    if r[3] > regions[i + 1][3]:
                        outer.append(el1)
                        outer_r.append(r)

                # Track the last element we parsed.
                last = el1

            # Track the previous region.
            previous = r

        # Populate remaining elements with their text
        while outer:
            if last.text is None:
                last.text = data[previous[1]+offset:previous[2]+offset]
            if last.tail is None and last is not outer[-1]:
                last.tail = data[previous[3]+offset:outer_r[-1][2]+offset]
            last = outer.pop()
            previous = outer_r.pop()

        return cast('etree.Element', el), idx

    def increment_next_position(self, start: int, count: int, offset: int) -> None:
        """
        Increment cache position to the next location that we can initiate an insertion.

        Cache position should be the first match after our current replacement.
        This gives us an anchor to calculate the new offset after insertion.
        """

         # Determine next offset
        self.cache_index += count
        if self.cache_index < len(self.regions):
            self.cache_pos = self.regions[self.cache_index][0]
            # Legacy position is for older Python Markdown and must be
            # the start of the last inserted region before offsets change.
            # This allows us to skip anything before our target cache position.
            self.cache_legacy_pos = start + offset
            while self.stack:
                entry = self.stack.popleft()
                if entry[0] > start:
                    self.cache_pos = entry[0]
                    break

        # Nothing left to process
        else:
            self.reset()

    def get_cached_result(self, pos: int, data: str) -> tuple[etree.Element, int, int]:
        """Get a cached result."""

        # Process the next region(s) in the cache
        regions = self.regions
        offset = pos - self.cache_pos if pos != self.cache_pos else pos - regions[self.cache_index][0]
        start, end = regions[self.cache_index][0], regions[self.cache_index][3]
        el, count = self._build_element(data, self.cache_index, offset)
        self.increment_next_position(start, count, offset)
        return el, start + offset, end + offset

    def handleMatch(  # type: ignore[override]
        self,
        m: re.Match[str],
        data: str
    ) -> tuple[etree.Element | None, int | None, int | None]:
        """Parse delimiter pattern."""

        # TODO: Remove when Python Markdown > 3.10.3 releases.
        if not MD_FAST and self.cache_legacy_pos > -1 and m.end(0) < self.cache_legacy_pos:
            return None, m.start(0), self.cache_legacy_pos
        self.cache_legacy_pos = -1

        # Do we have entries we haven't returned yet?
        if self.regions:
            return self.get_cached_result(m.start(0), data)

        # If token is not an opening, quit
        m2 = self.boundary.match(data, m.start(0))
        if m2 is None or m2.lastgroup[0] == 'e':  # type: ignore[index]
            if m2 is not None:
                m = m2
            # Advance past the full length of the delimiter found
            return None, m.start(0), m.end(0)

        # Get the stack and regions
        stack = self.stack
        regions = self.regions

        start = m2.start(0)
        end = m2.end(0)
        l = end - start
        is_ambiguous =  m2.lastgroup[0] != 's'  # type: ignore[index]
        self.stack.append((start, start + l, is_ambiguous, l))

        # Track how many tokens in the stack require or possibly require no spaces.
        no_space = 1 if l == 1 or l > 2 else 0
        # Track how many single width tokens we have in the stack.
        # This bookkeeping allows us to know when we can no longer pair matches.
        singles = 0

        # Pair tokens until the stack is empty or we can no longer find tokens.
        while stack:
            m2 = self.boundary.search(data, end)
            if m2 is None:
                break
            start = m2.start(0)
            end = m2.end(0)

            # Get current and last delimiter size
            current = len(m2.group(0))
            last = stack[-1][-1]

            # Some delimiters may be ambiguous and look like both a start or an end
            is_start = m2.lastgroup[0] != 'e'  # type: ignore[index]
            is_end = not is_start or m2.lastgroup[0] != 's'  # type: ignore[index]
            is_ambiguous = is_start and is_end

            # Find closing tokens
            # Looking for:
            # - `*em*`
            # - `**strong**`
            # - `***strong,em***`
            # - `*em**`
            # - `*em***`
            # - `**strong***`
            #
            # Avoid ambiguous tokens that could be a start or an end.
            # Consume starts until the end token is fully consumed.
            # If we don't consume the entire end, see if next rule consumes it.
            if is_end and ((not is_ambiguous and current > last) or (current <= 3 and current == last) or current >= 3):
                is_start = False

                # Consume previous points until the delimiter is consumed
                original = current
                furthest = stack[-1]
                while current and last <= current:
                    okay = True
                    delimiter = stack.pop()
                    # Reject start/end pair if whitespace requirement is not satisfied.
                    # Try to find a pair that can work if the first fails.
                    if self.no_space:
                        if delimiter[-1] == 1:
                            singles -= 1
                        while True:
                            okay = True
                            if (no_space or current == 1) and self.SPACE.search(data[delimiter[1]:start]):
                                okay = False
                                if stack:
                                    if delimiter[-1] != 2:
                                        no_space -= 1
                                    delimiter = stack.pop()
                                    if delimiter[-1] == 1:
                                        singles -= 1
                                    last = delimiter[-1]
                                    continue
                            break

                    # We've exhausted our options, unable to make a reasonable pair.
                    # Append the furthest we searched so we can avoid it on next pass.
                    if not okay:
                        stack.append(furthest)
                        break

                    # Build up region for pair and adjust accounting.
                    size = min(delimiter[-1], self.max_size)
                    regions.append((delimiter[1] - size, delimiter[1], start, start + size, size))
                    start += size
                    current -= size
                    new = 0
                    if size < delimiter[-1] and (not self.double or (delimiter[-1] - size) != 1):
                        new = delimiter[-1] - size
                        stack.append((delimiter[0], delimiter[1] - size, delimiter[2], new))
                    if not stack:
                        is_end = False
                        break

                    last = stack[-1][-1]
                    if delimiter[-1] != 2 and last == 2:
                        no_space -= 1

                # Should remainder be treated as a new start?
                if original >= 3 and current and is_ambiguous:
                    self.stack.append((regions[-1][3], end, False, current))
                    is_end = False

                # Do we still have more to consume?
                else:
                    is_end = current and stack and last > current

            # Find closing tokens
            # Looking for:
            # - `***em*`
            # - `***strong**`
            # - `**em*`
            if is_end and (last >= 3 or not is_ambiguous) and last > current:
                delimiter = stack.pop()

                # Don't pair with an ambiguous opening
                while stack and delimiter[2] and last > current:
                    delimiter =  stack.pop()
                    last = delimiter[-1]
                if delimiter[2]:
                    break

                ignore = False
                # Reject end if the content's white space invalidates it.
                if self.no_space:
                    if (current == 1 or self.single) and self.SPACE.search(data[delimiter[1]:m2.start(0)]):
                        stack.append(delimiter)
                        ignore = True

                # Create new region if end is valid.
                # If not valid, ignore the end but continue parsing.
                if not ignore:
                    is_start = False
                    ds, de = delimiter[:2]
                    while current and (not self.double or current != 1):
                        size = min(current, self.max_size)
                        new = last - size
                        regions.append((ds + new, de, start, start + size, size))
                        start += size
                        current -= size
                        last -= size
                        de -= size
                    if not self.double or last != 1:
                        stack.append((ds, de, False, last))

                    # Bookkeeping for no space requirement
                    if self.no_space:
                        if last == 1:
                            singles += 1
                        if delimiter[-1] != 2 and last == 2:
                            no_space -= 1

            # Find opening tokens
            # Looking for:
            # - `*em ...*`
            # - `**strong ...*`
            # - `***em ...*`
            if is_start and (not self.double or current != 1):
                # Start a new nested span, but avoid adding new spans if it no space requirement
                # cannot be fulfilled. Abort if it is impossible to meet the requirement.
                if self.no_space and no_space and self.SPACE.search(data[stack[-1][1]:start]):
                    if no_space > 1 or singles:
                        break
                    continue

                stack.append((start, end, is_ambiguous, current))

                # Bookkeeping for no space requirement
                if self.no_space:
                    if current != 2:
                        no_space += 1
                    if current == 1:
                        singles += 1

        # Build the HTML elements
        if regions:
            # Regions may be out of order.
            regions.sort(key=lambda x: x[0])
            start, end = regions[0][0], regions[0][3]
            el, count = self._build_element(data)
            self.increment_next_position(start, count, 0)
            return el, start, end

        # We failed to pair any valid start/end delimiters, avoid the parsed range next pass.
        start = m.start(0)
        end = stack[-1][1] if stack and (MD_FAST or len(stack) > 1) else m.end(0)
        self.reset()
        return None, start, end


def deprecated(message: str, stacklevel: int = 2) -> Callable[..., Any]:  # pragma: no cover
    """
    Raise a `DeprecationWarning` when wrapped function/method is called.

    Usage:

        @deprecated("This method will be removed in version X; use Y instead.")
        def some_method()"
            pass
    """

    def _wrapper(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def _deprecated_func(*args: Any, **kwargs: Any) -> Any:
            warnings.warn(
                f"'{func.__name__}' is deprecated. {message}",
                category=DeprecationWarning,
                stacklevel=stacklevel
            )
            return func(*args, **kwargs)
        return _deprecated_func
    return _wrapper


def warn_deprecated(message: str, stacklevel: int = 2) -> None:  # pragma: no cover
    """Warn deprecated."""

    warnings.warn(
        message,
        category=DeprecationWarning,
        stacklevel=stacklevel
    )
