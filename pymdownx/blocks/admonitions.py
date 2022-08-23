"""Admonitions."""
import xml.etree.ElementTree as etree
from .block import Block, type_string, type_class


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
    ARGUMENTS = {'required': 1, 'parsers': [type_string]}
    OPTIONS = {
        'type': ['', type_class],
    }

    def on_create(self, parent):
        """Create the element."""

        # Create the admonition
        el = etree.SubElement(parent, 'div')

        # Create the title
        title = self.args[0]
        ad_title = etree.SubElement(el, 'p', {'class': 'admonition-title'})
        ad_title.text = title

        # Set classes
        classes = ['admonition']
        if self.options['type']:
            classes.append(self.options['type'])

        el.set('class', ' '.join(classes))
        return el


class Note(Admonition):
    """Note."""

    NAME = 'note'
    ARGUMENTS = {'optional': 1, 'parsers': [type_string]}
    OPTIONS = {}

    def on_parse(self):
        """Handle on parse event."""

        self.options['type'] = self.NAME
        if not self.args:
            self.args.append(self.NAME.title())
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
