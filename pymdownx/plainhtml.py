"""
Plain HTML.

pymdownx.plainhtml
An extension for Python Markdown.
Strip classes, styles, and ids from html

MIT license.

Copyright (c) 2014 - 2017 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
from __future__ import unicode_literals
from markdown import Extension
from . import striphtml
from .util import PymdownxDeprecationWarning
import warnings


class PlainHtmlExtension(Extension):
    """Plain HTML extension."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'strip_comments': [
                True,
                "Strip HTML comments at the end of processing. "
                "- Default: True"
            ],
            'strip_attributes': [
                'id class style',
                "A string of attributes separated by spaces."
                "- Default: 'id class style']"
            ],
            'strip_js_on_attributes': [
                True,
                "Strip JavaScript script attribues with the pattern on*. "
                " - Default: True"
            ]
        }
        super(PlainHtmlExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """Strip unwanted attributes to give a plain HTML."""

        warnings.warn(
            "'PlainHTML' has been renamed to 'StripHTML' (pymdownx.striphtml).\n"
            "The usage of pymdownx.plainhtml is deprecated and will be removed\n"
            "in the future.  It is advised to switch over to StripHTML, but please\n"
            "read the documentation as some of the option formats and defaults are\n"
            "are different in the new StripHTML extension.",
            PymdownxDeprecationWarning
        )

        config = self.getConfigs()
        plainhtml = striphtml.StripHtmlPostprocessor(
            config.get('strip_comments'),
            config.get('strip_js_on_attributes'),
            config.get('strip_attributes').split(),
            md
        )
        md.postprocessors.add("plain-html", plainhtml, "_end")
        md.registerExtension(self)


def makeExtension(*args, **kwargs):
    """Return extension."""

    return PlainHtmlExtension(*args, **kwargs)
