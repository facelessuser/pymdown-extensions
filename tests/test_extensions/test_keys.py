"""Test cases for Keys."""
from .. import util


class TestKeys(util.MdCase):
    """Tests for Keys."""

    extension = [
        'pymdownx.keys'
    ]

    def test_avoid_base64(self):
        """Test complex case where `**text*text***` may be detected on accident."""

        self.check_markdown(
            "![](data:image/png;base64,aaaaa++a++aaaa) ++ctrl+a++ ++ctrl+'custom'++",
            '<p><img alt="" src="data:image/png;base64,aaaaa++a++aaaa" /> <span class="keys"><kbd class="key-control">Ctrl</kbd><span>+</span><kbd class="key-a">A</kbd></span> <span class="keys"><kbd class="key-control">Ctrl</kbd><span>+</span><kbd>custom</kbd></span></p>'  # noqa: E501
        )

    def test_quoted_escaped_backslashes(self):
        """Test that each escaped backslash in a quoted key is kept."""

        self.check_markdown(
            r'++"a\\\\b"++ ++"\\\""++',
            '<p><span class="keys"><kbd>a\\\\b</kbd></span> <span class="keys"><kbd>\\"</kbd></span></p>'
        )

    def test_quoted_plus(self):
        """Test that an unescaped `+` inside a quoted key is content, not a separator."""

        self.check_markdown(
            r'''++"a+b"++ ++"+"++ ++ctrl+"+"++ ++'a+b'+x++ ++"a\+b"++''',
            '<p><span class="keys"><kbd>a+b</kbd></span> '
            '<span class="keys"><kbd>+</kbd></span> '
            '<span class="keys"><kbd class="key-control">Ctrl</kbd><span>+</span><kbd>+</kbd></span> '
            '<span class="keys"><kbd>a+b</kbd><span>+</span><kbd class="key-x">X</kbd></span> '
            '<span class="keys"><kbd>a+b</kbd></span></p>'
        )

    def test_quoted_plus_escaped_backslash(self):
        """Test that escaped backslashes next to a `+` in a quoted key follow the pair rule."""

        self.check_markdown(
            r'''++"a\\+b"++ ++"a\\\+b"++''',
            '<p><span class="keys"><kbd>a\\+b</kbd></span> <span class="keys"><kbd>a\\+b</kbd></span></p>'
        )
