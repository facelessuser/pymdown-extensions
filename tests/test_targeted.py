"""Test `uniprops`."""
from pymdownx import util
from unittest import mock
from urllib.parse import urlparse as _real_urlparse
import unittest
import pytest


def _urlparse_py316(url):
    """Emulate Python 3.16's `urlparse`, which rejects an invalid port (gh-88037)."""

    parsed = _real_urlparse(url)
    netloc = parsed.netloc
    hostport = netloc.rsplit('@', 1)[-1]
    port = ''
    if hostport.startswith('['):
        end = hostport.find(']')
        if end != -1 and hostport[end + 1:end + 2] == ':':
            port = hostport[end + 2:]
    elif ':' in hostport:
        port = hostport.rsplit(':', 1)[-1]
    if port and (not port.isdigit() or not port.isascii() or not 0 <= int(port) <= 65535):
        raise ValueError(f"Port could not be cast to integer value as {port!r}")
    return parsed


class TestUrlParse(unittest.TestCase):
    """Test UrlParse."""

    def test_url(self):
        """Test URL."""

        url = 'http://www.google.com'
        scheme, netloc, _, _, _, _, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, 'http')
        self.assertEqual(netloc, 'www.google.com')
        self.assertEqual(is_url, True)
        self.assertEqual(is_absolute, False)

    def test_fragment(self):
        """Test fragment."""

        url = '#header'
        scheme, netloc, _, _, _, fragment, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, '')
        self.assertEqual(netloc, '')
        self.assertEqual(fragment, 'header')
        self.assertEqual(is_url, True)
        self.assertEqual(is_absolute, False)

    def test_file_windows(self):
        """Test file windows."""

        url = 'file://c:/path'
        scheme, _, path, _, _, _, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, 'file')
        self.assertEqual(path, '/c:/path')
        self.assertEqual(is_url, False)
        self.assertEqual(is_absolute, True)

    def test_file_windows_backslash(self):
        """Test file windows with backslash."""

        url = r'file://c:\path'
        scheme, _, path, _, _, _, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, 'file')
        self.assertEqual(path, '/c:/path')
        self.assertEqual(is_url, False)
        self.assertEqual(is_absolute, True)

    def test_file_windows_start_backslash(self):
        """Test file windows start with backslash."""

        url = r'file://\c:\path'
        scheme, _, path, _, _, _, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, 'file')
        self.assertEqual(path, '/c:/path')
        self.assertEqual(is_url, False)
        self.assertEqual(is_absolute, True)

    def test_file_windows_start_backslash_py316(self):
        """Test file windows start with backslash under Python 3.16 port validation."""

        url = r'file://\c:\path'
        with mock.patch('pymdownx.util.urlparse', _urlparse_py316):
            scheme, _, path, _, _, _, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, 'file')
        self.assertEqual(path, '/c:/path')
        self.assertEqual(is_url, False)
        self.assertEqual(is_absolute, True)

    def test_url_template_port_py316(self):
        """Test URL with a template port under Python 3.16 port validation."""

        url = 'http://localhost:{port}/'
        with mock.patch('pymdownx.util.urlparse', _urlparse_py316):
            scheme, netloc, path, _, _, _, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, 'http')
        self.assertEqual(netloc, 'localhost:{port}')
        self.assertEqual(path, '/')
        self.assertEqual(is_url, True)
        self.assertEqual(is_absolute, False)

    def test_scp_style_url_py316(self):
        """Test SCP-style URL under Python 3.16 port validation."""

        url = 'git+ssh://git@github.com:org/repo.git'
        with mock.patch('pymdownx.util.urlparse', _urlparse_py316):
            scheme, netloc, path, _, _, _, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, 'git+ssh')
        self.assertEqual(netloc, 'git@github.com:org')
        self.assertEqual(path, '/repo.git')
        self.assertEqual(is_url, True)
        self.assertEqual(is_absolute, False)

    def test_file_windows_netpath(self):
        """Test file windows netpath."""

        url = 'file://\\\\path'
        scheme, _, path, _, _, _, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, 'file')
        self.assertEqual(path, '//path')
        self.assertEqual(is_url, False)
        self.assertEqual(is_absolute, True)

    def test_nix_path(self):
        """Test file Linux/Unix path."""

        url = 'file:///path'
        scheme, _, path, _, _, _, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, 'file')
        self.assertEqual(path, '/path')
        self.assertEqual(is_url, False)
        self.assertEqual(is_absolute, True)

    def test_windows_path_forward_slash(self):
        """Test windows path."""

        url = 'c:/path'
        scheme, _, path, _, _, _, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, 'file')
        self.assertEqual(path, '/c:/path')
        self.assertEqual(is_url, False)
        self.assertEqual(is_absolute, True)

    def test_windows_path_backslash(self):
        """Test file windows path with backslash."""

        url = r'c:\path'
        scheme, _, path, _, _, _, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, 'file')
        self.assertEqual(path, '/c:/path')
        self.assertEqual(is_url, False)
        self.assertEqual(is_absolute, True)

    def test_windows_netpath_forward_slash(self):
        """Test netpath with forward slash."""

        url = '//file/path'
        scheme, _, path, _, _, _, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, 'file')
        self.assertEqual(path, '//file/path')
        self.assertEqual(is_url, False)
        self.assertEqual(is_absolute, True)

    def test_windows_netpath_backslash(self):
        """Test windows netpath with backslash."""

        url = '\\\\file\\path'
        scheme, _, path, _, _, _, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, '')
        self.assertEqual(path, '\\\\file\\path')
        self.assertEqual(is_url, False)
        self.assertEqual(is_absolute, True)

    def test_relative_path(self):
        """Test relative path."""

        url = '../file/path'
        scheme, _, path, _, _, _, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, '')
        self.assertEqual(path, '../file/path')
        self.assertEqual(is_url, False)
        self.assertEqual(is_absolute, False)

    def test_windows_relative_path(self):
        """Test windows relative with backslash."""

        url = '..\\file\\path'
        scheme, _, path, _, _, _, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, '')
        self.assertEqual(path, '..\\file\\path')
        self.assertEqual(is_url, False)
        self.assertEqual(is_absolute, False)

    def test_clamp(self):
        """Test clamp."""

        self.assertEqual(util.clamp(3, None, None), 3)
        self.assertEqual(util.clamp(3, 4, None), 4)
        self.assertEqual(util.clamp(4, 4, None), 4)
        self.assertEqual(util.clamp(4, None, 4), 4)
        self.assertEqual(util.clamp(5, None, 4), 4)
        self.assertEqual(util.clamp(3, 4, 6), 4)
        self.assertEqual(util.clamp(7, 4, 6), 6)
        self.assertEqual(util.clamp(4, 4, 6), 4)
        self.assertEqual(util.clamp(6, 4, 6), 6)


def run():
    """Run pytest."""

    pytest.main(
        [
            'tests/test_targeted.py',
            '-p', 'no:pytest_cov'
        ]
    )
