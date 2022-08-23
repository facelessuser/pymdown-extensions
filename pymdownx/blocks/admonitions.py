"""Admonitions."""
import xml.etree.ElementTree as etree
from .block import Block, type_class


class Admonition(Block):
    """
    Admonitions.

    Arguments (1):
    - Title

    Options:
    - class: space delimited list of classes
    - id: An ID

    Content:

    Content within the admonitions.
    """

    NAME = 'admonition'
    ARGUMENTS = {'optional': 1}
    OPTIONS = {
        'type': ['', type_class],
    }

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


class Note(Admonition):
    """Note."""

    NAME = 'note'
    OPTIONS = {}

    def on_parse(self):
        """Handle on parse event."""

        self.options['type'] = self.NAME
        return True


class Attention(Note):
    """Attention."""

    NAME = 'attention'


class Caution(Note):
    """Caution."""

    NAME = 'caution'


class Danger(Note):
    """Danger."""

    NAME = 'danger'


class Error(Note):
    """Error."""

    NAME = 'error'


class Tip(Note):
    """Tip."""

    NAME = 'tip'


class Hint(Note):
    """Hint."""

    NAME = 'hint'


class Important(Note):
    """Important."""

    NAME = 'danger'


class Warn(Note):
    """Warning."""

    NAME = 'warning'
