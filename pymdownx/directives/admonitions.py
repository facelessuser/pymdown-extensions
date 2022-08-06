"""Admonitions."""
import xml.etree.ElementTree as etree
from .directive import Directive


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

    @classmethod
    def on_validate(cls, args):
        """Validate arguments."""

        return bool(args)

    def on_create(self, parent):
        """Create the element."""

        # Create the admonition
        el = etree.SubElement(parent, 'div')

        # Create the title
        title = self.args[0]
        ad_title = etree.SubElement(el, 'p', {'class': 'admonition-title'})
        ad_title.text = title

        # Set classes
        classes = []
        for c in self.options.get('class', '').split(' '):
            if c:
                classes.append(c)

        classes.insert(0, 'admonition')
        el.set('class', ' '.join(classes))
        return el


class Note(Admonition):
    """Note."""

    NAME = 'note'

    @classmethod
    def on_validate(cls, args):
        """Validate arguments."""

        return True

    def config(self, args, **options):
        """Parse configuration."""

        if 'class' in options:
            options['class'] = '{} {}'.format(self.NAME, options['class'].strip())
        else:
            options['class'] = self.NAME
        super().config(args, **options)
        if not self.args:
            self.args.append(self.NAME.title())


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
