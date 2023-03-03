"""Test cases for Blocks (HTML)."""
from ... import util


class TestBlocksHTML(util.MdCase):
    """Test Blocks HTML cases."""

    extension = ['pymdownx.blocks.html', 'md_in_html']

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
                markdown: inline

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
            /// html | div.some.classes#an-id[name1 name2=value name3="string value"]
            Some *content*

            And more `content`.
            ///
            ''',
            r'''
            <div class="some classes" id="an-id" name1="name1" name2="value" name3="string value">
            <p>Some <em>content</em></p>
            <p>And more <code>content</code>.</p>
            </div>
            ''',  # noqa: E501
            True
        )

    def test_bad_attributes(self):
        """Test no attributes."""

        self.check_markdown(
            R'''
            /// html | div.+
            content
            ///
            ''',
            '''
            <p>/// html | div.+
            content
            ///</p>
            ''',
            True
        )

    def test_multi_class(self):
        """Test multiple classes."""

        self.check_markdown(
            R'''
            /// html | div.a.b[class=c]
            content
            ///
            ''',
            '''
            <div class="a b c">
            <p>content</p>
            </div>
            ''',
            True
        )

    def test_multi_class2(self):
        """Test multiple classes."""

        self.check_markdown(
            R'''
            /// html | div[class="a b"].c
            content
            ///
            ''',
            '''
            <div class="a b c">
            <p>content</p>
            </div>
            ''',
            True
        )

    def test_inline_and_md_in_html(self):
        """Test inline format and HTML content."""

        self.check_markdown(
            R'''
            /// html | div
                markdown: inline

            <div markdown="block">
            **content**
            </div>

            **content**
            ///
            ''',
            '''
            <div><div markdown="block">
            **content**
            </div>



            <strong>content</strong></div>
            ''',
            True
        )

    def test_raw_and_md_in_html(self):
        """Test raw format and HTML content."""

        self.check_markdown(
            R'''
            /// html | div
                markdown: raw

                <div>
                **content**
                </div>

                this is <span>raw</span> **content**
            ///
            ''',
            '''
            <div>&lt;div&gt;
            **content**
            &lt;/div&gt;

            this is &lt;span&gt;raw&lt;/span&gt; **content**</div>
            ''',
            True
        )

    def test_html_and_html(self):
        """Test HTML mode format with HTML code."""

        self.check_markdown(
            R'''
            /// html | div
                markdown: html

                <div>
                **content**
                </div>

                this is <span>raw</span> **content**
            ///
            ''',
            '''
            <div><div>
            **content**
            </div>

            this is <span>raw</span> **content**</div>
            ''',
            True
        )

    def test_html_and_script(self):
        """Test inline format that script."""

        self.check_markdown(
            R'''
            /// html | script

                const el = document.querySelector('div');
                el.innerHTML = '<span>test</span>
            ///
            ''',
            '''
            <script>const el = document.querySelector('div');
            el.innerHTML = '<span>test</span></script>
            ''',
            True
        )
