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
from markdown import Extension
from markdown.preprocessors import Preprocessor
import functools
import urllib.request as request
import re
import codecs
import os
from . import util

MI = 1024 * 1024  # mebibyte (MiB)
DEFAULT_URL_SIZE = MI * 32
DEFAULT_URL_TIMEOUT = 10.0  # in seconds


class SnippetMissingError(Exception):
    """Snippet missing exception."""


class SnippetPreprocessor(Preprocessor):
    """Handle snippets in Markdown content."""

    RE_ALL_SNIPPETS = re.compile(
        r'''(?x)
        ^(?P<space>[ \t]*)
        (?P<all>
            (?P<inline_marker>-{2,}8<-{2,}[ \t]+)
            (?P<snippet>(?:"(?:\\"|[^"\n\r])+?"|'(?:\\'|[^'\n\r])+?'))(?![ \t]) |
            (?P<block_marker>-{2,}8<-{2,})(?![ \t])
        )\r?$
        '''
    )

    RE_SNIPPET = re.compile(
        r'''(?x)
        ^(?P<space>[ \t]*)
        (?P<snippet>.*?)\r?$
        '''
    )

    def __init__(self, config, md):
        """Initialize."""

        base = config.get('base_path')
        if isinstance(base, str):
            base = [base]
        self.base_path = base
        self.encoding = config.get('encoding')
        self.check_paths = config.get('check_paths')
        self.auto_append = config.get('auto_append')
        self.url_download = config['url_download']
        self.url_max_size = config['url_max_size']
        self.url_timeout = config['url_timeout']
        self.tab_length = md.tab_length
        super(SnippetPreprocessor, self).__init__()

    def get_snippet_path(self, path):
        """Get snippet path."""

        snippet = None
        for base in self.base_path:
            if os.path.exists(base):
                if os.path.isdir(base):
                    filename = os.path.join(base, path)
                    if os.path.exists(filename):
                        snippet = filename
                        break
                else:
                    basename = os.path.basename(base)
                    dirname = os.path.dirname(base)
                    if basename.lower() == path.lower():
                        filename = os.path.join(dirname, path)
                        if os.path.exists(filename):
                            snippet = filename
                            break
        return snippet

    @functools.lru_cache()
    def download(self, url):
        """
        Actually download the snippet pointed to by the passed URL.

        The most recently used files are kept in a cache until the next reset.
        """

        timeout = None if self.url_timeout == 0 else self.url_timeout
        with request.urlopen(url, timeout=timeout) as response:

            # Fail if status is not OK
            status = response.status if util.PY39 else response.code
            if status != 200:
                raise SnippetMissingError('Cannot download snippet {}'.format(url))

            # We provide some basic protection against absurdly large files.
            # 32MB is chosen as an arbitrary upper limit. This can be raised if desired.
            length = response.headers.get("content-length")
            if length is None:
                raise ValueError("Missing content-length header")
            content_length = int(length)

            if self.url_max_size != 0 and content_length >= self.url_max_size:
                raise ValueError("refusing to read payloads larger than or equal to {}".format(self.url_max_size))

            # Nothing to return
            if content_length == 0:
                return ['']

            # Process lines
            return [l.decode(self.encoding) for l in response.readlines()]

    def parse_snippets(self, lines, file_name=None, is_url=False):
        """Parse snippets snippet."""

        if file_name:
            # Track this file.
            self.seen.add(file_name)

        new_lines = []
        inline = False
        block = False
        for line in lines:
            # Check for snippets on line
            inline = False
            m = self.RE_ALL_SNIPPETS.match(line)
            if m:
                if block and m.group('inline_marker'):
                    # Don't use inline notation directly under a block.
                    # It's okay if inline is used again in sub file though.
                    continue

                elif m.group('inline_marker'):
                    # Inline
                    inline = True

                else:
                    # Block
                    block = not block
                    continue

            elif not block:
                # Not in snippet, and we didn't find an inline,
                # so just a normal line
                new_lines.append(line)
                continue

            if block and not inline:
                # We are in a block and we didn't just find a nested inline
                # So check if a block path
                m = self.RE_SNIPPET.match(line)

            if m:
                # Get spaces and snippet path.  Remove quotes if inline.
                space = m.group('space').expandtabs(self.tab_length)
                path = m.group('snippet')[1:-1].strip() if inline else m.group('snippet').strip()

                if not inline:
                    # Block path handling
                    if not path:
                        # Empty path line, insert a blank line
                        new_lines.append('')
                        continue

                # Ignore commented out lines
                if path.startswith('; '):
                    continue

                # Ignore path links if we are in external, downloaded content
                is_link = path.lower().startswith(('https://', 'http://'))
                if is_url and not is_link:
                    continue

                # If this is a link, and we are allowing URLs, set `url` to true.
                # Make sure we don't process `path` as a local file reference.
                url = self.url_download and is_link
                snippet = self.get_snippet_path(path) if not url else path

                if snippet:

                    # This is in the stack and we don't want an infinite loop!
                    if snippet in self.seen:
                        continue

                    if not url:
                        # Read file content
                        with codecs.open(snippet, 'r', encoding=self.encoding) as f:
                            s_lines = [l for l in f]
                    else:
                        # Read URL content
                        try:
                            s_lines = self.download(snippet)
                        except SnippetMissingError:
                            if self.check_paths:
                                raise
                            s_lines = []

                    # Process lines looking for more snippets
                    new_lines.extend(
                        [
                            space + l2 for l2 in self.parse_snippets(
                                [l.rstrip('\r\n') for l in s_lines],
                                snippet,
                                is_url=url
                            )
                        ]
                    )

                elif self.check_paths:
                    raise SnippetMissingError("Snippet at path %s could not be found" % path)

        # Pop the current file name out of the cache
        if file_name:
            self.seen.remove(file_name)

        return new_lines

    def run(self, lines):
        """Process snippets."""

        self.seen = set()
        if self.auto_append:
            lines.extend("\n\n--8<--\n{}\n--8<--\n".format('\n\n'.join(self.auto_append)).split('\n'))

        return self.parse_snippets(lines)


class SnippetExtension(Extension):
    """Snippet extension."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'base_path': [["."], "Base path for snippet paths - Default: [\".\"]"],
            'encoding': ["utf-8", "Encoding of snippets - Default: \"utf-8\""],
            'check_paths': [False, "Make the build fail if a snippet can't be found - Default: \"False\""],
            "auto_append": [
                [],
                "A list of snippets (relative to the 'base_path') to auto append to the Markdown content - Default: []"
            ],
            'url_download': [False, "Download external URLs as snippets - Default: \"False\""],
            'url_max_size': [DEFAULT_URL_SIZE, "External URL max size (0 means no limit)- Default: 32 MiB"],
            'url_timeout': [DEFAULT_URL_TIMEOUT, 'Defualt URL timeout (0 means no timeout) - Default: 10 sec']
        }

        super(SnippetExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        """Register the extension."""

        self.md = md
        md.registerExtension(self)
        config = self.getConfigs()
        snippet = SnippetPreprocessor(config, md)
        md.preprocessors.register(snippet, "snippet", 32)

    def reset(self):
        """Reset."""

        self.md.preprocessors['snippet'].download.cache_clear()


def makeExtension(*args, **kwargs):
    """Return extension."""

    return SnippetExtension(*args, **kwargs)
