"""Details."""
import xml.etree.ElementTree as etree
from .block import Block, type_class, type_boolean
import re

RE_SEP = re.compile(r'[_-]+')
RE_VALID_NAME = re.compile(r'[\w-]+')


class Details(Block):
    """
    Details.

    Arguments (1 optional):
    - A summary.

    Options:
    - `open` (boolean): force the details block to be in an open state opposed to collapsed.
    - `type` (string): Attach a single special class for styling purposes. If more are needed,
      use the built-in `attributes` options to apply as many classes as desired.

    Content:
    Detail body.
    """

    NAME = 'details'

    ARGUMENTS = {'optional': 1}
    OPTIONS = {
        'open': [False, type_boolean],
        'type': ['', type_class]
    }

    CONFIG = {
        "types": []
    }

    @classmethod
    def on_register(cls, blocks_extension, md, config):
        """Handle registration event."""

        # Generate an admonition subclass based on the given names.
        for b in config.get('types', []):
            subclass = RE_SEP.sub('', b.title())
            blocks_extension.register(
                type(subclass, (Details,), {'OPTIONS': {'open': [False, type_boolean]}, 'NAME': b, 'CONFIG': {}}), {}
            )

    def on_parse(self):
        """Handle on parse event."""

        if self.NAME != 'details':
            self.options['type'] = self.NAME
        return True

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
