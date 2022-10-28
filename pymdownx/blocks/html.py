"""HTML."""
import xml.etree.ElementTree as etree
from .block import Block, type_string_in, type_tag
import re


class HTML(Block):
    """
    HTML.

    Arguments (1 required):
    - HTML tag name

    Options:
    - `markdown` (string): specify how content inside the element should be treated:
      - `auto`: will automatically determine how an element's content should be handled.
      - `span`: treat content as an inline element's content.
      - `block`: treat content as a block element's content.
      - `raw`: treat the content as raw content (atomic).

    Content:
    HTML element content.
    """

    NAME = 'html'
    TAG = re.compile('^[a-z][a-z0-9-]*$', re.I)

    ARGUMENTS = {'required': 1, 'parsers': [type_tag]}
    OPTIONS = {
        'markdown': ['auto', type_string_in(['auto', 'span', 'block', 'raw'])]
    }

    def __init__(self, length, tracker, md, config):
        """Initialize."""

        self.markdown = None
        super().__init__(length, tracker, md, config)

    def on_markdown(self):
        """Check if this is atomic."""

        return self.options['markdown']

    def on_create(self, parent):
        """Create the element."""

        # Create element
        return etree.SubElement(parent, self.args[0].lower())
