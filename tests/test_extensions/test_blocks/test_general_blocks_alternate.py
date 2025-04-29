"""Using the "tab" Blocks extension, test general cases for Blocks for the alternate attribute syntax."""
from ... import util
import unittest
from pymdownx.blocks import block
import markdown

class TestBlockUndefinedOptionAlternate(util.MdCase):
    """Test Blocks with undefined options."""

    extension = ['pymdownx.blocks.html', 'pymdownx.blocks.definition']

    def test_undefined_option(self):
        """An undefined option will cause the block parsing to fail."""

        self.check_markdown(
            R'''
            /// html | div
            @option: whatever

            content
            ///
            ''',
            '''
            <p>/// html | div
                option: whatever</p>
            <p>content
            ///</p>
            ''',
            True
        )

    def test_bad_option(self):
        """An undefined option will cause the block parsing to fail."""

        self.check_markdown(
            R'''
            /// html | div
            @attrs: whatever

            content
            ///
            ''',
            '''
            <p>/// html | div
                attrs: whatever</p>
            <p>content
            ///</p>
            ''',
            True
        )

    def test_no_arg(self):
        """Test no options."""

        self.check_markdown(
            R'''
            /// html
            @attrs: whatever

            content
            ///
            ''',
            '''
            <p>/// html
                attrs: whatever</p>
            <p>content
            ///</p>
            ''',
            True
        )

    def test_too_many_args(self):
        """Test too many options."""

        self.check_markdown(
            R'''
            /// define
            @option: whatever

            content
            ///
            ''',
            '''
            <p>/// define
                option: whatever</p>
            <p>content
            ///</p>
            ''',
            True
        )

    def test_commented_frontmatter(self):
        """Test commented frontmatter."""

        self.check_markdown(
            R'''
            /// html | div
                # @attrs: {class: test}

            content
            ///
            ''',
            '''
            <div>
            <p>content</p>
            </div>
            ''',
            True
        )


class TestAttributesAlternate(util.MdCase):
    """Test Blocks tab cases."""

    extension = ['pymdownx.blocks.admonition']

    def test_attributes(self):
        """Test attributes."""

        self.check_markdown(
            R'''
            /// admonition | Title
            @attrs: {class: some classes, id: an-id, name: some value}

            content
            ///
            ''',
            '''
            <div class="admonition some classes" id="an-id" name="some value">
            <p class="admonition-title">Title</p>
            <p>content</p>
            </div>
            ''',
            True
        )

    def test_bad_attributes(self):
        """Test no attributes."""

        self.check_markdown(
            R'''
            /// admonition | Title
            @attrs: {'+': 'value'}
            content
            ///
            ''',
            '''
            <p>/// admonition | Title
                attrs: {'+': 'value'}
            content
            ///</p>
            ''',
            True
        )