"""Test cases for Snippets."""
from .. import util
import os
from pymdownx.snippets import SnippetMissingError, SnippetPreprocessor
from unittest.mock import patch, MagicMock
import urllib.error
import time

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
                &quot;&quot;&quot;Docstring.&quot;&quot;&quot;

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
                &quot;&quot;&quot;Docstring.&quot;&quot;&quot;

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
                &quot;&quot;&quot;Docstring.&quot;&quot;&quot;

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
            'max_retries': 3,
            'backoff_factor': 2,
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
        ]

        with self.assertRaises(SnippetMissingError) as cm:
            self.md.convert(
                R'''
                --8<-- "http://example.com"
                '''
            )

        self.assertIn("Cannot download snippet 'http://example.com': HTTP Error 429", str(cm.exception))

        mock_sleep.assert_any_call(2)
        mock_sleep.assert_any_call(4)
        self.assertEqual(mock_sleep.call_count, 2)

    @patch('urllib.request.urlopen')
    @patch('time.sleep')
    def test_custom_backoff(self, mock_sleep, mock_urlopen):
        """Test custom backoff factor."""

        self.extension_configs['pymdownx.snippets']['backoff_factor'] = 1.5

        snippet_preprocessor = None
        for preprocessor in self.md.preprocessors:
            if isinstance(preprocessor, SnippetPreprocessor):
                snippet_preprocessor = preprocessor
                break

        if snippet_preprocessor:
            original_backoff = snippet_preprocessor.backoff_factor
            snippet_preprocessor.backoff_factor = 1.5
        else:
            self.fail("SnippetPreprocessor not found in Markdown preprocessors.")

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

        if snippet_preprocessor:
            snippet_preprocessor.backoff_factor = original_backoff

    @patch('urllib.request.urlopen')
    @patch('time.sleep')
    def test_custom_max_retries(self, mock_sleep, mock_urlopen):
        """Test custom max retries."""

        snippet_preprocessor = None
        for preprocessor in self.md.preprocessors:
            if isinstance(preprocessor, SnippetPreprocessor):
                snippet_preprocessor = preprocessor
                break

        if snippet_preprocessor:
            original_max_retries = snippet_preprocessor.max_retries
            snippet_preprocessor.max_retries = 2
        else:
            self.fail("SnippetPreprocessor not found in Markdown preprocessors.")

        mock_urlopen.side_effect = [
            urllib.error.HTTPError('http://example.com', 429, 'Too Many Requests', {}, None),
            urllib.error.HTTPError('http://example.com', 429, 'Too Many Requests', {}, None),
            MagicMock(status=200, code=200, read=MagicMock(return_value=b'content'), headers={'content-length': '7'}, __enter__=lambda self: self, __exit__=lambda self, *args: None)
        ]

        with self.assertRaises(SnippetMissingError) as cm:
            self.md.convert(
                R'''
                --8<-- "http://example.com"
                '''
            )
        self.assertIn("Cannot download snippet 'http://example.com': HTTP Error 429", str(cm.exception))

        mock_sleep.assert_any_call(snippet_preprocessor.backoff_factor * 1)
        self.assertEqual(mock_sleep.call_count, 1)

        if snippet_preprocessor:
            snippet_preprocessor.max_retries = original_max_retries

    @patch('urllib.request.urlopen')
    @patch('time.sleep')
    def test_other_errors_during_retry(self, mock_sleep, mock_urlopen):
        """Test handling of other errors during retry."""

        # First attempt returns 429, second returns 500
        mock_urlopen.side_effect = [
            urllib.error.HTTPError('http://example.com', 429, 'Too Many Requests', {}, None),
            urllib.error.HTTPError('http://example.com', 500, 'Server Error', {}, None)
        ]

        with self.assertRaises(SnippetMissingError) as cm:
            self.check_markdown(
                R'''
                --8<-- "http://example.com"
                ''',
                '''
                ''',
                True
            )
        self.assertIn("Cannot download snippet 'http://example.com': HTTP Error 500: Server Error", str(cm.exception))

        mock_sleep.assert_called_once_with(2)