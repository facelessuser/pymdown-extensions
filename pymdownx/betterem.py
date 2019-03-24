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
from markdown.inlinepatterns import InlineProcessor, util
from collections import namedtuple
import re

SMART_UNDER_CONTENT = r'((?:[^_]|_(?=\w|\s)|(?<=\s)_+?(?=\s))+?_*?)'
SMART_STAR_CONTENT = r'((?:[^\*]|\*(?=[^\W_]|\*|\s)|(?<=\s)\*+?(?=\s))+?\**?)'
SMART_UNDER_MIXED_CONTENT = r'((?:[^_]|_(?=\w)|(?<=\s)_+?(?=\s))+?_*)'
SMART_STAR_MIXED_CONTENT = r'((?:[^\*]|\*(?=[^\W_]|\*)|(?<=\s)\*+?(?=\s))+?\**)'
UNDER_CONTENT = r'(_|(?:(?<=\s)_|[^_])+?)'
UNDER_CONTENT2 = r'((?:[^_]|(?<!_{2})_(?=[\w\s]))+?)'
STAR_CONTENT = r'(\*|(?:(?<=\s)\*|[^\*])+?)'
STAR_CONTENT2 = r'((?:[^\*]|(?<!\*{2})\*(?=[^\W_]|\*|\s))+?)'

# ***strong,em***
STAR_STRONG_EM = r'(\*{3})(?!\s)(\*{1,2}|[^\*]+?)(?<!\s)\1'
# ___strong,em___
UNDER_STRONG_EM = r'(_{3})(?!\s)(_{1,2}|[^_]+?)(?<!\s)\1'
# ***strong,em*strong**
STAR_STRONG_EM2 = r'(\*{3})(?![\s\*])%s(?<!\s)\*%s(?<!\s)\*{2}' % (STAR_CONTENT, STAR_CONTENT2)
# ___strong,em_strong__
UNDER_STRONG_EM2 = r'(_{3})(?![\s_])%s(?<!\s)_%s(?<!\s)_{2}' % (UNDER_CONTENT, UNDER_CONTENT2)
# ***em,strong**em*
STAR_EM_STRONG = r'(\*{3})(?![\s\*])%s(?<!\s)\*{2}%s(?<!\s)\*' % (STAR_CONTENT2, STAR_CONTENT)
# **em*em,strong***
STAR_STRONG_EM3 = r'(\*{2})(?![\s\*])%s\*(?![\s\*])%s(?<!\s)\*{3}' % (STAR_CONTENT2, STAR_CONTENT)
# ___em,strong__em_
UNDER_EM_STRONG = r'(_{3})(?![\s_])%s(?<!\s)_{2}%s(?<!\s)_' % (UNDER_CONTENT2, UNDER_CONTENT)
# __em_em,strong___
UNDER_STRONG_EM3 = r'(_{2})(?![\s_])%s_(?![\s_])%s(?<!\s)_{3}' % (UNDER_CONTENT2, UNDER_CONTENT)
# **strong**
STAR_STRONG = r'(\*{2})(?!\s)%s(?<!\s)\1' % STAR_CONTENT2
# __strong__
UNDER_STRONG = r'(_{2})(?!\s)%s(?<!\s)\1' % UNDER_CONTENT2
# *emphasis*
STAR_EM = r'(\*)(?!\s)%s(?<!\s)\1' % STAR_CONTENT
# _emphasis_
UNDER_EM = r'(_)(?!\s)%s(?<!\s)\1' % UNDER_CONTENT

# Smart rules for when "smart underscore" is enabled
# SMART: ___strong,em___
SMART_UNDER_STRONG_EM = r'(?<!\w)(_{3})(?![\s_])%s(?<!\s)\1(?!\w)' % SMART_UNDER_CONTENT
# ___strong,em_ strong__
SMART_UNDER_STRONG_EM2 = \
    r'(?<!\w)(_{3})(?![\s_])%s(?<!\s)_(?!\w)%s(?<!\s)_{2}(?!\w)' % (SMART_UNDER_MIXED_CONTENT, SMART_UNDER_CONTENT)
# ___em,strong__ em_
SMART_UNDER_EM_STRONG = \
    r'(?<!\w)(_{3})(?![\s_])%s(?<!\s)_{2}(?!\w)%s(?<!\s)_(?!\w)' % (SMART_UNDER_MIXED_CONTENT, SMART_UNDER_CONTENT)
# __strong__
SMART_UNDER_STRONG = r'(?<!\w)(_{2})(?![\s_])%s(?<!\s)\1(?!\w)' % SMART_UNDER_CONTENT
# SMART _em_
SMART_UNDER_EM = r'(?<!\w)(_)(?![\s_])%s(?<!\s)\1(?!\w)' % SMART_UNDER_CONTENT

# Smart rules for when "smart asterisk" is enabled
# SMART: ***strong,em***
SMART_STAR_STRONG_EM = r'(?:(?<=_)|(?<![\w\*]))(\*{3})(?![\s\*])%s(?<!\s)\1(?:(?=_)|(?![\w\*]))' % SMART_STAR_CONTENT
# ***strong,em* strong**
SMART_STAR_STRONG_EM2 = \
    r'(?:(?<=_)|(?<![\w\*]))(\*{3})(?![\s\*])%s(?<!\s)\*(?:(?=_)|(?![\w\*]))%s(?<!\s)\*{2}(?:(?=_)|(?![\w\*]))' % (
        SMART_STAR_MIXED_CONTENT, SMART_STAR_CONTENT
    )
# ***em,strong** em*
SMART_STAR_EM_STRONG = \
    r'(?:(?<=_)|(?<![\w\*]))(\*{3})(?![\s\*])%s(?<!\s)\*{2}(?:(?=_)|(?![\w\*]))%s(?<!\s)\*(?:(?=_)|(?![\w\*]))' % (
        SMART_STAR_MIXED_CONTENT, SMART_STAR_CONTENT
    )
# **strong**
SMART_STAR_STRONG = r'(?:(?<=_)|(?<![\w\*]))(\*{2})(?![\s\*])%s(?<!\s)\1(?:(?=_)|(?![\w\*]))' % SMART_STAR_CONTENT
# SMART *em*
SMART_STAR_EM = r'(?:(?<=_)|(?<![\w\*]))(\*)(?![\s\*])%s(?<!\s)\1(?:(?=_)|(?![\w\*]))' % SMART_STAR_CONTENT


class EmStrongItem(namedtuple('EmStrongItem', ['pattern', 'builder', 'tags'])):
    """Emphasis/strong pattern item."""


class AsteriskProcessor(InlineProcessor):
    """Emphasis processor for handling strong and em matches."""

    PATTERNS = [
        EmStrongItem(re.compile(STAR_STRONG_EM, re.DOTALL | re.UNICODE), 'double', 'strong,em'),
        EmStrongItem(re.compile(STAR_EM_STRONG, re.DOTALL | re.UNICODE), 'double', 'em,strong'),
        EmStrongItem(re.compile(STAR_STRONG_EM2, re.DOTALL | re.UNICODE), 'double', 'strong,em'),
        EmStrongItem(re.compile(STAR_STRONG_EM3, re.DOTALL | re.UNICODE), 'double2', 'strong,em'),
        EmStrongItem(re.compile(STAR_STRONG, re.DOTALL | re.UNICODE), 'single', 'strong'),
        EmStrongItem(re.compile(STAR_EM, re.DOTALL | re.UNICODE), 'single', 'em')
    ]

    def build_single(self, m, tag, idx):
        """Return single tag."""
        el1 = util.etree.Element(tag)
        text = m.group(2)
        self.parse_sub_patterns(text, el1, None, idx)
        return el1

    def build_double(self, m, tags, idx):
        """Return double tag."""

        tag1, tag2 = tags.split(",")
        el1 = util.etree.Element(tag1)
        el2 = util.etree.Element(tag2)
        text = m.group(2)
        self.parse_sub_patterns(text, el2, None, idx)
        el1.append(el2)
        if len(m.groups()) == 3:
            text = m.group(3)
            self.parse_sub_patterns(text, el1, el2, idx)
        return el1

    def build_double2(self, m, tags, idx):
        """Return double tags (variant 2): `<strong>text <em>text</em></strong>`."""

        tag1, tag2 = tags.split(",")
        el1 = util.etree.Element(tag1)
        el2 = util.etree.Element(tag2)
        text = m.group(2)
        self.parse_sub_patterns(text, el1, None, idx)
        text = m.group(3)
        el1.append(el2)
        self.parse_sub_patterns(text, el2, None, idx)
        return el1

    def parse_sub_patterns(self, data, parent, last, idx):
        """
        Parses sub patterns.

        `data` (`str`):
            text to evaluate.

        `parent` (`etree.Element`):
            Parent to attach text and sub elements to.

        `last` (`etree.Element`):
            Last appended child to parent. Can also be None if parent has no children.

        `idx` (`int`):
            Current pattern index that was used to evaluate the parent.

        """

        offset = 0
        pos = 0

        length = len(data)
        while pos < length:
            # Find the start of potential emphasis or strong tokens
            if self.compiled_re.match(data, pos):
                matched = False
                # See if the we can match an emphasis/strong pattern
                for index, item in enumerate(self.PATTERNS):
                    # Only evaluate patterns that are after what was used on the parent
                    if index <= idx:
                        continue
                    m = item.pattern.match(data, pos)
                    if m:
                        # Append child nodes to parent
                        # Text nodes should be appended to the last
                        # child if present, and if not, it should
                        # be added as the parent's text node.
                        text = data[offset:m.start(0)]
                        if text:
                            if last is not None:
                                last.tail = text
                            else:
                                parent.text = text
                        el = self.build_element(m, item.builder, item.tags, index)
                        parent.append(el)
                        last = el
                        # Move our position past the matched hunk
                        offset = pos = m.end(0)
                        matched = True
                if not matched:
                    # We matched nothing, move on to the next character
                    pos += 1
            else:
                # Increment position as no potential emphasis start was found.
                pos += 1

        # Append any leftover text as a text node.
        text = data[offset:]
        if text:
            if last is not None:
                last.tail = text
            else:
                parent.text = text

    def build_element(self, m, builder, tags, index):
        """Element builder."""

        if builder == 'double2':
            return self.build_double2(m, tags, index)
        elif builder == 'double':
            return self.build_double(m, tags, index)
        else:
            return self.build_single(m, tags, index)

    def handleMatch(self, m, data):
        """Parse patterns."""

        el = None
        start = None
        end = None

        for index, item in enumerate(self.PATTERNS):
            m1 = item.pattern.match(data, m.start(0))
            if m1:
                start = m1.start(0)
                end = m1.end(0)
                el = self.build_element(m1, item.builder, item.tags, index)
                break
        return el, start, end


class SmartAsteriskProcessor(AsteriskProcessor):
    """Smart emphasis and strong processor."""

    PATTERNS = [
        EmStrongItem(re.compile(SMART_STAR_STRONG_EM, re.DOTALL | re.UNICODE), 'double', 'strong,em'),
        EmStrongItem(re.compile(SMART_STAR_EM_STRONG, re.DOTALL | re.UNICODE), 'double', 'em,strong'),
        EmStrongItem(re.compile(SMART_STAR_STRONG_EM2, re.DOTALL | re.UNICODE), 'double', 'strong,em'),
        EmStrongItem(re.compile(SMART_STAR_STRONG, re.DOTALL | re.UNICODE), 'single', 'strong'),
        EmStrongItem(re.compile(SMART_STAR_EM, re.DOTALL | re.UNICODE), 'single', 'em')
    ]


class UnderscoreProcessor(AsteriskProcessor):
    """Emphasis processor for handling strong and em matches."""

    PATTERNS = [
        EmStrongItem(re.compile(UNDER_STRONG_EM, re.DOTALL | re.UNICODE), 'double', 'strong,em'),
        EmStrongItem(re.compile(UNDER_EM_STRONG, re.DOTALL | re.UNICODE), 'double', 'em,strong'),
        EmStrongItem(re.compile(UNDER_STRONG_EM2, re.DOTALL | re.UNICODE), 'double', 'strong,em'),
        EmStrongItem(re.compile(UNDER_STRONG_EM3, re.DOTALL | re.UNICODE), 'double2', 'strong,em'),
        EmStrongItem(re.compile(UNDER_STRONG, re.DOTALL | re.UNICODE), 'single', 'strong'),
        EmStrongItem(re.compile(UNDER_EM, re.DOTALL | re.UNICODE), 'single', 'em')
    ]


class SmartUnderscoreProcessor(AsteriskProcessor):
    """Emphasis processor for handling strong and em matches."""

    PATTERNS = [
        EmStrongItem(re.compile(SMART_UNDER_STRONG_EM, re.DOTALL | re.UNICODE), 'double', 'strong,em'),
        EmStrongItem(re.compile(SMART_UNDER_EM_STRONG, re.DOTALL | re.UNICODE), 'double', 'em,strong'),
        EmStrongItem(re.compile(SMART_UNDER_STRONG_EM2, re.DOTALL | re.UNICODE), 'double', 'strong,em'),
        EmStrongItem(re.compile(SMART_UNDER_STRONG, re.DOTALL | re.UNICODE), 'single', 'strong'),
        EmStrongItem(re.compile(SMART_UNDER_EM, re.DOTALL | re.UNICODE), 'single', 'em')
    ]


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

        asterisk = SmartAsteriskProcessor(r'\*') if enable_star else AsteriskProcessor(r'\*')
        md.inlinePatterns.register(asterisk, "strong_em", 50)
        underscore = SmartUnderscoreProcessor('_') if enable_under else UnderscoreProcessor('_')
        md.inlinePatterns.register(underscore, "strong_em2", 40)


def makeExtension(*args, **kwargs):
    """Return extension."""

    return BetterEmExtension(*args, **kwargs)
