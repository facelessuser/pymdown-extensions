"""
pymdownx.plainhtml
An extension for Python Markdown.
Strip classes, styles, and ids from html

MIT license.

Copyright (c) 2014 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from __future__ import unicode_literals
from markdown import Extension
from markdown.postprocessors import Postprocessor
import re


# Strip out id, class, on<word>, and style attributes for a simple html output
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

RE_TAG_BAD_ATTR = re.compile(
    r'''(?x)
    (?P<attr>
        (?:
            \s+(?:id|class|style|on[\w]+)
            (?:\s*=\s*(?:"[^"]*"|'[^']*'))
        )*
    )
    ''',
    re.DOTALL | re.UNICODE
)


def repl(m):
    if m.group('comments'):
        tag = ''
    else:
        tag = m.group('open')
        tag += RE_TAG_BAD_ATTR.sub('', m.group('attr'))
        tag += m.group('close')
    return tag


class PlainHtmlPostprocessor(Postprocessor):
    def run(self, text):
        """ Strip out ids and classes for a simplified HTML output """

        return RE_TAG_HTML.sub(repl, text)


class PlainHtmlExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        """ Strip unwanted attributes to give a plain HTML """

        plainhtml = PlainHtmlPostprocessor(md)
        md.postprocessors.add("plain-html", plainhtml, "_end")
        md.registerExtension(self)


def makeExtension(*args, **kwargs):
    return PlainHtmlExtension(*args, **kwargs)
