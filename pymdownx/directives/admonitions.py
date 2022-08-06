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

    def on_create(self, parent):
        """Create the element."""

        # Create the admonition
        el = etree.SubElement(parent, 'div')

        # Create the title
        t = self.options.get('type', '').lower()
        title = self.args[0] if self.args and self.args[0] else t.title()
        if not title:
            title = 'Attention'
        ad_title = etree.SubElement(el, 'p', {'class': 'admonition-title'})
        ad_title.text = title

        # Set classes
        classes = []
        for c in self.options.get('class', '').split(' '):
            c = c.strip()
            if c:
                classes.append(c)
        if t != 'admonition':
            classes.insert(0, t)
        classes.insert(0, 'admonition')
        el.set('class', ' '.join(classes))
        return el


class Note(Admonition):
    """Note."""

    NAME = 'note'

    def config(self, args, **options):
        """Parse configuration."""

        super().config(args, **options)
        self.options['type'] = 'note'


class Attention(Admonition):
    """Attention."""

    NAME = 'attention'

    def config(self, args, **options):
        """Parse configuration."""

        super().config(args, **options)
        self.options['type'] = 'attention'


class Caution(Admonition):
    """Caution."""

    NAME = 'caution'

    def config(self, args, **options):
        """Parse configuration."""

        super().config(args, **options)
        self.options['type'] = 'caution'


class Danger(Admonition):
    """Danger."""

    NAME = 'danger'

    def config(self, args, **options):
        """Parse configuration."""

        super().config(args, **options)
        self.options['type'] = 'danger'


class Error(Admonition):
    """Error."""

    NAME = 'error'

    def config(self, args, **options):
        """Parse configuration."""

        super().config(args, **options)
        self.options['type'] = 'error'


class Tip(Admonition):
    """Tip."""

    NAME = 'tip'

    def config(self, args, **options):
        """Parse configuration."""

        super().config(args, **options)
        self.options['type'] = 'tip'


class Hint(Admonition):
    """Hint."""

    NAME = 'hint'

    def config(self, args, **options):
        """Parse configuration."""

        super().config(args, **options)
        self.options['type'] = 'hint'


class Important(Admonition):
    """Important."""

    NAME = 'danger'

    def config(self, args, **options):
        """Parse configuration."""

        super().config(args, **options)
        self.options['type'] = 'danger'


class Warn(Admonition):
    """Warning."""

    NAME = 'warning'

    def config(self, args, **options):
        """Parse configuration."""

        super().config(args, **options)
        self.options['type'] = 'warning'
