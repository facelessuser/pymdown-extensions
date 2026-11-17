"""Test cases for Base 64."""
from .. import util
import os

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))


class TestB64(util.MdCase):
    """Test Base 64."""

    extension = ['pymdownx.b64']
    extension_configs = {
        "pymdownx.b64": {
            "base_path": CURRENT_DIR
        }
    }

    def test_in_script(self):
        """Test that we do not parse image in script."""

        self.check_markdown(
            r'''
            <script>
            var str = '<img alt="picture" src="_assets/bg.png" />'
            </script>
            ''',
            r'''
            <script>
            var str = '<img alt="picture" src="_assets/bg.png" />'
            </script>
            ''',
            True
        )

    def test_comment(self):
        """Don't convert image in comment."""

        self.check_markdown(
            '<!-- ![picture](_assets/bg.png) -->',
            '<!-- ![picture](_assets/bg.png) -->',
            True
        )

    def test_attribute_value_looks_like_src(self):
        """Test that something that looks like `src` inside another attribute's value is not converted."""

        html = self.md.postprocessors['b64'].run(
            '<img alt=\' src="_assets/bg.png"\' src="_assets/bg.png">'
        )
        self.assertTrue(html.startswith('<img alt=\' src="_assets/bg.png"\' src="data:image/png;base64,'))
        self.assertEqual(html.count('data:image/png;base64,'), 1)

    def test_script_self_closed(self):
        """Test that a self closed `script` tag is respected, so what follows is parsed as normal."""

        html = self.md.postprocessors['b64'].run('<script src="bg.js" /> <img src="_assets/bg.png">')
        self.assertTrue(html.startswith('<script src="bg.js" /> <img src="data:image/png;base64,'))

    def test_uppercase_tags(self):
        """Test that tag and attribute names are matched case insensitively."""

        html = self.md.postprocessors['b64'].run('<IMG SRC="_assets/bg.png">')
        self.assertTrue(html.startswith('<IMG src="data:image/png;base64,'))

    def test_uppercase_script(self):
        """Test that the content of an uppercase `script` is avoided, and the closing tag may differ in case."""

        html = '<SCRIPT>var s = \'<img src="_assets/bg.png">\'</script>'
        self.assertEqual(self.md.postprocessors['b64'].run(html), html)

    def test_tag_name_prefix(self):
        """Test that a tag that merely starts with `script` is not treated as a `script`."""

        html = self.md.postprocessors['b64'].run('<scripty><img src="_assets/bg.png"></scripty>')
        self.assertTrue(html.startswith('<scripty><img src="data:image/png;base64,'))

    def test_unclosed_script(self):
        """Test that an unclosed `script` or `style` is treated as running to the end, as browsers do."""

        for tag in ('script', 'style'):
            html = '<span><{}>a</span> <img alt="picture" src="_assets/bg.png">'.format(tag)
            self.check_markdown(html, '<p>{}</p>'.format(html))

    def test_unclosed_comment(self):
        """Test that an unclosed comment is treated as running to the end, as browsers do."""

        html = '<!-- unclosed <img alt="picture" src="_assets/bg.png">'
        self.assertEqual(self.md.postprocessors['b64'].run(html), html)

    def test_relative_path(self):
        """Test relative path."""

        self.check_markdown(
            '![picture](../test_extensions/_assets/bg.png)',
            '<p><img alt="picture" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHgAAAB4CAMAAAAOusbgAAAAqFBMVEU5eZdll66Yucjd7h7d7h7d7h5ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll66YuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYucgXVONTAAABDklEQVRoge3XR3ICQRBE0b/Ce2+FAAnkLeb+N9MRNBvFR0H2vuJFT3dX5VAqV6q1eqPZane6vf5gOBpPprP5YnnD72t1u95s7+53+4fHp+eX17f3j8+v78PxdC5Qi+SWkNwykltBcqtIbg3JrSO5DSS3ieS2kNw2kttBcrtIbg/J7SO5AyR3iOSOkNwxkjtBcqdI7gzJnSO5CyR3WaD0T1xrv3Hjxo0bN27cuHHjxo0bN27c63Sx9ov1nbHOF+teYd1nrHeE9X6x+gZWv8Lqk1j9GWsuYM0jrDmINX+x5j5W3sDKOVj5CivXYeVJrByLlZ+xcnuB0n/5vxA3bty4cePGjRs3bty4cePGvUj3B2JzyvcNRmTGAAAAAElFTkSuQmCC" /></p>',  # noqa: E501
            True
        )

    def test_unquoted_attribute(self):
        """Test that a tag with an unquoted attribute value is still converted."""

        self.check_markdown(
            '<img alt="picture" src="_assets/bg.png" width=100>',
            '<p><img alt="picture" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHgAAAB4CAMAAAAOusbgAAAAqFBMVEU5eZdll66Yucjd7h7d7h7d7h5ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll66YuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYucgXVONTAAABDklEQVRoge3XR3ICQRBE0b/Ce2+FAAnkLeb+N9MRNBvFR0H2vuJFT3dX5VAqV6q1eqPZane6vf5gOBpPprP5YnnD72t1u95s7+53+4fHp+eX17f3j8+v78PxdC5Qi+SWkNwykltBcqtIbg3JrSO5DSS3ieS2kNw2kttBcrtIbg/J7SO5AyR3iOSOkNwxkjtBcqdI7gzJnSO5CyR3WaD0T1xrv3Hjxo0bN27cuHHjxo0bN27c63Sx9ov1nbHOF+teYd1nrHeE9X6x+gZWv8Lqk1j9GWsuYM0jrDmINX+x5j5W3sDKOVj5CivXYeVJrByLlZ+xcnuB0n/5vxA3bty4cePGjRs3bty4cePGvUj3B2JzyvcNRmTGAAAAAElFTkSuQmCC" width=100></p>',  # noqa: E501
            True
        )

    def test_relative_path_outside(self):
        """Test relative path."""

        self.check_markdown(
            '![picture](../extensions/_assets/bg.png)',
            '<p><img alt="picture" src="../extensions/_assets/bg.png" /></p>',
            True
        )

    def test_cache_busting(self):
        """Test we can convert cache busted images."""

        self.check_markdown(
            '![picture with cache busting](_assets/bg.png?v2)',
            '<p><img alt="picture with cache busting" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHgAAAB4CAMAAAAOusbgAAAAqFBMVEU5eZdll66Yucjd7h7d7h7d7h5ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll66YuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYucgXVONTAAABDklEQVRoge3XR3ICQRBE0b/Ce2+FAAnkLeb+N9MRNBvFR0H2vuJFT3dX5VAqV6q1eqPZane6vf5gOBpPprP5YnnD72t1u95s7+53+4fHp+eX17f3j8+v78PxdC5Qi+SWkNwykltBcqtIbg3JrSO5DSS3ieS2kNw2kttBcrtIbg/J7SO5AyR3iOSOkNwxkjtBcqdI7gzJnSO5CyR3WaD0T1xrv3Hjxo0bN27cuHHjxo0bN27c63Sx9ov1nbHOF+teYd1nrHeE9X6x+gZWv8Lqk1j9GWsuYM0jrDmINX+x5j5W3sDKOVj5CivXYeVJrByLlZ+xcnuB0n/5vxA3bty4cePGjRs3bty4cePGvUj3B2JzyvcNRmTGAAAAAElFTkSuQmCC" /></p>',  # noqa: E501
            True
        )

    def test_does_not_exist(self):
        """Test handling of file that does not exist."""

        self.check_markdown(
            '![Some windows path link](file:///c:/does_not_exist.png)',
            '<p><img alt="Some windows path link" src="file:///c:/does_not_exist.png" /></p>',
            True
        )


class TestB64Unrestrict(util.MdCase):
    """Test Base 64 with unrestricted path."""

    extension = ['pymdownx.b64']
    extension_configs = {
        "pymdownx.b64": {
            "base_path": CURRENT_DIR,
            "restrict_path": False
        }
    }

    def test_relative_path_outside(self):
        """Test relative path."""

        self.check_markdown(
            '![picture](../extensions/_assets/bg.png)',
            '<p><img alt="picture" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHgAAAB4CAMAAAAOusbgAAAAqFBMVEU5eZdll66Yucjd7h7d7h7d7h5ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll66YuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYucgXVONTAAABDklEQVRoge3XR3ICQRBE0b/Ce2+FAAnkLeb+N9MRNBvFR0H2vuJFT3dX5VAqV6q1eqPZane6vf5gOBpPprP5YnnD72t1u95s7+53+4fHp+eX17f3j8+v78PxdC5Qi+SWkNwykltBcqtIbg3JrSO5DSS3ieS2kNw2kttBcrtIbg/J7SO5AyR3iOSOkNwxkjtBcqdI7gzJnSO5CyR3WaD0T1xrv3Hjxo0bN27cuHHjxo0bN27c63Sx9ov1nbHOF+teYd1nrHeE9X6x+gZWv8Lqk1j9GWsuYM0jrDmINX+x5j5W3sDKOVj5CivXYeVJrByLlZ+xcnuB0n/5vxA3bty4cePGjRs3bty4cePGvUj3B2JzyvcNRmTGAAAAAElFTkSuQmCC" /></p>',  # noqa: E501
            True
        )


class TestB64RestrictRoot(util.MdCase):
    """Test Base 64 with restricted path, but root adjusted to contained it."""

    extension = ['pymdownx.b64']
    extension_configs = {
        "pymdownx.b64": {
            "root_path": os.path.dirname(CURRENT_DIR),
            "base_path": CURRENT_DIR,
            "restrict_path": True
        }
    }

    def test_relative_path_outside(self):
        """Test relative path."""

        self.check_markdown(
            '![picture](../extensions/_assets/bg.png)',
            '<p><img alt="picture" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHgAAAB4CAMAAAAOusbgAAAAqFBMVEU5eZdll66Yucjd7h7d7h7d7h5ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll66YuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYucgXVONTAAABDklEQVRoge3XR3ICQRBE0b/Ce2+FAAnkLeb+N9MRNBvFR0H2vuJFT3dX5VAqV6q1eqPZane6vf5gOBpPprP5YnnD72t1u95s7+53+4fHp+eX17f3j8+v78PxdC5Qi+SWkNwykltBcqtIbg3JrSO5DSS3ieS2kNw2kttBcrtIbg/J7SO5AyR3iOSOkNwxkjtBcqdI7gzJnSO5CyR3WaD0T1xrv3Hjxo0bN27cuHHjxo0bN27c63Sx9ov1nbHOF+teYd1nrHeE9X6x+gZWv8Lqk1j9GWsuYM0jrDmINX+x5j5W3sDKOVj5CivXYeVJrByLlZ+xcnuB0n/5vxA3bty4cePGjRs3bty4cePGvUj3B2JzyvcNRmTGAAAAAElFTkSuQmCC" /></p>',  # noqa: E501
            True
        )
