r"""
Arithmatex.

pymdownx.arithmatex
Extension that preserves the following for MathJax use:

$Equation$, \(Equation\)

$$
  Display Equations
$$

\[
  Display Equations
\]

\begin{align}
  Display Equations
\end{align}

and $Inline MathJax Equations$

Inline equations are converted to the following form for HTML output by default:

\(Inline MathJax Equations\)

While block/display equations are converted to the following form for HTML output by default:

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
from markdown import util as md_util
from . import util
import re
from .util import PymdownxDeprecationWarning
import warnings

DEPRECATION_WARN = """'%s' is deprecated and is now unnecessary and does nothing.
Please discontinue using this option as it will be removed in the future.
See documentation to see why this have been deprecated."""

RE_DOLLAR_INLINE = r'(?:(?<!\\)((?:\\{2})+)(?=\$)|(?<!\\)(\$)(?!\s)((?:\\.|[^\$])+?)(?<!\s)(?:\$))'
RE_BRACKET_INLINE = r'(?:(?<!\\)((?:\\{2})+?)(?=\\\()|(?<!\\)(\\\()((?:\\[^)]|[^\\])+?)(?:\\\)))'


class InlineArithmatexPattern(Pattern):
    """Arithmatex inline pattern handler."""

    ESCAPED_BSLASH = '%s%s%s' % (md_util.STX, ord('\\'), md_util.ETX)

    def __init__(self, pattern, preview):
        """Initialize."""

        self.preview = preview
        Pattern.__init__(self, pattern)

    def handleMatch(self, m):
        """Handle notations and switch them to something that will be more detectable in HTML."""

        # Handle escapes
        escapes = m.group(2)
        if not escapes:
            escapes = m.group(5)
        if escapes:
            return escapes.replace('\\\\', self.ESCAPED_BSLASH)

        # Handle Tex
        math = m.group(4)
        if not math:
            math = m.group(7)

        if self.preview:
            el = md_util.etree.Element('span')
            preview = md_util.etree.SubElement(el, 'span', {'class': 'MathJax_Preview'})
            preview.text = md_util.AtomicString(math)
            script = md_util.etree.SubElement(el, 'script', {'type': 'math/tex'})
            script.text = md_util.AtomicString(math)
        else:
            el = md_util.etree.Element('script', {'type': 'math/tex'})
            el.text = md_util.AtomicString(math)
        return el


class BlockArithmatexProcessor(BlockProcessor):
    """Mathjax block processor to find $$mathjax$$ content."""

    RE_DOLLAR_BLOCK = r'(?P<dollar>[$]{2})(?P<math>.+?)(?P=dollar)'
    RE_TEX_BLOCK = r'(?P<math2>\\begin\{(?P<env>[a-z]+\*?)\}.+?\\end\{(?P=env)\})'
    RE_BRACKET_BLOCK = r'\\\[(?P<math3>(?:\\[^\]]|[^\\])+?)\\\]'

    def __init__(self, preview, allowed_patterns, md):
        """Initialize."""

        self.preview = preview
        pattern = []
        if 'dollar' in allowed_patterns:
            pattern.append(self.RE_DOLLAR_BLOCK)
        if 'square' in allowed_patterns:
            pattern.append(self.RE_BRACKET_BLOCK)
        if 'begin' in allowed_patterns:
            pattern.append(self.RE_TEX_BLOCK)

        self.match = None
        if pattern:
            self.pattern = re.compile(r'(?s)^(?:%s)[ ]*$' % '|'.join(pattern))
        else:
            self.pattern = None

        BlockProcessor.__init__(self, md.parser)

    def test(self, parent, block):
        """Return 'True' for future Python Markdown block compatibility."""

        self.match = self.pattern.match(block) if self.pattern is not None else None
        return self.match is not None

    def run(self, parent, blocks):
        """Find and handle block content."""

        blocks.pop(0)

        math = self.match.group('math')
        if not math:
            math = self.match.group('math2')
        if not math:
            math = self.match.group('math3')
        if self.preview:
            grandparent = parent
            parent = md_util.etree.SubElement(grandparent, 'div')
            preview = md_util.etree.SubElement(parent, 'div', {'class': 'MathJax_Preview'})
            preview.text = md_util.AtomicString(math)
        el = md_util.etree.SubElement(parent, 'script', {'type': 'math/tex; mode=display'})
        el.text = md_util.AtomicString(math)
        return True


class ArithmatexExtension(Extension):
    """Adds delete extension to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'tex_inline_wrap': [[], "Deprecated"],
            'tex_block_wrap': [[], "Deprecated"],
            "block_syntax": [
                ['dollar', 'square', 'begin'],
                'Enable block syntax: "dollar" ($$...$$), "square" (\\[...\\]), and '
                '"begin" (\\begin{env}...\\end{env}). - Default: ["dollar", "square", "begin"]'
            ],
            "inline_syntax": [
                ['dollar', 'round'],
                'Enable block syntax: "dollar" ($$...$$), "bracket" (\\(...\\)) '
                ' - Default: ["dollar", "round"]'
            ],
            'insert_as_script': [False, "Deprecated"],
            'preview': [
                True,
                "Insert a preview for scripts. - Default: False"
            ]
        }

        super(ArithmatexExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """Extend the inline and block processor objects."""

        md.registerExtension(self)
        util.escape_chars(md, ['$'])

        config = self.getConfigs()
        preview = config.get('preview', False)

        for option in ('tex_inline_wrap', 'tex_block_wrap', 'insert_as_script'):
            if config.get(option):  # pragma: no cover
                warnings.warn(DEPRECATION_WARN % option, PymdownxDeprecationWarning)

        allowed_inline = set(config.get('inline_syntax', ['dollar', 'round']))
        inline_patterns = []
        if 'dollar' in allowed_inline:
            inline_patterns.append(RE_DOLLAR_INLINE)
        if 'round' in allowed_inline:
            inline_patterns.append(RE_BRACKET_INLINE)
        if inline_patterns:
            inline = InlineArithmatexPattern(
                '(?:%s)' % '|'.join(inline_patterns),
                preview
            )
            md.inlinePatterns.add("arithmatex-inline", inline, ">backtick")
        md.parser.blockprocessors.add(
            'arithmatex-block',
            BlockArithmatexProcessor(preview, set(config.get('block_syntax', ['dollar', 'square', 'begin'])), md),
            "<code"
        )


def makeExtension(*args, **kwargs):
    """Return extension."""

    return ArithmatexExtension(*args, **kwargs)
