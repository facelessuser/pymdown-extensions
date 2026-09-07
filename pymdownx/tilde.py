"""
Tilde.

pymdownx.tilde
Really simple plugin to add support for
`<del>test</del>` tags as `~~test~~` and
`<sub>test</sub>` tags as `~test~`

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
from markdown import Extension
from . import util


class DeleteSubExtension(Extension):
    """Add delete and/or subscript extension to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'smart_delete': [True, "Treat ~~connected~~words~~ intelligently - Default: True"],
            'delete': [True, "Enable delete - Default: True"],
            'subscript': [True, "Enable subscript - Default: True"]
        }

        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        """Insert `<del>test</del>` tags as `~~test~~` and `<sub>test</sub>` tags as `~test~`."""

        config = self.getConfigs()
        delete = bool(config.get('delete', True))
        subscript = bool(config.get('subscript', True))
        smart = bool(config.get('smart_delete', True))

        md.registerExtension(self)

        escape_chars = []
        if delete or subscript:
            escape_chars.append('~')
        if subscript:
            escape_chars.append(' ')
        util.escape_chars(md, escape_chars)

        tilde = None
        if delete and subscript:
            if smart:
                tilde = util.DelimiterProcessor(r'~', 'del,sub', md, smart=True, no_space=True)
            else:
                tilde = util.DelimiterProcessor(r'~', 'del,sub', md, no_space=True)
        elif delete:
            if smart:
                tilde = util.DelimiterProcessor(r'~', 'del', md, smart=True, no_space=True, double=True)
            else:
                tilde = util.DelimiterProcessor(r'~', 'del', md, no_space=True, double=True)
        elif subscript:
            tilde = util.DelimiterProcessor(r'~', 'sub', md, no_space=True)

        if tilde is not None:
            md.inlinePatterns.register(tilde, "sub_del", 65)


def makeExtension(*args, **kwargs):
    """Return extension."""

    return DeleteSubExtension(*args, **kwargs)
