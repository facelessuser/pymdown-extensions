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

    def test_relative_path(self):
        """Test relative path."""

        self.check_markdown(
            '![picture](../test_extensions/_assets/bg.png)',
            '<p><img alt="picture" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHgAAAB4CAMAAAAOusbgAAAAqFBMVEU5eZdll66Yucjd7h7d7h7d7h5ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll65ll66YuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYuciYucgXVONTAAABDklEQVRoge3XR3ICQRBE0b/Ce2+FAAnkLeb+N9MRNBvFR0H2vuJFT3dX5VAqV6q1eqPZane6vf5gOBpPprP5YnnD72t1u95s7+53+4fHp+eX17f3j8+v78PxdC5Qi+SWkNwykltBcqtIbg3JrSO5DSS3ieS2kNw2kttBcrtIbg/J7SO5AyR3iOSOkNwxkjtBcqdI7gzJnSO5CyR3WaD0T1xrv3Hjxo0bN27cuHHjxo0bN27c63Sx9ov1nbHOF+teYd1nrHeE9X6x+gZWv8Lqk1j9GWsuYM0jrDmINX+x5j5W3sDKOVj5CivXYeVJrByLlZ+xcnuB0n/5vxA3bty4cePGjRs3bty4cePGvUj3B2JzyvcNRmTGAAAAAElFTkSuQmCC" /></p>',  # noqa: E501
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
