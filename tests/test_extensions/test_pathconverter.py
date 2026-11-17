"""Test cases for PathConverter."""
from .. import util
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)


class TestRelative(util.MdCase):
    """Test relative paths."""

    extension = ["pymdownx.pathconverter"]
    extension_configs = {
        "pymdownx.pathconverter": {
            "base_path": CURRENT_DIR,
            "relative_path": PARENT_DIR
        }
    }

    def test_in_script(self):
        """Test that we do not parse image in script."""

        self.check_markdown(
            r'''
            <script>
            var str = '<img alt="picture" src="../test_extensions/_assets/bg.png" />'
            </script>
            ''',
            r'''
            <script>
            var str = '<img alt="picture" src="../test_extensions/_assets/bg.png" />'
            </script>
            ''',
            True
        )

    def test_comment(self):
        """Test comment."""

        self.check_markdown(
            r'<!-- ![picture](../test_extensions/_assets/bg.png) -->',
            r'<!-- ![picture](../test_extensions/_assets/bg.png) -->'
        )

    def test_script_src(self):
        """Test that the `src` of a `script` tag is converted, but its content is not."""

        self.check_markdown(
            r'''<script src="../test_extensions/_assets/bg.js" async>
var str = '<img alt="picture" src="../test_extensions/_assets/bg.png" />'
</script> <img alt="picture" src="../test_extensions/_assets/bg.png">''',
            r'''<script src="test_extensions/_assets/bg.js" async>
var str = '<img alt="picture" src="../test_extensions/_assets/bg.png" />'
</script>
<p><img alt="picture" src="test_extensions/_assets/bg.png"></p>'''
        )

    def test_script_src_unclosed(self):
        """Test that the `src` of an unclosed `script` tag is converted."""

        self.check_markdown(
            '<script src="../test_extensions/_assets/bg.js">',
            '<script src="test_extensions/_assets/bg.js">'
        )

    def test_script_self_closed(self):
        """Test that a self closed `script` tag is respected, so what follows is parsed as normal."""

        self.check_markdown(
            '''<script src="../test_extensions/_assets/bg.js" /> <img src="../test_extensions/_assets/bg.png">''',
            '''<script src="test_extensions/_assets/bg.js" />
<p><img src="test_extensions/_assets/bg.png"></p>'''
        )

    def test_attribute_value_looks_like_src(self):
        """Test that something that looks like `src` inside another attribute's value is not converted."""

        self.check_markdown(
            r'''<img alt=' src="../test_extensions/_assets/bg.png"' src="../test_extensions/_assets/bg.png">''',
            r'''<p><img alt=' src="../test_extensions/_assets/bg.png"' src="test_extensions/_assets/bg.png"></p>'''
        )

    def test_uppercase_tags(self):
        """Test that tag and attribute names are matched case insensitively."""

        self.check_markdown(
            '''<IMG SRC="../test_extensions/_assets/bg.png"> <A HREF="../test_extensions/_assets/bg.png">x</A>''',
            '''<p><IMG SRC="test_extensions/_assets/bg.png"> <A HREF="test_extensions/_assets/bg.png">x</A></p>'''
        )

    def test_uppercase_script(self):
        """Test that the content of an uppercase `script` is avoided, and the closing tag may differ in case."""

        self.check_markdown(
            '''<SCRIPT SRC="../test_extensions/_assets/bg.js">var s = '<img src="../x/bg.png">'</script>''',
            '''<SCRIPT SRC="test_extensions/_assets/bg.js">var s = '<img src="../x/bg.png">'</script>'''
        )

    def test_tag_name_prefix(self):
        """Test that a tag that merely starts with `script` is not treated as a `script`."""

        self.check_markdown(
            '''<scripty><img src="../test_extensions/_assets/bg.png"></scripty>''',
            '''<p><scripty><img src="test_extensions/_assets/bg.png"></scripty></p>'''
        )

    def test_unclosed_script(self):
        """Test that an unclosed `script` or `style` is treated as running to the end, as browsers do."""

        for tag in ('script', 'style'):
            html = '<span><{}>a</span> <img alt="picture" src="../test_extensions/_assets/bg.png">'.format(tag)
            self.check_markdown(html, '<p>{}</p>'.format(html))

    def test_unclosed_comment(self):
        """Test that an unclosed comment is treated as running to the end, as browsers do."""

        html = '<!-- unclosed <img alt="picture" src="../test_extensions/_assets/bg.png">'
        self.assertEqual(self.md.postprocessors['path-converter'].run(html), html)

    def test_whitespace_before_comment(self):
        """Test that comments preceded by whitespace are still avoided."""

        html = '<p>x</p>\n  \n<!-- <img alt="picture" src="../test_extensions/_assets/bg.png"> -->  \n<p>y</p>'
        self.assertEqual(self.md.postprocessors['path-converter'].run(html), html)

    def test_relative_path(self):
        """Test relative path."""

        self.check_markdown(
            r'![picture](../test_extensions/_assets/bg.png)',
            r'<p><img alt="picture" src="test_extensions/_assets/bg.png" /></p>'
        )

    def test_unquoted_attribute(self):
        """Test that a tag with an unquoted attribute value is still converted."""

        self.check_markdown(
            r'<img alt="picture" src="../test_extensions/_assets/bg.png" width=100>',
            r'<p><img alt="picture" src="test_extensions/_assets/bg.png" width=100></p>'
        )

    def test_file_win_file_path_root(self):
        """Test windows file:// path with root slash."""

        self.check_markdown(
            r'[file link windows abs](file:///c:/path/file.html)',
            r'<p><a href="file:///c:/path/file.html">file link windows abs</a></p>'
        )

    def test_win_file_path(self):
        """Test windows file:// path."""

        self.check_markdown(
            r'[file link windows abs2](file://c:/path/file.html)',
            r'<p><a href="file://c:/path/file.html">file link windows abs2</a></p>'
        )

    def test_file_root(self):
        """Test Linux/Unix style root file:// path."""

        self.check_markdown(
            r'[file link abs](file:///path/file.html)',
            r'<p><a href="file:///path/file.html">file link abs</a></p>'
        )

    def test_root(self):
        """Test /root path."""

        self.check_markdown(
            r'[absolute](/absolute)',
            r'<p><a href="/absolute">absolute</a></p>'
        )

    def test_url(self):
        """Test normal URL."""

        self.check_markdown(
            r'[link](http://www.google.com)',
            r'<p><a href="http://www.google.com">link</a></p>'
        )

    def test_fragment(self):
        """Test HTML fragment."""

        self.check_markdown(
            r'[fragment](#fragment)',
            r'<p><a href="#fragment">fragment</a></p>'
        )

    def test_windows(self):
        """Test Windows file path."""

        self.check_markdown(
            r'[windows path abs](c:/path/file.html)',
            r'<p><a href="c:/path/file.html">windows path abs</a></p>'
        )

    def test_network_path(self):
        """Test network path."""

        self.check_markdown(
            r'[windows network path](//network/path/file.html)',
            r'<p><a href="//network/path/file.html">windows network path</a></p>'
        )

    def test_strange_url(self):
        """Test strange URL."""

        self.check_markdown(
            r'[strange link](strange://odd/link/file.html)',
            r'<p><a href="strange://odd/link/file.html">strange link</a></p>'
        )

    def test_strange_url2(self):
        """Test additional strange URL."""

        self.check_markdown(
            r'[strange link 2](strange://www.odd.com/link/file.html)',
            r'<p><a href="strange://www.odd.com/link/file.html">strange link 2</a></p>'
        )

    def test_scheme_without_netloc(self):
        """Test URLs with a scheme but no network location."""

        self.check_markdown(
            r'[magnet](magnet:?xt=urn:btih:abc) [sms](sms:+123) [xmpp](xmpp:me@example.org)',
            r'<p><a href="magnet:?xt=urn:btih:abc">magnet</a> <a href="sms:+123">sms</a> '
            r'<a href="xmpp:me@example.org">xmpp</a></p>'
        )

    def test_mail(self):
        """Test mail link."""

        self.check_markdown(
            r'<mail@mail.com>',
            r'<p><a href="&#109;&#97;&#105;&#108;&#116;&#111;&#58;&#109;&#97;&#105;&#108;&#64;&#109;&#97;&#105;&#108;'
            r'&#46;&#99;&#111;&#109;">&#109;&#97;&#105;&#108;&#64;&#109;&#97;&#105;&#108;&#46;&#99;&#111;&#109;</a></p>'
        )


class TestAbsolute(util.MdCase):
    """Test absolute paths."""

    extension = ["pymdownx.pathconverter"]
    extension_configs = {
        "pymdownx.pathconverter": {
            "base_path": "/Some/fake/path",
            "absolute": True
        }
    }

    def test_in_script(self):
        """Test that we do not parse image in script."""

        self.check_markdown(
            r'''
            <script>
            var str = '<img alt="picture" src="../test_extensions/_assets/bg.png" />'
            </script>
            ''',
            r'''
            <script>
            var str = '<img alt="picture" src="../test_extensions/_assets/bg.png" />'
            </script>
            ''',
            True
        )

    def test_comment(self):
        """Test comment."""

        self.check_markdown(
            r'<!-- ![picture](../test_extensions/_assets/bg.png) -->',
            r'<!-- ![picture](../test_extensions/_assets/bg.png) -->'
        )

    def test_relative_path(self):
        """Test relative path."""

        self.check_markdown(
            r'![picture](./test_extensions/_assets/bg.png)',
            r'<p><img alt="picture" src="/Some/fake/path/test_extensions/_assets/bg.png" /></p>'
        )

    def test_unquoted_attribute(self):
        """Test that a tag with an unquoted attribute value is still converted."""

        self.check_markdown(
            r'<a href="./test_extensions/page.html" class=link>page</a>',
            r'<p><a href="/Some/fake/path/test_extensions/page.html" class=link>page</a></p>'
        )

    def test_file_win_file_path_root(self):
        """Test windows file:// path with root slash."""

        self.check_markdown(
            r'[file link windows abs](file:///c:/path/file.html)',
            r'<p><a href="file:///c:/path/file.html">file link windows abs</a></p>'
        )

    def test_win_file_path(self):
        """Test windows file:// path."""

        self.check_markdown(
            r'[file link windows abs2](file://c:/path/file.html)',
            r'<p><a href="file://c:/path/file.html">file link windows abs2</a></p>'
        )

    def test_file_root(self):
        """Test Linux/Unix style root file:// path."""

        self.check_markdown(
            r'[file link abs](file:///path/file.html)',
            r'<p><a href="file:///path/file.html">file link abs</a></p>'
        )

    def test_root(self):
        """Test /root path."""

        self.check_markdown(
            r'[absolute](/absolute)',
            r'<p><a href="/absolute">absolute</a></p>'
        )

    def test_url(self):
        """Test normal URL."""

        self.check_markdown(
            r'[link](http://www.google.com)',
            r'<p><a href="http://www.google.com">link</a></p>'
        )

    def test_fragment(self):
        """Test HTML fragment."""

        self.check_markdown(
            r'[fragment](#fragment)',
            r'<p><a href="#fragment">fragment</a></p>'
        )

    def test_windows(self):
        """Test Windows file path."""

        self.check_markdown(
            r'[windows path abs](c:/path/file.html)',
            r'<p><a href="c:/path/file.html">windows path abs</a></p>'
        )

    def test_network_path(self):
        """Test network path."""

        self.check_markdown(
            r'[windows network path](//network/path/file.html)',
            r'<p><a href="//network/path/file.html">windows network path</a></p>'
        )

    def test_strange_url(self):
        """Test strange URL."""

        self.check_markdown(
            r'[strange link](strange://odd/link/file.html)',
            r'<p><a href="strange://odd/link/file.html">strange link</a></p>'
        )

    def test_strange_url2(self):
        """Test additional strange URL."""

        self.check_markdown(
            r'[strange link 2](strange://www.odd.com/link/file.html)',
            r'<p><a href="strange://www.odd.com/link/file.html">strange link 2</a></p>'
        )

    def test_scheme_without_netloc(self):
        """Test URLs with a scheme but no network location."""

        self.check_markdown(
            r'[magnet](magnet:?xt=urn:btih:abc) [sms](sms:+123) [xmpp](xmpp:me@example.org)',
            r'<p><a href="magnet:?xt=urn:btih:abc">magnet</a> <a href="sms:+123">sms</a> '
            r'<a href="xmpp:me@example.org">xmpp</a></p>'
        )

    def test_mail(self):
        """Test mail link."""

        self.check_markdown(
            r'<mail@mail.com>',
            r'<p><a href="&#109;&#97;&#105;&#108;&#116;&#111;&#58;&#109;&#97;&#105;&#108;&#64;&#109;&#97;&#105;&#108;'
            r'&#46;&#99;&#111;&#109;">&#109;&#97;&#105;&#108;&#64;&#109;&#97;&#105;&#108;&#46;&#99;&#111;&#109;</a></p>'
        )


class TestAbsoluteFileScheme(TestAbsolute):
    """Test absolute paths with file:// scheme."""

    extension = ["pymdownx.pathconverter"]
    extension_configs = {
        "pymdownx.pathconverter": {
            "base_path": "/Some/fake/path",
            "absolute": True,
            "file_scheme": True,
        }
    }

    def test_relative_path(self):
        """Test relative path."""

        self.check_markdown(
            r'![picture](./test_extensions/_assets/bg.png)',
            r'<p><img alt="picture" src="file:///Some/fake/path/test_extensions/_assets/bg.png" /></p>'
        )

    def test_unquoted_attribute(self):
        """Test that a tag with an unquoted attribute value is still converted."""

        self.check_markdown(
            r'<a href="./test_extensions/page.html" class=link>page</a>',
            r'<p><a href="file:///Some/fake/path/test_extensions/page.html" class=link>page</a></p>'
        )


class TestWindowsAbs(util.MdCase):
    """Test windows specific cases for absolute."""

    extension = ["pymdownx.pathconverter"]
    extension_configs = {
        "pymdownx.pathconverter": {
            "base_path": "C:/Some/fake/path",
            "absolute": True
        }
    }

    def test_windows_root_conversion(self):
        """Test Windows c:/ Conversion."""

        if util.is_win():
            self.check_markdown(
                r'![picture](./extensions/_assets/bg.png)',
                r'<p><img alt="picture" src="/C:/Some/fake/path/extensions/_assets/bg.png" /></p>'
            )
        else:
            self.check_markdown(
                r'![picture](./extensions/_assets/bg.png)',
                r'<p><img alt="picture" src="/C%3A/Some/fake/path/extensions/_assets/bg.png" /></p>'
            )


class TestWindowsAbsFileScheme(util.MdCase):
    """Test windows specific cases for absolute with file:// scheme."""

    extension = ["pymdownx.pathconverter"]
    extension_configs = {
        "pymdownx.pathconverter": {
            "base_path": "C:/Some/fake/path",
            "absolute": True,
            "file_scheme": True,
        }
    }

    def test_windows_root_conversion(self):
        """Test Windows c:/ Conversion."""
        if util.is_win():
            self.check_markdown(
                r'![picture](./extensions/_assets/bg.png)',
                r'<p><img alt="picture" src="file:///C:/Some/fake/path/extensions/_assets/bg.png" /></p>'
            )
        else:
            self.check_markdown(
                r'![picture](./extensions/_assets/bg.png)',
                r'<p><img alt="picture" src="file:///C%3A/Some/fake/path/extensions/_assets/bg.png" /></p>'
            )


class TestWindowsRel(util.MdCase):
    """Test windows specific cases for relative."""

    extension = ["pymdownx.pathconverter"]
    extension_configs = {
        "pymdownx.pathconverter": {
            "base_path": "C:/Some/fake/path",
            "relative_path": "C:/Some/other/path"
        }
    }

    def test_windows_root_conversion(self):
        """Test Windows c:/ Conversion."""

        if util.is_win():
            self.check_markdown(
                r'![picture](./extensions/_assets/bg.png)',
                r'<p><img alt="picture" src="../../fake/path/extensions/_assets/bg.png" /></p>'
            )
        else:
            self.check_markdown(
                r'![picture](./extensions/_assets/bg.png)',
                r'<p><img alt="picture" src="../../fake/path/extensions/_assets/bg.png" /></p>'
            )


class TestTags(util.MdCase):
    """Test limiting which tags are converted."""

    extension = ["pymdownx.pathconverter"]
    extension_configs = {
        "pymdownx.pathconverter": {
            "base_path": "/Some/fake/path",
            "absolute": True,
            "tags": "img a link"
        }
    }

    def test_script_not_in_tags(self):
        """Test that `script` is not converted when it is not one of the tags."""

        self.check_markdown(
            '<script src="bg.js"></script>',
            '<script src="bg.js"></script>'
        )
