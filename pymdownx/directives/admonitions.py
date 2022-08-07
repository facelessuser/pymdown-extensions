"""Admonitions."""
import xml.etree.ElementTree as etree
from .directive import Directive, to_string, to_classes, to_html_attribute


class Admonition(Directive):
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
    ARGUMENTS = {'required': 1, 'parsers': [to_string]}
    OPTIONS = {
        'class': [[], to_classes],
        'id': ['', to_html_attribute]
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
        classes = self.options['class']
        classes.insert(0, 'admonition')

        el.set('class', ' '.join(classes))
        return el


class Note(Admonition):
    """Note."""

    NAME = 'note'
    ARGUMENTS = {'optional': 1, 'parsers': [to_string]}

    def on_parse(self):
        """Handle on parse event."""

        if self.NAME not in self.options['class']:
            self.options['class'].insert(0, self.NAME)
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
