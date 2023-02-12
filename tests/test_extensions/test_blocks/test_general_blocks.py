"""Using the "tab" Blocks extension, test general cases for Blocks."""
from ... import util
import unittest
from pymdownx.blocks import block
import xml.etree.ElementTree as etree
import markdown


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

        self.assertEqual(4, block.type_ranged_integer(3, 8)(4))
        self.assertEqual(4, block.type_ranged_integer(3, 8)(4.0))
        with self.assertRaises(ValueError):
            block.type_ranged_integer(3, 8)(4.3)
        with self.assertRaises(ValueError):
            block.type_ranged_integer(3, 8)(2)
        with self.assertRaises(ValueError):
            block.type_ranged_integer(3, 8)(9)

    def test_type_html_tag(self):
        """Test `type_html_tag`."""

        self.assertEqual('div', block.type_html_tag('div'))
        with self.assertRaises(ValueError):
            block.type_html_tag('3bad')

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

        self.assertEqual('some-value', block.type_html_attribute_value('some-value'))
        self.assertEqual('&quot;some-value&quot;', block.type_html_attribute_value('"some-value"'))
        with self.assertRaises(ValueError):
            block.type_html_attribute_value(3)

    def test_type_html_attribute_name(self):
        """Test `type_html_attribute_name`."""

        self.assertEqual('attribute', block.type_html_attribute_name('attribute'))
        self.assertEqual('attr_ibute', block.type_html_attribute_name('attr@ibute'))

    def test_type_string_in(self):
        """Test `type_string_in`."""

        self.assertEqual('this', block.type_string_in(['this', 'that'])('this'))
        with self.assertRaises(ValueError):
            block.type_string_in(['this', 'that'])('bad')

    def test_type_string_delimiter(self):
        """Test `type_string_delimiter`."""

        self.assertEqual(['this', 'that'], block.type_string_delimiter(';')('this; that'))
        self.assertEqual(['this', 'that'], block.type_string_delimiter(' ')('this  that'))

    def test_type_html_attribute_dict(self):
        """Test `type_html_attribute_dict`."""

        self.assertEqual(
            {'test': "test", "class": ["one", "two", "three"]},
            block.type_html_attribute_dict({'test': "test", "class": "one two three"})
        )

        with self.assertRaises(ValueError):
            block.type_html_attribute_dict(3)

    def test_type_html_class(self):
        """Test `type_html_class`."""

        self.assertEqual('this', block.type_html_class('this'))
        with self.assertRaises(ValueError):
            block.type_html_class('this that')

    def test_type_html_classes(self):
        """Test `type_html_classes`."""

        self.assertEqual(['this', 'that'], block.type_html_classes('this that'))


class TestGeneral(unittest.TestCase):
    """Test general cases."""

    def test_attribute_override(self):
        """Test that attributes cannot be overridden."""

        class AttrOverride(block.Block):
            NAME = 'override'

            OPTIONS = {
                'attributes': [False, block.type_boolean],
            }

            def on_create(self, parent):
                """Create."""

                return etree.SubElement(parent, 'div')

        with self.assertRaises(ValueError):
            markdown.markdown(
                '/// override\n///',
                extensions=['pymdownx.blocks'],
                extension_configs={'pymdownx.blocks': {'blocks': [AttrOverride]}}
            )

    def test_duplicate_blocks(self):
        """Test duplicate blocks."""

        with self.assertRaises(ValueError):
            markdown.markdown(
                '/// override\n///',
                extensions=['pymdownx.blocks'],
                extension_configs={
                    'pymdownx.blocks': {'block_configs': {'admonition': {'types': ['danger', 'danger']}}}
                }
            )


class TestBlockUndefinedOption(util.MdCase):
    """Test Blocks with undefined options."""

    class UndefinedBlock(block.Block):
        """Undefined option block."""

        NAME = 'undefined'

        def on_create(self, parent):
            """Create."""

            return etree.SubElement(parent, 'div')

    extension = ['pymdownx.blocks']
    extension_configs = {'pymdownx.blocks': {'blocks': [UndefinedBlock]}}

    def test_undefined_option(self):
        """An undefined option will cause the block parsing to fail."""

        self.check_markdown(
            R'''
            /// undefined
                option: whatever

            content
            ///
            ''',
            '''
            <p>/// undefined
                option: whatever</p>
            <p>content
            ///</p>
            ''',
            True
        )


class TestMiscCases(util.MdCase):
    """Test some miscellaneous cases."""

    class MiscBlock(block.Block):
        """A miscellaneous block."""

        NAME = 'misc'
        OPTIONS = {'test': ['whatever', block.type_string]}

        def on_create(self, parent):
            """Create."""

            return etree.SubElement(parent, 'div', {'test': self.options['test']})

    class MiscInline(block.Block):
        """A miscellaneous block."""

        NAME = 'miscinline'

        def on_create(self, parent):
            """Create."""

            return etree.SubElement(parent, 'span')

    extension = ['pymdownx.blocks', 'pymdownx.superfences']
    extension_configs = {'pymdownx.blocks': {'blocks': [MiscBlock, MiscInline]}}

    def test_general_config(self):
        """Test that content block should have a blank line between config."""

        self.check_markdown(
            R'''
            /// misc
                test: misc
            content
            ///
            ''',
            '''
            <div test="misc">
            <p>content</p>
            </div>
            ''',
            True
        )

    def test_no_content(self):
        """Test config and no content."""

        self.check_markdown(
            R'''
            /// misc
                test: misc
            ///
            ''',
            '''
            <div test="misc"></div>
            ''',
            True
        )

    def test_unfenced_config_and_no_content(self):
        """Test no fenced config and no content."""

        self.check_markdown(
            R'''
            /// misc
                test: misc
            ///
            ''',
            '''
            <div test="misc"></div>
            ''',
            True
        )

    def test_content_after_only_config_block(self):
        """Test content after only config block."""

        self.check_markdown(
            R'''
            /// misc
                test: misc
            ///
            more
            ''',
            '''
            <div test="misc"></div>
            <p>more</p>
            ''',
            True
        )

    def test_superfence_block(self):
        """Test blocks with fenced code content."""

        self.check_markdown(
            R'''
            /// misc
            ```python
            import foo
            ```
            ///
            ''',
            '''
            <div test="whatever">
            <div class="highlight"><pre><span></span><code><span class="kn">import</span> <span class="nn">foo</span>
            </code></pre></div>
            </div>
            ''',
            True
        )

    def test_superfence_inline(self):
        """Test blocks with fenced code content."""

        self.check_markdown(
            R'''
            /// miscinline
            ```python
            import foo
            ```

            Other content
            ///
            ''',
            '''
            <span><code>python
            import foo</code>

            Other content</span>
            ''',
            True
        )


class TestAlternateSyntax(util.MdCase):
    """Test the alpha/beta alternate syntax."""

    extension = ['pymdownx.blocks']
    extension_configs = {'pymdownx.blocks': {'colon_syntax': True}}

    def test_colon_syntax(self):
        """Test the colon syntax."""

        self.check_markdown(
            R'''
            :::: html | div
            ::: html | div

            content
            :::
            ::::
            ''',
            '''
            <div>
            <div>
            <p>content</p>
            </div>
            </div>
            ''',
            True
        )


class TestMiscYAMLFenceCases(util.MdCase):
    """Test some miscellaneous cases."""

    class MiscBlock(block.Block):
        """A miscellaneous block."""

        NAME = 'misc'
        OPTIONS = {'test': ['whatever', block.type_string]}

        def on_create(self, parent):
            """Create."""

            return etree.SubElement(parent, 'div', {'test': self.options['test']})

    extension = ['pymdownx.blocks', 'pymdownx.superfences']
    extension_configs = {'pymdownx.blocks': {'blocks': [MiscBlock]}}

    def test_no_config(self):
        """Test no YAML config and no new line."""

        self.check_markdown(
            R'''
            /// misc
            content
            ///
            ''',
            '''
            <div test="whatever">
            <p>content</p>
            </div>
            ''',
            True
        )

    def test_config_no_new_line(self):
        """Test YAML config and no new line."""

        self.check_markdown(
            R'''
            /// misc
                test: tag
            content
            ///
            ''',
            '''
            <div test="tag">
            <p>content</p>
            </div>
            ''',
            True
        )

    def test_config_no_fence(self):
        """Test YAML config and no fence."""

        self.check_markdown(
            R'''
            /// misc
            test: tag

            content
            ///
            ''',
            '''
            <div test="whatever">
            <p>test: tag</p>
            <p>content</p>
            </div>
            ''',
            True
        )

    def test_config_with_new_line_before(self):
        """Test YAML config and with new line before it."""

        self.check_markdown(
            R'''
            /// misc

                test: tag

            content
            ///
            ''',
            '''
            <div test="whatever">
            <pre><code>test: tag
            </code></pre>
            <p>content</p>
            </div>
            ''',
            True
        )


class TestBadArgOptionParsers(util.MdCase):
    """Test when a block's options do not fulfill the parser's expectations."""

    class FailBlock(block.Block):
        """Test failure to satisfy parser."""

        NAME = 'fail'
        ARGUMENTS = {'required': 1, 'parsers': [block.type_html_tag]}
        OPTIONS = {'test': ['tag', block.type_html_tag]}

        def on_create(self, parent):
            """Create."""

            return etree.SubElement(parent, 'div')

    extension = ['pymdownx.blocks']
    extension_configs = {'pymdownx.blocks': {'blocks': [FailBlock]}}

    def test_fail_args(self):
        """Test failure of arguments."""

        self.check_markdown(
            R'''
            /// fail | 3tag
            ///
            ''',
            '''
            <p>/// fail | 3tag
            ///</p>
            ''',
            True
        )

    def test_fail_opts(self):
        """Test failure of options."""

        self.check_markdown(
            R'''
            /// fail | tag
                test: 3tag

            content
            ///
            ''',
            '''
            <p>/// fail | tag
                test: 3tag</p>
            <p>content
            ///</p>
            ''',
            True
        )

    def test_bad_config(self):
        """Test when content is used in place of config."""

        self.check_markdown(
            R'''
            /// fail | tag
                content
            ///
            ''',
            '''
            <p>/// fail | tag
                content
            ///</p>
            ''',
            True
        )

    def test_bad_yaml(self):
        """Test config is bad YAML."""

        self.check_markdown(
            R'''
            /// fail | tag
                :
            ///
            ''',
            '''
            <p>/// fail | tag
                :
            ///</p>
            ''',
            True
        )


class TestBlockSplit(util.MdCase):
    """Test Blocks that split arguments."""

    class SplitBlock(block.Block):
        """Split block."""

        NAME = 'split'

        ARGUMENTS = {'required': 2}

        def on_create(self, parent):
            """Create."""

            return etree.SubElement(parent, 'div', {self.args[0]: '0', self.args[1]: '1'})

    extension = ['pymdownx.blocks']
    extension_configs = {'pymdownx.blocks': {'blocks': [SplitBlock]}}

    def test_split(self):
        """Test that attributes cannot be overridden."""

        self.check_markdown(
            R'''
            /// split | this that
            ///
            ''',
            '''
            <div that="1" this="0"></div>
            ''',
            True
        )

    def test_split_less(self):
        """Test failure when arguments are too few."""

        self.check_markdown(
            R'''
            /// split | this
            ///
            ''',
            '''
            <p>/// split | this
            ///</p>
            ''',
            True
        )

    def test_split_greater(self):
        """Test failure when arguments are too many."""

        self.check_markdown(
            R'''
            /// split | this that another
            ///
            ''',
            '''
            <p>/// split | this that another
            ///</p>
            ''',
            True
        )


class TestBlocksTab(util.MdCase):
    """Test Blocks tab cases."""

    extension = ['pymdownx.blocks', 'pymdownx.superfences', 'markdown.extensions.def_list', 'pymdownx.details']
    extension_configs = {
        'pymdownx.blocks': {
            'block_configs': {
                'tab': {
                    'alternate_style': True
                }
            }
        }
    }

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
