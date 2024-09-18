"""Test cases for Details."""
from .. import util


class TestFancyLists(util.MdCase):
    """Test fancy lists."""

    extension = ['pymdownx.fancylists', 'pymdownx.saneheaders']
    extension_configs = {}

    def test_unordered(self):
        """Test unordered lists."""

        self.check_markdown(
            R'''
            - item 1
            * item 2
            + item 3
            ''',
            r'''
            <ul>
            <li>item 1</li>
            <li>item 2</li>
            <li>item 3</li>
            </ul>
            ''',
            True
        )

    def test_ordered(self):
        """Test ordered lists."""

        self.check_markdown(
            R'''
            1. item 1
            2. item 2
            3. item 3
            ''',
            r'''
            <ol type="1">
            <li>item 1</li>
            <li>item 2</li>
            <li>item 3</li>
            </ol>
            ''',
            True
        )

    def test_ordered_paren(self):
        """Test ordered lists with parenthesis."""

        self.check_markdown(
            R'''
            1) item 1
            2) item 2
            3) item 3
            ''',
            r'''
            <ol type="1">
            <li>item 1</li>
            <li>item 2</li>
            <li>item 3</li>
            </ol>
            ''',
            True
        )

    def test_oredered_generic(self):
        """Test generic ordered list."""

        self.check_markdown(
            R'''
            #. item 1
            #. item 2
            #. item 3
            ''',
            r'''
            <ol type="1">
            <li>item 1</li>
            <li>item 2</li>
            <li>item 3</li>
            </ol>
            ''',
            True
        )

    def test_oredered_generic_paren(self):
        """Test generic ordered list with parenthesis."""

        self.check_markdown(
            R'''
            #) item 1
            #) item 2
            #) item 3
            ''',
            r'''
            <ol type="1">
            <li>item 1</li>
            <li>item 2</li>
            <li>item 3</li>
            </ol>
            ''',
            True
        )

    def test_roman(self):
        """Test Roman numeral lists."""

        self.check_markdown(
            R'''
            i.   item 1
            ii.  item 2
            iii. item 3
            iv.  item 4
            v.   item 5
            vi.  item 6
            ''',
            r'''
            <ol type="i">
            <li>item 1</li>
            <li>item 2</li>
            <li>item 3</li>
            <li>item 4</li>
            <li>item 5</li>
            <li>item 6</li>
            </ol>
            ''',
            True
        )

    def test_roman_paren(self):
        """Test Roman numeral lists with parenthesis."""

        self.check_markdown(
            R'''
            i)   item 1
            ii)  item 2
            iii) item 3
            ''',
            r'''
            <ol type="i">
            <li>item 1</li>
            <li>item 2</li>
            <li>item 3</li>
            </ol>
            ''',
            True
        )

    def test_roman_upper(self):
        """Test Roman numeral uppercase lists."""

        self.check_markdown(
            R'''
            I.   item 1
            II.  item 2
            III. item 3
            ''',
            r'''
            <ol type="I">
            <li>item 1</li>
            <li>item 2</li>
            <li>item 3</li>
            </ol>
            ''',
            True
        )

    def test_roman_upper_paren(self):
        """Test Roman numeral uppercase lists with parenthesis."""

        self.check_markdown(
            R'''
            I)   item 1
            II)  item 2
            III) item 3
            ''',
            r'''
            <ol type="I">
            <li>item 1</li>
            <li>item 2</li>
            <li>item 3</li>
            </ol>
            ''',
            True
        )

    def test_alpha(self):
        """Test alphabetical lists."""

        self.check_markdown(
            R'''
            a. item 1
            b. item 2
            c. item 3
            ''',
            r'''
            <ol type="a">
            <li>item 1</li>
            <li>item 2</li>
            <li>item 3</li>
            </ol>
            ''',
            True
        )

    def test_alpha_paren(self):
        """Test alphabetical lists with parenthesis."""

        self.check_markdown(
            R'''
            a) item 1
            b) item 2
            c) item 3
            ''',
            r'''
            <ol type="a">
            <li>item 1</li>
            <li>item 2</li>
            <li>item 3</li>
            </ol>
            ''',
            True
        )

    def test_alpha_upper(self):
        """Test alphabetical uppercase lists."""

        self.check_markdown(
            R'''
            A.  item 1
            B.  item 2
            C.  item 3
            ''',
            r'''
            <ol type="A">
            <li>item 1</li>
            <li>item 2</li>
            <li>item 3</li>
            </ol>
            ''',
            True
        )

    def test_alpha_upper_paren(self):
        """Test alphabetical uppercase lists with parenthesis."""

        self.check_markdown(
            R'''
            A) item 1
            B) item 2
            C) item 3
            ''',
            r'''
            <ol type="A">
            <li>item 1</li>
            <li>item 2</li>
            <li>item 3</li>
            </ol>
            ''',
            True
        )

    def test_alpha_two_spaces(self):
        """Test alphabetical two space uppercase requirement."""

        self.check_markdown(
            R'''
            A.  item 1
            A. item 2
            ''',
            R'''
            <ol type="A">
            <li>item 1
            A. item 2</li>
            </ol>
            ''',
            True
        )

    def test_roman_alpha(self):
        """Test behavior of alphabetical and Roman numeral."""

        self.check_markdown(
            R'''
            v) item 1
            a) item 2

            i. item 1
            a. item 1
            b. item 2

            ''',
            r'''
            <ol start="22" type="a">
            <li>item 1</li>
            <li>item 2</li>
            </ol>
            <ol type="i">
            <li>item 1</li>
            </ol>
            <ol type="a">
            <li>item 1</li>
            <li>item 2</li>
            </ol>
            ''',
            True
        )

    def test_bad_roman(self):
        """Test bad Roman numeral."""

        self.check_markdown(
            R'''
            iviv. item 1
            ''',
            R'''
            <p>iviv. item 1</p>
            ''',
            True
        )


    def test_roman_start(self):
        """Test bad Roman numeral."""

        self.check_markdown(
            R'''
            iv. item 1
            v.  item 2
            ''',
            R'''
            <ol start="4" type="i">
            <li>item 1</li>
            <li>item 2</li>
            </ol>
            ''',
            True
        )

    def test_roman_two_spaces(self):
        """Test Roman numeral two space uppercase requirement."""

        self.check_markdown(
            R'''
            I.  item 1
            I. item 2
            ''',
            R'''
            <ol type="I">
            <li>item 1
            I. item 2</li>
            </ol>
            ''',
            True
        )

    def test_roman_relaxed(self):
        """Test cases related to our less strict approach."""

        self.check_markdown(
            R'''
            iiii.  item 1

            MCCCCCCVI. item 1
            ''',
            R'''
            <ol start="4" type="i">
            <li>item 1</li>
            </ol>
            <ol start="1606" type="I">
            <li>item 1</li>
            </ol>
            ''',
            True
        )

    def test_list_nested_same_line(self):
        """Test list nested on same line."""

        self.check_markdown(
            R'''
            a) a) subitem1
                b) subitem2
            ''',
            R'''
            <ol type="a">
            <li>
            <ol type="a">
            <li>subitem1</li>
            <li>subitem2</li>
            </ol>
            </li>
            </ol>
            ''',
            True
        )

    def test_indented_content(self):
        """Test indented content."""

        self.check_markdown(
            R'''
            #.  A paragraph
                that is short.

                Another paragraph.

                #. A sublist

                Another paragraph.

            #. A new list item.
            ''',
            R'''
            <ol type="1">
            <li>
            <p>A paragraph
                that is short.</p>
            <p>Another paragraph.</p>
            <ol type="1">
            <li>A sublist</li>
            </ol>
            <p>Another paragraph.</p>
            </li>
            <li>
            <p>A new list item.</p>
            </li>
            </ol>
            ''',
            True
        )

    def test_unindented_content(self):
        """Test indented content with unindented lines."""

        self.check_markdown(
            R'''
            #.  A paragraph
            that is short.

                Another paragraph
            with unindented lines.

                #.  A sublist
                with unindented lines.

            #.  A new list item.
            ''',
            R'''
            <ol type="1">
            <li>
            <p>A paragraph
            that is short.</p>
            <p>Another paragraph
            with unindented lines.</p>
            <ol type="1">
            <li>A sublist
            with unindented lines.</li>
            </ol>
            </li>
            <li>
            <p>A new list item.</p>
            </li>
            </ol>
            ''',
            True
        )

    def test_header_case(self):
        """Test case where list follows header."""

        self.check_markdown(
            R'''
            Tight List:

            * # Header1
            Line 1-2 - **not** a header *or* paragraph!
            * # Header2
            Line 2-2 - not a header or paragraph!

            Loose List:

            * # Header1
            Line 1-2 - *a* paragraph

            * # Header2
            Line 2-2 - a paragraph
            ''',
            R'''
            <p>Tight List:</p>
            <ul>
            <li>
            <h1>Header1</h1>
            Line 1-2 - <strong>not</strong> a header <em>or</em> paragraph!</li>
            <li>
            <h1>Header2</h1>
            Line 2-2 - not a header or paragraph!</li>
            </ul>
            <p>Loose List:</p>
            <ul>
            <li>
            <h1>Header1</h1>
            <p>Line 1-2 - <em>a</em> paragraph</p>
            </li>
            <li>
            <h1>Header2</h1>
            <p>Line 2-2 - a paragraph</p>
            </li>
            </ul>
            ''',
            True
        )

    def test_mixed_nesting_case(self):
        """Test mixed nesting case."""

        self.check_markdown(
            R'''
            * item 1
                * item 1-1
                * item 1-2
                    * item 1-2-1
            * item 2
            * item 3
            * item 4
                * item 4-1
                * item 4-2
                * item 4-3

                    Paragraph under item 4-3

                Paragraph under item 4
            ''',
            R'''
            <ul>
            <li>item 1<ul>
            <li>item 1-1</li>
            <li>item 1-2<ul>
            <li>item 1-2-1</li>
            </ul>
            </li>
            </ul>
            </li>
            <li>item 2</li>
            <li>item 3</li>
            <li>
            <p>item 4</p>
            <ul>
            <li>item 4-1</li>
            <li>item 4-2</li>
            <li>
            <p>item 4-3</p>
            <p>Paragraph under item 4-3</p>
            </li>
            </ul>
            <p>Paragraph under item 4</p>
            </li>
            </ul>
            ''',
            True
        )

    def test_tight_loose_mix(self):
        """Test inconsistent loose and tight list item spacing."""

        self.check_markdown(
            R'''
            * item 1
            * item 2

            * item 3
            * item 4
            ''',
            R'''
            <ul>
            <li>item 1</li>
            <li>
            <p>item 2</p>
            </li>
            <li>
            <p>item 3</p>
            </li>
            <li>item 4</li>
            </ul>
            ''',
            True
        )


class TestFancyListsDisableAlpha(util.MdCase):
    """Test fancy lists."""

    extension = ['pymdownx.fancylists', 'pymdownx.saneheaders']
    extension_configs = {
        'pymdownx.fancylists': {
            'additional_ordered_styles': ['roman', 'generic']
        }
    }

    def test_no_alpha(self):
        """Test lists when alphabetical lists is disabled."""

        self.check_markdown(
            R'''
            i.  item 1
            ii. item 2

            a. item 1

            V.  item 1
            ''',
            R'''
            <ol type="i">
            <li>item 1</li>
            <li>item 2</li>
            </ol>
            <p>a. item 1</p>
            <ol start="5" type="I">
            <li>item 1</li>
            </ol>
            ''',
            True
        )


class TestFancyListsDisableRoman(util.MdCase):
    """Test fancy lists."""

    extension = ['pymdownx.fancylists', 'pymdownx.saneheaders']
    extension_configs = {
        'pymdownx.fancylists': {
            'additional_ordered_styles': ['alpha', 'generic']
        }
    }

    def test_no_roman(self):
        """Test lists when Roman numerals lists is disabled."""

        self.check_markdown(
            R'''
            i. item 1
            ii. item 2

            a. item 2

            V.  item 1
            ''',
            R'''
            <ol start="9" type="a">
            <li>
            <p>item 1
            ii. item 2</p>
            </li>
            <li>
            <p>item 2</p>
            </li>
            </ol>
            <ol start="22" type="A">
            <li>item 1</li>
            </ol>
            ''',
            True
        )
