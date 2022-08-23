"""Test cases for Blocks (tab)."""
from ... import util


class TestBlocksTab(util.MdCase):
    """Test Blocks tab cases."""

    extension = ['pymdownx.blocks', 'pymdownx.superfences', 'markdown.extensions.def_list', 'pymdownx.details']
    extension_configs = {'pymdownx.tabbed': {'alternate_style': True}}

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
