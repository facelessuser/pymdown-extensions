"""Test cases for SaneHeaders."""
from .. import util


class TestSaneHeadersWithMagicLink(util.MdCase):
    """Test cases for SaneHeaders and MagicLink (the motivation behind creating SaneHeaders)."""

    extension = [
        'pymdownx.saneheaders',
        'pymdownx.magiclink',
    ]

    extension_configs = {
        'pymdownx.magiclink': {
            'repo_url_shorthand': True,
            'user': 'facelessuser',
            'repo': 'pymdown-extensions'
        }
    }

    def test_header1(self):
        """Test header level 1."""

        self.check_markdown(
            r'# Header',
            r'<h1>Header</h1>'
        )

    def test_header2(self):
        """Test header level 2."""

        self.check_markdown(
            r'## Header',
            r'<h2>Header</h2>'
        )

    def test_header3(self):
        """Test header level 3."""

        self.check_markdown(
            r'### Header',
            r'<h3>Header</h3>'
        )

    def test_header4(self):
        """Test header level 4."""

        self.check_markdown(
            r'#### Header',
            r'<h4>Header</h4>'
        )

    def test_header5(self):
        """Test header level 5."""

        self.check_markdown(
            r'##### Header',
            r'<h5>Header</h5>'
        )

    def test_header6(self):
        """Test header level 6."""

        self.check_markdown(
            r'###### Header',
            r'<h6>Header</h6>'
        )

    def test_header_trailing(self):
        """Test header trailing hashes."""

        self.check_markdown(
            r'## Header ##',
            r'<h2>Header</h2>'
        )

    def test_too_many_hashes(self):
        """Test header with too many hashes."""

        self.check_markdown(
            r'####### Header',
            r'<p>####### Header</p>'
        )

    def test_no_header(self):
        """Test no header match."""

        self.check_markdown(
            r'##Header',
            r'<p>##Header</p>'
        )

    def test_header_with_magiclink(self):
        """Test no header match."""

        self.check_markdown(
            r'#3',
            r'<p><a class="magiclink magiclink-github magiclink-issue" href="https://github.com/facelessuser/pymdown-extensions/issues/3" title="GitHub Issue: facelessuser/pymdown-extensions #3">#3</a></p>'  # noqa: E501
        )
