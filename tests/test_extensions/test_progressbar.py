"""Test cases for ProgressBar."""
from .. import util


class TestProgressBar(util.MdCase):
    """Tests for ProgressBar."""

    extension = [
        'pymdownx.progressbar'
    ]

    def test_non_decimal_separator_after_100(self):
        """Test that `100` followed by a non-dot separator is not treated as a decimal."""

        self.check_markdown(
            '[=100,0%]',
            '<p>[=100,0%]</p>'
        )
