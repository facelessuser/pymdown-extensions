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
from __future__ import absolute_import
from __future__ import unicode_literals
from markdown import Extension
from markdown.inlinepatterns import InlineProcessor
from markdown.inlinepatterns import util as md_util
from . import util
import re

SMART_UNDER_CONTENT = r'((?:[^_]|_(?=\w|\s)|(?<=\s)_+?(?=\s))+?_*?)'
SMART_STAR_CONTENT = r'((?:[^\*]|\*(?=[^\W_]|\*|\s)|(?<=\s)\*+?(?=\s))+?\**?)'
SMART_UNDER_MIXED_CONTENT = r'((?:[^_]|_(?=\w)|(?<=\s)_+?(?=\s))+?_*)'
SMART_STAR_MIXED_CONTENT = r'((?:[^\*]|\*(?=[^\W_]|\*)|(?<=\s)\*+?(?=\s))+?\**)'
UNDER_CONTENT = r'(_|(?:(?<=\s)_|[^_])+?)'
UNDER_CONTENT2 = r'((?:[^_]|(?<!_)_(?=\w))+?)'
STAR_CONTENT = r'(\*|(?:(?<=\s)\*|[^\*])+?)'
STAR_CONTENT2 = r'((?:[^\*]|(?<!\*)\*(?=[^\W_]|\*))+?)'


class BetterEmPattern(InlineProcessor):
    """Handle strong and emphasis for `*` patterns."""

    # ***strong,em***
    STRONG_EM = re.compile(
        r'(\*{3})(?!\s)(\*{1,2}|[^\*]+?)(?<!\s)\1', re.DOTALL | re.UNICODE
    )
    # ***strong,em*strong**
    STRONG_EM2 = re.compile(
        r'(\*{3})(?![\s\*])%s(?<!\s)\*%s(?<!\s)\*{2}' % (STAR_CONTENT, STAR_CONTENT2), re.DOTALL | re.UNICODE
    )
    # ***em,strong**em*
    EM_STRONG = re.compile(
        r'(\*{3})(?![\s\*])%s(?<!\s)\*{2}%s(?<!\s)\*' % (STAR_CONTENT2, STAR_CONTENT), re.DOTALL | re.UNICODE
    )
    # **em*em,strong***
    STRONG_EM3 = re.compile(
        r'(\*{2})(?![\s\*])%s\*(?![\s\*])%s(?<!\s)\*{3}' % (STAR_CONTENT2, STAR_CONTENT), re.DOTALL | re.UNICODE
    )
    # **strong**
    STRONG = re.compile(
        r'(\*{2})(?!\s)%s(?<!\s)\1' % STAR_CONTENT2, re.DOTALL | re.UNICODE
    )
    # *emphasis*
    EM = re.compile(
        r'(\*)(?!\s)%s(?<!\s)\1' % STAR_CONTENT, re.DOTALL | re.UNICODE
    )

    # Smart rules for when "smart asterisk" is enabled
    # SMART: ***strong,em***
    SMART_STRONG_EM = re.compile(
        r'(?:(?<=_)|(?<![\w\*]))(\*{3})(?![\s\*])%s(?<!\s)\1(?:(?=_)|(?![\w\*]))' % SMART_STAR_CONTENT,
        re.DOTALL | re.UNICODE
    )
    # ***strong,em* strong**
    SMART_STRONG_EM2 = re.compile(
        r'(?:(?<=_)|(?<![\w\*]))(\*{3})(?![\s\*])%s(?<!\s)\*(?:(?=_)|(?![\w\*]))%s(?<!\s)\*{2}(?:(?=_)|(?![\w\*]))' % (
            SMART_STAR_MIXED_CONTENT, SMART_STAR_CONTENT
        ),
        re.DOTALL | re.UNICODE
    )
    # **em*em,strong***
    SMART_STRONG_EM3 = re.compile(
        r'''(?x)
        (?:(?<=_)|(?<![\w\*]))(\*{2})(?![\s\*])%s(?:(?<=_)|(?<![\w\*]))\*(?![\s\*])%s(?<!\s)\*{3}(?:(?=_)|(?![\w\*]))
        ''' % (SMART_STAR_CONTENT, SMART_STAR_CONTENT),
        re.DOTALL | re.UNICODE
    )
    # ***em,strong** em*
    SMART_EM_STRONG = re.compile(
        r'(?:(?<=_)|(?<![\w\*]))(\*{3})(?![\s\*])%s(?<!\s)\*{2}(?:(?=_)|(?![\w\*]))%s(?<!\s)\*(?:(?=_)|(?![\w\*]))' % (
            SMART_STAR_MIXED_CONTENT, SMART_STAR_CONTENT
        ),
        re.DOTALL | re.UNICODE
    )
    # **strong**
    SMART_STRONG = re.compile(
        r'(?:(?<=_)|(?<![\w\*]))(\*{2})(?![\s\*])%s(?<!\s)\1(?:(?=_)|(?![\w\*]))' % SMART_STAR_CONTENT,
        re.DOTALL | re.UNICODE
    )
    # SMART *em*
    SMART_EM = re.compile(
        r'(?:(?<=_)|(?<![\w\*]))(\*)(?![\s\*])%s(?<!\s)\1(?:(?=_)|(?![\w\*]))' % SMART_STAR_CONTENT,
        re.DOTALL | re.UNICODE
    )

    def __init__(self, pattern, smart=False, md=None):
        """Initialize."""

        self.smart = smart
        super(BetterEmPattern, self).__init__(pattern, md)

        self.setup_pattern_list()

    def setup_pattern_list(self):
        """Setup pattern list."""

        self.patterns = util.odict()
        if self.smart:
            self.patterns[self.SMART_STRONG_EM] = (self.double_pattern, 'strong,em')
            self.patterns[self.SMART_EM_STRONG] = (self.double_pattern, 'em,strong')
            self.patterns[self.SMART_STRONG_EM2] = (self.double_pattern, 'strong,em')
            self.patterns[self.SMART_STRONG_EM3] = (self.double_pattern2, 'strong,em')
            self.patterns[self.SMART_STRONG] = (self.simple_pattern, 'strong')
            self.patterns[self.SMART_EM] = (self.simple_pattern, 'em')
        else:
            self.patterns[self.STRONG_EM] = (self.double_pattern, 'strong,em')
            self.patterns[self.EM_STRONG] = (self.double_pattern, 'em,strong')
            self.patterns[self.STRONG_EM2] = (self.double_pattern, 'strong,em')
            self.patterns[self.STRONG_EM3] = (self.double_pattern2, 'strong,em')
            self.patterns[self.STRONG] = (self.simple_pattern, 'strong')
            self.patterns[self.EM] = (self.simple_pattern, 'em')

    def handleMatch(self, m, data):
        """Handle emphasis match."""

        for pattern, value in self.patterns.items():
            m1 = pattern.match(data, m.start(0))
            if m1 is not None:
                return value[0](m1, value[1])
        return None, None, None

    def simple_pattern(self, m, tag):
        """Simple pattern."""

        el = md_util.etree.Element(tag)
        el.text = m.group(2)
        return el, m.start(0), m.end(0)

    def double_pattern(self, m, tags):
        """Double pattern."""

        tag1, tag2 = tags.split(",")
        el1 = md_util.etree.Element(tag1)
        el2 = md_util.etree.SubElement(el1, tag2)
        el2.text = m.group(2)
        if len(m.groups()) == 3:
            el2.tail = m.group(3)
        return el1, m.start(0), m.end(0)

    def double_pattern2(self, m, tags):
        """Double pattern 2."""

        tag1, tag2 = tags.split(",")
        el1 = md_util.etree.Element(tag1)
        el2 = md_util.etree.SubElement(el1, tag2)
        el1.text = m.group(2)
        el2.text = m.group(3)
        return el1, m.start(0), m.end(0)


class BetterEmUnderPattern(BetterEmPattern):
    """Handle strong and emphasis for `_` patterns."""

    # ___strong,em___
    STRONG_EM = re.compile(
        r'(_{3})(?!\s)(_{1,2}|[^_]+?)(?<!\s)\1',
        re.DOTALL | re.UNICODE
    )
    # ___strong,em_strong__
    STRONG_EM2 = re.compile(
        r'(_{3})(?![\s_])%s(?<!\s)_%s(?<!\s)_{2}' % (UNDER_CONTENT, UNDER_CONTENT2),
        re.DOTALL | re.UNICODE
    )
    # ___em,strong__em_
    EM_STRONG = re.compile(
        r'(_{3})(?![\s_])%s(?<!\s)_{2}%s(?<!\s)_' % (UNDER_CONTENT2, UNDER_CONTENT),
        re.DOTALL | re.UNICODE
    )
    # __em_em,strong___
    STRONG_EM3 = re.compile(
        r'(_{2})(?![\s_])%s_(?![\s_])%s(?<!\s)_{3}' % (UNDER_CONTENT2, UNDER_CONTENT),
        re.DOTALL | re.UNICODE
    )
    # __strong__
    STRONG = re.compile(
        r'(_{2})(?!\s)%s(?<!\s)\1' % UNDER_CONTENT2,
        re.DOTALL | re.UNICODE
    )
    # _emphasis_
    EM = re.compile(
        r'(_)(?!\s)%s(?<!\s)\1' % UNDER_CONTENT,
        re.DOTALL | re.UNICODE
    )

    # Smart rules for when "smart underscore" is enabled
    # SMART: ___strong,em___
    SMART_STRONG_EM = re.compile(
        r'(?<!\w)(_{3})(?![\s_])%s(?<!\s)\1(?!\w)' % SMART_UNDER_CONTENT,
        re.DOTALL | re.UNICODE
    )
    # ___strong,em_ strong__
    SMART_STRONG_EM2 = re.compile(
        r'(?<!\w)(_{3})(?![\s_])%s(?<!\s)_(?!\w)%s(?<!\s)_{2}(?!\w)' % (SMART_UNDER_MIXED_CONTENT, SMART_UNDER_CONTENT),
        re.DOTALL | re.UNICODE
    )
    SMART_STRONG_EM3 = re.compile(
        r'(?<!\w)(_{2})(?![\s_])%s(?<!\w)_(?![\s_])%s(?<!\s)_{3}(?!\w)' % (SMART_UNDER_CONTENT, SMART_UNDER_CONTENT),
        re.DOTALL | re.UNICODE
    )
    # ___em,strong__ em_
    SMART_EM_STRONG = re.compile(
        r'(?<!\w)(_{3})(?![\s_])%s(?<!\s)_{2}(?!\w)%s(?<!\s)_(?!\w)' % (SMART_UNDER_MIXED_CONTENT, SMART_UNDER_CONTENT),
        re.DOTALL | re.UNICODE
    )
    # __strong__
    SMART_STRONG = re.compile(
        r'(?<!\w)(_{2})(?![\s_])%s(?<!\s)\1(?!\w)' % SMART_UNDER_CONTENT,
        re.DOTALL | re.UNICODE
    )
    # SMART _em_
    SMART_EM = re.compile(
        r'(?<!\w)(_)(?![\s_])%s(?<!\s)\1(?!\w)' % SMART_UNDER_CONTENT,
        re.DOTALL | re.UNICODE
    )


class BetterEmExtension(Extension):
    """Add extension to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'smart_enable': ["underscore", "Treat connected words intelligently - Default: underscore"]
        }

        super(BetterEmExtension, self).__init__(*args, **kwargs)

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
        if enabled:
            enable_all = enabled == "all"
            enable_under = enabled == "underscore" or enable_all
            enable_star = enabled == "asterisk" or enable_all

        # Delete all default properties and register with new
        md.inlinePatterns.deregister('em_strong', strict=False)
        md.inlinePatterns.deregister('strong_em', strict=False)
        md.inlinePatterns.deregister('strong', strict=False)
        md.inlinePatterns.deregister('emphasis', strict=False)
        md.inlinePatterns.deregister('strong2', strict=False)
        md.inlinePatterns.deregister('emphasis2', strict=False)

        md.inlinePatterns.register(BetterEmPattern(r'\*', smart=enable_all or enable_star), 'strong_em', 50)
        md.inlinePatterns.register(BetterEmUnderPattern(r'_', smart=enable_all or enable_under), 'strong_em2', 60)


def makeExtension(*args, **kwargs):
    """Return extension."""

    return BetterEmExtension(*args, **kwargs)
