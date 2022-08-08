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
        'id': ['', to_html_attribute],
        'figheight': ['', to_html_attribute],
        'figwidth': ['', to_html_attribute],
        'figclass': [[], to_classes],
        'target': ['', to_html_attribute],
        'align': ['', to_html_attribute]
    }

    def on_init(self):
        """On initialize."""

        self.content = 0

    def last_child(self, parent):
        """Return the last child of an `etree` element."""

        if len(parent):
            return parent[-1]
        else:
            return None

    def on_add(self, el):
        """Return the `figcaption`."""

        self.content += 1

        # Caption
        if self.content == 1:
            caption = etree.SubElement(el, 'figcaption')
            return etree.SubElement(caption, 'span', {'class': 'caption-text'})

        # Legend
        elif self.content == 2:
            return etree.SubElement(self.last_child(el), 'div', {'class': 'legend'})
        return self.last_child(self.last_child(el))

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
        if self.options['target']:
            attributes['target'] = self.options['target']
        if self.options['align']:
            attributes['align'] = self.options['align']

        classes = self.options['class']
        if classes:
            attributes['class'] = ' '.join(classes)

        attributes2 = {}
        if self.options['id']:
            attributes2['id'] = self.options['id']
        if self.options['figwidth']:
            attributes2['figwidth'] = self.options['figwidth']
        figclasses = self.options['figclass']
        if figclasses:
            attributes2['class'] = ' '.join(figclasses)

        fig = etree.SubElement(parent, 'figure', attributes2)
        etree.SubElement(fig, 'img', attributes)

        return fig
