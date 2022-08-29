"""Figures."""
import xml.etree.ElementTree as etree
from .block import Block, type_boolean


class Figure(Block):
    """
    Figure capture Block.

    Work in progress.
    """

    NAME = 'figure'

    ARGUMENTS = {'optional': 1}
    OPTIONS = {'caption-top': [False, type_boolean]}

    def on_end(self, el):
        """Return the last child of an `etree` element."""

        caption = etree.Element('figcaption')

        # Parse the caption
        if self.args[0]:
            self.md.parser.parseChunk(caption, self.args[0])

        # Anything after the first block will be considered a caption
        text = el.text
        count = 0 if not text or not text.strip() else 1
        for child in list(el):
            count += 1

            # Do we have content at tail?
            # If so, count as a block
            if count == 1:
                tail = child.tail
                if not tail or not tail.strip():
                    continue

            if count == 1:
                print('here?')
                caption.text = child.tail
                child.tail = None
            else:
                el.remove(child)
                caption.append(child)

        if caption.text or len(caption):
            if self.options['caption-top']:
                el.insert(0, caption)
            else:
                el.append(caption)

    def on_create(self, parent):
        """Create the element."""

        return etree.SubElement(parent, 'figure')
