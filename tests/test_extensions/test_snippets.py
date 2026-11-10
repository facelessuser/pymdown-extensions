"""Test cases for Snippets."""
from .. import util
import os
import random
import re
import tempfile
import markdown
import datetime
from types import SimpleNamespace
from pymdownx.snippets import SnippetMissingError, SnippetPreprocessor
from unittest.mock import patch, MagicMock
import urllib.error
from http.client import HTTPMessage

BASE = os.path.abspath(os.path.dirname(__file__))


class TestSnippetDedent(util.MdCase):
    """Test snippet cases."""

    extension = [
        'pymdownx.snippets', 'pymdownx.superfences'
    ]

    extension_configs = {
        'pymdownx.snippets': {
            'base_path': [os.path.join(BASE, '_snippets')],
            'dedent_subsections': True
        }
    }

    def test_dedent_section(self):
        """Test dedenting sections."""

        self.check_markdown(
            R'''
            ```text
            ---8<--- "indented.txt:py-section"
            ```
            ''',
            R'''
            <div class="highlight"><pre><span></span><code>def some_method(self, param):
                """Docstring."""

                return param
            </code></pre></div>
            ''',
            True
        )

    def test_dedent_lines(self):
        """Test dedenting lines."""

        self.check_markdown(
            R'''
            ```text
            ---8<--- "indented.txt:5:8"
            ```
            ''',
            R'''
            <div class="highlight"><pre><span></span><code>def some_method(self, param):
                """Docstring."""

                return param
            </code></pre></div>
            ''',
            True
        )

    def test_dedent_indented(self):
        """Test dedenting sections that has indented insertion."""

        self.check_markdown(
            R'''
            Paragraph

                ---8<--- "indented.txt:py-section"
            ''',
            R'''
            <p>Paragraph</p>
            <pre><code>def some_method(self, param):
                """Docstring."""

                return param
            </code></pre>
            ''',
            True
        )


class TestSnippets(util.MdCase):
    """Test snippet cases."""

    extension = [
        'pymdownx.snippets', 'pymdownx.superfences'
    ]

    extension_configs = {
        'pymdownx.snippets': {
            'base_path': [os.path.join(BASE, '_snippets')]
        }
    }

    def test_inline(self):
        """Test inline."""

        self.check_markdown(
            R'''
            ---8<--- "loop.txt"
            ---8<--- "a.txt"
            ---8<--- "b.txt"
            ;---8<--- "b.txt"

            - Testing indentation

                ---8<--- "b.txt"
            ''',
            R'''
            <p>Snippet</p>
            <p>Snippet</p>
            <p>---8&lt;--- "b.txt"</p>
            <ul>
            <li>
            <p>Testing indentation</p>
            <p>Snippet</p>
            </li>
            </ul>
            ''',
            True
        )

    def test_block(self):
        """Test block."""

        self.check_markdown(
            R'''
            ---8<---
            loop_block.txt
            c.txt

            d.txt
            ---8<---

            ;---8<---
            d.txt
            ;---8<---

            - Testing indentation

                ---8<---
                d.txt

                ; d.txt
                # Nested inline won't work
                --8<-- "a.txt"
                --8<-- "; b.txt"
                ---8<---

                # Un-nested Inline
                --8<-- "a.txt"
                --8<-- "; b.txt"
            ''',
            R'''
            <p>Snippet</p>
            <p>Snippet</p>
            <p>---8&lt;---
            d.txt
            ---8&lt;---</p>
            <ul>
            <li>
            <p>Testing indentation</p>
            <p>Snippet</p>
            <h1>Un-nested Inline</h1>
            <p>Snippet</p>
            </li>
            </ul>
            ''',
            True
        )

    def test_mixed(self):
        """Test mixed."""

        self.check_markdown(
            R'''
            ---8<--- "a.txt"

            ---8<---
            loop_block.txt
            c.txt

            d.txt
            ---8<---
            ''',
            R'''
            <p>Snippet</p>
            <p>Snippet</p>
            <p>Snippet</p>
            ''',
            True
        )

    def test_start_line_inline(self):
        """Test starting line with inline syntax."""

        self.check_markdown(
            R'''
            ---8<--- "lines.txt:4"
            ''',
            '''
            <p>Content resides on various lines.
            If we use line specifiers,
            we can select any number of lines we want.</p>
            <p>This is the end of the file.
            There is no more.</p>
            ''',
            True
        )

    def test_start_1_1(self):
        """Test beginning of file, single line range."""

        self.check_markdown(
            R'''
            ---8<--- "lines.txt:1:1"
            ''',
            '''
            <p>This is a multi-line</p>
            ''',
            True
        )

    def test_start_1_2(self):
        """Test beginning of file span of multiple lines."""

        self.check_markdown(
            R'''
            ---8<--- "lines.txt:1:2"
            ''',
            '''
            <p>This is a multi-line
            snippet.</p>
            ''',
            True
        )

    def test_start_multi(self):
        """Test multiple line specifiers."""

        self.check_markdown(
            R'''
            ---8<--- "lines.txt:1:2,8:9"
            ''',
            '''
            <p>This is a multi-line
            snippet.
            This is the end of the file.
            There is no more.</p>
            ''',
            True
        )

    def test_start_multi_no_end(self):
        """Test multiple line specifiers but the last has no end."""

        self.check_markdown(
            R'''
            ---8<--- "lines.txt:1:2,8"
            ''',
            '''
            <p>This is a multi-line
            snippet.
            This is the end of the file.
            There is no more.</p>
            ''',
            True
        )

    def test_start_multi_no_start(self):
        """Test multiple line specifiers but the last has no start."""

        self.check_markdown(
            R'''
            ---8<--- "lines.txt:1:2,:8"
            ''',
            '''
            <p>This is a multi-line
            snippet.
            This is a multi-line
            snippet.</p>
            <p>Content resides on various lines.
            If we use line specifiers,
            we can select any number of lines we want.</p>
            <p>This is the end of the file.</p>
            ''',
            True
        )

    def test_start_multi_hanging_comma(self):
        """Test multiple line specifiers but there is a hanging comma."""

        self.check_markdown(
            R'''
            ---8<--- "lines.txt:1:2,"
            ''',
            '''
            ''',
            True
        )

    def test_negative_range(self):
        """Test negative indexing range."""

        self.check_markdown(
            R'''
            ---8<--- "lines.txt:-3:-2"
            ''',
            '''
            <p>This is the end of the file.
            There is no more.</p>
            ''',
            True
        )

    def test_negative_single(self):
        """Test negative indexing single line."""

        self.check_markdown(
            R'''
            ---8<--- "lines.txt:-2:-2"
            ''',
            '''
            <p>There is no more.</p>
            ''',
            True
        )

    def test_mixed_negative(self):
        """Test negative indexing single line."""

        self.check_markdown(
            R'''
            ---8<--- "lines.txt:8:-2"

            ---8<--- "lines.txt:-3:9"
            ''',
            '''
            <p>This is the end of the file.
            There is no more.</p>
            <p>This is the end of the file.
            There is no more.</p>
            ''',
            True
        )

    def test_start_negative_multi(self):
        """Test multiple line specifiers with negative indexes."""

        self.check_markdown(
            R'''
            ---8<--- "lines.txt:1:2,-3:-2"
            ''',
            '''
            <p>This is a multi-line
            snippet.
            This is the end of the file.
            There is no more.</p>
            ''',
            True
        )

    def test_end_line_inline(self):
        """Test ending line with inline syntax."""

        self.check_markdown(
            R'''
            ---8<--- "lines.txt::6"
            ''',
            '''
            <p>This is a multi-line
            snippet.</p>
            <p>Content resides on various lines.
            If we use line specifiers,
            we can select any number of lines we want.</p>
            ''',
            True
        )

    def test_start_end_line_inline(self):
        """Test starting and ending line with inline syntax."""

        self.check_markdown(
            R'''
            ---8<--- "lines.txt:4:6"
            ''',
            '''
            <p>Content resides on various lines.
            If we use line specifiers,
            we can select any number of lines we want.</p>
            ''',
            True
        )

    def test_start_line_block(self):
        """Test starting line with block syntax."""

        self.check_markdown(
            R'''
            --8<--
            lines.txt:4
            --8<--
            ''',
            '''
            <p>Content resides on various lines.
            If we use line specifiers,
            we can select any number of lines we want.</p>
            <p>This is the end of the file.
            There is no more.</p>
            ''',
            True
        )

    def test_end_line_block(self):
        """Test ending line with block syntax."""

        self.check_markdown(
            R'''
            --8<--
            lines.txt::6
            --8<--
            ''',
            '''
            <p>This is a multi-line
            snippet.</p>
            <p>Content resides on various lines.
            If we use line specifiers,
            we can select any number of lines we want.</p>
            ''',
            True
        )

    def test_start_end_line_block(self):
        """Test starting and ending line with block syntax."""

        self.check_markdown(
            R'''
            --8<--
            lines.txt:4:6
            --8<--
            ''',
            '''
            <p>Content resides on various lines.
            If we use line specifiers,
            we can select any number of lines we want.</p>
            ''',
            True
        )

    def test_section_inline(self):
        """Test section partial in inline snippet."""

        self.check_markdown(
            R'''
            ```
            --8<-- "section.txt:css-section"
            ```
            ''',
            '''
            <div class="highlight"><pre><span></span><code>div {
                color: red;
            }
            </code></pre></div>
            ''',
            True
        )

    def test_section_inline_min(self):
        """Test section partial in inline snippet using minimum tokens."""

        self.check_markdown(
            R'''
            ```
            -8<- "section.txt:css-section"
            ```
            ''',
            '''
            <div class="highlight"><pre><span></span><code>div {
                color: red;
            }
            </code></pre></div>
            ''',
            True
        )

    def test_section_inline_ignore_other_section(self):
        """Test nested sections."""

        self.check_markdown(
            R'''
            ```
            -8<- "section_nested.txt:css-section"
            ```
            ''',
            '''
            <div class="highlight"><pre><span></span><code>div {
                color: red;
                background-color: white;
                padding: 16px
            }
            </code></pre></div>
            ''',
            True
        )

    def test_section_inline_escaped_other_section(self):
        """Test nested escaped sections."""

        self.check_markdown(
            R'''
            ```
            -8<- "section_nested.txt:css-section3"
            ```
            ''',
            '''
            <div class="highlight"><pre><span></span><code>div {
                color: red;
                /* --8&lt;-- [start: css-section4] */
                background-color: white;
                padding: 16px
                /* --8&lt;-- [end: css-section4] */
            }
            </code></pre></div>
            ''',
            True
        )

    def test_whole_file_with_sections(self):
        """Test whole file with sections."""

        self.check_markdown(
            R'''
            ```
            -8<- "section_nested.txt"
            ```
            ''',
            '''
            <div class="highlight"><pre><span></span><code>div {
                color: red;
                background-color: white;
                padding: 16px
            }


            div {
                color: red;
                /* --8&lt;-- [start: css-section4] */
                background-color: white;
                padding: 16px
                /* --8&lt;-- [end: css-section4] */
            }

            div {
                color: red;
                background-color: white;
                padding: 16px
            }
            </code></pre></div>
            ''',
            True
        )

    def test_section_ignore_double_start_section(self):
        """Test nested sections."""

        self.check_markdown(
            R'''
            ```
            -8<- "section_nested.txt:css-section5"
            ```
            ''',
            '''
            <div class="highlight"><pre><span></span><code>div {
                color: red;
                background-color: white;
                padding: 16px
            }
            </code></pre></div>
            ''',
            True
        )

    def test_section_block(self):
        """Test section partial in block snippet."""

        self.check_markdown(
            R'''
            --8<--
            section.txt:html-section
            --8<--
            ''',
            '''
            <div><p>content</p></div>
            ''',
            True
        )

    def test_section_block_min(self):
        """Test section partial in block snippet using minimum tokens."""

        self.check_markdown(
            R'''
            -8<-
            section.txt:html-section
            -8<-
            ''',
            '''
            <div><p>content</p></div>
            ''',
            True
        )

    def test_section_end_first(self):
        """Test section when the end is specified first."""

        self.check_markdown(
            R'''
            --8<--
            section.txt:css-section2
            --8<--
            ''',
            '''
            ''',
            True
        )

    def test_section_escaped_end_before_start(self):
        """Test an escaped end before the section start."""

        self.check_markdown(
            R'''
            --8<-- "section_escaped_end_first.txt:api"
            ''',
            '''
            <p>keep me</p>
            ''',
            True
        )

    def test_section_escaped_start_before_start(self):
        """Test an escaped start before the section start."""

        self.check_markdown(
            R'''
            --8<-- "section_escaped_start_first.txt:api"
            ''',
            '''
            <p>keep me</p>
            ''',
            True
        )

    def test_section_no_end(self):
        """Test section when the end is not specified."""

        self.check_markdown(
            R'''
            --8<--
            section.txt:html-section2
            --8<--
            ''',
            '''
            <div><p>content</p></div>
            ''',
            True
        )


class _PathLikeExampleObject:
    def __fspath__(self):
        return os.path.join(BASE, '_snippets')


class TestSnippetsPathLike(util.MdCase):
    """Test snippet cases with path-like objects."""

    extension = [
        'pymdownx.snippets'
    ]

    extension_configs = {
        'pymdownx.snippets': {
            'base_path': _PathLikeExampleObject()
        }
    }

    def test_inline(self):
        """Test inline."""

        self.check_markdown(
            R'''
            ---8<--- "a.txt"
            ''',
            R'''
            <p>Snippet</p>
            ''',
            True
        )



class TestSnippetsFile(util.MdCase):
    """Test snippet file case."""

    extension = [
        'pymdownx.snippets',
    ]

    extension_configs = {
        'pymdownx.snippets': {
            'base_path': os.path.join(BASE, '_snippets', 'b.txt')
        }
    }

    def test_user(self):
        """Test file."""

        self.check_markdown(
            R'''
            --8<-- "b.txt"
            ''',
            '''
            <p>Snippet</p>
            ''',
            True
        )


class TestSnippetsNested(util.MdCase):
    """Test nested restriction."""

    extension = [
        'pymdownx.snippets',
    ]

    extension_configs = {
        'pymdownx.snippets': {
            'base_path': os.path.join(BASE, '_snippets', 'nested'),
            'check_paths': True
        }
    }

    def test_restricted(self):
        """Test file restriction."""

        with self.assertRaises(SnippetMissingError):
            self.check_markdown(
                R'''
                --8<-- "../b.txt"
                ''',
                '''
                <p>Snippet</p>
                ''',
                True
            )

    def test_restricted_directory_traversal(self):
        """Test file restriction directory traversal."""

        with self.assertRaises(SnippetMissingError):
            self.check_markdown(
                R'''
                --8<-- "../nested_b.txt"
                ''',
                '''
                <p>Snippet</p>
                ''',
                True
            )


class TestSnippetsMultiNested(util.MdCase):
    """Test multi-nested restriction."""

    extension = [
        'pymdownx.snippets',
    ]

    extension_configs = {
        'pymdownx.snippets': {
            'base_path': os.path.join(BASE),
            'check_paths': True
        }
    }

    def test_restricted_multi_nested(self):
        """Test file restriction."""

        self.check_markdown(
            R'''
            --8<-- "_snippets/b.txt"
            ''',
            '''
            <p>Snippet</p>
            ''',
            True
        )


class TestSnippetsNestedUnrestricted(util.MdCase):
    """Test nested no bounds."""

    extension = [
        'pymdownx.snippets',
    ]

    extension_configs = {
        'pymdownx.snippets': {
            'base_path': os.path.join(BASE, '_snippets', 'nested'),
            'restrict_base_path': False
        }
    }

    def test_restricted(self):
        """Test file restriction."""

        self.check_markdown(
            R'''
            --8<-- "../b.txt"
            ''',
            '''
            <p>Snippet</p>
            ''',
            True
        )

    def test_restricted_directory_traversal(self):
        """Test file restriction directory traversal."""

        self.check_markdown(
            R'''
            --8<-- "../nested_b.txt"
            ''',
            '''
            <p>Snippet</p>
            ''',
            True
        )


class TestSnippetsAutoAppend(util.MdCase):
    """Test snippet file case."""

    extension = [
        'pymdownx.snippets',
    ]

    extension_configs = {
        'pymdownx.snippets': {
            'base_path': [os.path.join(BASE, '_snippets')],
            'auto_append': ['b.txt']
        }
    }

    def test_auto_append(self):
        """Test auto append."""

        self.check_markdown(
            R'''
            Test
            ''',
            '''
            <p>Test</p>
            <p>Snippet</p>
            ''',
            True
        )


class TestSnippetsMissing(util.MdCase):
    """Test snippet file case."""

    extension = [
        'pymdownx.snippets',
    ]

    extension_configs = {
        'pymdownx.snippets': {
            'base_path': [os.path.join(BASE, '_snippets')],
            'check_paths': True
        }
    }

    def test_good(self):
        """Test found file."""

        self.check_markdown(
            '''
            --8<--- "d.txt"
            ''',
            '''
            <p>Snippet</p>
            ''',
            True
        )

    def test_top_level(self):
        """Test top level."""

        with self.assertRaises(SnippetMissingError):
            self.check_markdown(
                R'''
                --8<-- "not-here.txt"
                ''',
                '''
                ''',
                True
            )

    def test_nested(self):
        """Test nested."""

        with self.assertRaises(SnippetMissingError):
            self.check_markdown(
                R'''
                --8<-- "missing.txt"
                ''',
                '''
                ''',
                True
            )

    def test_missing_file_lines(self):
        """Test missing file with line numbers."""

        with self.assertRaises(SnippetMissingError):
            self.check_markdown(
                R'''
                --8<-- ":3:4"
                ''',
                '''
                ''',
                True
            )

    def test_missing_section(self):
        """Test missing section."""

        with self.assertRaises(SnippetMissingError):
            self.check_markdown(
                R'''
                --8<-- "section.txt:missing-section"
                ''',
                '''
                ''',
                True
            )


class TestSnippetsGracefulMissing(util.MdCase):
    """Test snippet file case."""

    extension = [
        'pymdownx.snippets',
    ]

    extension_configs = {
        'pymdownx.snippets': {
            'base_path': [os.path.join(BASE, '_snippets')]
        }
    }

    def test_top_level(self):
        """Test top level."""

        self.check_markdown(
            R'''
            --8<-- "not-here.txt"
            ''',
            '''
            ''',
            True
        )

    def test_nested(self):
        """Test nested."""

        self.check_markdown(
            R'''
            --8<-- "missing.txt"
            ''',
            '''
            ''',
            True
        )

    def test_missing_lines(self):
        """Test missing file with lines."""

        self.check_markdown(
            R'''
            --8<-- ":3:4"
            ''',
            '''
            ''',
            True
        )


class TestURLSnippets(util.MdCase):
    """Test snippet URL cases."""

    extension = [
        'pymdownx.snippets',
    ]

    extension_configs = {
        'pymdownx.snippets': {
            'base_path': [os.path.join(BASE, '_snippets')],
            'url_download': True
        }
    }

    @patch('urllib.request.urlopen')
    def test_url(self, mock_urlopen):
        """Test URL."""

        cm = MagicMock()
        cm.status = 200
        cm.code = 200
        cm.read.return_value = b'contents'
        cm.headers = {'content-length': '8'}
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        self.check_markdown(
            R'''
            --8<-- "https://test.com/myfile.md"
            ''',
            '''
            <p>contents</p>
            ''',
            True
        )

    @patch('urllib.request.urlopen')
    def test_url_nested(self, mock_urlopen):
        """Test nested URLs."""

        cm = MagicMock()
        cm.status = 200
        cm.code = 200
        cm.read.side_effect = [b'content\n\n--8<-- "https://test.com/myfile2.md"', b'other']
        cm.headers = {'content-length': '8'}
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        self.check_markdown(
            R'''
            --8<-- "https://test.com/myfile.md"
            ''',
            '''
            <p>content</p>
            <p>other</p>
            ''',
            True
        )

    @patch('urllib.request.urlopen')
    def test_url_nested_duplicatqe(self, mock_urlopen):
        """Test nested duplicate file."""

        cm = MagicMock()
        cm.status = 200
        cm.code = 200
        cm.read.side_effect = [b'content\n\n--8<-- "https://test.com/myfile.md"', b'other']
        cm.headers = {'content-length': '8'}
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        self.check_markdown(
            R'''
            --8<-- "https://test.com/myfile.md"
            ''',
            '''
            <p>content</p>
            ''',
            True
        )

    @patch('urllib.request.urlopen')
    def test_url_nested_file(self, mock_urlopen):
        """Test nested file in URL."""

        cm = MagicMock()
        cm.status = 200
        cm.code = 200
        cm.read.return_value = b'content\n\n--8<-- "b.txt"'
        cm.headers = {'content-length': '8'}
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        self.check_markdown(
            R'''
            --8<-- "https://test.com/myfile.md"
            ''',
            '''
            <p>content</p>
            ''',
            True
        )

    @patch('urllib.request.urlopen')
    def test_url_lines(self, mock_urlopen):
        """Test specifying specific lines in a URL."""

        with open('tests/test_extensions/_snippets/lines.txt', 'rb') as f:
            content = f.read()
        length = len(content)

        cm = MagicMock()
        cm.status = 200
        cm.code = 200
        cm.read.return_value = content
        cm.headers = {'content-length': length}
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        self.check_markdown(
            R'''
            --8<-- "https://test.com/myfile.md:4:6"
            ''',
            '''
            <p>Content resides on various lines.
            If we use line specifiers,
            we can select any number of lines we want.</p>
            ''',
            True
        )

    @patch('urllib.request.urlopen')
    def test_missing(self, mock_urlopen):
        """Test missing URL."""

        cm = MagicMock()
        cm.status = 404
        cm.code = 404
        cm.read.return_value = b''
        cm.headers = {'content-length': '0'}
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        self.check_markdown(
            R'''
            --8<-- "https://test.com/myfile.md"
            ''',
            '',
            True
        )

    @patch('urllib.request.urlopen')
    def test_missing_content_length(self, mock_urlopen):
        """Test missing content length header."""

        cm = MagicMock()
        cm.status = 200
        cm.code = 200
        cm.read.return_value = b''
        cm.headers = {}
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        self.check_markdown(
            R'''
            --8<-- "https://test.com/myfile.md"
            ''',
            '''
            ''',
            True
        )

    @patch('urllib.request.urlopen')
    def test_missing_content_length_too_big(self, mock_urlopen):
        """Test content length too big."""

        cm = MagicMock()
        cm.status = 200
        cm.code = 200
        cm.read.return_value = b''
        cm.headers = {'content-length': str(1024 * 1024 * 48)}
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        with self.assertRaises(ValueError):
            self.check_markdown(
                R'''
                --8<-- "https://test.com/myfile.md"
                ''',
                '''
                ''',
                True
            )

    @patch('urllib.request.urlopen')
    def test_content_too_big_no_content_length(self, mock_urlopen):
        """Test content length too big."""

        cm = MagicMock()
        cm.status = 200
        cm.code = 200
        cm.read = lambda count: b"-" * (1024 * 1024 * 48)
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        with self.assertRaises(ValueError):
            self.check_markdown(
                R'''
                --8<-- "https://test.com/myfile.md"
                ''',
                '''
                ''',
                True
            )
    @patch('urllib.request.urlopen')
    def test_content_length_zero(self, mock_urlopen):
        """Test empty content."""

        cm = MagicMock()
        cm.status = 200
        cm.code = 200
        cm.read.return_value = b''
        cm.headers = {'content-length': '0'}
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        self.check_markdown(
            R'''
            --8<-- "https://test.com/myfile.md"
            ''',
            '',
            True
        )

    @patch('urllib.request.urlopen')
    def test_url_sections(self, mock_urlopen):
        """Test specifying a section in a URL."""

        with open('tests/test_extensions/_snippets/section.txt', 'rb') as f:
            content = f.read()
        length = len(content)

        cm = MagicMock()
        cm.status = 200
        cm.code = 200
        cm.read.return_value = content
        cm.headers = {'content-length': length}
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        self.check_markdown(
            R'''
            --8<-- "https://test.com/myfile.md:html-section"
            ''',
            '''
            <div><p>content</p></div>
            ''',
            True
        )


class TestURLDedentSnippets(util.MdCase):
    """Test snippet URL cases."""

    extension = [
        'pymdownx.snippets', 'pymdownx.superfences'
    ]

    extension_configs = {
        'pymdownx.snippets': {
            'base_path': [os.path.join(BASE, '_snippets')],
            'url_download': True,
            'dedent_subsections': True
        }
    }

    @patch('urllib.request.urlopen')
    def test_url_sections(self, mock_urlopen):
        """Test specifying a section in a URL."""

        with open('tests/test_extensions/_snippets/indented.txt', 'rb') as f:
            content = f.read()
        length = len(content)

        cm = MagicMock()
        cm.status = 200
        cm.code = 200
        cm.read.return_value = content
        cm.headers = {'content-length': length}
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        self.check_markdown(
            R'''
            ```
            --8<-- "https://test.com/myfile.md:py-section"
            ```
            ''',
            '''
            <div class="highlight"><pre><span></span><code>def some_method(self, param):
                """Docstring."""

                return param
            </code></pre></div>
            ''',
            True
        )


class TestURLSnippetsNoMax(util.MdCase):
    """Test snippet URL cases no max size."""

    extension = [
        'pymdownx.snippets',
    ]

    extension_configs = {
        'pymdownx.snippets': {
            'base_path': [os.path.join(BASE, '_snippets')],
            'url_download': True,
            'url_max_size': 0
        }
    }

    @patch('urllib.request.urlopen')
    def test_content_length_zero(self, mock_urlopen):
        """Test empty content."""

        cm = MagicMock()
        cm.status = 200
        cm.code = 200
        cm.read.return_value = b'contents'
        cm.headers = {'content-length': str(1024 * 1024 * 48)}
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        self.check_markdown(
            R'''
            --8<-- "https://test.com/myfile.md"
            ''',
            '''
            <p>contents</p>
            ''',
            True
        )


class TestURLSnippetsMissing(util.MdCase):
    """Test snippet URL cases with missing URL and 'check paths'."""

    extension = [
        'pymdownx.snippets',
    ]

    extension_configs = {
        'pymdownx.snippets': {
            'base_path': [os.path.join(BASE, '_snippets')],
            'url_download': True,
            'url_max_size': 0,
            'check_paths': True
        }
    }

    @patch('urllib.request.urlopen')
    def test_missing(self, mock_urlopen):
        """Test missing URL."""

        cm = MagicMock()
        cm.status = 404
        cm.code = 404
        cm.read.return_value = b''
        cm.headers = {'content-length': '0'}
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        with self.assertRaises(SnippetMissingError):
            self.check_markdown(
                R'''
                --8<-- "https://test.com/myfile.md"
                ''',
                '',
                True
            )


class TestURLSnippetsRetry(util.MdCase):
    """Test snippet URL retry cases."""

    extension = [
        'pymdownx.snippets',
    ]
    extension_configs = {
        'pymdownx.snippets': {
            'base_path': [os.path.join(BASE, '_snippets')],
            'url_download': True,
            'check_paths': True
        }
    }

    @patch('urllib.request.urlopen')
    @patch('time.sleep')
    def test_successful_retry(self, mock_sleep, mock_urlopen):
        """Test successful retry after 429."""

        cm = MagicMock()
        cm.status = 200
        cm.code = 200
        cm.read.return_value = b'content\n'
        cm.headers = {'content-length': '8'}
        cm.__enter__.return_value = cm
        cm.__exit__.return_value = None  # Mock __exit__

        mock_urlopen.side_effect = [
            urllib.error.HTTPError('http://example.com', 429, 'Too Many Requests', {}, None),
            urllib.error.HTTPError('http://example.com', 429, 'Too Many Requests', {}, None),
            cm
        ]

        self.check_markdown(
            R'''
            --8<-- "http://example.com"
            ''',
            '''
            <p>content</p>
            ''',
            True
        )

        mock_sleep.assert_any_call(2)
        mock_sleep.assert_any_call(4)

    @patch('urllib.request.urlopen')
    @patch('time.sleep')
    def test_exhaust_retries(self, mock_sleep, mock_urlopen):
        """Test exhausting all retries."""

        mock_urlopen.side_effect = [
            urllib.error.HTTPError('http://example.com', 429, 'Too Many Requests', {}, None),
            urllib.error.HTTPError('http://example.com', 429, 'Too Many Requests', {}, None),
            urllib.error.HTTPError('http://example.com', 429, 'Too Many Requests', {}, None),
            urllib.error.HTTPError('http://example.com', 429, 'Too Many Requests', {}, None),
        ]

        with self.assertRaises(SnippetMissingError) as cm:
            self.md.convert(
                R'''
                --8<-- "http://example.com"
                '''
            )

        self.assertIn("Cannot download snippet 'http://example.com' (HTTP Error 429)", str(cm.exception))

        mock_sleep.assert_any_call(2)
        mock_sleep.assert_any_call(4)
        mock_sleep.assert_any_call(6)


class TestURLSnippetsRetryCustomBackoff(util.MdCase):
    """Test snippet URL retry cases with custom backoff."""

    extension = [
        'pymdownx.snippets',
    ]
    extension_configs = {
        'pymdownx.snippets': {
            'base_path': [os.path.join(BASE, '_snippets')],
            'url_download': True,
            'backoff_factor': 1.5,
            'check_paths': True
        }
    }

    @patch('urllib.request.urlopen')
    @patch('time.sleep')
    def test_custom_backoff(self, mock_sleep, mock_urlopen):
        """Test custom backoff factor."""

        cm = MagicMock()
        cm.status = 200
        cm.code = 200
        cm.read.return_value = b'content\n'
        cm.headers = {'content-length': '8'}
        cm.__enter__.return_value = cm
        cm.__exit__.return_value = None  # Mock __exit__

        mock_urlopen.side_effect = [
            urllib.error.HTTPError('http://example.com', 429, 'Too Many Requests', {}, None),
            cm
        ]

        self.check_markdown(
            R'''
            --8<-- "http://example.com"
            ''',
            '''
            <p>content</p>
            ''',
            True
        )

        mock_sleep.assert_called_once_with(1.5)


class TestURLSnippetsRetryCustomRetries(util.MdCase):
    """Test snippet URL retry cases with custom retries."""

    extension = [
        'pymdownx.snippets',
    ]
    extension_configs = {
        'pymdownx.snippets': {
            'base_path': [os.path.join(BASE, '_snippets')],
            'url_download': True,
            'max_retries': 2,
            'check_paths': True
        }
    }

    @patch('urllib.request.urlopen')
    @patch('time.sleep')
    def test_custom_max_retries(self, mock_sleep, mock_urlopen):
        """Test custom max retries."""

        mock_urlopen.side_effect = [
            urllib.error.HTTPError('http://example.com', 429, 'Too Many Requests', {}, None),
            urllib.error.HTTPError('http://example.com', 429, 'Too Many Requests', {}, None),
            urllib.error.HTTPError('http://example.com', 429, 'Too Many Requests', {}, None),
        ]

        with self.assertRaises(SnippetMissingError) as cm:
            self.md.convert(
                R'''
                --8<-- "http://example.com"
                '''
            )
        self.assertIn("Cannot download snippet 'http://example.com' (HTTP Error 429)", str(cm.exception))

        mock_sleep.assert_any_call(2)
        mock_sleep.assert_any_call(4)


class TestSnippetsLinear(util.MdCase):
    """
    Test that long lines and paths are handled and give the same results as the regular expressions we replaced.

    These inputs are long enough that a quadratic implementation takes seconds instead of milliseconds. We do not
    assert on timing, as that is unreliable, so a regression would show up as a very slow test.
    """

    extension = ['pymdownx.snippets']
    extension_configs = {'pymdownx.snippets': {'base_path': [os.path.join(BASE, '_snippets')]}}

    # The section pattern as it was before skipping positions that can't be the shortest match.
    REFERENCE_SECTION = re.compile(
        r'''(?xi)
        ^(?P<pre>.*?)
        (?P<escape>;*)
        (?P<inline_marker>-{1,}8<-{1,}[ \t]+)
        (?P<section>\[[ \t]*(?P<type>start|end)[ \t]*:[ \t]*(?P<name>[a-z][-_0-9a-z]*)[ \t]*\])
        (?P<post>.*?)$
        '''
    )

    def setUp(self):
        """Setup."""

        super().setUp()
        self.preprocessor = self.md.preprocessors['snippet']

    def test_split_path_known(self):
        """Test splitting known paths."""

        for path, expected in (
            ('a/b.md', ('a/b.md', None, None)),
            ('a/b.md:10:20', ('a/b.md', ':10:20', None)),
            ('a/b.md:1:5,10:20,30:', ('a/b.md', ':1:5,10:20,30:', None)),
            ('a/b.md:-3:-1', ('a/b.md', ':-3:-1', None)),
            ('a/b.md:section-name_1', ('a/b.md', None, ':section-name_1')),
            ('a/b.md:SECTION', ('a/b.md', None, ':SECTION')),
            ('C:/dir/b.md:3', ('C:/dir/b.md', ':3', None)),
            ('a:1:2:3', ('a:1', ':2:3', None)),
            ('a:1,', ('a:1,', None, None)),
            ('a:b:c', ('a:b', None, ':c')),
            (':3', ('', ':3', None)),
            # Paths with newlines defer to the regular expression, which does not match them
            ('a:1\n:2', None),
        ):
            with self.subTest(path=path):
                self.assertEqual(self.preprocessor.split_path(path), expected)

    def test_split_path_matches_regex(self):
        """Test the linear split gives the same result as the regular expression."""

        rng = random.Random(11)
        alphabets = (
            ['a', '.', '/', ':', '-', ',', '1', '2', 'x', 's', '_'],
            [':', ',', '-', '1', '2'],
            # Includes characters that only match `[a-z]` due to case folding, other numerals, and newlines
            [':', ',', '1', 'a', '-', 'A', '_', '9', ' ', '\n', '\r', '\u017f', '\u212a', '\u00e9', '\u0663'],
        )
        for alphabet in alphabets:
            for _ in range(20000):
                path = ''.join(rng.choice(alphabet) for _ in range(rng.randint(0, 14)))
                m = SnippetPreprocessor.RE_SNIPPET_FILE.match(path)
                expected = None if m is None else m.groups()
                self.assertEqual(self.preprocessor.split_path(path), expected, repr(path))

    def test_split_path_long(self):
        """Test splitting long paths."""

        path = 'a' + ':1,' * 6000 + 'x'
        self.assertEqual(self.preprocessor.split_path(path), (path, None, None))

        path = 'a' + ':1,' * 6000 + '1:5'
        self.assertEqual(self.preprocessor.split_path(path), ('a', path[1:], None))

    def test_section_matches_reference(self):
        """Test the section pattern matches exactly what it did before."""

        rng = random.Random(7)
        tokens = [
            ';', '-', '--', '8<-', '8<--', ' ', '\t', '[start:a]', '[end:b1]', '[Start : x ]', '[', ']', 'a', 'x',
            ':', '-8<- ', ';-8<- ', '\r', 'START'
        ]
        found = 0
        for _ in range(100000):
            line = ''.join(rng.choice(tokens) for _ in range(rng.randint(0, 9)))
            expected = self.REFERENCE_SECTION.match(line)
            actual = self.preprocessor.match_section(line)
            self.assertEqual(
                None if actual is None else actual.groupdict(),
                None if expected is None else expected.groupdict(),
                repr(line)
            )
            found += expected is not None
        # Make sure we are actually exercising matches
        self.assertGreater(found, 1000)

    def test_long_runs_in_content(self):
        """Test long runs of `;` and `-` in content."""

        for line in (';' * 20000, '-' * 20000, '-' * 20000 + '8<-x', ';' * 20000 + '-8<-x'):
            with self.subTest(line=line[:12], length=len(line)):
                html = markdown.markdown(line, extensions=['pymdownx.snippets'])
                # Content is left alone (a line of only `-` is a horizontal rule)
                self.assertTrue(html == '<hr />' or line[:10] in html)

    def test_long_runs_in_section_extraction(self):
        """Test long runs of `;` in a snippet file when extracting a section."""

        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, 'long.md'), 'w', encoding='utf-8') as f:
                f.write(f'-8<- [start:s]\n{";" * 20000}\nkept\n-8<- [end:s]\n')
            html = markdown.markdown(
                '-8<- "long.md:s"',
                extensions=['pymdownx.snippets'],
                extension_configs={'pymdownx.snippets': {'base_path': [d]}}
            )
            self.assertIn('kept', html)


class TestSnippetBasePaths(util.MdCase):
    """Test base paths are only checked once per run."""

    def test_checked_once_per_run(self):
        """Test base paths are not checked again for every snippet."""

        with tempfile.TemporaryDirectory() as d:
            for name in ('one', 'two'):
                os.makedirs(os.path.join(d, name))
            with open(os.path.join(d, 'two', 'file.md'), 'w', encoding='utf-8') as f:
                f.write('found\n')

            md = markdown.Markdown(
                extensions=['pymdownx.snippets'],
                extension_configs={
                    'pymdownx.snippets': {
                        'base_path': [os.path.join(d, 'one'), os.path.join(d, 'two'), os.path.join(d, 'missing')]
                    }
                }
            )
            with patch('pymdownx.snippets.os.path.isdir', wraps=os.path.isdir) as isdir:
                html = md.convert('\n\n'.join('-8<- "file.md"' for _ in range(10)))

            self.assertEqual(html.count('found'), 10)
            # Only the two bases that exist are checked, and only once
            self.assertEqual(isdir.call_count, 2)

    def test_checked_again_each_run(self):
        """Test a base path that appears between runs is found."""

        with tempfile.TemporaryDirectory() as d:
            base = os.path.join(d, 'base')
            md = markdown.Markdown(
                extensions=['pymdownx.snippets'],
                extension_configs={'pymdownx.snippets': {'base_path': [base]}}
            )
            self.assertNotIn('found', md.reset().convert('-8<- "file.md"'))

            os.makedirs(base)
            with open(os.path.join(base, 'file.md'), 'w', encoding='utf-8') as f:
                f.write('found\n')
            self.assertIn('found', md.reset().convert('-8<- "file.md"'))

            # And is dropped again if it disappears
            os.remove(os.path.join(base, 'file.md'))
            os.rmdir(base)
            self.assertNotIn('found', md.reset().convert('-8<- "file.md"'))

    def test_file_base_path(self):
        """Test a base path that is a file only allows that file."""

        with tempfile.TemporaryDirectory() as d:
            for name in ('file.md', 'other.md'):
                with open(os.path.join(d, name), 'w', encoding='utf-8') as f:
                    f.write(f'{name[:-3]} content\n')

            md = markdown.Markdown(
                extensions=['pymdownx.snippets'],
                extension_configs={'pymdownx.snippets': {'base_path': [os.path.join(d, 'file.md')]}}
            )
            html = md.convert('-8<- "file.md"\n\n-8<- "other.md"')
            self.assertIn('file content', html)
            self.assertNotIn('other content', html)


class TestURLFailures(util.MdCase):
    """Test that a URL that fails is only requested once per run."""

    URL = 'https://test.com/missing.md'

    def make(self, check_paths=False):
        """Make a Markdown object."""

        return markdown.Markdown(
            extensions=['pymdownx.snippets'],
            extension_configs={
                'pymdownx.snippets': {
                    'base_path': [os.path.join(BASE, '_snippets')],
                    'url_download': True,
                    'check_paths': check_paths
                }
            }
        )

    @staticmethod
    def ok(content):
        """Make a successful response."""

        cm = MagicMock()
        cm.status = 200
        cm.code = 200
        cm.read.return_value = content
        cm.headers = {'content-length': str(len(content))}
        cm.__enter__.return_value = cm
        return cm

    @patch('urllib.request.urlopen')
    def test_failure_requested_once(self, mock_urlopen):
        """Test a failing URL is not requested again for every include."""

        mock_urlopen.side_effect = urllib.error.HTTPError(self.URL, 404, 'Not Found', {}, None)

        html = self.make().convert('\n\n'.join(f'--8<-- "{self.URL}"' for _ in range(10)))

        self.assertEqual(html, '')
        self.assertEqual(mock_urlopen.call_count, 1)

    @patch('time.sleep')
    @patch('urllib.request.urlopen')
    def test_rate_limited_failure_retried_once(self, mock_urlopen, mock_sleep):
        """Test the retries and waiting for a rate limited URL are not repeated for every include."""

        mock_urlopen.side_effect = urllib.error.HTTPError(self.URL, 429, 'Too Many Requests', {}, None)

        self.make().convert('\n\n'.join(f'--8<-- "{self.URL}"' for _ in range(5)))

        # The first attempt and three retries, and only once
        self.assertEqual(mock_urlopen.call_count, 4)
        self.assertEqual(mock_sleep.call_count, 3)

    @patch('urllib.request.urlopen')
    def test_failure_does_not_affect_other_urls(self, mock_urlopen):
        """Test a failing URL does not stop other URLs, including repeats of those that work."""

        def urlopen(request, timeout=None):
            if request.full_url == self.URL:
                raise urllib.error.HTTPError(self.URL, 404, 'Not Found', {}, None)
            return self.ok(b'contents')

        mock_urlopen.side_effect = urlopen

        html = self.make().convert(
            f'--8<-- "{self.URL}"\n\n--8<-- "https://test.com/ok.md"\n\n--8<-- "{self.URL}"\n\n'
            '--8<-- "https://test.com/ok.md"'
        )

        self.assertEqual(html.count('contents'), 2)
        # The missing URL once and the good URL once (it is cached)
        self.assertEqual(mock_urlopen.call_count, 2)

    @patch('urllib.request.urlopen')
    def test_failure_retried_next_run(self, mock_urlopen):
        """Test a URL that failed is tried again in the next run, as it may be available now."""

        md = self.make()

        mock_urlopen.side_effect = urllib.error.HTTPError(self.URL, 404, 'Not Found', {}, None)
        self.assertEqual(md.convert(f'--8<-- "{self.URL}"\n\n--8<-- "{self.URL}"'), '')
        self.assertEqual(mock_urlopen.call_count, 1)

        mock_urlopen.side_effect = None
        mock_urlopen.return_value = self.ok(b'contents')
        self.assertEqual(
            md.reset().convert(f'--8<-- "{self.URL}"\n\n--8<-- "{self.URL}"'),
            '<p>contents</p>\n<p>contents</p>'
        )
        self.assertEqual(mock_urlopen.call_count, 2)

    @patch('urllib.request.urlopen')
    def test_failure_raises_with_check_paths(self, mock_urlopen):
        """Test `check_paths` still raises on the first failure."""

        mock_urlopen.side_effect = urllib.error.HTTPError(self.URL, 404, 'Not Found', {}, None)

        with self.assertRaises(SnippetMissingError):
            self.make(check_paths=True).convert(f'--8<-- "{self.URL}"\n\n--8<-- "{self.URL}"')

        self.assertEqual(mock_urlopen.call_count, 1)


class RetryAfterCase(util.MdCase):
    """Helpers for testing the `Retry-After` header."""

    URL = 'http://example.com'

    extension = ['pymdownx.snippets']
    extension_configs = {
        'pymdownx.snippets': {
            'base_path': [os.path.join(BASE, '_snippets')],
            'url_download': True,
            'check_paths': True
        }
    }

    def limited(self, retry_after=None):
        """Make a 429 response with an optional `Retry-After`."""

        headers = {} if retry_after is None else {'Retry-After': retry_after}
        return urllib.error.HTTPError(self.URL, 429, 'Too Many Requests', headers, None)

    @staticmethod
    def ok():
        """Make a successful response."""

        cm = MagicMock()
        cm.status = 200
        cm.code = 200
        cm.read.return_value = b'content\n'
        cm.headers = {'content-length': '8'}
        cm.__enter__.return_value = cm
        cm.__exit__.return_value = None
        return cm

    def convert(self):
        """Convert a document that includes the URL."""

        return self.md.convert(f'--8<-- "{self.URL}"')


class TestURLSnippetsRetryAfter(RetryAfterCase):
    """Test that the `Retry-After` header is respected when we are rate limited (default 3 retries, 2 second factor)."""

    @patch('urllib.request.urlopen')
    @patch('time.sleep')
    def test_seconds_used_instead_of_backoff(self, mock_sleep, mock_urlopen):
        """Test a number of seconds from the server is used in place of our own backoff."""

        mock_urlopen.side_effect = [self.limited('1'), self.limited(' 5 '), self.ok()]

        self.assertEqual(self.convert(), '<p>content</p>')
        self.assertEqual([c.args[0] for c in mock_sleep.call_args_list], [1, 5])

    @patch('urllib.request.urlopen')
    @patch('time.sleep')
    def test_longer_than_we_would_wait_fails_fast(self, mock_sleep, mock_urlopen):
        """Test we give up immediately when asked to wait longer than the most we would wait ourselves."""

        mock_urlopen.side_effect = [self.limited('7'), self.ok()]

        with self.assertRaises(SnippetMissingError) as cm:
            self.convert()

        self.assertIn('HTTP Error 429', str(cm.exception))
        self.assertIn('7 seconds', str(cm.exception))
        self.assertEqual(mock_urlopen.call_count, 1)
        mock_sleep.assert_not_called()

    @patch('urllib.request.urlopen')
    @patch('time.sleep')
    def test_limit_is_the_longest_backoff(self, mock_sleep, mock_urlopen):
        """Test that asking for exactly the longest we would wait (6 seconds by default) is allowed."""

        mock_urlopen.side_effect = [self.limited('6'), self.ok()]

        self.assertEqual(self.convert(), '<p>content</p>')
        mock_sleep.assert_called_once_with(6)

    @staticmethod
    def fixed_now():
        """Fix what the current time is when working out how long a date is from now."""

        class Now(datetime.datetime):
            """Fixed time."""

            @classmethod
            def now(cls, tz=None):
                """Get the fixed time."""

                return datetime.datetime(2015, 10, 21, 7, 28, 0, tzinfo=tz)

        return patch('pymdownx.snippets.datetime', SimpleNamespace(datetime=Now, timezone=datetime.timezone))

    @patch('urllib.request.urlopen')
    @patch('time.sleep')
    def test_http_date(self, mock_sleep, mock_urlopen):
        """Test a date from the server is how long to wait from now."""

        mock_urlopen.side_effect = [self.limited('Wed, 21 Oct 2015 07:28:05 GMT'), self.ok()]

        with self.fixed_now():
            self.assertEqual(self.convert(), '<p>content</p>')
        mock_sleep.assert_called_once_with(5)

    @patch('urllib.request.urlopen')
    @patch('time.sleep')
    def test_http_date_time_zones(self, mock_sleep, mock_urlopen):
        """Test dates without a time zone, or with a different one, are worked out in UTC (the time is 07:28:00)."""

        for date in (
            # No time zone, or an unknown one (`-0000`), are treated as UTC
            'Wed, 21 Oct 2015 07:28:05',
            'Wed, 21 Oct 2015 07:28:05 -0000',
            # The same moment in time zones with offsets
            'Wed, 21 Oct 2015 09:28:05 +0200',
            'Wed, 21 Oct 2015 02:28:05 -0500',
        ):
            with self.subTest(date=date):
                mock_sleep.reset_mock()
                mock_urlopen.side_effect = [self.limited(date), self.ok()]

                with self.fixed_now():
                    self.assertEqual(self.md.reset().convert(f'--8<-- "{self.URL}"'), '<p>content</p>')
                mock_sleep.assert_called_once_with(5)

    @patch('urllib.request.urlopen')
    @patch('time.sleep')
    def test_http_date_in_the_past(self, mock_sleep, mock_urlopen):
        """Test a date that has already passed means we do not need to wait."""

        mock_urlopen.side_effect = [self.limited('Wed, 21 Oct 2015 07:27:00 GMT'), self.ok()]

        with self.fixed_now():
            self.assertEqual(self.convert(), '<p>content</p>')
        mock_sleep.assert_called_once_with(0)

    @patch('urllib.request.urlopen')
    @patch('time.sleep')
    def test_http_date_too_far_away(self, mock_sleep, mock_urlopen):
        """Test a date further away than we would wait fails fast."""

        mock_urlopen.side_effect = [self.limited('Wed, 21 Oct 2015 07:29:00 GMT'), self.ok()]

        with self.fixed_now(), self.assertRaises(SnippetMissingError) as cm:
            self.convert()

        self.assertIn('60 seconds', str(cm.exception))
        self.assertEqual(mock_urlopen.call_count, 1)
        mock_sleep.assert_not_called()

    @patch('urllib.request.urlopen')
    @patch('time.sleep')
    def test_unusable_values_use_backoff(self, mock_sleep, mock_urlopen):
        """Test values we cannot use fall back to our own backoff."""

        mock_urlopen.side_effect = [
            self.limited('soon'),
            self.limited(''),
            self.limited('-5'),
            self.limited('1.5'),
        ]

        with self.assertRaises(SnippetMissingError):
            self.convert()

        # All four attempts were made, and we waited using our own backoff
        self.assertEqual(mock_urlopen.call_count, 4)
        self.assertEqual([c.args[0] for c in mock_sleep.call_args_list], [2, 4, 6])

    @patch('urllib.request.urlopen')
    @patch('time.sleep')
    def test_no_header(self, mock_sleep, mock_urlopen):
        """Test no header, and no headers at all, still use our own backoff."""

        error = urllib.error.HTTPError(self.URL, 429, 'Too Many Requests', None, None)
        mock_urlopen.side_effect = [error, self.limited(), self.ok()]

        self.assertEqual(self.convert(), '<p>content</p>')
        self.assertEqual([c.args[0] for c in mock_sleep.call_args_list], [2, 4])

    @patch('urllib.request.urlopen')
    @patch('time.sleep')
    def test_real_headers_are_case_insensitive(self, mock_sleep, mock_urlopen):
        """Test headers from a real response, which are not case sensitive like a `dict`, are found."""

        for name in ('retry-after', 'RETRY-AFTER', 'Retry-After'):
            with self.subTest(name=name):
                mock_sleep.reset_mock()
                headers = HTTPMessage()
                headers[name] = '3'
                mock_urlopen.side_effect = [
                    urllib.error.HTTPError(self.URL, 429, 'Too Many Requests', headers, None),
                    self.ok()
                ]

                self.assertEqual(self.md.reset().convert(f'--8<-- "{self.URL}"'), '<p>content</p>')
                mock_sleep.assert_called_once_with(3)

    @patch('urllib.request.urlopen')
    @patch('time.sleep')
    def test_fail_fast_is_only_requested_once(self, mock_sleep, mock_urlopen):
        """Test a URL we gave up on because of the server's request is not tried again when included again."""

        mock_urlopen.side_effect = self.limited('60')
        md = markdown.Markdown(
            extensions=['pymdownx.snippets'],
            extension_configs={
                'pymdownx.snippets': {
                    'base_path': [os.path.join(BASE, '_snippets')],
                    'url_download': True,
                    'check_paths': False
                }
            }
        )

        self.assertEqual(md.convert('\n\n'.join(f'--8<-- "{self.URL}"' for _ in range(5))), '')
        self.assertEqual(mock_urlopen.call_count, 1)
        mock_sleep.assert_not_called()

    @patch('urllib.request.urlopen')
    @patch('time.sleep')
    def test_only_for_429(self, mock_sleep, mock_urlopen):
        """Test other responses with a `Retry-After`, such as 503, are not retried."""

        mock_urlopen.side_effect = [
            urllib.error.HTTPError(self.URL, 503, 'Service Unavailable', {'Retry-After': '1'}, None),
            self.ok()
        ]

        with self.assertRaises(SnippetMissingError) as cm:
            self.convert()

        self.assertIn('HTTP Error 503', str(cm.exception))
        self.assertEqual(mock_urlopen.call_count, 1)
        mock_sleep.assert_not_called()


class TestURLSnippetsRetryAfterNoBackoff(RetryAfterCase):
    """Test `Retry-After` when we are configured never to wait."""

    extension_configs = {
        'pymdownx.snippets': {
            'base_path': [os.path.join(BASE, '_snippets')],
            'url_download': True,
            'check_paths': True,
            'backoff_factor': 0
        }
    }

    @patch('urllib.request.urlopen')
    @patch('time.sleep')
    def test_retry_after_fails_fast(self, mock_sleep, mock_urlopen):
        """Test any `Retry-After` is longer than we would wait, so we give up instead of retrying right away."""

        mock_urlopen.side_effect = [self.limited('1'), self.ok()]

        with self.assertRaises(SnippetMissingError) as cm:
            self.convert()

        self.assertIn('server asked to wait 1 seconds', str(cm.exception))
        self.assertEqual(mock_urlopen.call_count, 1)
        mock_sleep.assert_not_called()

    @patch('urllib.request.urlopen')
    @patch('time.sleep')
    def test_no_header_retries_right_away(self, mock_sleep, mock_urlopen):
        """Test without the header we retry without waiting, as we always have."""

        mock_urlopen.side_effect = [self.limited(), self.limited(), self.ok()]

        self.assertEqual(self.convert(), '<p>content</p>')
        self.assertEqual([c.args[0] for c in mock_sleep.call_args_list], [0, 0])


class TestURLSnippetsRetryAfterCustom(RetryAfterCase):
    """Test the longest we will wait is based on our configuration."""

    extension_configs = {
        'pymdownx.snippets': {
            'base_path': [os.path.join(BASE, '_snippets')],
            'url_download': True,
            'check_paths': True,
            'max_retries': 2,
            'backoff_factor': 1
        }
    }

    @patch('urllib.request.urlopen')
    @patch('time.sleep')
    def test_limit_is_the_longest_backoff(self, mock_sleep, mock_urlopen):
        """Test the limit is now 2 seconds."""

        mock_urlopen.side_effect = [self.limited('2'), self.ok()]
        self.assertEqual(self.convert(), '<p>content</p>')
        mock_sleep.assert_called_once_with(2)

        mock_sleep.reset_mock()
        mock_urlopen.side_effect = [self.limited('3'), self.ok()]
        with self.assertRaises(SnippetMissingError):
            self.md.reset().convert(f'--8<-- "{self.URL}"')
        mock_sleep.assert_not_called()


class TestSnippetReadLines(util.MdCase):
    """Test reading a file as lines gives what reading it line by line always did."""

    extension = ['pymdownx.snippets']

    @staticmethod
    def reference(path, encoding='utf-8'):
        """Read lines the way we did before."""

        with open(path, 'r', encoding=encoding) as f:
            last = False
            lines = []
            for line in f:
                last = line.endswith(('\r', '\n'))
                lines.append(line.strip('\r\n'))
            if last:
                lines.append('')
        return lines

    def setUp(self):
        """Setup."""

        super().setUp()
        self.preprocessor = self.md.preprocessors['snippet']

    def test_known(self):
        """Test known content, including empty files and the various line endings."""

        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, 'file.txt')
            for content, expected in (
                (b'', []),
                (b'\n', ['', '']),
                (b'\r\n', ['', '']),
                (b'\r', ['', '']),
                (b'a', ['a']),
                (b'a\n', ['a', '']),
                (b'a\nb', ['a', 'b']),
                (b'a\r\nb\rc\n', ['a', 'b', 'c', '']),
                (b'\n\n\n', ['', '', '', '']),
                ('caf\u00e9\n\u4e2d'.encode(), ['caf\u00e9', '\u4e2d']),
                # Not line endings for files, even though they are for `str.splitlines`
                ('a\u2028b\x0bc\x85d\x0ce\n'.encode(), ['a\u2028b\x0bc\x85d\x0ce', ''])
            ):
                with self.subTest(content=content):
                    with open(path, 'wb') as f:
                        f.write(content)
                    self.assertEqual(self.preprocessor.read_lines(path), expected)

    def test_matches_reference(self):
        """Test random content, with all of the line endings mixed together."""

        rng = random.Random(3)
        pieces = [
            'a', 'b', ' ', '\t', '\n', '\r', '\r\n', '\n\n', '\u2028', '\x0b', '\x0c', '\x85', '\x1c', '\u00e9',
            '\u4e2d', '-8<-'
        ]
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, 'file.txt')
            for _ in range(5000):
                content = ''.join(rng.choice(pieces) for _ in range(rng.randint(0, 12)))
                with open(path, 'wb') as f:
                    f.write(content.encode('utf-8'))
                self.assertEqual(self.preprocessor.read_lines(path), self.reference(path), repr(content))

    def test_encoding(self):
        """Test the configured encoding is used."""

        md = markdown.Markdown(
            extensions=['pymdownx.snippets'], extension_configs={'pymdownx.snippets': {'encoding': 'latin-1'}}
        )
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, 'file.txt')
            with open(path, 'wb') as f:
                f.write('caf\u00e9\nline'.encode('latin-1'))
            self.assertEqual(md.preprocessors['snippet'].read_lines(path), ['caf\u00e9', 'line'])
