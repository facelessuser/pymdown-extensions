"""
Tabbed.

pymdownx.tabbed

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
from markdown import Extension
from markdown import util as md_util
from markdown.blockprocessors import BlockProcessor
import xml.etree.ElementTree as etree
import re


class TabbedProcessor(BlockProcessor):
    """Tabbed block processor."""

    START = re.compile(
        r'(?:^|\n)={3}(!)? +"(.*?)" *(?:\n|$)'
    )
    COMPRESS_SPACES = re.compile(r' {2,}')

    def __init__(self, *args):
        """Initialize."""

        super().__init__(*args)
        self.tab_group_count = 0

    def test(self, parent, block):
        """Test block."""

        sibling = self.lastChild(parent)
        return (
            self.START.search(block) or
            (
                block.startswith(' ' * self.tab_length) and sibling is not None and
                sibling.tag.lower() == 'div' and sibling.attrib.get('class', '') == 'tabbed-set'
            )
        )

    def run(self, parent, blocks):
        """Convert to tabbed block."""

        sibling = self.lastChild(parent)
        block = blocks.pop(0)

        m = self.START.search(block)
        if m:
            # remove the first line
            block = block[m.end():]

        # Get the tabs block and the non-tab content
        block, non_tabs = self.detab(block)

        if m:
            special = m.group(1) if m.group(1) else ''
            title = m.group(2) if m.group(2) else m.group(3)

            if (
                sibling and sibling.tag.lower() == 'div' and
                sibling.attrib.get('class', '') == 'tabbed-set' and
                special != '!'
            ):
                first = False
                sfences = sibling
            else:
                first = True
                self.tab_group_count += 1
                sfences = etree.SubElement(
                    parent,
                    'div',
                    {'class': 'tabbed-set', 'data-tabs': '%d:0' % self.tab_group_count}
                )

            data = sfences.attrib['data-tabs'].split(':')
            tab_set = int(data[0])
            tab_count = int(data[1]) + 1

            attributes = {
                "name": "__tabbed_%d" % tab_set,
                "type": "radio",
                "id": "__tabbed_%d_%d" % (tab_set, tab_count)
            }

            if first:
                attributes['checked'] = 'checked'

            etree.SubElement(
                sfences,
                'input',
                attributes
            )
            lab = etree.SubElement(
                sfences,
                "label",
                {
                    "for": "__tabbed_%d_%d" % (tab_set, tab_count)
                }
            )
            lab.text = md_util.AtomicString(title)

            div = etree.SubElement(
                sfences,
                "div",
                {
                    "class": "tabbed-content"
                }
            )
            sfences.attrib['data-tabs'] = '%d:%d' % (tab_set, tab_count)
        else:
            div = self.lastChild(sibling)

        self.parser.parseChunk(div, block)

        if non_tabs:
            # Insert the non-details content back into blocks
            blocks.insert(0, non_tabs)


class TabbedExtension(Extension):
    """Add Tabbed extension."""

    def extendMarkdown(self, md):
        """Add Tabbed to Markdown instance."""
        md.registerExtension(self)

        self.tab_processor = TabbedProcessor(md.parser)
        md.parser.blockprocessors.register(self.tab_processor, "tabbed", 105)

    def reset(self):
        """Reset."""

        self.tab_processor.tab_group_count = 0


def makeExtension(*args, **kwargs):
    """Return extension."""

    return TabbedExtension(*args, **kwargs)
