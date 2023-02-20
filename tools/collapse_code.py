"""Collapsible code."""
import xml.etree.ElementTree as etree
from markdown import util as mutil
import re
from pymdownx.blocks.block import Block  # noqa: E402

# Fenced block placeholder for SuperFences
FENCED_BLOCK_RE = re.compile(
    r'^([\> ]*){}({}){}$'.format(
        mutil.HTML_PLACEHOLDER[0],
        mutil.HTML_PLACEHOLDER[1:-1] % r'([0-9]+)',
        mutil.HTML_PLACEHOLDER[-1]
    )
)


class CollapseCode(Block):
    """Collapse code."""

    NAME = 'collapse-code'
    CONFIG = {
        'expand_text': 'Expand',
        'collapse_text': 'Collapse',
        'expand_title': 'expand',
        'collapse_title': 'collapse'
    }

    def on_init(self):
        """Handle initialization."""

        # Track tab group count across the entire page.
        if 'collapse_code_count' not in self.tracker:
            self.tracker['collapse_code_count'] = 0

        self.expand = self.config['expand_text']
        if not isinstance(self.expand, str):
            raise ValueError("'expand_text' must be a string")

        self.collapse = self.config['collapse_text']
        if not isinstance(self.collapse, str):
            raise ValueError("'collapse_text' must be a string")

        self.expand_title = self.config['expand_title']
        if not isinstance(self.expand_title, str):
            raise ValueError("'expand_title' must be a string")

        self.collapse_title = self.config['collapse_text']
        if not isinstance(self.collapse_title, str):
            raise ValueError("'collapse_title' must be a string")

    def on_create(self, parent):
        """Create the element."""

        self.count = self.tracker['collapse_code_count']
        self.tracker['collapse_code_count'] += 1
        el = etree.SubElement(parent, 'div', {'class': 'collapse-code'})
        etree.SubElement(
            el,
            'input',
            {
                "type": "checkbox",
                "id": "__collapse{}".format(self.count),
                "name": "__collapse{}".format(self.count),
                'checked': 'checked'
            }
        )
        return el

    def on_end(self, block):
        """Convert non list items to details."""

        el = etree.SubElement(block, 'div', {'class': 'code-footer'})
        expand = etree.SubElement(
            el,
            'label',
            {'for': '__collapse{}'.format(self.count), 'class': 'expand', 'title': self.expand_title}
        )
        expand.text = self.expand
        collapse = etree.SubElement(
            el,
            'label',
            {'for': '__collapse{}'.format(self.count), 'class': 'collapse', 'title': self.collapse_title}
        )
        collapse.text = self.collapse
