"""Details."""
import xml.etree.ElementTree as etree
from .block import Block, type_class, type_boolean


class Details(Block):
    """
    Details.

    Arguments (1):
    - summary

    Options:
    - class: space delimited list of classes
    - type: A type class to use.

    Content:

    Content to hide with the details.
    """

    NAME = 'details'

    ARGUMENTS = {'optional': 1}
    OPTIONS = {
        'open': [False, type_boolean],
        'type': ['', type_class]
    }

    def on_create(self, parent):
        """Create the element."""

        # Is it open?
        attributes = {}
        if self.options['open']:
            attributes['open'] = 'open'

        # Set classes
        dtype = self.options['type']
        if dtype:
            attributes['class'] = dtype

        # Create Detail element
        el = etree.SubElement(parent, 'details', attributes)

        # Create the summary
        if not self.args:
            if not dtype:
                summary = None
            else:
                summary = dtype.capitalize()
        else:
            summary = self.args[0]

        # Create the summary
        if summary is not None:
            s = etree.SubElement(el, 'summary')
            s.text = summary

        return el
