"""Test cases for SuperFences."""
from .. import util


class TestLegacyTab(util.MdCase):
    """Test legacy tab cases."""

    extension = ['pymdownx.tabbed', 'pymdownx.superfences', 'markdown.extensions.def_list', 'pymdownx.details']
    extension_configs = {}

    def test_with_preceding_text(self):
        """Test content directly before tabs."""

        expected = r'''
            <p>foo
            <strong>foo</strong></p>
            <div class="tabbed-set" data-tabs="1:1"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><label for="__tabbed_1_1">Tab</label><div class="tabbed-content"></div>
            </div>
            '''  # noqa: E501

        self.check_markdown(
            r'''
            foo
            **foo**
            === "Tab"
            ''',
            expected,
            True
        )

    def test_tabbed(self):
        """Test tabbed."""

        self.check_markdown(
            r'''
            === "Tab"
                Some *content*

                And more `content`.

            === "Another Tab"
                Some more content.

                ```
                code
                ```
            ''',
            r'''
            <div class="tabbed-set" data-tabs="1:2"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><label for="__tabbed_1_1">Tab</label><div class="tabbed-content">
            <p>Some <em>content</em></p>
            <p>And more <code>content</code>.</p>
            </div>
            <input id="__tabbed_1_2" name="__tabbed_1" type="radio" /><label for="__tabbed_1_2">Another Tab</label><div class="tabbed-content">
            <p>Some more content.</p>
            <div class="highlight"><pre><span></span><code>code
            </code></pre></div>
            </div>
            </div>
            ''',  # noqa: E501
            True
        )

    def test_tabbed_markdown_title(self):
        """Test tabbed."""

        self.check_markdown(
            r'''
            === "**Tab**"
                Some *content*

                And more `content`.

            === "_Another Tab_"
                Some more content.

                ```
                code
                ```
            ''',
            r'''
            <div class="tabbed-set" data-tabs="1:2"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><label for="__tabbed_1_1"><strong>Tab</strong></label><div class="tabbed-content">
            <p>Some <em>content</em></p>
            <p>And more <code>content</code>.</p>
            </div>
            <input id="__tabbed_1_2" name="__tabbed_1" type="radio" /><label for="__tabbed_1_2"><em>Another Tab</em></label><div class="tabbed-content">
            <p>Some more content.</p>
            <div class="highlight"><pre><span></span><code>code
            </code></pre></div>
            </div>
            </div>
            ''',  # noqa: E501
            True
        )

    def test_nested_tabbed(self):
        """Test nested tabbed."""

        self.check_markdown(
            r'''
            === "Tab"
                Some *content*

                === "Tab A"
                    - item 1

                    - item 2

                === "Tab B"
                    - item A

                    - item B

            === "Another Tab"
                Some more content.
            ''',
            r'''
            <div class="tabbed-set" data-tabs="1:2"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><label for="__tabbed_1_1">Tab</label><div class="tabbed-content">
            <p>Some <em>content</em></p>
            <div class="tabbed-set" data-tabs="2:2"><input checked="checked" id="__tabbed_2_1" name="__tabbed_2" type="radio" /><label for="__tabbed_2_1">Tab A</label><div class="tabbed-content">
            <ul>
            <li>
            <p>item 1</p>
            </li>
            <li>
            <p>item 2</p>
            </li>
            </ul>
            </div>
            <input id="__tabbed_2_2" name="__tabbed_2" type="radio" /><label for="__tabbed_2_2">Tab B</label><div class="tabbed-content">
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
            <input id="__tabbed_1_2" name="__tabbed_1" type="radio" /><label for="__tabbed_1_2">Another Tab</label><div class="tabbed-content">
            <p>Some more content.</p>
            </div>
            </div>
            ''',  # noqa: E501
            True
        )

    def test_tabbed_split(self):
        """Force a split of tab sets."""

        self.check_markdown(
            r'''
            === "Tab"
                Some *content*

                And more `content`.

            ===! "Another Tab"
                Some more content.

                ```
                code
                ```
            ''',
            r'''
            <div class="tabbed-set" data-tabs="1:1"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><label for="__tabbed_1_1">Tab</label><div class="tabbed-content">
            <p>Some <em>content</em></p>
            <p>And more <code>content</code>.</p>
            </div>
            </div>
            <div class="tabbed-set" data-tabs="2:1"><input checked="checked" id="__tabbed_2_1" name="__tabbed_2" type="radio" /><label for="__tabbed_2_1">Another Tab</label><div class="tabbed-content">
            <p>Some more content.</p>
            <div class="highlight"><pre><span></span><code>code
            </code></pre></div>
            </div>
            </div>
            ''',  # noqa: E501
            True
        )

    def test_tabbed_break(self):
        """Test that tabs are properly terminated on blocks that are not under the tab."""

        self.check_markdown(
            r'''
            === "Tab"
                Some *content*

                And more `content`.
            Content
            ''',
            r'''
            <div class="tabbed-set" data-tabs="1:1"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><label for="__tabbed_1_1">Tab</label><div class="tabbed-content">
            <p>Some <em>content</em></p>
            <p>And more <code>content</code>.</p>
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

                === "Tab"

                    - Paragraph

                        Paragraph
            ''',

            '''
            <ul>
            <li>
            <p>List</p>
            <div class="tabbed-set" data-tabs="1:1"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><label for="__tabbed_1_1">Tab</label><div class="tabbed-content">
            <ul>
            <li>
            <p>Paragraph</p>
            <p>Paragraph</p>
            </li>
            </ul>
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

                === "Tab"

                    - Paragraph

                        Paragraph

                    - Paragraph

                        paragraph
            ''',
            '''
            <ul>
            <li>
            <p>List</p>
            <div class="tabbed-set" data-tabs="1:1"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><label for="__tabbed_1_1">Tab</label><div class="tabbed-content">
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

                === "Tab"

                    - Paragraph

                        === "Tab"

                            1. Paragraph

                                Paragraph
            ''',
            '''
            <ul>
            <li>
            <p>List</p>
            <div class="tabbed-set" data-tabs="1:1"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><label for="__tabbed_1_1">Tab</label><div class="tabbed-content">
            <ul>
            <li>
            <p>Paragraph</p>
            <div class="tabbed-set" data-tabs="2:1"><input checked="checked" id="__tabbed_2_1" name="__tabbed_2" type="radio" /><label for="__tabbed_2_1">Tab</label><div class="tabbed-content">
            <ol>
            <li>
            <p>Paragraph</p>
            <p>Paragraph</p>
            </li>
            </ol>
            </div>
            </div>
            </li>
            </ul>
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

                === "Tab"

                    Term

                    :   Definition

                        More text

                    :   Another
                        definition

                        Even more text
            ''',
            '''
            <ul>
            <li>
            <p>List</p>
            <div class="tabbed-set" data-tabs="1:1"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><label for="__tabbed_1_1">Tab</label><div class="tabbed-content">
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
            </li>
            </ul>
            ''',  # noqa: E501
            True
        )

    def test_with_details(self):
        """Test with definition list."""

        self.check_markdown(
            '''
            === "Output"
                ???+ note "Open styled details"

                    ??? danger "Nested details!"
                        And more content again.
            ''',
            '''
            <div class="tabbed-set" data-tabs="1:1"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><label for="__tabbed_1_1">Output</label><div class="tabbed-content">
            <details class="note" open="open">
            <summary>Open styled details</summary>
            <details class="danger">
            <summary>Nested details!</summary>
            <p>And more content again.</p>
            </details>
            </details>
            </div>
            </div>
            ''',  # noqa: E501
            True
        )

    def test_tabbed_complex_list(self):
        """Test tabbed complex list scenario."""

        self.check_markdown(
            '''
            === "Tab with loose lists"
                - Parent 1

                    - Child 1
                    - Child 2
            ''',
            '''
            <div class="tabbed-set" data-tabs="1:1"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><label for="__tabbed_1_1">Tab with loose lists</label><div class="tabbed-content">
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
            ''',  # noqa: E501
            True
        )

    def test_tabbed_complex_list_unindented_content(self):
        """Test tabbed complex list scenario with un-indented content."""

        self.check_markdown(
            '''
            === "Tab with loose lists"
                - Parent 1

                    - Child 1
                    - Child 2
            - Parent 2
            ''',
            '''
            <div class="tabbed-set" data-tabs="1:1"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><label for="__tabbed_1_1">Tab with loose lists</label><div class="tabbed-content">
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
            <ul>
            <li>Parent 2</li>
            </ul>
            ''',  # noqa: E501
            True
        )
