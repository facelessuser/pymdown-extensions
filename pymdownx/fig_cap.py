"""
Figure and Figcaption Extension.

This extension adds figure and figcaption handling.
"""
import re
from markdown import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree


class FigcaptionBlockProcessor(BlockProcessor):
    """Figcaption block processor."""

    START = re.compile(r'(?:^|\n)%\: {1,3}(.+?) *(?:\n|$)')

    def test(self, parent, block):
        """Test block."""

        return (parent.tag == 'figure' and self.START.search(block))

    def run(self, parent, blocks):
        """Convert to figcaption block."""

        block = blocks.pop(0)
        m = self.START.search(block)
        div = etree.SubElement(parent, 'figcaption')
        div.text = m.group(1)
        block = block[m.end():]
        if block:
            div.text = div.text + '\n' + block


class FigureBlockProcessor(BlockProcessor):
    """Figure block processor."""

    COMPRESS_SPACES = re.compile(r' {2,}')
    START = re.compile(
        r'''(?:^|\n)(?P<starter>%{3})(?: +(?P<class>[\w\-]+(?: +[\w\-]+)*?))? *(?:\n|$)'''
    )

    def test(self, parent, block):
        """Test block."""

        sibling = self.lastChild(parent)
        return (self.START.search(block) or 
                (block.startswith(' ' * self.tab_length) and sibling is not None and sibling.tag == 'figure'))

    def run(self, parent, blocks):
        """Convert to figure block."""

        sibling = self.lastChild(parent)
        block = blocks.pop(0)

        m = self.START.search(block)
        if m:
            # remove the first line
            block = block[m.end():]
            if not block:
                # This is not a figure. Most likely a paragraph that
                # starts with the figure starter at the beginning
                # of a document or list.
                blocks.insert(0, m.group('starter'))
                return False

        # Get the figure block and and the non-figure content
        block, non_figure = self.detab(block)

        if m:
            div = etree.SubElement(parent, 'figure')
            div_class = '' if m.group(
                'class') is None else self.COMPRESS_SPACES.sub(
                    ' ',
                    m.group('class').lower())
            if div_class:
                div.set('class', div_class)
        else:
            div = sibling

        self.parser.parseChunk(div, block)

        if non_figure:
            # Insert the non-figure content back into blocks
            blocks.insert(0, non_figure)


class FigCapTreeprocessor(Treeprocessor):
    """Get rid of the <p> tag if <img> is the only thing in the <p>."""

    def run(self, root):
        """Operate the <p> that only has a <img> in it and without any text."""
        for figure in root.iterfind('figure'):
            for p in figure.iterfind('p'):
                if len(p) == 1:
                    img = p.find('img')
                    if img is not None and p.text is None and img.tail == '':
                        p.attrib = img.attrib
                        p.tag = img.tag
                        p.remove(img)


class FigCapExtension(Extension):
    """Add FigCap extension."""

    def extendMarkdown(self, md):
        """Add FigCap to Markdown instance."""

        md.registerExtension(self)
        md.parser.blockprocessors.register(
            FigcaptionBlockProcessor(md.parser), 'figcaption', 95.1)
        md.parser.blockprocessors.register(
            FigureBlockProcessor(md.parser), 'figure', 95)
        # the priority here should lower than the attr_list extension
        md.treeprocessors.register(FigCapTreeprocessor(md), 'fig_cap', 7)


def makeExtension(*args, **kwargs):
    """Return extension."""

    return FigCapExtension(*args, **kwargs)
