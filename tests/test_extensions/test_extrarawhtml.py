"""Test cases for SuperFences."""
import unittest
import markdown
from .. import util
from pymdownx.util import PymdownxDeprecationWarning
import warnings


class TestWaringings(unittest.TestCase):
    """Test warnings."""

    def test_highlight_code(self):
        """Test highlight code warning."""

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            markdown.Markdown(
                extensions=['pymdownx.extrarawhtml']
            )

            self.assertTrue(len(w) == 1)
            self.assertTrue(issubclass(w[-1].category, PymdownxDeprecationWarning))


class TestExtraRawHtml(util.MdCase):
    """Test extra raw HTML."""

    extension = ['pymdownx.extrarawhtml']
    extension_configs = {}

    def test_extrarawhtml(self):
        """Test working extra raw HTML."""

        self.check_markdown(
            r'''
            <div markdown="1">
            This **will** be processed.
            </div>
            ''',
            r'''
            <div>
            <p>This <strong>will</strong> be processed.</p>
            </div>
            ''',
            True
        )

    def test_extrarawhtml_fail(self):
        """Test working extra raw HTML will not work."""

        self.check_markdown(
            r'''
            <div>
            This will **not** be processed.
            </div>
            ''',
            r'''
            <div>
            This will **not** be processed.
            </div>
            ''',
            True
        )
