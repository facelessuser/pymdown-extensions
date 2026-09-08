"""
Mark.

pymdownx.mark
Really simple plugin to add support for
<mark>test</mark> tags as ==test==

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


class MarkExtension(Extension):
    """Add the mark extension to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'smart_mark': [True, "Treat ==connected==words== intelligently - Default: True"]
        }

        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        """Insert `<mark>test</mark>` tags as `==test==`."""

        config = self.getConfigs()
        smart = bool(config.get('smart_mark', True))

        md.registerExtension(self)

        escape_chars = []
        escape_chars.append('=')
        util.escape_chars(md, escape_chars)

        if smart:
            mark = util.DelimiterProcessor('=', 'mark', md, smart=True, double=True)
        else:
            mark = util.DelimiterProcessor('=', 'mark', md, double=True)

        self.processor = mark
        md.inlinePatterns.register(mark, "mark", 65)

    def reset(self):
        """Reset."""

        self.processor.reset()


def makeExtension(*args, **kwargs):
    """Return extension."""

    return MarkExtension(*args, **kwargs)
