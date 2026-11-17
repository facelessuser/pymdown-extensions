"""
Strip HTML (previously named Plain HTML).

pymdownx.striphtml
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
from markdown import Extension
from markdown.postprocessors import Postprocessor
import re


# Comments and the content of `script` and `style` tags are not matched in full by the regular expression, only their
# start is. `StripHtmlPostprocessor.run` then looks for the end, which avoids the regular expression repeatedly scanning
# to the end of the document for every unclosed start, and avoids it scanning whitespace in front of a comment more than
# once, both of which can lead to quadratic behavior.
RE_TAG_HTML = re.compile(
    r'''(?x)
    (?:
        (?P<comments><!--)|
        (?P<scripts>
            (?P<script_open><(?P<script_name>style|script))
            (?P<script_attr>(?:\s+[\w\-:]+(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s"'`=<>]+))?)*)
            (?P<script_rest>\s*>)
        )|
        (?P<open><(?P<name>[\w\:\.\-]+))
        (?P<attr>(?:\s+[\w\-:]+(?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s"'`=<>]+))?)*)
        (?P<close>\s*(?P<self_close>/)?>)|
        (?P<close_tag></(?P<close_name>[\w\:\.\-]+)\s*>)
    )
    ''',
    re.DOTALL | re.UNICODE | re.IGNORECASE
)

# What can follow a comment for the whitespace around it to be stripped with it
RE_COMMENT_TRAIL = re.compile(r'\s*(?=\r?\n)')

RE_SCRIPT_CLOSE = {
    'script': re.compile(r'</script\s*>', re.IGNORECASE),
    'style': re.compile(r'</style\s*>', re.IGNORECASE)
}

TAG_BAD_ATTR = r'''(?x)
(?P<attr>
    (?:
        \s+(?:%s)
        (?:\s*=\s*(?:"[^"]*"|'[^']*'|[^\s"'`=<>]+))
    )*
)
'''


class StripHtmlPostprocessor(Postprocessor):
    """Post processor to strip out unwanted content."""

    def __init__(self, strip_comments, strip_js_on_attributes, strip_attributes, md):
        """Initialize."""

        self.strip_comments = strip_comments
        self.re_attributes = None
        attributes = [re.escape(a.strip()) for a in strip_attributes]
        if strip_js_on_attributes:
            attributes.append(r'on[\w]+')
        if attributes:
            self.re_attributes = re.compile(
                TAG_BAD_ATTR % '|'.join(attributes),
                re.DOTALL | re.UNICODE | re.IGNORECASE
            )

        super().__init__(md)

    def strip_attributes(self, attributes):
        """Strip unwanted attributes."""

        return attributes if self.re_attributes is None else self.re_attributes.sub('', attributes)

    def run(self, text):
        """Strip out comments and unwanted attributes."""

        if not (self.strip_comments or self.re_attributes):
            return text

        out = []
        # Everything before `last` has been handled, and `pos` is where we search from next
        last = pos = 0
        # Once we fail to find an end, there can't be one for anything that follows
        can_close = {'comments': True, 'script': True, 'style': True}

        while True:
            m = RE_TAG_HTML.search(text, pos)
            if m is None:
                break

            if m.group('comments'):
                # Comments are stripped along with the whitespace that precedes them and follows them on
                # a line, but only when the comment is followed by a newline.
                end = text.find('-->', m.end()) if can_close['comments'] else -1
                if end == -1:
                    # Unclosed comments are left as is
                    can_close['comments'] = False
                    pos = m.end()
                    continue
                start = m.start()
                end += 3
                trail = RE_COMMENT_TRAIL.match(text, end)
                if trail:
                    end = trail.end()
                    while start > last and text[start - 1].isspace():
                        start -= 1
                out.append(text[last:start])
                if not self.strip_comments:
                    out.append(text[start:end])
                last = pos = end
                continue

            out.append(text[last:m.start()])
            last = pos = m.end()

            if m.group('scripts'):
                out.append(m.group('script_open'))
                out.append(self.strip_attributes(m.group('script_attr')))
                out.append(m.group('script_rest'))
                # The content is left alone, but an unclosed tag has no content to skip
                name = m.group('script_name').lower()
                if can_close[name]:
                    close = RE_SCRIPT_CLOSE[name].search(text, last)
                    if close is None:
                        can_close[name] = False
                    else:
                        out.append(text[last:close.end()])
                        last = pos = close.end()
            elif m.group('close_tag'):
                out.append(m.group(0))
            else:
                out.append(m.group('open'))
                out.append(self.strip_attributes(m.group('attr')))
                out.append(m.group('close'))

        out.append(text[last:])
        return ''.join(out)


class StripHtmlExtension(Extension):
    """StripHTML extension."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'strip_comments': [
                True,
                "Strip HTML comments at the end of processing. "
                "- Default: True"
            ],
            'strip_attributes': [
                [],
                "A string of attributes separated by spaces."
                "- Default: 'id class style']"
            ],
            'strip_js_on_attributes': [
                True,
                "Strip JavaScript script attribues with the pattern on*. "
                " - Default: True"
            ]
        }
        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        """Strip unwanted HTML attributes and/or comments."""

        md.registerExtension(self)
        config = self.getConfigs()
        striphtml = StripHtmlPostprocessor(
            config.get('strip_comments'),
            config.get('strip_js_on_attributes'),
            config.get('strip_attributes'),
            md
        )
        md.postprocessors.register(striphtml, "strip-html", 1)


def makeExtension(*args, **kwargs):
    """Return extension."""

    return StripHtmlExtension(*args, **kwargs)
