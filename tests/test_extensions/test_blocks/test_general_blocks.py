"""Using the "tab" Blocks extension, test general cases for Blocks."""
from ... import util
import unittest
from pymdownx.blocks import block


class TestTypeFunctions(unittest.TestCase):
    """Validate various type functions."""

    def test_type_number(self):
        """Test `type_number`."""

        self.assertEqual(3, block.type_number(3))
        self.assertEqual(3.0, block.type_number(3.0))
        with self.assertRaises(ValueError):
            block.type_number('string')

    def test_type_integer(self):
        """Test `type_integer`."""

        self.assertEqual(3, block.type_integer(3))
        self.assertEqual(3, block.type_integer(3.0))
        with self.assertRaises(ValueError):
            block.type_integer(3.3)

    def test_type_ranged_number(self):
        """Test `type_ranged_number`."""

        self.assertEqual(4.7, block.type_ranged_number(3, 8)(4.7))
        with self.assertRaises(ValueError):
            block.type_ranged_number(3, 8)(2.7)
        with self.assertRaises(ValueError):
            block.type_ranged_number(3, 8)(9.2)
        self.assertEqual(-4.7, block.type_ranged_number(None, 8)(-4.7))
        with self.assertRaises(ValueError):
            block.type_ranged_number(None, 8)(9.2)
        self.assertEqual(1004.7, block.type_ranged_number(3, None)(1004.7))
        with self.assertRaises(ValueError):
            block.type_ranged_number(3, None)(2.3)
        with self.assertRaises(ValueError):
            block.type_ranged_number(3, 8)('string')

    def test_type_ranged_integer(self):
        """Test `type_ranged_integer`."""

    def test_type_tag(self):
        """Test `type_tag`."""

    def test_type_boolean(self):
        """Test `type_boolean`."""

        self.assertEqual(True, block.type_boolean(True))
        self.assertEqual(False, block.type_boolean(False))
        with self.assertRaises(ValueError):
            block.type_boolean(None)

    def test_type_ternary(self):
        """Test `type_ternary`."""

        self.assertEqual(True, block.type_ternary(True))
        self.assertEqual(False, block.type_ternary(False))
        self.assertEqual(None, block.type_ternary(None))
        with self.assertRaises(ValueError):
            block.type_ternary(3)

    def test_type_string(self):
        """Test `type_string`."""

        self.assertEqual('string', block.type_string('string'))
        with self.assertRaises(ValueError):
            block.type_string(3)

    def test_type_string_insensitive(self):
        """Test `type_string_insensitive`."""

        self.assertEqual('string', block.type_string_insensitive('STRING'))
        with self.assertRaises(ValueError):
            block.type_string_insensitive(3)

    def test_type_html_attribute_value(self):
        """Test `type_html_attribute_value`."""

    def test_type_html_attribute_name(self):
        """Test `type_html_attribute_name`."""

    def test_type_string_in(self):
        """Test `type_string_in`."""

    def test_type_string_delimiter(self):
        """Test `type_string_delimiter`."""

    def test_type_attribute_dict(self):
        """Test `type_attribute_dict`."""

    def test_type_class(self):
        """Test `type_class`."""

    def test_type_classes(self):
        """Test `type_classes`."""


class TestBlocksTab(util.MdCase):
    """Test Blocks tab cases."""

    extension = ['pymdownx.blocks', 'pymdownx.superfences', 'markdown.extensions.def_list', 'pymdownx.details']
    extension_configs = {'pymdownx.tabbed': {'alternate_style': True}}

    def test_with_preceding_text(self):
        """Test content directly before tabs."""

        expected = r'''
            <p>foo
            <strong>foo</strong></p>
            <div class="tabbed-set tabbed-alternate" data-tabs="1:1"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><div class="tabbed-labels"><label for="__tabbed_1_1">Tab</label></div>
            <div class="tabbed-content">
            <div class="tabbed-block"></div>
            </div>
            </div>
            '''  # noqa: E501

        self.check_markdown(
            R'''
            foo
            **foo**
            /// tab | Tab
            ///
            ''',
            expected,
            True
        )

    def test_nested_tabbed(self):
        """Test nested tabbed."""

        self.check_markdown(
            R'''
            //// tab | Tab

            Some *content*

            /// tab | Tab A

            - item 1

            - item 2
            ///

            /// tab | Tab B

            - item A

            - item B
            ///
            ////

            /// tab | Another Tab

            Some more content.
            ///
            ''',
            r'''
            <div class="tabbed-set tabbed-alternate" data-tabs="1:2"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><input id="__tabbed_1_2" name="__tabbed_1" type="radio" /><div class="tabbed-labels"><label for="__tabbed_1_1">Tab</label><label for="__tabbed_1_2">Another Tab</label></div>
            <div class="tabbed-content">
            <div class="tabbed-block">
            <p>Some <em>content</em></p>
            <div class="tabbed-set tabbed-alternate" data-tabs="2:2"><input checked="checked" id="__tabbed_2_1" name="__tabbed_2" type="radio" /><input id="__tabbed_2_2" name="__tabbed_2" type="radio" /><div class="tabbed-labels"><label for="__tabbed_2_1">Tab A</label><label for="__tabbed_2_2">Tab B</label></div>
            <div class="tabbed-content">
            <div class="tabbed-block">
            <ul>
            <li>
            <p>item 1</p>
            </li>
            <li>
            <p>item 2</p>
            </li>
            </ul>
            </div>
            <div class="tabbed-block">
            <ul>
            <li>
            <p>item A</p>
            </li>
            <li>
            <p>item B</p>
            </li>
            </ul>
            </div>
            </div>
            </div>
            </div>
            <div class="tabbed-block">
            <p>Some more content.</p>
            </div>
            </div>
            </div>
            ''',  # noqa: E501
            True
        )

    def test_tabbed_break(self):
        """Test that tabs are properly terminated on blocks that are not under the tab."""

        self.check_markdown(
            r'''
            /// tab | Tab

            Some *content*

            And more `content`.
            ///
            Content
            ''',
            r'''
            <div class="tabbed-set tabbed-alternate" data-tabs="1:1"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><div class="tabbed-labels"><label for="__tabbed_1_1">Tab</label></div>
            <div class="tabbed-content">
            <div class="tabbed-block">
            <p>Some <em>content</em></p>
            <p>And more <code>content</code>.</p>
            </div>
            </div>
            </div>
            <p>Content</p>
            ''',  # noqa: E501
            True
        )

    def test_with_lists(self):
        """Test with lists."""

        self.check_markdown(
            '''
            - List

                /// tab | Tab

                - Paragraph

                    Paragraph
                ///
            ''',

            '''
            <ul>
            <li>
            <p>List</p>
            <div class="tabbed-set tabbed-alternate" data-tabs="1:1"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><div class="tabbed-labels"><label for="__tabbed_1_1">Tab</label></div>
            <div class="tabbed-content">
            <div class="tabbed-block">
            <ul>
            <li>
            <p>Paragraph</p>
            <p>Paragraph</p>
            </li>
            </ul>
            </div>
            </div>
            </div>
            </li>
            </ul>
            ''',  # noqa: E501
            True
        )

    def test_with_big_lists(self):
        """Test details with a longer list."""

        self.check_markdown(
            '''
            - List

                /// tab | Tab

                - Paragraph

                    Paragraph

                - Paragraph

                    paragraph
                ///
            ''',
            '''
            <ul>
            <li>
            <p>List</p>
            <div class="tabbed-set tabbed-alternate" data-tabs="1:1"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><div class="tabbed-labels"><label for="__tabbed_1_1">Tab</label></div>
            <div class="tabbed-content">
            <div class="tabbed-block">
            <ul>
            <li>
            <p>Paragraph</p>
            <p>Paragraph</p>
            </li>
            <li>
            <p>Paragraph</p>
            <p>paragraph</p>
            </li>
            </ul>
            </div>
            </div>
            </div>
            </li>
            </ul>
            ''',  # noqa: E501
            True
        )

    def test_with_complex_lists(self):
        """Test details in a complex list scenario."""

        self.check_markdown(
            '''
            - List

                /// tab | Tab

                - Paragraph

                    /// tab | Tab

                    1. Paragraph

                        Paragraph
                    ///
                ///
        ''',
            '''
            <ul>
            <li>
            <p>List</p>
            <div class="tabbed-set tabbed-alternate" data-tabs="1:1"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><div class="tabbed-labels"><label for="__tabbed_1_1">Tab</label></div>
            <div class="tabbed-content">
            <div class="tabbed-block">
            <ul>
            <li>
            <p>Paragraph</p>
            <div class="tabbed-set tabbed-alternate" data-tabs="2:1"><input checked="checked" id="__tabbed_2_1" name="__tabbed_2" type="radio" /><div class="tabbed-labels"><label for="__tabbed_2_1">Tab</label></div>
            <div class="tabbed-content">
            <div class="tabbed-block">
            <ol>
            <li>
            <p>Paragraph</p>
            <p>Paragraph</p>
            </li>
            </ol>
            </div>
            </div>
            </div>
            </li>
            </ul>
            </div>
            </div>
            </div>
            </li>
            </ul>
            ''',  # noqa: E501
            True
        )

    def test_definition_list(self):
        """Test with definition list."""

        self.check_markdown(
            '''
            - List

                /// tab | Tab

                Term

                :   Definition

                    More text

                :   Another
                    definition

                    Even more text
                ///
            ''',
            '''
            <ul>
            <li>
            <p>List</p>
            <div class="tabbed-set tabbed-alternate" data-tabs="1:1"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><div class="tabbed-labels"><label for="__tabbed_1_1">Tab</label></div>
            <div class="tabbed-content">
            <div class="tabbed-block">
            <dl>
            <dt>Term</dt>
            <dd>
            <p>Definition</p>
            <p>More text</p>
            </dd>
            <dd>
            <p>Another
            definition</p>
            <p>Even more text</p>
            </dd>
            </dl>
            </div>
            </div>
            </div>
            </li>
            </ul>
            ''',  # noqa: E501
            True
        )

    def test_with_details(self):
        """Test with definition list."""

        self.check_markdown(
            '''
            /// tab | Output

            ???+ note "Open styled details"

                ??? danger "Nested details!"
                    And more content again.
            ///
            ''',
            '''
            <div class="tabbed-set tabbed-alternate" data-tabs="1:1"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><div class="tabbed-labels"><label for="__tabbed_1_1">Output</label></div>
            <div class="tabbed-content">
            <div class="tabbed-block">
            <details class="note" open="open">
            <summary>Open styled details</summary>
            <details class="danger">
            <summary>Nested details!</summary>
            <p>And more content again.</p>
            </details>
            </details>
            </div>
            </div>
            </div>
            ''',  # noqa: E501
            True
        )

    def test_tabbed_complex_list(self):
        """Test tabbed complex list scenario."""

        self.check_markdown(
            '''
            /// tab | Tab with loose lists

            - Parent 1

                - Child 1
                - Child 2
            ///
            ''',
            '''
            <div class="tabbed-set tabbed-alternate" data-tabs="1:1"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><div class="tabbed-labels"><label for="__tabbed_1_1">Tab with loose lists</label></div>
            <div class="tabbed-content">
            <div class="tabbed-block">
            <ul>
            <li>
            <p>Parent 1</p>
            <ul>
            <li>Child 1</li>
            <li>Child 2</li>
            </ul>
            </li>
            </ul>
            </div>
            </div>
            </div>
            ''',  # noqa: E501
            True
        )

    def test_tabbed_complex_list_unindented_content(self):
        """Test tabbed complex list scenario with un-indented content."""

        self.check_markdown(
            '''
            /// tab | Tab with loose lists

            - Parent 1

                - Child 1
                - Child 2
            ///
            - Parent 2
            ''',
            '''
            <div class="tabbed-set tabbed-alternate" data-tabs="1:1"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><div class="tabbed-labels"><label for="__tabbed_1_1">Tab with loose lists</label></div>
            <div class="tabbed-content">
            <div class="tabbed-block">
            <ul>
            <li>
            <p>Parent 1</p>
            <ul>
            <li>Child 1</li>
            <li>Child 2</li>
            </ul>
            </li>
            </ul>
            </div>
            </div>
            </div>
            <ul>
            <li>Parent 2</li>
            </ul>
            ''',  # noqa: E501
            True
        )
