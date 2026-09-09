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

RE_WIN_DRIVE_LETTER = re.compile(r"^[A-Za-z]$")
RE_WIN_DRIVE_PATH = re.compile(r"^[A-Za-z]:(?:\\.*)?$")
RE_URL = re.compile('(http|ftp)s?|data|mailto|tel|news')
RE_WIN_DEFAULT_PROTOCOL = re.compile(r"^///[A-Za-z]:(?:/.*)?$")

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

        self.no_space = no_space
        self.smart = smart
        self.tags = tags.split(',')
        self.double = len(tags) != 2 and double
        self.reset()
        super().__init__(self._build_patterns(token), md)

    def reset(self) -> None:
        """Reset."""

        # Cache info
        self.regions: list[tuple[int, int, int, int, int]] = []
        self.stack: deque[tuple[int, int, int]] = deque()
        self.cache_index = 0
        self.cache_pos = 0
        self.cache_legacy_pos = -1

    def _build_patterns(self, token: str) -> str:
        """Build regular expression patterns."""

        # Build up patterns
        self.token = token
        etoken = re.escape(token)
        avoid_start = fr'(?:(?<=_)|(?<![\w{etoken}]))' if token != '_' else fr'(?<![\w{etoken}])'
        avoid_end = fr'(?:(?=_)|(?![\w{etoken}]))' if token != '_' else fr'(?![\w{etoken}])'

        # Patterns for when the larger delimiter is "smart" and the smaller is "dumb".
        if self.smart and self.no_space and len(self.tags) == 2:
            self.boundary = re.compile(
                fr'''(?x)(?:
                (?:
                    (?P<ambiguous3>(?<!^)(?<![\s{etoken}]){etoken}{{3}}(?![\s{etoken}])(?!$))|
                    (?P<end3>(?<!^)(?<![\s{etoken}]){etoken}{{3}})|
                    (?P<start3>{etoken}{{3}}(?![\s{etoken}])(?!$))
                )|
                (?:
                    (?P<ambiguous2>(?<!^)(?<![\s{etoken}]){avoid_start}{etoken}{{2}}{avoid_end}(?![\s{etoken}])(?!$))|
                    (?P<end2>(?<!^)(?<![\s{etoken}]){etoken}{{2}}{avoid_end})|
                    (?P<start2>{avoid_start}{etoken}{{2}}(?![\s{etoken}])(?!$))
                )|
                (?:
                    (?P<ambiguous1>(?<!^)(?<![\s{etoken}]){etoken}{{1}}(?![\s{etoken}])(?!$))|
                    (?P<end1>(?<!^)(?<![\s{etoken}]){etoken}{{1}})|
                    (?P<start1>{etoken}{{1}}(?![\s{etoken}])(?!$))
                )
                )''',
                flags=re.UNICODE
            )
        # Patterns for "smart" cases.
        elif self.smart and (not self.no_space or self.double):
            if len(self.tags) == 2:
                self.boundary = re.compile(
                    fr'''(?x)
                    (?P<ambiguous>(?<!^)(?<![\s{etoken}]){avoid_start}{etoken}{{1,3}}{avoid_end}(?![\s{etoken}])(?!$))|
                    (?P<end>(?<!^)(?<![\s{etoken}]){etoken}{{1,3}}{avoid_end})|
                    (?P<start>{avoid_start}{etoken}{{1,3}}(?![\s{etoken}])(?!$))
                    ''',
                    flags=re.UNICODE
                )
            elif self.double:
                self.boundary = re.compile(
                    fr'''(?x)
                    (?P<ambiguous>(?<!^)(?<![\s{etoken}]){avoid_start}{etoken}{{2}}{avoid_end}(?![\s{etoken}])(?!$))|
                    (?P<end>(?<!^)(?<![\s{etoken}]){etoken}{{2}}{avoid_end})|
                    (?P<start>{avoid_start}{etoken}{{2}}(?![\s{etoken}])(?!$))
                    ''',
                    flags=re.UNICODE
                )
            else:  # pragma: no cover
                # This case is not currently used
                self.boundary = re.compile(
                    fr'''(?x)
                    (?P<ambiguous>(?<!^)(?<![\s{etoken}]){avoid_start}{etoken}{{1}}{avoid_end}(?![\s{etoken}])(?!$))|
                    (?P<end>(?<!^)(?<![\s{etoken}]){etoken}{{1}}{avoid_end})|
                    (?P<start>{avoid_start}{etoken}{{1}}(?![\s{etoken}])(?!$))
                    ''',
                    flags=re.UNICODE
                )
        # Patterns for "dumb" cases.
        else:
            if len(self.tags) == 2:
                self.boundary = re.compile(
                    fr'''(?x)(?:
                    (?P<ambiguous>(?<!^)(?<![\s{etoken}]){etoken}{{1,3}}(?![\s{etoken}])(?!$))|
                    (?P<end>(?<!^)(?<![\s{etoken}]){etoken}{{1,3}})|
                    (?P<start>{etoken}{{1,3}}(?![\s{etoken}])(?!$))
                    )''',
                    flags=re.UNICODE
                )
            elif self.double:
                self.boundary = re.compile(
                    fr'''(?x)
                    (?P<ambiguous>(?<!^)(?<![\s{etoken}]){etoken}{{2}}(?![\s{etoken}])(?!$))|
                    (?P<end>(?<!^)(?<![\s{etoken}]){etoken}{{2}})|
                    (?P<start>{etoken}{{2}}(?![\s{etoken}])(?!$))
                    ''',
                    flags=re.UNICODE
                )
            else:
                self.boundary = re.compile(
                    fr'''(?x)
                    (?P<ambiguous>(?<!^)(?<![\s{etoken}]){etoken}{{1}}(?![\s{etoken}])(?!$))|
                    (?P<end>(?<!^)(?<![\s{etoken}]){etoken}{{1}})|
                    (?P<start>{etoken}{{1}}(?![\s{etoken}])(?!$))
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

        triple = set()
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
            if idx and r[0] > regions[start][3]:
                idx -= 1
                break
            # Get the appropriate element(s)
            if r[4] == 3:
                el1 = etree.Element(greater)
                el2 = etree.Element(lesser)
            elif r[4] == 2:
                el1 = etree.Element(greater)
                el2 = None
            else:
                el1 = etree.Element(lesser)
                el2 = None

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

                # Double nested element (triple token)
                if outer[-1] in triple:
                    outer[-1][-1].append(el1)

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

            # Nest secondary element if there is one.
            # Track triple tokens (double elements)
            # so we can identify quickly and properly nest.
            if el2 is not None:
                el1.append(el2)
                last = el2
                triple.add(el1)

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

    def increment_next_position(self, start: int, end: int, count: int, offset: int) -> None:
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
                if entry[0] > end:
                    self.cache_pos = entry[0]
                    break

        # Nothing left to process
        else:
            self.reset()

    def get_cached_result(self, pos: int, data: str) -> tuple[etree.Element, int, int]:
        """Get a cached result."""

        # Process the next region(s) in the cache
        regions = self.regions
        offset = pos - self.cache_pos
        start, end = regions[self.cache_index][0], regions[self.cache_index][3]
        el, count = self._build_element(data, self.cache_index, offset)
        self.increment_next_position(start, end, count, offset)
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

        # Delimiter length
        l = len(m2.group(0))
        # Data offset
        offset = m2.end(0)
        # Stack of opening delimiters
        stack.append((m2.start(0), offset, l))
        # Track how many tokens in the stack require or possibly require no spaces.
        no_space = 1 if l != 2 else 0
        # Track how many single width tokens we have in the stack.
        # This bookkeeping allows us to know when we can no longer pair matches.
        singles = 0

        # Pair tokens until the stack is empty or we can no longer find tokens.
        while stack:
            m2 = self.boundary.search(data, offset)
            if m2 is None:
                break
            offset = m2.end(0)

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
            if is_end and ((not is_ambiguous and current > last) or (current == last)):
                is_start = False

                # Consume previous points until the delimiter is consumed
                s = m2.start(0)
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
                            if (no_space or current == 1) and self.SPACE.search(data[delimiter[1]:s]):
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
                    regions.append((delimiter[0], delimiter[1], s, s + delimiter[-1], delimiter[-1]))
                    s += delimiter[-1]
                    current -= delimiter[-1]
                    if not stack:
                        is_end = False
                        break
                    last = stack[-1][-1]
                    if delimiter[-1] != 2 and last == 2:
                        no_space -= 1

                # Do we still have more to consume?
                is_end = current and stack and last > current

            # Find closing tokens
            # Looking for:
            # - `***em*`
            # - `***strong**`
            # - `**em*`
            if is_end and (last == 3 or not is_ambiguous) and last > current:
                delimiter = stack.pop()
                ignore = False
                # Reject end if the content's white space invalidates it.
                if self.no_space:
                    if current == 1 and self.SPACE.search(data[delimiter[1]:m2.start(0)]):
                        stack.append(delimiter)
                        ignore = True

                # Create new region if end is valid.
                # If not valid, ignore the end but continue parsing.
                if not ignore:
                    is_start = False
                    new = last - current
                    regions.append((delimiter[0] + new, delimiter[1], m2.start(0), offset, current))
                    stack.append((delimiter[0], delimiter[0] + new, new))

                    # Bookkeeping for no space requirement
                    if self.no_space:
                        if new == 1:
                            singles += 1
                        if delimiter[-1] != 2 and new == 2:
                            no_space -= 1

            # Find opening tokens
            # Looking for:
            # - `*em ...*`
            # - `**strong ...*`
            # - `***em ...*`
            if is_start:
                # Start a new nested span, but avoid adding new spans if it no space requirement
                # cannot be fulfilled. Abort if it is impossible to meet the requirement.
                if self.no_space and no_space and self.SPACE.search(data[stack[-1][1]:m2.start(0)]):
                    if no_space > 1 or singles:
                        break
                    continue

                stack.append((m2.start(0), m2.end(0), current))

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
            self.increment_next_position(start, end, count, 0)
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
