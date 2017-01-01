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
from markdown.postprocessors import Postprocessor
import re


RE_TAG_HTML = re.compile(
    r'''(?x)
    (?:
        (?P<comments>(\r?\n?\s*)<!--[\s\S]*?-->(\s*)(?=\r?\n)|<!--[\s\S]*?-->)|
        (?P<open><[\w\:\.\-]+)
        (?P<attr>(?:\s+[\w\-:]+(?:\s*=\s*(?:"[^"]*"|'[^']*'))?)*)
        (?P<close>\s*(?:\/?)>)
    )
    ''',
    re.DOTALL | re.UNICODE
)

TAG_BAD_ATTR = r'''(?x)
(?P<attr>
    (?:
        \s+(?:%s)
        (?:\s*=\s*(?:"[^"]*"|'[^']*'))
    )*
)
'''


def repl(m, attributes, strip_comments):
    """Replace comments and unwanted attributes."""

    if m.group('comments'):
        tag = '' if strip_comments else m.group('comments')
    else:
        tag = m.group('open')
        if attributes is not None:
            tag += attributes.sub('', m.group('attr'))
        else:
            tag += m.group('attr')
        tag += m.group('close')
    return tag


class PlainHtmlPostprocessor(Postprocessor):
    """Post processor to strip out unwanted content."""

    def run(self, text):
        """Strip out ids and classes for a simplified HTML output."""

        attr_str = self.config.get('strip_attributes', 'id class style').strip()
        attributes = [re.escape(a) for a in attr_str.split(' ')] if attr_str else []
        if self.config.get('strip_js_on_attributes', True):
            attributes.append(r'on[\w]+')
        if len(attributes):
            re_attributes = re.compile(
                TAG_BAD_ATTR % '|'.join(attributes),
                re.DOTALL | re.UNICODE
            )
        else:
            re_attributes = None
        strip_comments = self.config.get('strip_comments', True)

        return RE_TAG_HTML.sub(
            lambda m: repl(m, re_attributes, strip_comments),
            text
        )


class PlainHtmlExtension(Extension):
    """PlainHtml extension."""

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

        plainhtml = PlainHtmlPostprocessor(md)
        plainhtml.config = self.getConfigs()
        md.postprocessors.add("plain-html", plainhtml, "_end")
        md.registerExtension(self)


def makeExtension(*args, **kwargs):
    """Return extension."""

    return PlainHtmlExtension(*args, **kwargs)
