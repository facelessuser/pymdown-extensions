"""
Caret.

pymdownx.caret
Really simple plugin to add support for

`<ins>test</ins>` tags as `^^test^^` and
`<sup>test</sup>` tags as `^test^`

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


class InsertSupExtension(Extension):
    """Add insert and/or superscript extension to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'smart_insert': [False, "Treat ^^connected^^words^^ intelligently - Default: True"],
            'insert': [True, "Enable insert - Default: True"],
            'superscript': [True, "Enable superscript - Default: True"],
            'no_space': [True, "Pandoc style 'no space' requirement"]
        }

        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        """Insert `<ins>test</ins>` tags as `^^test^^` and `<sup>test</sup>` tags as `^test^`."""

        config = self.getConfigs()
        insert = bool(config.get('insert', True))
        superscript = bool(config.get('superscript', True))
        smart = bool(config.get('smart_insert', True))
        no_space = bool(config.get('no_space', True))

        md.registerExtension(self)

        escape_chars = []
        if insert or superscript:
            escape_chars.append('^')
        if superscript and no_space:
            escape_chars.append(' ')
        util.escape_chars(md, escape_chars)

        caret = None
        if insert and superscript:
            caret = util.DelimiterProcessor('^', 'ins,sup', md, smart=smart, no_space=no_space)
        elif insert:
            caret = util.DelimiterProcessor('^', 'ins', md, smart=smart, no_space=no_space, double=True)
        elif superscript:
            caret = util.DelimiterProcessor('^', 'sup', md, no_space=no_space)

        self.processor = caret

        if caret is not None:
            md.inlinePatterns.register(caret, "sup_ins", 65)

    def reset(self):
        """Reset."""

        if self.processor is not None:
            self.processor.reset()


def makeExtension(*args, **kwargs):
    """Return extension."""

    return InsertSupExtension(*args, **kwargs)
