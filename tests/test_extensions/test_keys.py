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
