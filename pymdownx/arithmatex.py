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

RE_DOLLAR_INLINE = r'(?:(?<!\\)((?:\\{2})+)(?=\$)|(?<!\\)(\$)(?!\s)((?:\\.|[^\$])+?)(?<!\s)(?:\$))'
RE_BRACKET_INLINE = r'(?:(?<!\\)((?:\\{2})+?)(?=\\\()|(?<!\\)(\\\()((?:\\.|[^\\])+?)(?:\\\)))'


def _escape(txt):
    """Escape HTML content."""

    txt = txt.replace('&', '&amp;')
    txt = txt.replace('<', '&lt;')
    txt = txt.replace('>', '&gt;')
    txt = txt.replace('"', '&quot;')
    return txt


class InlineArithmatexPattern(Pattern):
    """Arithmatex inline pattern handler."""

    ESCAPED_BSLASH = '%s%s%s' % (md_util.STX, ord('\\'), md_util.ETX)

    def __init__(self, pattern, wrap, script, md):
        """Initialize."""

        self.script = script
        self.wrap = wrap[0] + '%s' + wrap[1]
        Pattern.__init__(self, pattern)
        self.markdown = md

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
        if self.script:
            el = md_util.etree.Element('script', {'type': 'math/tex'})
            el.text = md_util.AtomicString(math)
        else:
            el = self.markdown.htmlStash.store(self.wrap % _escape(math), safe=True)
        return el


class BlockArithmatexProcessor(BlockProcessor):
    """Mathjax block processor to find $$mathjax$$ content."""

    RE_DOLLAR_BLOCK = r'(?P<dollar>[$]{2})(?P<math>.+?)(?P=dollar)'
    RE_TEX_BLOCK = r'(?P<math2>\\begin\{(?P<env>[a-z]+\*?)\}.+?\\end\{(?P=env)\})'
    RE_BRACKET_BLOCK = r'\\\[(?P<math3>(?:\\[^\]]|[^\\])+?)\\\]'

    def __init__(self, config, md):
        """Initialize."""

        self.script = config.get('insert_as_script', False)
        wrap = config.get('tex_block_wrap', ['\\[', '\\]'])
        self.wrap = wrap[0] + '%s' + wrap[1]

        allowed_patterns = set(config.get('block_syntax', ['dollar', 'square', 'begin']))
        self.pattern = []
        if 'dollar' in allowed_patterns:
            self.pattern.append(self.RE_DOLLAR_BLOCK)
        if 'square' in allowed_patterns:
            self.pattern.append(self.RE_BRACKET_BLOCK)
        if 'begin' in allowed_patterns:
            self.pattern.append(self.RE_TEX_BLOCK)

        BlockProcessor.__init__(self, md.parser)
        self.markdown = md

    def test(self, parent, block):
        """Return 'True' for future Python Markdown block compatibility."""

        return bool(len(self.pattern))

    def run(self, parent, blocks):
        """Find and handle block content."""

        handled = False

        pattern = re.compile(r'(?s)^(?:%s)[ ]*$' % '|'.join(self.pattern))
        m = pattern.match(blocks[0])

        if m:
            handled = True
            block = blocks.pop(0)

            math = m.group('math')
            if not math:
                math = m.group('math2')
            if not math:
                math = m.group('math3')
            if self.script:
                script = md_util.etree.SubElement(parent, 'script', {'type': 'math/tex; mode=display'})
                script.text = md_util.AtomicString(math)
            else:
                block = self.markdown.htmlStash.store(self.wrap % _escape(math), safe=True)
                blocks.insert(0, block)
        return handled


class ArithmatexExtension(Extension):
    """Adds delete extension to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'tex_inline_wrap': [
                ["\\(", "\\)"],
                "Wrap inline content with the provided text ['open', 'close'] - Default: ['', '']"
            ],
            'tex_block_wrap': [
                ["\\[", "\\]"],
                "Wrap blick content with the provided text ['open', 'close'] - Default: ['', '']"
            ],
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
            'insert_as_script': [
                False,
                "Insert the math Tex notation into a script tag. Overrides wrapping. - Default: False"
            ]
        }

        super(ArithmatexExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """Extend the inline and block processor objects."""

        md.registerExtension(self)
        util.escape_chars(md, ['$'])

        config = self.getConfigs()

        allowed_inline = set(config.get('inline_syntax', ['dollar', 'round']))
        inline_patterns = []
        if 'dollar' in allowed_inline:
            inline_patterns.append(RE_DOLLAR_INLINE)
        if 'round' in allowed_inline:
            inline_patterns.append(RE_BRACKET_INLINE)
        if inline_patterns:
            inline = InlineArithmatexPattern(
                '(?:%s)' % '|'.join(inline_patterns),
                config.get('tex_inline_wrap', ["\\(", "\\)"]),
                config.get('insert_as_script', False),
                md
            )
            md.inlinePatterns.add("arithmatex-inline", inline, ">backtick")
        md.parser.blockprocessors.add('arithmatex-block', BlockArithmatexProcessor(config, md), "<code")


def makeExtension(*args, **kwargs):
    """Return extension."""

    return ArithmatexExtension(*args, **kwargs)
