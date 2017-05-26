"""
Spoilers.

pymdownx.spoilers

MIT license.

Copyright (c) 2017 Isaac Muse <isaacmuse@gmail.com>

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
from __future__ import absolute_import
from __future__ import unicode_literals
from markdown import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
import re


class SpoilersProcessor(BlockProcessor):
    """Spoilers block processor."""

    CLASS = 'spoilers'
    START = re.compile(r'(?:^|\n)\?{3}(\+)? ?([\w\-]+)?(?: +"(.*?)") *(?:\n|$)')

    def test(self, parent, block):
        """Test block."""

        sibling = self.lastChild(parent)
        return (
            self.START.search(block) or
            (
                block.startswith(' ' * self.tab_length) and sibling is not None and
                sibling.get('class', '').find(self.CLASS) != -1
            )
        )

    def run(self, parent, blocks):
        """Convert to details/summary block."""

        sibling = self.lastChild(parent)
        block = blocks.pop(0)

        m = self.START.search(block)
        if m:
            # remove the first line
            block = block[m.end():]

        # Get the spoiler block and and the non-spoiler content
        block, non_spoiler = self.detab(block)

        if m:
            state = m.group(1)
            is_open = state is not None
            class_name = m.group(2)
            class_name = '' if class_name is None else (" " + class_name.lower())
            title = m.group(3)

            div = etree.SubElement(parent, 'details', ({'open': ''} if is_open else {}))
            div.set('class', '%s%s' % (self.CLASS, class_name))
            summary = etree.SubElement(div, 'summary')
            summary.text = title
        else:
            div = sibling

        self.parser.parseChunk(div, block)

        if non_spoiler:
            # Insert the non-spoiler content back into blocks
            blocks.insert(0, non_spoiler)


class SpoilersExtension(Extension):
    """Add Spoilers extension."""

    def extendMarkdown(self, md, md_globals):
        """Add Spoilers to Markdown instance."""
        md.registerExtension(self)

        md.parser.blockprocessors.add('spoilers', SpoilersProcessor(md.parser), '_begin')


def makeExtension(*args, **kwargs):
    """Return extension."""

    return SpoilersExtension(*args, **kwargs)
