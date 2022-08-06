"""Figures."""
import xml.etree.ElementTree as etree
from .directive import Directive


class Figure(Directive):
    """
    Figure capture directive.

    Arguments (1):
    - Image path

    Options:
    - `height`: image height
    - `width`: image width
    - `alt`: alternate text for image
    - `title`: title for image
    - `class`: classes for figure (space separated)
    - `id`: Id for figure

    Content:

    Figure caption
    """

    NAME = 'figure'

    @classmethod
    def on_validate(cls, args):
        """Validate arguments."""

        return bool(args)

    def on_add(self, el):
        """Return the `figcaption`."""

        return list(el)[-1]

    def on_create(self, parent):
        """Create the element."""

        height = self.options.get('height', '').replace('"', '&quote;')
        width = self.options.get('width', '').replace('"', '&quote;')
        alt = self.options.get('alt', '').replace('"', '&quote;')
        title = self.options.get('title', '').replace('"', '&quote;')
        tag_id = self.options.get('id', '').replace('"', '&quote;')
        classes = [c for c in self.options.get('class', '').split(' ') if c]

        attributes = {"src": self.args[0].replace('"', '&quote;')}
        if height:
            attributes['height'] = height
        if width:
            attributes['width'] = width
        if alt:
            attributes['alt'] = alt
        if title:
            attributes['title'] = title

        attributes2 = {}
        if tag_id:
            attributes2['id'] = tag_id
        if classes:
            attributes2['class'] = ' '.join(classes)

        fig = etree.SubElement(parent, 'figure', attributes2)
        etree.SubElement(fig, 'img', attributes)
        etree.SubElement(fig, 'figcaption')

        return fig
