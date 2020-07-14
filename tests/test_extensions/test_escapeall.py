"""Test cases for BetterEm."""
from .. import util


class TestEscapeAll(util.MdCase):
    """Test escaping cases."""

    extension = [
        'pymdownx.escapeall'
    ]
    extension_configs = {}

    def test_html_special_char_lt(self):
        """Test `<`."""

        self.check_markdown(
            r'\<pre>foo',
            '<p>&lt;pre&gt;foo</p>'
        )

    def test_html_special_char_gt(self):
        """Test `>`."""

        self.check_markdown(
            r'<span\>foo',
            '<p>&lt;span&gt;foo</p>'
        )

    def test_html_special_char_amp(self):
        """Test `&`."""

        self.check_markdown(
            r'This \& that',
            '<p>This &amp; that</p>'
        )
