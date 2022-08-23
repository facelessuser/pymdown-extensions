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
    - id: An ID

    Content:

    Content to hide with the details.
    """

    NAME = 'details'

    ARGUMENTS = {'required': 1}
    OPTIONS = {
        'open': [[], type_boolean],
        'type': ['', type_class]
    }

    def on_create(self, parent):
        """Create the element."""

        # Is it open?
        attributes = {}
        if self.options['open']:
            attributes['open'] = 'open'

        # Set classes
        if self.options['type']:
            attributes['class'] = self.options['type']

        # Create Detail element
        el = etree.SubElement(parent, 'details', attributes)

        # Create the summary
        summary = etree.SubElement(el, 'summary')
        summary.text = self.args[0]

        return el
