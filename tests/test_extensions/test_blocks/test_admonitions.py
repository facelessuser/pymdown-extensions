"""Test cases for Blocks (admonitions)."""
from ... import util


class TestBlocksAdmonitions(util.MdCase):
    """Test Blocks admonitions cases."""

    extension = ['pymdownx.blocks.admonition']
    extension_configs = {
        'pymdownx.blocks.admonition': {'types': ['note', 'custom']}
    }

    def test_optional_title(self):
        """Test that tab is not processed if title is omitted."""

        self.check_markdown(
            R'''
            /// admonition
            Some *content*
            ///
            ''',
            r'''
            <div class="admonition">
            <p>Some <em>content</em></p>
            </div>
            ''',  # noqa: E501
            True
        )

    def test_type_no_title(self):
        """Test test type as title."""

        self.check_markdown(
            R'''
            /// admonition
                type: note
                attrs: {class: other}

            Some *content*
            ///
            ''',
            r'''
            <div class="admonition note other">
            <p class="admonition-title">Note</p>
            <p>Some <em>content</em></p>
            </div>
            ''',  # noqa: E501
            True
        )

    def test_admonition(self):
        """Test admonition with title."""

        self.check_markdown(
            R'''
            /// admonition | A Title
            Some *content*
            ///
            ''',
            r'''
            <div class="admonition">
            <p class="admonition-title">A Title</p>
            <p>Some <em>content</em></p>
            </div>
            ''',  # noqa: E501
            True
        )

    def test_note_no_title(self):
        """Test note with no title."""

        self.check_markdown(
            R'''
            /// note
            Some *content*
            ///
            ''',
            r'''
            <div class="admonition note">
            <p class="admonition-title">Note</p>
            <p>Some <em>content</em></p>
            </div>
            ''',  # noqa: E501
            True
        )

    def test_note_with_title(self):
        """Test note with no title."""

        self.check_markdown(
            R'''
            /// note | A Title
            Some *content*
            ///
            ''',
            r'''
            <div class="admonition note">
            <p class="admonition-title">A Title</p>
            <p>Some <em>content</em></p>
            </div>
            ''',  # noqa: E501
            True
        )

    def test_custom(self):
        """Test custom type (one not shipped by default)."""

        self.check_markdown(
            R'''
            /// custom | A Title
            Some *content*
            ///
            ''',
            r'''
            <div class="admonition custom">
            <p class="admonition-title">A Title</p>
            <p>Some <em>content</em></p>
            </div>
            ''',  # noqa: E501
            True
        )
