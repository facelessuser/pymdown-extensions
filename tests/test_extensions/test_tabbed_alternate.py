"""Test cases for SuperFences."""
from .. import util
from pymdownx.slugs import slugify


class TestLegacyTab(util.MdCase):
    """Test legacy tab cases."""

    extension = ['pymdownx.tabbed', 'pymdownx.superfences', 'markdown.extensions.def_list', 'pymdownx.details']
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
            <div class="tabbed-set tabbed-alternate" data-tabs="1:2"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><input id="__tabbed_1_2" name="__tabbed_1" type="radio" /><div class="tabbed-labels"><label for="__tabbed_1_1">Tab</label><label for="__tabbed_1_2">Another Tab</label></div>
            <div class="tabbed-content">
            <div class="tabbed-block">
            <p>Some <em>content</em></p>
            <p>And more <code>content</code>.</p>
            </div>
            <div class="tabbed-block">
            <p>Some more content.</p>
            <div class="highlight"><pre><span></span><code>code
            </code></pre></div>
            </div>
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
            <div class="tabbed-set tabbed-alternate" data-tabs="1:2"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><input id="__tabbed_1_2" name="__tabbed_1" type="radio" /><div class="tabbed-labels"><label for="__tabbed_1_1"><strong>Tab</strong></label><label for="__tabbed_1_2"><em>Another Tab</em></label></div>
            <div class="tabbed-content">
            <div class="tabbed-block">
            <p>Some <em>content</em></p>
            <p>And more <code>content</code>.</p>
            </div>
            <div class="tabbed-block">
            <p>Some more content.</p>
            <div class="highlight"><pre><span></span><code>code
            </code></pre></div>
            </div>
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
            <div class="tabbed-set tabbed-alternate" data-tabs="1:1"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><div class="tabbed-labels"><label for="__tabbed_1_1">Tab</label></div>
            <div class="tabbed-content">
            <div class="tabbed-block">
            <p>Some <em>content</em></p>
            <p>And more <code>content</code>.</p>
            </div>
            </div>
            </div>
            <div class="tabbed-set tabbed-alternate" data-tabs="2:1"><input checked="checked" id="__tabbed_2_1" name="__tabbed_2" type="radio" /><div class="tabbed-labels"><label for="__tabbed_2_1">Another Tab</label></div>
            <div class="tabbed-content">
            <div class="tabbed-block">
            <p>Some more content.</p>
            <div class="highlight"><pre><span></span><code>code
            </code></pre></div>
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
            === "Tab"
                Some *content*

                And more `content`.
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

    def test_tabbed_select(self):
        """Test selecting a tab."""

        self.check_markdown(
            r'''
            === "Tab 1"
                content

            ===+ "Tab 2"
                content

            === "Tab 3"
                content
            ''',
            r'''
            <div class="tabbed-set tabbed-alternate" data-tabs="1:3"><input id="__tabbed_1_1" name="__tabbed_1" type="radio" /><input checked="checked" id="__tabbed_1_2" name="__tabbed_1" type="radio" /><input id="__tabbed_1_3" name="__tabbed_1" type="radio" /><div class="tabbed-labels"><label for="__tabbed_1_1">Tab 1</label><label for="__tabbed_1_2">Tab 2</label><label for="__tabbed_1_3">Tab 3</label></div>
            <div class="tabbed-content">
            <div class="tabbed-block">
            <p>content</p>
            </div>
            <div class="tabbed-block">
            <p>content</p>
            </div>
            <div class="tabbed-block">
            <p>content</p>
            </div>
            </div>
            </div>
            ''',  # noqa: E501
            True
        )

    def test_tabbed_select_mulitiple(self):
        """Test selecting multiple tabs."""

        self.check_markdown(
            r'''
            === "Tab 1"
                content

            ===+ "Tab 2"
                content

            ===+ "Tab 3"
                content
            ''',
            r'''
            <div class="tabbed-set tabbed-alternate" data-tabs="1:3"><input id="__tabbed_1_1" name="__tabbed_1" type="radio" /><input id="__tabbed_1_2" name="__tabbed_1" type="radio" /><input checked="checked" id="__tabbed_1_3" name="__tabbed_1" type="radio" /><div class="tabbed-labels"><label for="__tabbed_1_1">Tab 1</label><label for="__tabbed_1_2">Tab 2</label><label for="__tabbed_1_3">Tab 3</label></div>
            <div class="tabbed-content">
            <div class="tabbed-block">
            <p>content</p>
            </div>
            <div class="tabbed-block">
            <p>content</p>
            </div>
            <div class="tabbed-block">
            <p>content</p>
            </div>
            </div>
            </div>
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
            === "Output"
                ???+ note "Open styled details"

                    ??? danger "Nested details!"
                        And more content again.
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
            === "Tab with loose lists"
                - Parent 1

                    - Child 1
                    - Child 2
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
            === "Tab with loose lists"
                - Parent 1

                    - Child 1
                    - Child 2
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


class TestLegacyTabSlugs(util.MdCase):
    """Test legacy tab slug cases."""

    extension = ['pymdownx.tabbed', 'toc']
    extension_configs = {'pymdownx.tabbed': {'slugify': slugify(case='lower'), 'alternate_style': True}}

    MD = """
    ### Here is some text

    === "Here is some text"
        content

    === "Here is some text"
        content
    """

    def test_tab_slugs(self):
        """Test tab slugs."""

        self.check_markdown(
            self.MD,
            '''
            <h3 id="here-is-some-text">Here is some text</h3>
            <div class="tabbed-set tabbed-alternate" data-tabs="1:2"><input checked="checked" id="here-is-some-text_1" name="__tabbed_1" type="radio" /><input id="here-is-some-text_2" name="__tabbed_1" type="radio" /><div class="tabbed-labels"><label for="here-is-some-text_1">Here is some text</label><label for="here-is-some-text_2">Here is some text</label></div>
            <div class="tabbed-content">
            <div class="tabbed-block">
            <p>content</p>
            </div>
            <div class="tabbed-block">
            <p>content</p>
            </div>
            </div>
            </div>
            ''',  # noqa: E501
            True
        )


class TestLegacyTabSlugsSep(util.MdCase):
    """Test legacy tab slug separator cases."""

    extension = ['pymdownx.tabbed', 'toc']
    extension_configs = {
        'pymdownx.tabbed': {'slugify': slugify(case='lower'), 'separator': '_', 'alternate_style': True}
    }

    MD = """
    ### Here is some text

    === "Here is some text"
        content

    === "Here is some text"
        content
    """

    def test_slug_with_separator(self):
        """Test tab slugs with separator."""

        self.check_markdown(
            self.MD,
            '''
            <h3 id="here-is-some-text">Here is some text</h3>
            <div class="tabbed-set tabbed-alternate" data-tabs="1:2"><input checked="checked" id="here_is_some_text" name="__tabbed_1" type="radio" /><input id="here_is_some_text_1" name="__tabbed_1" type="radio" /><div class="tabbed-labels"><label for="here_is_some_text">Here is some text</label><label for="here_is_some_text_1">Here is some text</label></div>
            <div class="tabbed-content">
            <div class="tabbed-block">
            <p>content</p>
            </div>
            <div class="tabbed-block">
            <p>content</p>
            </div>
            </div>
            </div>
            ''',  # noqa: E501
            True
        )
