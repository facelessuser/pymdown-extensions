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
from markdown.util import nearing_recursion_limit
from email.utils import parsedate_to_datetime
import datetime
import functools
import urllib
import re
import os
from . import util
import textwrap
import time

MI = 1024 * 1024  # mebibyte (MiB)
DEFAULT_URL_SIZE = MI * 32
DEFAULT_URL_TIMEOUT = 10.0  # in seconds
DEFAULT_URL_REQUEST_HEADERS = {}
DEFAULT_MAX_RETRIES = 3
DEFAULT_BACKOFF_FACTOR = 2


class SnippetMissingError(Exception):
    """Snippet missing exception."""


class SnippetPreprocessor(Preprocessor):
    """Handle snippets in Markdown content."""

    RE_ALL_SNIPPETS = re.compile(
        r'''(?x)
        ^(?P<space>[ \t]*)
        (?P<escape>;*)
        (?P<all>
            (?P<inline_marker>-{1,}8<-{1,}[ \t]+)
            (?P<snippet>(?:"(?:\\"|[^"\n\r])+?"|'(?:\\'|[^'\n\r])+?'))(?![ \t]) |
            (?P<block_marker>-{1,}8<-{1,})(?![ \t])
        )\r?$
        '''
    )

    RE_SNIPPET = re.compile(
        r'''(?x)
        ^(?P<space>[ \t]*)
        (?P<snippet>.*?)\r?$
        '''
    )

    # The lazy `pre` tries every position, and the runs of `;` and `-` after it get re-scanned from each one.
    # The lookarounds skip positions that cannot be the shortest match in constant time (it can't follow a `;`,
    # and it can't split a run of `-` as the marker would have absorbed them), so we never re-scan a run.
    RE_SNIPPET_SECTION = re.compile(
        r'''(?xi)
        ^(?P<pre>.*?)
        (?<!;)(?!(?<=-)-)
        (?P<escape>;*)
        (?P<inline_marker>-{1,}8<-{1,}[ \t]+)
        (?P<section>\[[ \t]*(?P<type>start|end)[ \t]*:[ \t]*(?P<name>[a-z][-_0-9a-z]*)[ \t]*\])
        (?P<post>.*?)$
        '''
    )

    # Reference for how a path is split into the path, line ranges, and section. This is not used directly, other
    # than for paths with newlines, as backtracking makes it quadratic on long paths. See `split_path`.
    RE_SNIPPET_FILE = re.compile(
        r'(?i)(.*?)(?:((?::-?[0-9]*){1,2}(?:(?:,(?=[-0-9:])-?[0-9]*)(?::-?[0-9]*)?)*)|(:[a-z][-_0-9a-z]*))?$'
    )
    RE_SECTION_CHAR = re.compile(r'(?i)[-_0-9a-z]')
    RE_SECONDS = re.compile(r'[0-9]+')
    RE_LETTER = re.compile(r'(?i)[a-z]')

    def __init__(self, config, md):
        """Initialize."""

        base = config.get('base_path')
        if isinstance(base, (str, os.PathLike)):
            base = [base]
        self.base_path = [os.path.abspath(b) for b in base]
        self.bases = None
        self.failed = set()
        self.restrict_base_path = config['restrict_base_path']
        self.encoding = config.get('encoding')
        self.check_paths = config.get('check_paths')
        self.auto_append = config.get('auto_append')
        self.url_download = config['url_download']
        self.url_max_size = config['url_max_size']
        self.url_timeout = config['url_timeout']
        self.url_request_headers = config['url_request_headers']
        self.dedent_subsections = config['dedent_subsections']
        self.max_retries = config['max_retries']
        self.backoff_factor = config['backoff_factor']
        self.tab_length = md.tab_length
        super().__init__()

        self.download.cache_clear()

    def match_section(self, line):
        """Match a section marker in the line, if there is one."""

        # Every section marker contains `8<-`. Checking for it is far cheaper than the regular expression, and
        # nearly every line in a document does not have it.
        return self.RE_SNIPPET_SECTION.match(line) if '8<-' in line else None

    def split_path(self, path):
        """
        Split a snippet path into the path, the line ranges (`:1:5,10:`), and the section (`:name`).

        This returns the same groups as `RE_SNIPPET_FILE.match(path).groups()`, but in linear time.

        The path is everything before the first `:` that starts a valid specifier that runs to the end of the string.
        Each part of a specifier is unambiguous (digits are never confused with `:` or `,`), so there is nothing
        for the regular expression to backtrack into. We can therefore find which `:` are valid starts in a single
        pass from the end instead of trying, and re-scanning the remainder for, each one.
        """

        if '\n' in path:
            # Newlines are handled specially by `.` and `$`, so let the regular expression decide.
            m = self.RE_SNIPPET_FILE.match(path)
            return None if m is None else m.groups()

        if ':' not in path:
            return path, None, None

        size = len(path)

        # The end of the run of digits starting at each index
        digits = [size] * (size + 1)
        for i in range(size - 1, -1, -1):
            digits[i] = digits[i + 1] if '0' <= path[i] <= '9' else i

        def number_end(i):
            """Get the end of an optionally negative number (`-?[0-9]*`) that starts at `i`."""

            return digits[i + 1] if i < size and path[i] == '-' else digits[i]

        # Is everything from each index a (possibly empty) series of `,N` or `,N:N` items?
        # A comma has to be followed by something that can start a number.
        tail = [False] * (size + 1)
        tail[size] = True
        for i in range(size - 1, -1, -1):
            if path[i] == ',' and i + 1 < size and path[i + 1] in '-0123456789:':
                j = number_end(i + 1)
                if j < size and path[j] == ':':
                    j = number_end(j + 1)
                tail[i] = tail[j]

        # Where the run of section name characters at the end of the path starts
        name = size
        while name > 0 and self.RE_SECTION_CHAR.fullmatch(path[name - 1]):
            name -= 1

        colon = path.find(':')
        while colon != -1:
            # Line ranges: `:N`, and an optional second `:N` (which is not optional if it is there), and then the tail
            end = number_end(colon + 1)
            if end < size and path[end] == ':':
                end = number_end(end + 1)
            if tail[end]:
                return path[:colon], path[colon:], None

            # Section: `:` and a letter, and then only name characters until the end
            if name <= colon + 1 < size and self.RE_LETTER.fullmatch(path[colon + 1]):
                return path[:colon], None, path[colon:]

            colon = path.find(':', colon + 1)

        return path, None, None

    def extract_section(self, section, lines):
        """Extract the specified section from the lines."""

        new_lines = []
        start = False
        found = False
        for l in lines:

            # Found a snippet section marker with our specified name
            m = self.match_section(l)

            # Handle escaped line
            if m and m.group('escape'):
                l = (
                    m.group('pre') + m.group('escape').replace(';', '', 1) + m.group('inline_marker') +
                    m.group('section') + m.group('post')
                )

            # Found a section we are looking for.
            elif m is not None and m.group('name') == section:

                # We found the start
                if not start and m.group('type') == 'start':
                    start = True
                    found = True
                    continue

                # Ignore duplicate start
                elif start and m.group('type') == 'start':
                    continue

                # We found the end
                elif start and m.group('type') == 'end':
                    start = False
                    break

                # We found an end, but no start
                else:
                    break

            # Found a section we don't care about, so ignore it.
            elif m and start:
                continue

            # We are currently in a section, so append the line
            if start:
                new_lines.append(l)

        if not found and self.check_paths:
            raise SnippetMissingError(f"Snippet section '{section}' could not be located")

        return self.dedent(new_lines) if self.dedent_subsections else new_lines

    def dedent(self, lines):
        """De-indent lines."""

        return textwrap.dedent('\n'.join(lines)).split('\n')

    def read_lines(self, path):
        """
        Read a file as a list of lines without line endings.

        Opening the file in text mode already turns every kind of line ending into a plain newline, so we can split on
        that. A file that ends with a line ending has a final empty line, and an empty file has no lines at all.
        """

        with open(path, 'r', encoding=self.encoding) as f:
            text = f.read()
        return text.split('\n') if text else []

    def get_bases(self):
        """
        Get the base paths that exist, and whether each is a directory.

        This is only checked once per run, instead of for every snippet, as it will not change while we process
        a document.
        """

        if self.bases is None:
            self.bases = [(base, os.path.isdir(base)) for base in self.base_path if os.path.exists(base)]
        return self.bases

    def get_snippet_path(self, path):
        """Get snippet path."""

        snippet = None
        for base, is_dir in self.get_bases():
            if is_dir:
                if self.restrict_base_path:
                    filename = os.path.abspath(os.path.join(base, path))
                    # If the absolute path is no longer under the specified base path, reject the file
                    # Append `os.sep` so a sibling directory whose name shares a prefix
                    # (e.g. `/x/docs` vs `/x/docs_evil`) cannot satisfy the check.
                    if not filename.startswith(base + os.sep if not base.endswith(os.sep) else base):
                        continue
                else:
                    filename = os.path.join(base, path)
                if os.path.exists(filename):
                    snippet = filename
                    break
            else:
                dirname = os.path.dirname(base)
                filename = os.path.join(dirname, path)
                if os.path.exists(filename) and os.path.samefile(filename, base):
                    snippet = filename
                    break
        return snippet

    def get_retry_after(self, error):
        """
        Get how many seconds the server asked us to wait before trying again, if it did.

        The `Retry-After` header is either a number of seconds or an HTTP date. If it is missing or we cannot
        understand it, `None` is returned, and we fall back to our own backoff.
        """

        headers = getattr(error, 'headers', None)
        value = headers.get('Retry-After') if headers is not None else None
        if not isinstance(value, str):
            return None

        value = value.strip()
        if self.RE_SECONDS.fullmatch(value):
            return int(value)

        try:
            date = parsedate_to_datetime(value)
        except (TypeError, ValueError, OverflowError):
            return None

        if date.tzinfo is None:
            date = date.replace(tzinfo=datetime.timezone.utc)
        return max(0, (date - datetime.datetime.now(datetime.timezone.utc)).total_seconds())

    @functools.lru_cache  # noqa: B019
    def download(self, url):
        """
        Actually download the snippet pointed to by the passed URL.

        The most recently used files are kept in a cache until the next reset.
        """

        retries = self.max_retries

        while True:
            try:
                http_request = urllib.request.Request(url, headers=self.url_request_headers)
                timeout = None if self.url_timeout == 0 else self.url_timeout
                with urllib.request.urlopen(http_request, timeout=timeout) as response:
                    # Fail if status is not OK
                    status = response.status if util.PY39 else response.code

                    if status != 200:
                        raise SnippetMissingError(f"Cannot download snippet '{url}' (HTTP Error {status})")

                    # We provide some basic protection against absurdly large files.
                    # 32MB is chosen as an arbitrary upper limit. This can be raised if desired.
                    content = None
                    if "content-length" not in response.headers:
                        # we have to read to know if we went over the max, but never more than `url_max_size`
                        # where `url_max_size` == 0 means unlimited
                        content = response.read(self.url_max_size) if self.url_max_size != 0 else response.read()
                        content_length = len(content)
                    else:
                        content_length = int(response.headers["content-length"])

                    if self.url_max_size != 0 and content_length >= self.url_max_size:
                        raise ValueError(f"refusing to read payloads larger than or equal to {self.url_max_size}")

                    # Nothing to return
                    if content_length == 0:
                        return ['']

                    if content is None:
                        # content-length was in the header, so we did not read yet
                        content = response.read()

                    # Process lines
                    last = content.endswith((b'\r', b'\n'))
                    s_lines = [l.decode(self.encoding) for l in content.splitlines()]
                    if last:
                        s_lines.append('')
                    return s_lines

            except urllib.error.HTTPError as e:
                # Handle rate limited error codes
                if e.code == 429 and retries:
                    retries -= 1
                    wait = self.backoff_factor * (self.max_retries - retries)

                    # If the server told us how long to wait, respect that. Retrying sooner is pointless, so if it is
                    # more than the longest we would wait on our own, give up now instead of failing after waiting.
                    retry_after = self.get_retry_after(e)
                    if retry_after is not None:
                        if retry_after > self.backoff_factor * self.max_retries:
                            raise SnippetMissingError(
                                f"Cannot download snippet '{url}' (HTTP Error 429, "
                                f"server asked to wait {retry_after:.0f} seconds before retrying)"
                            ) from e
                        wait = retry_after

                    time.sleep(wait)
                    continue
                raise SnippetMissingError(f"Cannot download snippet '{url}' (HTTP Error {e.code})") from e

    def parse_snippet_target(self, path):
        """
        Parse a snippet path specifier into a target.

        Splits `file.md:1:5`, `file.md:1:2,8:9` or `file.md:section` into a dictionary
        with the keys `path`, `start`, `end` and `section`. Returns `None` if no path is found.
        """

        start = []
        end = []
        section = None
        parts = self.split_path(path)
        path = '' if parts is None else parts[0].strip()
        if not path:
            return None
        if parts[1]:
            for nums in parts[1][1:].split(','):
                span = nums.split(':')
                st = int(span[0]) if span[0] else None
                start.append(st if st is None or st < 0 else max(0, st - 1))
                en = int(span[1]) if len(span) > 1 and span[1] else None
                end.append(en)
        elif parts[2]:
            section = parts[2][1:]

        return {'path': path, 'start': start, 'end': end, 'section': section}

    def extract_lines(self, start, end, lines):
        """Extract the specified line ranges from the lines."""

        total = len(lines)
        final_lines = []
        for sel in zip(start, end, strict=True):
            s_start = util.clamp(total + sel[0], 0, total) if sel[0] and sel[0] < 0 else sel[0]
            s_end = util.clamp(total + 1 + sel[1], 0, total) if sel[1] and sel[1] < 0 else sel[1]
            final_lines.extend(lines[slice(s_start, s_end, None)])
        return self.dedent(final_lines) if self.dedent_subsections else final_lines

    def select_snippet_lines(self, lines, target):
        """Select the lines requested by the target (line ranges or section)."""

        if not lines:
            return lines
        if target['start'] and target['end']:
            return self.extract_lines(target['start'], target['end'], lines)
        if target['section']:
            return self.extract_section(target['section'], lines)
        return lines

    def process_snippet_lines(self, lines, target):
        """
        Process the selected lines of a snippet. By default, the lines are returned unchanged.

        This is called after the lines (the whole file, line ranges, or a section) are selected, and *before* any
        snippets nested in those lines are expanded. This means `lines` still contain snippet notation, and anything
        that rewrites text, like a find and replace, can change the notation of a nested snippet and break it. Use
        `get_syntax_mask` to leave the notation alone. It also means this does not see the content of nested
        snippets, only the nested snippets themselves get their own call.

        In addition to the keys returned by `parse_snippet_target`, `target` contains `snippet` (the resolved file
        path or URL) and `is_url`.

        Return the new lines, and do not modify `lines` in place.
        """

        return lines

    def get_syntax_mask(self, lines, is_section=False):
        """
        Get which lines are snippet notation.

        Returns a list with a boolean for each line, which is `True` if the line is part of the snippet notation
        (inline snippets, block markers and the paths between them, and section markers) and will not end up in the
        content as written. Escaped notation is content, so it is `False`. Pass `is_section` if the lines are a
        section extracted from a file, as that is when section markers are not treated as notation.
        """

        mask = []
        block = False
        for line in lines:
            m = self.RE_ALL_SNIPPETS.match(line)
            if m:
                if m.group('escape'):
                    mask.append(False)
                    continue
                if not m.group('inline_marker'):
                    block = not block
                mask.append(True)
            elif block:
                mask.append(True)
            elif is_section:
                mask.append(False)
            else:
                m2 = self.match_section(line)
                mask.append(m2 is not None and not m2.group('escape'))
        return mask

    def parse_snippets(self, lines, file_name=None, is_url=False, is_section=False):
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
                if m.group('escape'):
                    # The snippet has been escaped, replace first `;` and continue.
                    new_lines.append(line.replace(';', '', 1))
                    continue

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
                if not is_section:
                    # Check for section line, if present remove, if escaped, reformat it
                    m2 = self.match_section(line)
                    if m2 and m2.group('escape'):
                        line = (
                            m2.group('pre') + m2.group('escape').replace(';', '', 1) + m2.group('inline_marker') +
                            m2.group('section') + m2.group('post')
                        )
                        m2 = None

                    # Found a section that must be removed
                    if m2 is not None:
                        continue

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
                if path.startswith(';'):
                    continue

                # Get path, line numbers and section (if specified)
                target = self.parse_snippet_target(path)
                # Looks like we have an empty file and only lines specified
                if target is None:
                    if self.check_paths:
                        raise SnippetMissingError("Snippet at path '' could not be found")
                    else:
                        continue
                path = target['path']

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
                    # Also, stop short of the recursion limit if the nested includes get too deep.
                    if snippet in self.seen or nearing_recursion_limit():
                        continue

                    if not url:
                        # Read file content
                        s_lines = self.read_lines(snippet)
                    else:
                        # Read URL content
                        s_lines = []
                        # Don't try a URL that already failed again, as each attempt can take a long time
                        # (timeouts, retries, and backoff), but do try again the next time we run.
                        if snippet not in self.failed:
                            try:
                                s_lines = self.download(snippet)
                            except SnippetMissingError:
                                if self.check_paths:
                                    raise
                                self.failed.add(snippet)

                    target['snippet'] = snippet
                    target['is_url'] = url
                    s_lines = self.select_snippet_lines(s_lines, target)
                    s_lines = self.process_snippet_lines(s_lines, target)

                    # Process lines looking for more snippets
                    new_lines.extend(
                        [
                            space + l2 for l2 in self.parse_snippets(
                                s_lines,
                                snippet,
                                is_url=url,
                                is_section=target['section'] is not None
                            )
                        ]
                    )

                elif self.check_paths:
                    raise SnippetMissingError(f"Snippet at path '{path}' could not be found")

        # Pop the current file name out of the cache
        if file_name:
            self.seen.remove(file_name)

        return new_lines

    def run(self, lines):
        """Process snippets."""

        self.seen = set()
        self.bases = None
        self.failed = set()
        if self.auto_append:
            lines.extend("\n\n-8<-\n{}\n-8<-\n".format('\n\n'.join(self.auto_append)).split('\n'))

        return self.parse_snippets(lines)


class SnippetExtension(Extension):
    """Snippet extension."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'base_path': [["."], "Base path for snippet paths - Default: [\".\"]"],
            'restrict_base_path': [
                True,
                "Restrict snippet paths such that they are under the base paths - Default: True"
            ],
            'encoding': ["utf-8", "Encoding of snippets - Default: \"utf-8\""],
            'check_paths': [False, "Make the build fail if a snippet can't be found - Default: \"False\""],
            "auto_append": [
                [],
                "A list of snippets (relative to the 'base_path') to auto append to the Markdown content - Default: []"
            ],
            'url_download': [False, "Download external URLs as snippets - Default: \"False\""],
            'url_max_size': [DEFAULT_URL_SIZE, "External URL max size (0 means no limit)- Default: 32 MiB"],
            'url_timeout': [DEFAULT_URL_TIMEOUT, 'Defualt URL timeout (0 means no timeout) - Default: 10 sec'],
            'url_request_headers': [DEFAULT_URL_REQUEST_HEADERS, "Extra request Headers - Default: {}"],
            'dedent_subsections': [False, "Dedent subsection extractions e.g. 'sections' and/or 'lines'."],
            'max_retries': [
                DEFAULT_MAX_RETRIES, "Maximum number of retry attempts for rate-limited requests - Default: 3"
            ],
            'backoff_factor': [DEFAULT_BACKOFF_FACTOR, "Backoff factor for retry attempts - Default: 2"]
        }

        super().__init__(*args, **kwargs)

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
