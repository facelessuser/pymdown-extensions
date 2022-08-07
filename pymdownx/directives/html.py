"""HTML."""
import xml.etree.ElementTree as etree
from .directive import Directive, to_ternary, to_html_attribute, to_tag
import re

RE_NAME = re.compile(
    r'[^A-Z_a-z\u00c0-\u00d6\u00d8-\u00f6\u00f8-\u02ff'
    r'\u0370-\u037d\u037f-\u1fff\u200c-\u200d'
    r'\u2070-\u218f\u2c00-\u2fef\u3001-\ud7ff'
    r'\uf900-\ufdcf\ufdf0-\ufffd'
    r'\:\-\.0-9\u00b7\u0300-\u036f\u203f-\u2040]+'
)


class HTML(Directive):
    """
    HTML.

    Arguments (2):
    - HTML tag name

    Options:
    - Any attribute name as key and attribute value as the value

    Special:
    - `markdown` attribute will determine if the element is treated as atomic (False),
      forced Markdown (True), or automatically based on tag type (unset or any other value).

    Content:
    HTML tag body
    """

    ARG_DELIM = ' '
    NAME = 'html'
    TAG = re.compile('^[a-z][a-z0-9-]*$', re.I)

    ARGUMENTS = {'required': 1, 'parsers': [to_tag]}
    OPTIONS = {
        'markdown': [None, to_ternary],
        '': ['', to_html_attribute]
    }

    def __init__(self, length, tracker, md):
        """Initialize."""

        self.markdown = None
        super().__init__(length, tracker, md)

    def is_atomic(self):
        """Check if this is atomic."""

        markdown = self.options['markdown']
        return self.atomic if markdown is None else not markdown

    def on_create(self, parent):
        """Create the element."""

        attributes = {}

        for k, v in self.options.items():
            if k == 'markdown':
                continue

            # Sanitize attribute names
            name = RE_NAME.sub('_', k)
            # Quote values
            attributes[name] = v

        # Create element
        return etree.SubElement(parent, self.args[0].lower(), attributes)
