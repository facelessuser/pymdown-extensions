"""
Spoilers.
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from markdown import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
import re


class SpoilersProcessor(BlockProcessor):

    CLASS = 'spoilers'
    START = re.compile(r'(?:^|\n)\?\?\?(?:\( *(open|close) *\))? ?([\w\-]+)?(?: +"(.*?)") *(?:\n|$)')

    def test(self, parent, block):
        sibling = self.lastChild(parent)
        return (
            self.START.search(block) or 
            (
                block.startswith(' ' * self.tab_length) and sibling is not None and
                sibling.get('class', '').find(self.CLASS) != -1
            )
        )

    def run(self, parent, blocks):
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
            is_open = state is not None and state == 'open'
            class_name = m.group(2).lower()
            class_name = '' if class_name is None else class_name + " "
            title = m.group(3)
            if title.strip() == '':
                title = "Spoiler"

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
    return SpoilersExtension(*args, **kwargs)
