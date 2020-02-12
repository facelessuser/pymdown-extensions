"""Test cases for SuperFences."""
from .. import util


class TestLegacyTab(util.MdCase):
    """Test legacy tab cases."""

    extension = ['pymdownx.tabbed', 'pymdownx.superfences']
    extension_configs = {}

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
