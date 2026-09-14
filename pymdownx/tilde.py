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
from .delimiterprocessor import DelimiterProcessor
from typing import cast


class DeleteSubExtension(Extension):
    """Add delete and/or subscript extension to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'smart_delete': [False, "Treat ~~connected~~words~~ intelligently - Default: False"],
            'delete': [True, "Enable delete - Default: True"],
            'subscript': [True, "Enable subscript - Default: True"],
            'no_space': [True, "Pandoc style 'no space' requirement - Default: True"]
        }

        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        """Insert `<del>test</del>` tags as `~~test~~` and `<sub>test</sub>` tags as `~test~`."""

        config = self.getConfigs()
        delete = bool(config.get('delete', True))
        subscript = bool(config.get('subscript', True))
        smart = bool(config.get('smart_delete', True))
        no_space = bool(config.get('no_space', True))

        md.registerExtension(self)

        escape_chars = []
        if delete or subscript:
            escape_chars.append('~')
        if subscript and no_space:
            escape_chars.append(' ')
        util.escape_chars(md, escape_chars)

        if not delete and not subscript:  # pragma: no cover
            self.processor: DelimiterProcessor | None = None
            return

        add = False
        if (
            'delimiter' not in md.inlinePatterns or
            not isinstance(md.inlinePatterns['delimiter'], DelimiterProcessor)
        ):
            add = True
            self.processor = DelimiterProcessor(md)
        else:
            self.processor = cast('DelimiterProcessor', md.inlinePatterns['delimiter'])

        if delete and subscript:
            self.processor.register(r'~', 'del,sub', smart=smart, no_space=no_space)
        elif delete:
            self.processor.register(r'~', 'del', smart=smart, no_space=no_space, double=True)
        else:
            self.processor.register(r'~', 'sub', no_space=no_space)

        if add:
            md.inlinePatterns.register(self.processor, "delimiter", 50)

    def reset(self):
        """Reset."""

        if self.processor is not None:
            self.processor.reset()


def makeExtension(*args, **kwargs):
    """Return extension."""

    return DeleteSubExtension(*args, **kwargs)
