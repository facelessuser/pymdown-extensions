"""Test cases for Blocks (admonitions)."""
from ... import util


class TestBlocksAdmonitions(util.MdCase):
    """Test Blocks admonitions cases."""

    extension = ['pymdownx.blocks.admonition']
    extension_configs = {
        'pymdownx.blocks.admonition': {
            'types': [
                'note',
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
            /// admonition
            Some *content*
            ///
            ''',
            r'''
            <div class="admonition">
            <p>Some <em>content</em></p>
            </div>
            ''',
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
            ''',
            True
        )

    def test_type_empty_title(self):
        """Test test empty title."""

        self.check_markdown(
            R'''
            /// admonition |
                type: note
                attrs: {class: other}

            Some *content*
            ///
            ''',
            r'''
            <div class="admonition note other">
            <p>Some <em>content</em></p>
            </div>
            ''',
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
            ''',
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
            ''',
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
            <div class="admonition custom">
            <p class="admonition-title">A Title</p>
            <p>Some <em>content</em></p>
            </div>
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
            <div class="admonition custom">
            <p class="admonition-title">Custom</p>
            <p>Some <em>content</em></p>
            </div>
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
            <div class="admonition custom2">
            <p class="admonition-title">Custom2</p>
            <p>Some <em>content</em></p>
            </div>
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
            <div class="admonition custom5">
            <p class="admonition-title">Default</p>
            <p>Some <em>content</em></p>
            </div>
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
            <div class="admonition different">
            <p class="admonition-title">Different</p>
            <p>Some <em>content</em></p>
            </div>
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
            <div class="admonition different">
            <p class="admonition-title">Default</p>
            <p>Some <em>content</em></p>
            </div>
            ''',
            True
        )
