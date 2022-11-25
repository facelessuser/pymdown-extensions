"""Admonitions."""
import xml.etree.ElementTree as etree
from .block import Block, type_class
import re

RE_SEP = re.compile(r'[_-]+')
RE_VALID_NAME = re.compile(r'[\w-]+')


class Admonition(Block):
    """
    Admonition.

    Arguments (1 optional):
    - A title.

    Options:
    - `type` (string): Attach a single special class for styling purposes. If more are needed,
      use the built-in `attributes` options to apply as many classes as desired.

    Content:
    Detail body.
    """

    NAME = 'admonition'
    ARGUMENTS = {'optional': 1}
    OPTIONS = {
        'type': ['', type_class],
    }
    CONFIG = {
        "types": ['note', 'attention', 'caution', 'danger', 'error', 'tip', 'hint', 'warning']
    }

    @classmethod
    def on_register(cls, blocks_extension, md, config):
        """Handle registration event."""

        # Generate an admonition subclass based on the given names.
        for b in config.get('types', []):
            subclass = RE_SEP.sub('', b.title())
            blocks_extension.register(type(subclass, (Admonition,), {'OPTIONS': {}, 'NAME': b, 'CONFIG': {}}), {})

    def on_parse(self):
        """Handle on parse event."""

        if self.NAME != 'admonition':
            self.options['type'] = self.NAME
        return True

    def on_create(self, parent):
        """Create the element."""

        # Set classes
        classes = ['admonition']
        atype = self.options['type']
        if atype and atype != 'admonition':
            classes.append(atype)

        # Create the admonition
        el = etree.SubElement(parent, 'div', {'class': ' '.join(classes)})

        # Create the title
        if not self.args:
            if not atype:
                title = None
            else:
                title = atype.capitalize()
        else:
            title = self.args[0]

        if title is not None:
            ad_title = etree.SubElement(el, 'p', {'class': 'admonition-title'})
            ad_title.text = title

        return el
