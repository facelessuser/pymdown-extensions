"""Test cases for Blocks (details)."""
from ... import util


class TestBlocksDetails(util.MdCase):
    """Test Blocks details cases."""

    extension = ['pymdownx.blocks']

    def test_optional_title(self):
        """Test that tab is not processed if title is omitted."""

        self.check_markdown(
            R'''
            /// details

            Some *content*
            ///
            ''',
            r'''
            <details>
            <p>Some <em>content</em></p>
            </details>
            ''',  # noqa: E501
            True
        )

    def test_type_no_title(self):
        """Test test type as title."""

        self.check_markdown(
            R'''
            /// details
            type: note
            attributes:
              class: other

            Some *content*
            ///
            ''',
            r'''
            <details class="note other">
            <summary>Note</summary>
            <p>Some <em>content</em></p>
            </details>
            ''',  # noqa: E501
            True
        )

    def test_details(self):
        """Test details with title."""

        self.check_markdown(
            R'''
            /// details | A Title

            Some *content*
            ///
            ''',
            r'''
            <details>
            <summary>A Title</summary>
            <p>Some <em>content</em></p>
            </details>
            ''',  # noqa: E501
            True
        )

    def test_details_open(self):
        """Test details forced open."""

        self.check_markdown(
            R'''
            /// details | A Title
            open: true

            Some *content*
            ///
            ''',
            r'''
            <details open="open">
            <summary>A Title</summary>
            <p>Some <em>content</em></p>
            </details>
            ''',  # noqa: E501
            True
        )
