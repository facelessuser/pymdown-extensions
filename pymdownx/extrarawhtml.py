"""
ExtraRawHtml.

Split out extra raw html parsing from Python Markdown.

---
Python-Markdown Extra Extension
===============================
See <https://pythonhosted.org/Markdown/extensions/extra.html>
for documentation.
Copyright The Python Markdown Project
License: [BSD](http://www.opensource.org/licenses/bsd-license.php)
"""
from __future__ import unicode_literals
from markdown import Extension
import re
from . import util
if util.MD32:  # pragma: no cover
    from markdown.extensions import md_in_html as module
else:  # pragma: no cover
    from markdown.extensions import extra as module


class ExtraRawHtmExtension(Extension):
    """Add raw HTML extensions to Markdown class."""

    def extendMarkdown(self, md):
        """Register extension instances."""

        util.PymdownxDeprecationWarning(
            "'extrarawhtml' extension is deprecated, 'markdown.extensions.md_in_html' should be used instead"
        )

        md.registerExtension(self)
        # Turn on processing of markdown text within raw html
        md.preprocessors['html_block'].markdown_in_raw = True
        md.parser.blockprocessors.register(
            module.MarkdownInHtmlProcessor(md.parser), 'markdown_block', 105
        )
        md.parser.blockprocessors.tag_counter = -1
        md.parser.blockprocessors.contain_span_tags = re.compile(
            r'^(p|h[1-6]|li|dd|dt|td|th|legend|address)$',
            re.IGNORECASE
        )


def makeExtension(*args, **kwargs):
    """Return extension."""

    return ExtraRawHtmExtension(*args, **kwargs)
