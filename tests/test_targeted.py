"""Test uniprops."""
from __future__ import unicode_literals
from pymdownx import util
import unittest
import pytest


class TestUrlParse(unittest.TestCase):
    """Test UrlParse."""

    def test_url(self):
        """Test url."""

        url = 'http://www.google.com'
        scheme, netloc, path, params, query, fragment, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, 'http')
        self.assertEqual(netloc, 'www.google.com')
        self.assertEqual(is_url, True)
        self.assertEqual(is_absolute, False)

    def test_fragment(self):
        """Test fragment."""

        url = '#header'
        scheme, netloc, path, params, query, fragment, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, '')
        self.assertEqual(netloc, '')
        self.assertEqual(fragment, 'header')
        self.assertEqual(is_url, True)
        self.assertEqual(is_absolute, False)

    def test_file_windows(self):
        """Test file windows."""

        url = 'file://c:/path'
        scheme, netloc, path, params, query, fragment, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, 'file')
        self.assertEqual(path, '/c:/path')
        self.assertEqual(is_url, False)
        self.assertEqual(is_absolute, True)

    def test_file_windows_backslash(self):
        """Test file windows with backslash."""

        url = 'file://c:\path'
        scheme, netloc, path, params, query, fragment, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, 'file')
        self.assertEqual(path, '/c:/path')
        self.assertEqual(is_url, False)
        self.assertEqual(is_absolute, True)

    def test_file_windows_start_backslash(self):
        """Test file windows start with backslash."""

        url = 'file://\c:\path'
        scheme, netloc, path, params, query, fragment, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, 'file')
        self.assertEqual(path, '/c:/path')
        self.assertEqual(is_url, False)
        self.assertEqual(is_absolute, True)

    def test_file_windows_netpath(self):
        """Test file windows netpath."""

        url = 'file://\\\\path'
        scheme, netloc, path, params, query, fragment, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, 'file')
        self.assertEqual(path, '//path')
        self.assertEqual(is_url, False)
        self.assertEqual(is_absolute, True)

    def test_nix_path(self):
        """Test file Linux/Unix path."""

        url = 'file:///path'
        scheme, netloc, path, params, query, fragment, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, 'file')
        self.assertEqual(path, '/path')
        self.assertEqual(is_url, False)
        self.assertEqual(is_absolute, True)

    def test_windows_path_forward_slash(self):
        """Test windows path."""

        url = 'c:/path'
        scheme, netloc, path, params, query, fragment, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, 'file')
        self.assertEqual(path, '/c:/path')
        self.assertEqual(is_url, False)
        self.assertEqual(is_absolute, True)

    def test_windows_path_backslash(self):
        """Test file windows path with backslash."""

        url = 'c:\path'
        scheme, netloc, path, params, query, fragment, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, 'file')
        self.assertEqual(path, '/c:/path')
        self.assertEqual(is_url, False)
        self.assertEqual(is_absolute, True)

    def test_windows_netpath_forward_slash(self):
        """Test netpath with forward slash."""

        url = '//file/path'
        scheme, netloc, path, params, query, fragment, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, 'file')
        self.assertEqual(path, '//file/path')
        self.assertEqual(is_url, False)
        self.assertEqual(is_absolute, True)

    def test_windows_netpath_backslash(self):
        """Test windows netpath with backslash."""

        url = '\\\\file\\path'
        scheme, netloc, path, params, query, fragment, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, '')
        self.assertEqual(path, '\\\\file\\path')
        self.assertEqual(is_url, False)
        self.assertEqual(is_absolute, True)

    def test_relative_path(self):
        """Test relative path."""

        url = '../file/path'
        scheme, netloc, path, params, query, fragment, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, '')
        self.assertEqual(path, '../file/path')
        self.assertEqual(is_url, False)
        self.assertEqual(is_absolute, False)

    def test_windows_relative_path(self):
        """Test windows relative with backslash."""

        url = '..\\file\\path'
        scheme, netloc, path, params, query, fragment, is_url, is_absolute = util.parse_url(url)
        self.assertEqual(scheme, '')
        self.assertEqual(path, '..\\file\\path')
        self.assertEqual(is_url, False)
        self.assertEqual(is_absolute, False)


def run():
    """Run pytest."""

    pytest.main(
        [
            'tests/test_targeted.py',
            '-p', 'no:pytest_cov'
        ]
    )
