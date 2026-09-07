"""Test caret."""
from .. import util


class TestMarkSmart(util.MdCase):
    """Test Mark smart cases."""

    extension = [
        'pymdownx.mark'
    ]
    extension_configs = {
        "pymdownx.mark": {
            "smart_mark": True
        }
    }

    def test_complex_cases(self):
        """Test some complex cases."""

        self.check_markdown(
            R'''
            Test: == Won't mark ==

            Test: ==Will mark==

            Test: ==A lot of equals=============is okay==

            Test: ==This will NOT all be marked ==because of the placement of the center equal signs.==

            Test: ==This will all be marked == because of the placement of the center equal sings.==

            Test: ==This will NOT all be marked== because of the placement of the center equal sings.==

            Test: ==This will all be marked= because of the token is less than that of the surrounding.==
            ''',
            '''
            <p>Test: == Won't mark ==</p>
            <p>Test: <mark>Will mark</mark></p>
            <p>Test: <mark>A lot of equals=============is okay</mark></p>
            <p>Test: ==This will NOT all be marked <mark>because of the placement of the center equal signs.</mark></p>
            <p>Test: <mark>This will all be marked == because of the placement of the center equal sings.</mark></p>
            <p>Test: <mark>This will NOT all be marked</mark> because of the placement of the center equal sings.==</p>
            <p>Test: <mark>This will all be marked= because of the token is less than that of the surrounding.</mark></p>
            ''',  # noqa: E501
            True
        )


class TestMarkNoSmart(util.MdCase):
    """Test Mark dumb cases."""

    extension = [
        'pymdownx.mark'
    ]
    extension_configs = {
        "pymdownx.mark": {
            "smart_mark": False
        }
    }

    def test_complex_cases(self):
        """Test some complex cases."""

        self.check_markdown(
            R'''
            Test: == Won't mark ==

            Test: ==Will mark==

            Test: ==All will = be marked==

            Test: ==All will not=== be marked==

            Test: ==All will === be marked==
            ''',
            '''
            <p>Test: == Won't mark ==</p>
            <p>Test: <mark>Will mark</mark></p>
            <p>Test: <mark>All will = be marked</mark></p>
            <p>Test: <mark>All will not</mark>= be marked==</p>
            <p>Test: <mark>All will === be marked</mark></p>
            ''',
            True
        )
