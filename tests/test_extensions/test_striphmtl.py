"""Test cases for StripHTML."""
from .. import util


class TestStripHTML(util.MdCase):
    """Test legacy stripping in HTML."""

    extension = ['pymdownx.striphtml']
    extension_configs = {}

    def test_multiple_inline(self):
        """Test multiple inline."""

        self.check_markdown(
            r'''
            Comments test:
            <!-- BEGIN INCLUDE -->

            - One
            - Two
            - Three
            <!-- END INCLUDE -->

            ## Paragraph

            <!-- BEGIN INCLUDE -->
            - One
            - Two
            - Three
            <!-- END INCLUDE -->
            Comments test end
            ''',
            r'''
            <p>Comments test:</p>
            <ul>
            <li>One</li>
            <li>Two</li>
            <li>Three</li>
            </ul>
            <h2>Paragraph</h2>
            <ul>
            <li>One</li>
            <li>Two</li>
            <li>Three</li>
            </ul>
            <p>Comments test end</p>
            ''',
            True
        )


class TestStripHTMLKeepComments(util.MdCase):
    """Test stripping with comments preserved."""

    extension = ['pymdownx.striphtml']
    extension_configs = {
        'pymdownx.striphtml': {
            'strip_comments': False
        }
    }

    def test_keep_comments(self):
        """Test that comments are kept and `on*` attributes are still stripped."""

        self.check_markdown(
            r'''
            <!-- comment -->

            <div onclick="alert()">text</div>
            ''',
            r'''
            <!-- comment -->

            <div>text</div>
            ''',
            True
        )
