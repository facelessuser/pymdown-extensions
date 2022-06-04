"""Test cases for Snippets."""
from .. import util
import os
from pymdownx.snippets import SnippetMissingError
from unittest.mock import patch, MagicMock

BASE = os.path.abspath(os.path.dirname(__file__))


class TestSnippets(util.MdCase):
    """Test snippet cases."""

    extension = [
        'pymdownx.snippets',
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
            ---8<--- "b.txt" 

            - Testing indentation

                ---8<--- "b.txt"
            ''',  # noqa: W291
            R'''
            <p>Snippet
            Snippet
            ---8&lt;--- "b.txt" </p>
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

            ---8<--- 
            d.txt
            ---8<--- 

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
            ---8&lt;--- </p>
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
