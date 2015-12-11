"""
HardBreak.

pymdownx.hardbreak

MIT license.

Copyright (c) 2015 Isaac Muse <isaacmuse@gmail.com>

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
from markdown.extensions import Extension
from markdown.inlinepatterns import SubstituteTagPattern

HARDBREAK_RE = r'%s\\\n'
LEADING_SPACE_RE = r' +'


class HardBreakExtension(Extension):
    """
    HardBreak extension.

    Inserts a hard line break if the newline is escaped.
    """

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'leading_space': [True, "Require one or more leading spaces before escaped newline - Default: True"]
        }

        super(HardBreakExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """Extend markdown object with hardbreak."""

        config = self.getConfigs()
        regex = HARDBREAK_RE % (LEADING_SPACE_RE if config.get('leading_space', True) else '')
        md.inlinePatterns.add('hardbreak', SubstituteTagPattern(regex, 'br'), '>linebreak')


def makeExtension(*args, **kwargs):
    """Return extension."""

    return HardBreakExtension(*args, **kwargs)
