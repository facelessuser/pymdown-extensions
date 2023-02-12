"""Test cases for Blocks (HTML)."""
from ... import util


class TestBlocksHTML(util.MdCase):
    """Test Blocks HTML cases."""

    extension = ['pymdownx.blocks']

    def test_bad_tag(self):
        """Test bad HTML tag."""

        self.check_markdown(
            R'''
            /// html | 3tag
            Some *content*
            ///
            ''',
            R'''
            <p>/// html | 3tag
            Some <em>content</em>
            ///</p>
            ''',  # noqa: E501
            True
        )

    def test_required_tag(self):
        """Test that tab is not processed if tag is omitted."""

        self.check_markdown(
            R'''
            /// html
            Some *content*
            ///
            ''',
            r'''
            <p>/// html
            Some <em>content</em>
            ///</p>
            ''',  # noqa: E501
            True
        )

    def test_html_block(self):
        """Test HTML block element."""

        self.check_markdown(
            R'''
            /// html | div
            Some *content*

            And more `content`.
            ///
            ''',
            r'''
            <div>
            <p>Some <em>content</em></p>
            <p>And more <code>content</code>.</p>
            </div>
            ''',  # noqa: E501
            True
        )

    def test_html_span(self):
        """Test HTML with span element."""

        self.check_markdown(
            R'''
            /// html | span
            Will be parsed as inline *content*

            And more `content`.
            ///
            ''',
            r'''
            <span>Will be parsed as inline <em>content</em>

            And more <code>content</code>.</span>
            ''',  # noqa: E501
            True
        )

    def test_html_raw_element(self):
        """Test HTML raw element."""

        self.check_markdown(
            R'''
            /// html | pre
            Some *content*

            And more `content`.
            ///
            ''',
            r'''
            <pre>Some *content*

            And more `content`.</pre>
            ''',  # noqa: E501
            True
        )

    def test_html_forced_raw_element(self):
        """Test HTML force raw element."""

        self.check_markdown(
            R'''
            /// html | div
                markdown: raw

            Some *content*

            And more `content`.
            ///
            ''',
            r'''
            <div>Some *content*

            And more `content`.</div>
            ''',  # noqa: E501
            True
        )

    def test_html_force_span(self):
        """Test HTML with force span element."""

        self.check_markdown(
            R'''
            /// html | div
                markdown: span

            Will be parsed as inline *content*

            And more `content`.
            ///
            ''',
            r'''
            <div>Will be parsed as inline <em>content</em>

            And more <code>content</code>.</div>
            ''',  # noqa: E501
            True
        )

    def test_html_force_block(self):
        """Test HTML force block element."""

        self.check_markdown(
            R'''
            /// html | span
                markdown: block

            Some *content*

            And more `content`.
            ///
            ''',
            r'''
            <span><p>Some <em>content</em></p><p>And more <code>content</code>.</p></span>
            ''',  # noqa: E501
            True
        )

    def test_attributes(self):
        """Test attributes."""

        self.check_markdown(
            R'''
            /// html | div
                attributes: {class: some classes, id: an-id}

            Some *content*

            And more `content`.
            ///
            ''',
            r'''
            <div class="some classes" id="an-id">
            <p>Some <em>content</em></p>
            <p>And more <code>content</code>.</p>
            </div>
            ''',  # noqa: E501
            True
        )
