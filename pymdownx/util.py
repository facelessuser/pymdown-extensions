"""
General utilities.

MIT license.

Copyright (c) 2017 Isaac Muse <isaacmuse@gmail.com>
"""
from __future__ import annotations
from markdown import Markdown
from markdown.blockparser import BlockParser
import xml.etree.ElementTree as etree
from types import FrameType
import sys
import copy
import re
import html
from urllib.request import pathname2url, url2pathname
from urllib.parse import urlparse
from functools import wraps
import warnings
from typing import Sequence, Callable, Any

if sys.platform.startswith('win'):
    _PLATFORM = "windows"
elif sys.platform == "darwin":  # pragma: no cover
    _PLATFORM = "osx"
else:
    _PLATFORM = "linux"

PY39 = (3, 9) <= sys.version_info
PY314 = (3, 14) <= sys.version_info

# Stop this many levels short of the recursion limit (the same margin Python Markdown uses)
RECURSION_MARGIN = 100


def nearing_depth_limit(parser: BlockParser, parent: etree.Element | None = None) -> bool:
    """
    Check if we are nearing the recursion limit, either on the call stack or in the element tree.

    Python Markdown's `nearing_recursion_limit` only considers the current call stack. Extensions that nest content
    without recursing (e.g. by tracking nested blocks or lists via state) can build an element tree that is deeper than
    the recursion limit even though the call stack stays shallow. The tree is later recursively walked by tree
    processors and the serializer, which will raise a `RecursionError` if it is too deep.

    Parsing is append only, so `parent` is always on the chain of last children from the root of the tree. We can
    determine the depth of the tree at `parent` by following that chain. Both the depth of the call stack and the
    depth of the tree are considered together, which is conservative as the tree gets walked from a shallower stack.
    """

    stack_depth = 0
    frame: FrameType | None = sys._getframe(1)
    while frame:
        stack_depth += 1
        frame = frame.f_back

    tree_depth = 0
    node = getattr(parser, 'root', None)
    while node is not None and node is not parent:
        tree_depth += 1
        node = node[-1] if len(node) else None

    return sys.getrecursionlimit() - (stack_depth + tree_depth) < RECURSION_MARGIN


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
