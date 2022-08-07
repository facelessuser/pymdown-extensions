"""Figures."""
import xml.etree.ElementTree as etree
from .directive import Directive, to_html_attribute, to_classes, to_string


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

    ARGUMENTS = {'required': 1, 'parsers': [to_string]}
    OPTIONS = {
        'height': ['', to_html_attribute],
        'width': ['', to_html_attribute],
        'alt': ['', to_html_attribute],
        'title': ['', to_html_attribute],
        'class': [[], to_classes],
        'id': ['', to_html_attribute]
    }

    def on_init(self):
        """On initialize."""

        self.content = 0

    def on_add(self, el):
        """Return the `figcaption`."""

        self.content += 1

        if self.content == 1:
            return etree.SubElement(el, 'figcaption')

        return el

    def on_create(self, parent):
        """Create the element."""

        attributes = {"src": self.args[0].replace('"', '&quote;')}
        if self.options['height']:
            attributes['height'] = self.options['height']
        if self.options['width']:
            attributes['width'] = self.options['width']
        if self.options['alt']:
            attributes['alt'] = self.options['alt']
        if self.options['title']:
            attributes['title'] = self.options['title']
        classes = self.options['class']
        tag_id = self.options['id']

        attributes2 = {}
        if tag_id:
            attributes2['id'] = tag_id
        if classes:
            attributes2['class'] = ' '.join(classes)

        fig = etree.SubElement(parent, 'figure', attributes2)
        etree.SubElement(fig, 'img', attributes)

        return fig
