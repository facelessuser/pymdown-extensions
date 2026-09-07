"""
Better Emphasis.

pymdownx.betterem
Add intelligent handling of to em and strong notations

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


class BetterEmExtension(Extension):
    """Add extension to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'smart_enable': ["underscore", "Treat connected words intelligently - Default: underscore"]
        }

        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        """Modify inline patterns."""

        # Not better yet, so let's make it better
        md.registerExtension(self)
        self.make_better(md)

    def make_better(self, md):
        """
        Configure all the pattern rules.

        This should be used instead of smart_strong package.
        pymdownx.extra should be used in place of markdown.extensions.extra.
        """

        config = self.getConfigs()
        enabled = config["smart_enable"]
        enable_all = enabled == "all"
        enable_under = enabled == "underscore" or enable_all
        enable_star = enabled == "asterisk" or enable_all

        # If we don't have to move an existing extension, use the same priority,
        # but if we do have to, move it closely to the relative needed position.
        md.inlinePatterns.deregister('not_strong', False)
        md.inlinePatterns.deregister('strong_em', False)
        md.inlinePatterns.deregister('em_strong', False)
        md.inlinePatterns.deregister('em_strong2', False)
        md.inlinePatterns.deregister('strong', False)
        md.inlinePatterns.deregister('emphasis', False)
        md.inlinePatterns.deregister('strong2', False)
        md.inlinePatterns.deregister('emphasis2', False)

        if enable_star:
            asterisk = util.DelimeterProcessor('*','strong,em', md, smart=True)
        else:
            asterisk = util.DelimeterProcessor('*', 'strong,em', md)
        md.inlinePatterns.register(asterisk, "strong_em", 50)

        if enable_under:
            underscore = util.DelimeterProcessor('_', 'strong,em', md, smart=True)
        else:
            underscore = util.DelimeterProcessor('_', 'strong,em', md)
        md.inlinePatterns.register(underscore, "strong_em2", 40)


def makeExtension(*args, **kwargs):
    """Return extension."""

    return BetterEmExtension(*args, **kwargs)
