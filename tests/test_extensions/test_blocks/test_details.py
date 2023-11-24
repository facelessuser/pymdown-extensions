"""Test cases for Blocks (details)."""
from ... import util


class TestBlocksDetails(util.MdCase):
    """Test Blocks details cases."""

    extension = ['pymdownx.blocks.details']
    extension_configs = {
        'pymdownx.blocks.details': {
            'types': [
                'custom',
                {'name': 'custom2'},
                {'name': 'custom3', 'class': 'different'},
                {'name': 'custom4', 'class': 'different', 'title': 'Default'},
                {'name': 'custom5', 'title': 'Default'}
            ]
        }
    }

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
            ''',
            True
        )

    def test_type_no_title(self):
        """Test test type as title."""

        self.check_markdown(
            R'''
            /// details
                type: note
                attrs: {class: other}

            Some *content*
            ///
            ''',
            r'''
            <details class="note other">
            <summary>Note</summary>
            <p>Some <em>content</em></p>
            </details>
            ''',
            True
        )

    def test_type_empty_title(self):
        """Test test empty title."""

        self.check_markdown(
            R'''
            /// details |
                type: note
                attrs: {class: other}

            Some *content*
            ///
            ''',
            r'''
            <details class="note other">
            <p>Some <em>content</em></p>
            </details>
            ''',
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
            ''',
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
            ''',
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
            <details class="custom">
            <summary>A Title</summary>
            <p>Some <em>content</em></p>
            </details>
            ''',
            True
        )

    def test_custom_title(self):
        """Test custom title."""

        self.check_markdown(
            R'''
            /// custom
            Some *content*
            ///
            ''',
            r'''
            <details class="custom">
            <summary>Custom</summary>
            <p>Some <em>content</em></p>
            </details>
            ''',
            True
        )

    def test_custom_dict_title(self):
        """Test custom title with dictionary form."""

        self.check_markdown(
            R'''
            /// custom2
            Some *content*
            ///
            ''',
            r'''
            <details class="custom2">
            <summary>Custom2</summary>
            <p>Some <em>content</em></p>
            </details>
            ''',
            True
        )

    def test_custom_explicit_title(self):
        """Test custom with an explicit, default title."""

        self.check_markdown(
            R'''
            /// custom5
            Some *content*
            ///
            ''',
            r'''
            <details class="custom5">
            <summary>Default</summary>
            <p>Some <em>content</em></p>
            </details>
            ''',
            True
        )

    def test_custom_with_class(self):
        """Test custom title with configured custom class."""

        self.check_markdown(
            R'''
            /// custom3
            Some *content*
            ///
            ''',
            r'''
            <details class="different">
            <summary>Different</summary>
            <p>Some <em>content</em></p>
            </details>
            ''',
            True
        )

    def test_custom_with_class_and_title(self):
        """Test custom title with configured custom class and title."""

        self.check_markdown(
            R'''
            /// custom4
            Some *content*
            ///
            ''',
            r'''
            <details class="different">
            <summary>Default</summary>
            <p>Some <em>content</em></p>
            </details>
            ''',
            True
        )
