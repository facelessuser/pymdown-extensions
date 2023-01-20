"""Test cases for Snippets."""
from .. import util
import os
from pymdownx.snippets import SnippetMissingError
from unittest.mock import patch, MagicMock

BASE = os.path.abspath(os.path.dirname(__file__))


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
            ''',  # noqa: W291
            R'''
            <p>Snippet
            Snippet
            ---8&lt;--- "b.txt"</p>
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
            ''',  # noqa: W291
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
            ''',  # noqa: W291
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
            --8<-- "section.txt:cssSection"
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
            -8<- "section.txt:cssSection"
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

    def test_section_block(self):
        """Test section partial in block snippet."""

        self.check_markdown(
            R'''
            --8<--
            section.txt:htmlSection
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
            section.txt:htmlSection
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
            section.txt:cssSection2
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
            section.txt:htmlSection2
            --8<--
            ''',
            '''
            <div><p>content</p></div>
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

    def test_missing_lines(self):
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
        cm.readlines.return_value = [b'contents']
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
        cm.readlines.side_effect = [[b'content', b'', b'--8<-- "https://test.com/myfile2.md"'], [b'other']]
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
        cm.readlines.side_effect = [[b'content', b'', b'--8<-- "https://test.com/myfile.md"'], [b'other']]
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
        cm.readlines.return_value = [b'content', b'', b'--8<-- "b.txt"']
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

        content = []
        length = 0
        with open('tests/test_extensions/_snippets/lines.txt', 'rb') as f:
            for l in f:
                length += len(l)
                content.append(l)

        cm = MagicMock()
        cm.status = 200
        cm.code = 200
        cm.readlines.return_value = content
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
        cm.readlines.return_value = []
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
        cm.readlines.return_value = []
        cm.headers = {}
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
    def test_missing_content_length_too_big(self, mock_urlopen):
        """Test content length too big."""

        cm = MagicMock()
        cm.status = 200
        cm.code = 200
        cm.readlines.return_value = []
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
    def test_content_length_zero(self, mock_urlopen):
        """Test empty content."""

        cm = MagicMock()
        cm.status = 200
        cm.code = 200
        cm.readlines.return_value = []
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

        content = []
        length = 0
        with open('tests/test_extensions/_snippets/section.txt', 'rb') as f:
            for l in f:
                length += len(l)
                content.append(l)

        cm = MagicMock()
        cm.status = 200
        cm.code = 200
        cm.readlines.return_value = content
        cm.headers = {'content-length': length}
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        self.check_markdown(
            R'''
            --8<-- "https://test.com/myfile.md:htmlSection"
            ''',
            '''
            <div><p>content</p></div>
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
        cm.readlines.return_value = [b'contents']
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
        cm.readlines.return_value = []
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
