"""
Snippet ---8<---.

pymdownx.snippet
Inject snippets

MIT license.

Copyright (c) 2017 Isaac Muse <isaacmuse@gmail.com>

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
from markdown import Extension
from markdown.preprocessors import Preprocessor
import re
import codecs
import os


class SnippetPreprocessor(Preprocessor):
    """Handle snippets in Markdown content."""

    RE_SNIPPETS = re.compile(
        r'''(?x)
        ^(?P<space>[ \t]*)
        (?P<all>
            (?P<marker>-{2,}8<-{2,}[ ]+)
            (?P<snippet>.*)
        )$
        '''
    )

    def __init__(self, config, md):
        """Initialize."""

        self.base_path = config.get('base_path')
        self.encoding = config.get('encoding')
        self.tab_length = md.tab_length
        super(SnippetPreprocessor, self).__init__()

    def parse_file(self, lines, file_name=None):
        """Parse snippet."""

        new_lines = []
        for line in lines:
            found = False
            m = self.RE_SNIPPETS.match(line)
            if m:
                space = m.group('space').replace('\t', ' ' * self.tab_length)
                snippet = os.path.join(self.base_path, m.group('snippet').strip())
                if os.path.exists(snippet):
                    if snippet in self.seen:
                        # This is in the stack and we don't want an infinite loop!
                        new_lines.append(line)
                        continue
                    elif file_name:
                        # Track this file.
                        self.seen.add(file_name)
                    try:
                        with codecs.open(snippet, 'r', encoding=self.encoding) as f:
                            new_lines.extend(
                                [space + l2 for l2 in self.parse_file([l.rstrip('\n') for l in f], snippet)]
                            )
                            found = True
                    except Exception:  # pragma: no cover
                        pass
                    if file_name:
                        self.seen.remove(file_name)
            if not found:
                new_lines.append(line)

        return new_lines

    def run(self, lines):
        """Process snippets."""

        self.seen = set()
        return self.parse_file(lines)


class SnippetExtension(Extension):
    """Snippet extension."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'base_path': [".", "Base path for snippet paths - Default: \"\""],
            'encoding': ["utf-8", "Encoding of snippets - Default: \"utf-8\""]
        }

        super(SnippetExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """Register the extension."""

        self.md = md
        md.registerExtension(self)
        config = self.getConfigs()
        snippet = SnippetPreprocessor(config, md)
        md.preprocessors.add('snippet', snippet, "<normalize_whitespace")


def makeExtension(*args, **kwargs):
    """Return extension."""

    return SnippetExtension(*args, **kwargs)
