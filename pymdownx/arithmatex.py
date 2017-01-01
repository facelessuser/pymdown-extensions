r"""
Arithmatex.

pymdownx.arithmatex
Extension that preserves the following for MathJax use:
$$
  Display Equations
$$

and $Inline MathJax Equations$

Inline equations are converted to the following form for HTML output:

\(Inline MathJax Equations\)

While block/display equations are converted to the following form for HTML output:

\[
  Display Equations
\]

MIT license.

Copyright (c) 2014 - 2017 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
from __future__ import unicode_literals
from markdown import Extension
from markdown.inlinepatterns import Pattern
from markdown.blockprocessors import BlockProcessor
import re

RE_MATH = r'((?<!\\)(?:\\{2})*)([$])(?!\s)((?:\\.|[^$])+?)(?<!\s)(\3)'
RE_DOLLAR_ESCAPE = re.compile(r'\\.')


def escape(txt):
    """Escape HTML content."""

    txt = txt.replace('&', '&amp;')
    txt = txt.replace('<', '&lt;')
    txt = txt.replace('>', '&gt;')
    txt = txt.replace('"', '&quot;')
    return txt


class InlineArithmatexPattern(Pattern):
    """Arithmatex inline pattern handler."""

    def __init__(self, pattern, md):
        """Initialize."""

        Pattern.__init__(self, pattern)
        self.markdown = md

    def handleMatch(self, m):
        """Handle notations and switch them to something that will be more detectable in HTML."""

        # Use the more reliable patterns to avoid '$'
        # false positives.
        math = "\\(%s\\)" % RE_DOLLAR_ESCAPE.sub(
            lambda m: '$' if m.group(0) == "\\$" else m.group(0),
            m.group(4)
        )
        return m.group(2) + self.markdown.htmlStash.store(
            escape(math),
            safe=True
        )


class BlockArithmatexProcessor(BlockProcessor):
    """Mathjax block processor to find $$mathjax$$ content."""

    RE_MATH_BLOCK = re.compile(
        r'(?s)^(?P<dollar>[$]{2})(?P<math>.*?)(?P=dollar)[ ]*$'
    )

    def __init__(self, md):
        """Initialize."""

        BlockProcessor.__init__(self, md.parser)
        self.markdown = md

    def test(self, parent, block):
        """Return 'True' for future Python Markdown block compatibility."""
        return True

    def run(self, parent, blocks):
        """Find and handle block content."""

        handled = False

        m = self.RE_MATH_BLOCK.match(blocks[0])

        if m:
            handled = True
            block = blocks.pop(0)
            # Use the more reliable patterns to avoid '$'
            # false positives.
            math = "\\[%s\\]" % RE_DOLLAR_ESCAPE.sub(
                lambda m: '$' if m.group(0) == "\\$" else m.group(0),
                m.group('math')
            )
            block = self.markdown.htmlStash.store(
                escape(math),
                safe=True
            )
            blocks.insert(0, block)
        return handled


class ArithmatexExtension(Extension):
    """Adds delete extension to Markdown class."""

    def extendMarkdown(self, md, md_globals):
        """Extend the inline and block processor objects."""

        md.registerExtension(self)
        if "$" not in md.ESCAPED_CHARS:
            md.ESCAPED_CHARS.append('$')

        md.inlinePatterns.add(
            "arithmatex-inline",
            InlineArithmatexPattern(RE_MATH, md),
            ">backtick"
        )

        md.parser.blockprocessors.add(
            'arithmatex-block',
            BlockArithmatexProcessor(md),
            "<code"
        )


def makeExtension(*args, **kwargs):
    """Return extension."""

    return ArithmatexExtension(*args, **kwargs)
