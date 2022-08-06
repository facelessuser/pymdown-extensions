"""Details."""
import xml.etree.ElementTree as etree
from .directive import Directive


class Details(Directive):
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

    @classmethod
    def on_validate(cls, args):
        """Validate arguments."""

        return bool(args)

    def on_create(self, parent):
        """Create the element."""

        # Create Detail element
        el = etree.SubElement(parent, 'details')

        # Is it open?
        args = {}
        if self.options.get('open', 'false').lower() == 'true':
            args['open'] = 'open'

        # Create the summary
        summary = etree.SubElement(el, 'summary')
        summary.text = self.args[0]

        # Compile and add classes
        classes = [c for c in self.options.get('class', '').split(' ') if c]
        if classes:
            el.set('class', ' '.join(classes))

        return el
