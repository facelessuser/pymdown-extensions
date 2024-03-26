"""Test cases for SmartSymbols."""
from .. import util
import markdown
from pymdownx.__meta__ import parse_version

PYMD_3_6 = parse_version(markdown.__version__) >= (3, 6, 0)


class TestSmartSymbols(util.MdCase):
    """Test smart symbols works in various scenarios."""

    extension = [
        'toc',
        'smarty',
        'pymdownx.smartsymbols'
    ]
    extension_configs = {}

    def test_copyright(self):
        """Test copyright."""

        self.check_markdown(
            'Copyright (c)',
            '<p>Copyright &copy;</p>'
        )

    def test_trademark(self):
        """Test trademark."""

        self.check_markdown(
            'Trademark(tm)',
            '<p>Trademark&trade;</p>'
        )

    def test_registered(self):
        """Test registered."""

        self.check_markdown(
            'Registered(r)',
            '<p>Registered&reg;</p>'
        )

    def test_plus_minus(self):
        """Test plus/minus."""

        self.check_markdown(
            '230 +/- 10% V',
            '<p>230 &plusmn; 10% V</p>'
        )

    def test_neq(self):
        """Test not equal."""

        self.check_markdown(
            'A =/= B',
            '<p>A &ne; B</p>'
        )

    def test_right(self):
        """Test right arrow."""

        self.check_markdown(
            'right arrow -->',
            '<p>right arrow &rarr;</p>'
        )

    def test_left(self):
        """Test left arrow."""

        self.check_markdown(
            'left arrow <--',
            '<p>left arrow &larr;</p>'
        )

    def test_double_arrow(self):
        """Test double arrow."""

        self.check_markdown(
            'double arrow <-->',
            '<p>double arrow &harr;</p>'
        )

    def test_ordinals(self):
        """Test ordinals."""

        self.check_markdown(
            """
            Good: 1st 2nd 3rd 11th 12th 13th 15th 32nd 103rd

            Bad: 1th 2th 3th 2rd 1nd 22th 33th 41nd 53nd
            """,
            """
            <p>Good: 1<sup>st</sup> 2<sup>nd</sup> 3<sup>rd</sup> 11<sup>th</sup> 12<sup>th</sup> 13<sup>th</sup> 15<sup>th</sup> 32<sup>nd</sup> 103<sup>rd</sup></p>
            <p>Bad: 1th 2th 3th 2rd 1nd 22th 33th 41nd 53nd</p>
            """,  # noqa: E501
            True
        )

    def test_fractions(self):
        """Test fractions."""

        self.check_markdown(
            """
            Fraction 1/2
            Fraction 1/4
            Fraction 3/4
            Fraction 1/3
            Fraction 2/3
            Fraction 1/5
            Fraction 2/5
            Fraction 3/5
            Fraction 4/5
            Fraction 1/6
            Fraction 5/6
            Fraction 1/8
            Fraction 3/8
            Fraction 5/8
            Fraction 7/8
            """,
            """
            <p>Fraction &frac12;
            Fraction &frac14;
            Fraction &frac34;
            Fraction &#8531;
            Fraction &#8532;
            Fraction &#8533;
            Fraction &#8534;
            Fraction &#8535;
            Fraction &#8536;
            Fraction &#8537;
            Fraction &#8538;
            Fraction &#8539;
            Fraction &#8540;
            Fraction &#8541;
            Fraction &#8542;</p>
            """,
            True
        )

    def test_toc_tokens(self):
        """Ensure smart symbols end up correctly in table of content tokens."""

        md = markdown.Markdown(extensions=['toc', 'pymdownx.smartsymbols'])
        md.convert('# *Foo* =/= `bar`')
        self.assertEqual(
            md.toc_tokens,
            [
                {
                    'children': [],
                    'data-toc-label': '',
                    'html': '<em>Foo</em> &ne; <code>bar</code>',
                    'id': 'foo-bar',
                    'level': 1,
                    'name': 'Foo &ne; bar'
                }
            ] if PYMD_3_6 else [
                {
                    'level': 1,
                    'id': 'foo-bar',
                    'name': 'Foo &ne; bar',
                    'children': []
                }
            ]
        )
