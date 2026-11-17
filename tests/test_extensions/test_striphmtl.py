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


class TestStripHTMLCase(util.MdCase):
    """Test that tag and attribute names are matched case insensitively."""

    extension = ['pymdownx.striphtml']
    extension_configs = {
        'pymdownx.striphtml': {
            'strip_attributes': ['class']
        }
    }

    def test_attribute_case(self):
        """Test that attributes are stripped regardless of case."""

        self.check_markdown(
            r'''<a ONCLICK="x" CLASS="y" OnLoad="z" href="#">text</a>''',
            r'''<p><a href="#">text</a></p>'''
        )

    def test_script_case(self):
        """Test that attributes on an uppercase `script` tag are stripped and the closing tag may differ in case."""

        self.check_markdown(
            r'''<SCRIPT ONLOAD="x" SRC="a.js">var s = '<a ONCLICK="y">';</script>''',
            r'''<SCRIPT SRC="a.js">var s = '<a ONCLICK="y">';</script>'''
        )


class TestStripHTMLNothing(util.MdCase):
    """Test that nothing is stripped when everything is disabled."""

    extension = ['pymdownx.striphtml']
    extension_configs = {
        'pymdownx.striphtml': {
            'strip_comments': False,
            'strip_js_on_attributes': False,
            'strip_attributes': []
        }
    }

    def test_nothing_to_strip(self):
        """Test that comments and attributes are left alone."""

        self.check_markdown(
            r'''
            <!-- comment -->

            <div class="a" onclick="alert()">text</div>
            ''',
            r'''
            <!-- comment -->

            <div class="a" onclick="alert()">text</div>
            ''',
            True
        )


class TestStripHTMLRaw(util.MdCase):
    """Test stripping on raw HTML, including unclosed content that Markdown would normally escape."""

    extension = ['pymdownx.striphtml']
    extension_configs = {
        'pymdownx.striphtml': {
            'strip_attributes': ['class']
        }
    }

    def check_raw(self, html, expected):
        """Check the output of the post processor."""

        self.assertEqual(self.md.postprocessors['strip-html'].run(html), expected)

    def test_comment_whitespace(self):
        """Test that whitespace around a comment is stripped only when the comment is followed by a newline."""

        self.check_raw('<p>x</p>\n<!-- a -->\n<p>y</p>\n<!-- b -->  \n<p>z</p>', '<p>x</p>\n<p>y</p>\n<p>z</p>')
        self.check_raw('<p>x</p>\n<!-- a --><p>y</p>', '<p>x</p>\n<p>y</p>')
        self.check_raw('a  \n  <!-- a -->  \n<!-- b -->\n<p>c</p>', 'a\n<p>c</p>')

    def test_unclosed_comment(self):
        """Test that an unclosed comment is left alone and what follows is still processed."""

        self.check_raw(
            '<p>x</p>\n<!-- unclosed\n<p onclick="z" class="c">q</p>',
            '<p>x</p>\n<!-- unclosed\n<p>q</p>'
        )
        self.check_raw('<!-- a -->\n<!-- unclosed <p onclick="z">', '\n<!-- unclosed <p>')

    def test_unclosed_script(self):
        """Test that an unclosed `script` or `style` has its attributes stripped and what follows is still processed."""

        self.check_raw(
            '<script onload="y" class="c">unclosed\n<p onclick="z">q</p>',
            '<script>unclosed\n<p>q</p>'
        )
        self.check_raw(
            '<style class="a">x</style>\n<style class="a">unclosed\n<p class="z">q</p>',
            '<style>x</style>\n<style>unclosed\n<p>q</p>'
        )

    def test_script_content(self):
        """Test that the content of a closed `script` is left alone, including anything that looks like a tag."""

        self.check_raw(
            '<script onload="y">var s = "<a onclick=\'x\'>"; <!-- c --></script><p onclick="z">q</p>',
            '<script>var s = "<a onclick=\'x\'>"; <!-- c --></script><p>q</p>'
        )
