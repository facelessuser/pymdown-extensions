"""Test cases for Blocks (tab)."""
from ... import util
from pymdownx.slugs import slugify


class TestTabSlugs(util.MdCase):
    """Test tab slug cases."""

    extension = ['pymdownx.blocks', 'toc']
    extension_configs = {
        'pymdownx.blocks': {
            'block_configs': {
                'tab': {
                    'slugify': slugify(case='lower'),
                    'alternate_style': True
                }
            }
        }
    }

    MD = r"""
    ### Here is some text

    /// tab | Here is some text
    content
    ///

    /// tab | Here is some text
    content
    ///
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


class TestTabSlugsSep(util.MdCase):
    """Test tab slug separator cases."""

    extension = ['pymdownx.blocks', 'toc']
    extension_configs = {
        'pymdownx.blocks': {
            'block_configs': {
                'tab': {
                    'slugify': slugify(case='lower'),
                    'separator': '_',
                    'alternate_style': True
                }
            }
        }
    }

    MD = r"""
    ### Here is some text

    /// tab | Here is some text
    content
    ///

    /// tab | Here is some text
    content
    ///
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

    def test_tabbed_select(self):
        """Test selecting a tab."""

        self.check_markdown(
            r'''
            /// tab | Tab 1
            content
            ///

            /// tab | Tab 2
                select: true

            content
            ///

            /// tab | Tab 3
            content
            ///
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

    def test_tabbed_select_multiple(self):
        """Test selecting multiple tabs."""

        self.check_markdown(
            r'''
            /// tab | Tab 1
            content
            ///

            /// tab | Tab 2
                select: true

            content
            ///

            /// tab | Tab 3
                select: true

            content
            ///
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

    def test_required_title(self):
        """Test that tab is not processed if title is omitted."""

        self.check_markdown(
            R'''
            /// tab

            Some *content*
            ///
            ''',
            r'''
            <p>/// tab</p>
            <p>Some <em>content</em>
            ///</p>
            ''',  # noqa: E501
            True
        )

    def test_tabbed(self):
        """Test tabbed."""

        self.check_markdown(
            R'''
            /// tab | Tab
            Some *content*

            And more `content`.
            ///

            /// tab | Another Tab
            Some more content.

            ```
            code
            ```
            ///
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
            R'''
            /// tab | **Tab**
            Some *content*

            And more `content`.
            ///

            /// tab | _Another Tab_
            Some more content.

            ```
            code
            ```
            ///
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

    def test_tabbed_split(self):
        """Force a split of tab sets."""

        self.check_markdown(
            R'''
            /// tab | Tab
            Some *content*

            And more `content`.
            ///

            /// tab | Another Tab
                new: true

            Some more content.

            ```
            code
            ```
            ///
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
