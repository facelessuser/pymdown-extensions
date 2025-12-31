"""Test cases for Quotes."""
from .. import util


class TestQuotes(util.MdCase):
    """Test cases for repo link shortening."""

    extension = [
        'pymdownx.superfences',
        'pymdownx.quotes',
    ]

    extension_configs = {
        'pymdownx.quotes': {
            'callouts': True
        }
    }

    def test_separate_quotes(self):
        """Test separate quotes."""

        self.check_markdown(
            """
            > This is a paragraph

            > This is another paragraph.
            """,
            """
            <blockquote>
            <p>This is a paragraph</p>
            </blockquote>
            <blockquote>
            <p>This is another paragraph.</p>
            </blockquote>
            """,
            True
        )

    def test_together_quotes(self):
        """Test separate quotes."""

        self.check_markdown(
            """
            > This is a paragraph
            >
            > This is another paragraph.
            """,
            """
            <blockquote>
            <p>This is a paragraph</p>
            <p>This is another paragraph.</p>
            </blockquote>
            """,
            True
        )

    def test_callout(self):
        """Test separate quotes."""

        self.check_markdown(
            """
            > [!note]
            > Here is a note
            """,
            """
            <div class="admonition note">
            <p class="admonition-title">Note</p>
            <p>Here is a note</p>
            </div>
            """,
            True
        )

    def test_callout_title(self):
        """Test separate quotes."""

        self.check_markdown(
            """
            > [!tip] Here's a tip
            > Use a custom title!
            """,
            """
            <div class="admonition tip">
            <p class="admonition-title">Here's a tip</p>
            <p>Use a custom title!</p>
            </div>
            """,
            True
        )

    def test_callout_open(self):
        """Test separate quotes."""

        self.check_markdown(
            """
            > [!danger]+ Click to see more
            > I'm collapsible.
            """,
            """
            <details class="danger" open="open">
            <summary>Click to see more</summary>
            <p>I'm collapsible.</p>
            </details>
            """,
            True
        )

    def test_callout_closed(self):
        """Test separate quotes."""

        self.check_markdown(
            """
            > [!danger]- Click to see more
            > I'm collapsible.
            """,
            """
            <details class="danger">
            <summary>Click to see more</summary>
            <p>I'm collapsible.</p>
            </details>
            """,
            True
        )

    def test_blank_start(self):
        """Test separate quotes."""

        self.check_markdown(
            """
            >
            > [!note]
            > This is a note

            >
            >>
            >> [!note]
            >> This is a note
            """,
            """
            <div class="admonition note">
            <p class="admonition-title">Note</p>
            <p>This is a note</p>
            </div>
            <blockquote>
            <div class="admonition note">
            <p class="admonition-title">Note</p>
            <p>This is a note</p>
            </div>
            </blockquote>
            """,
            True
        )

    def test_superfences(self):
        """Test Quotes with SuperFences."""

        self.check_markdown(
            """
            This will work.

            > ```
            > Test
            >
            > Test
            > ```

            This will not.

            > ```
            > Test

            > Test
            > ```
            """,
            """
            <p>This will work.</p>
            <blockquote>
            <div class="highlight"><pre><span></span><code>Test

            Test
            </code></pre></div>
            </blockquote>
            <p>This will not.</p>
            <blockquote>
            <p>```
            Test</p>
            </blockquote>
            <blockquote>
            <p>Test
            ```</p>
            </blockquote>
            """,
            True
        )

    def test_multi_class(self):
        """Test multiple classes."""

        self.check_markdown(
            """
            > [!note | inline | end]
            > This is a note
            """,
            """
            <div class="admonition note inline end">
            <p class="admonition-title">Note</p>
            <p>This is a note</p>
            </div>
            """,
            True
        )

    def test_nested(self):
        """Test multiple classes."""

        self.check_markdown(
            """
            > [!note]
            > Content
            > > [!danger]
            > > Content
            > > > [!important]
            > > > Content
            > > Content
            > >
            > > Content
            >
            > > [!tip]
            """,
            """
            <div class="admonition note">
            <p class="admonition-title">Note</p>
            <p>Content</p>
            <div class="admonition danger">
            <p class="admonition-title">Danger</p>
            <p>Content</p>
            <div class="admonition important">
            <p class="admonition-title">Important</p>
            <p>Content
            Content</p>
            </div>
            <p>Content</p>
            </div>
            <div class="admonition tip">
            <p class="admonition-title">Tip
            </p>
            </div>
            </div>
            """,
            True
        )
