"""BracketSpan."""
from markdown import Extension, Markdown
from markdown.inlinepatterns import InlineProcessor
from . import util
import re
import xml.etree.ElementTree as etree
from markdown.extensions import attr_list
from collections import deque
from typing import cast


class BracketSpanProcessor(InlineProcessor):
    """Return a link element from the given match."""

    ATTR_RE =re.compile(r'\{\:?[ ]*([^\}\n ][^\n]*)[ ]*\}|\{\s*\}')
    NAME_RE = attr_list.AttrListTreeprocessor.NAME_RE

    def __init__(
        self,
        pattern: str,
        md: Markdown | None = None,
    ) -> None:
        """Initialize."""

        self.attr_list_enabled = False
        self.stack: deque[tuple[int, list[tuple[etree.Element, int, int]]]] = deque()
        self.span: tuple[etree.Element, int, int] | None = None
        self.cache_pos = 0
        super().__init__(pattern, md)

    def get_next_entry(self) -> tuple[etree.Element, int, int] | None:
        """
        Get next entry.

        While getting next entry, flag the first match of `[` we encounter.
        We use this to correct our offset so we can jump to, and process the
        next entry without having to iterate all bad matches in between.
        """

        span = None
        updated = False
        for _ in range(len(self.stack)):
            entry = self.stack[0]
            if entry[1]:
                span = entry[1].pop(0)
                if not updated:
                    self.cache_pos = span[1]
                if not entry[1]:
                    self.stack.popleft()
                break
            else:
                if not updated:
                    self.cache_pos = self.stack[0][0]
                    updated = True
                self.stack.popleft()
        return span

    def get_cached_result(self, start: int) -> tuple[etree.Element, int, int]:
        """Get cached results."""

        offset = start - self.cache_pos
        span, start, end = cast('tuple[etree.Element, int, int]', self.span)
        self.span = None

        # See if there is another span
        self.cache_pos = end
        self.span = self.get_next_entry()
        # On earlier versions Python Markdown, we need another point
        # that requires no updates to the offset as a minimum.
        # The start of the replaced region is sufficient, and `cache_pos`
        # should be right after it.
        self.legacy_pos = start + offset

        # No more spans were found
        if self.span is None:
            self.reset()

        return span, start + offset, end + offset

    def build_element(
        self,
        data: str,
        end: int,
        current: tuple[int, list[tuple[etree.Element, int, int]]],
        attributes: str
    ) -> tuple[etree.Element, int]:
        """Build the element."""

        # Parse the attributes
        attrs, remainder = attr_list.get_attrs_and_remainder(attributes)
        roffset = len(remainder)

        # Build the element
        span = etree.Element('span')
        for k, v in attrs:
            if k == '.':
                # add to class
                cls = span.get('class')
                if cls:
                    span.set('class', '{} {}'.format(cls, v))
                else:
                    span.set('class', v)
            else:
                # assign attribute `k` with `v`
                span.set(self.NAME_RE.sub('_', k), v)

        s = current[0] + 1
        e = end
        for child in current[1]:
            s2 = child[1]
            e2 = child[2]
            if span.text is None:
                span.text = data[s:s2]
            elif len(span):
                span[-1].tail = data[s:s2]
            span.append(child[0])
            s = e2

        if span.text is None:
            span.text = data[s:e]
        elif len(span):
            span[-1].tail = data[s:e]
        return span, roffset

    def handleMatch(self, m: re.Match[str], data: str) -> tuple[etree.Element | str | None, int | None, int | None]:
        """Handle the match."""

        if not self.attr_list_enabled:
            return None, None, None

        if not util.MD_FAST and self.legacy_pos >= 0 and m.start(0) < self.legacy_pos:
            return None, m.start(0), m.end(0)
        self.legacy_pos = -1

        if self.span is not None:
            return self.get_cached_result(m.start(0))

        start = m.start(0)
        end = len(data)

        # Search for brackets
        for i in range(start, end):
            if data[i] == '[':
                self.stack.append((i, []))
            elif data[i] == ']':
                # Look for attribute list syntax
                m2 = self.ATTR_RE.match(data, i + 1)
                if m2:

                    current = self.stack.pop()
                    span, r_offset = self.build_element(data, i, current, m2.group(0)[1:-1])

                    # Store the span
                    if self.stack:
                        self.stack[-1][1].append((span, current[0], m2.end(0) - r_offset))
                    else:
                        self.span = (span, current[0], m2.end(0) - r_offset)

                    if not self.stack:
                        break

        # Everything not contained in a single element, find the first valid element
        if self.span is None:
            # Look for a valid span to return
            result = None, start, end
            temp = self.get_next_entry()
            if temp is not None:
                result = temp

            # See if there are more spans
            self.cache_pos = result[2]
            self.span = self.get_next_entry()
            # On earlier versions Python Markdown, we need another point
            # that requires no updates to the offset as a minimum.
            # The start of the replaced region is sufficient, and `cache_pos`
            # should be right after it.
            self.legacy_pos = result[1]

            # There are no more results
            if self.span is None:
                self.reset()

            return result

        # Return the span
        span, start, end = cast('tuple[etree.Element, int, int]', self.span)
        self.span = None
        return span, start, end

    def reset(self):
        """Rest."""

        self.stack.clear()
        self.span = None
        self.cache_pos = 0
        self.legacy_pos = -1


class BracketSpanExtension(Extension):
    """Add the mark extension to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {}

        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        """Insert `<mark>test</mark>` tags as `==test==`."""

        self.md = md
        self.md.registerExtension(self)

        escape_chars = []
        escape_chars.append('=')
        util.escape_chars(md, escape_chars)
        self.processor = BracketSpanProcessor(r'\[', self.md)
        self.md.inlinePatterns.register(self.processor, "bracket_span", 124)

    def reset(self):
        """Reset."""

        self.processor.reset()
        self.processor.attr_list_enabled = 'attr_list' in self.md.treeprocessors


def makeExtension(*args, **kwargs):
    """Return extension."""

    return BracketSpanExtension(*args, **kwargs)

