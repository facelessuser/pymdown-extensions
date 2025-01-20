"""Test cases for Details."""
from .. import util


class TestFancyLists(util.MdCase):
    """Test fancy lists."""

    extension = ['pymdownx.fancylists', 'pymdownx.saneheaders']
    extension_configs = {}

    def test_fail_case(self):
        """Test failed case."""

        self.check_markdown(
            """
            1. foo
            . bar

            1) foo
            ) bar
            """,
            """
            <ol type="1">
            <li>foo
            . bar</li>
            </ol>
            <ol type="1">
            <li>foo
            ) bar</li>
            </ol>
            """,
            True
        )

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

    def test_ordered_generic(self):
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

    def test_ordered_generic_paren(self):
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

    def test_ordered_generic_switch(self):
        """Test generic ordered list switching over to other style."""

        self.check_markdown(
            R'''
            #. item 1
            #. item 2
            #) item 1
            #) item 2
            ''',
            r'''
            <ol type="1">
            <li>item 1</li>
            <li>item 2</li>
            </ol>
            <ol type="1">
            <li>item 1</li>
            <li>item 2</li>
            </ol>
            ''',
            True
        )

    def test_ordered_generic_inherit(self):
        """Test generic ordered list inheritance."""

        self.check_markdown(
            R'''
            i.  item i
            #.  item ii
            #.  item iii
            I.  New list
            ''',
            r'''
            <ol type="i">
            <li>item i</li>
            <li>item ii</li>
            <li>item iii</li>
            </ol>
            <ol type="I">
            <li>New list</li>
            </ol>
            ''',
            True
        )

    def test_ordered_generic_inherit_no_change(self):
        """Test generic ordered list inheritance no new list if same type."""

        self.check_markdown(
            R'''
            i.  item i
            #.  item ii
            #.  item iii
            iv. item iv
            ''',
            r'''
            <ol type="i">
            <li>item i</li>
            <li>item ii</li>
            <li>item iii</li>
            <li>item iv</li>
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

    def test_roman_mitigation(self):
        """Test mitigation for conflict case with alphabetical lists."""

        self.check_markdown(
            R'''
            IIIII. Roman numeral V

            ---

            VIIIII. Roman numeral X

            ---

            XXXXX. Roman numeral L

            ---

            LXXXXX. Roman numeral C

            ---

            CCCCC. Roman numeral D

            ---

            DCCCCC. Roman numeral M

            /// fancylists | start=5 type=I
            V.  Alternate work around
            ///
            ''',
            R'''
            <ol start="5" type="I">
            <li>Roman numeral V</li>
            </ol>
            <hr />
            <ol start="10" type="I">
            <li>Roman numeral X</li>
            </ol>
            <hr />
            <ol start="50" type="I">
            <li>Roman numeral L</li>
            </ol>
            <hr />
            <ol start="100" type="I">
            <li>Roman numeral C</li>
            </ol>
            <hr />
            <ol start="500" type="I">
            <li>Roman numeral D</li>
            </ol>
            <hr />
            <ol start="1000" type="I">
            <li>Roman numeral M</li>
            </ol>
            <ol start="5" type="I">
            <li>Alternate work around</li>
            </ol>
            ''',
            True
        )

    def test_alpha_mitigation_start(self):
        """Test mitigation for conflict case with Roman numeral lists with explicit start."""

        self.check_markdown(
            R'''
            /// fancylists | start=3 type=a
            i.  Workaround
            j.  Workaround
            ///
            ''',
            R'''
            <ol start="3" type="a">
            <li>Workaround</li>
            <li>Workaround</li>
            </ol>
            ''',
            True
        )


    def test_alpha_mitigation(self):
        """Test mitigation for conflict case with Roman numeral lists with explicit start."""

        self.check_markdown(
            R'''
            /// fancylists | type=a
            i.  Workaround
            j.  Workaround
            ///

            /// fancylists | type=a
            i)  Workaround
            j)  Workaround
            ///
            ''',
            R'''
            <ol start="9" type="a">
            <li>Workaround</li>
            <li>Workaround</li>
            </ol>
            <ol start="9" type="a">
            <li>Workaround</li>
            <li>Workaround</li>
            </ol>
            ''',
            True
        )

    def test_alpha_mitigation_switch(self):
        """Test mitigation for conflict case with Roman numeral lists."""

        self.check_markdown(
            R'''
            /// fancylists | type=a
            i.  Workaround
            j)  Workaround
            ///
            ''',
            R'''
            <ol start="9" type="a">
            <li>Workaround</li>
            </ol>
            <ol start="10" type="a">
            <li>Workaround</li>
            </ol>
            ''',
            True
        )

    def test_alpha_mitigation_complex(self):
        """Test mitigation for complex conflict case with Roman numeral lists."""

        self.check_markdown(
            R'''
            /// fancylists | type=a
            i.  Workaround

                Workaround

            j.  Workaround
            ///
            ''',
            R'''
            <ol start="9" type="a">
            <li>
            <p>Workaround</p>
            <p>Workaround</p>
            </li>
            <li>
            <p>Workaround</p>
            </li>
            </ol>
            ''',
            True
        )

    def test_alpha_mitigation_ul_ignored(self):
        """Test that mitigation won't target unordered lists."""

        self.check_markdown(
            R'''
            /// fancylists | type=a
            -  Workaround

                Workaround

            -  Workaround
            ///
            ''',
            R'''
            <ul>
            <li>
            <p>Workaround</p>
            <p>Workaround</p>
            </li>
            <li>
            <p>Workaround</p>
            </li>
            </ul>
            ''',
            True
        )

    def test_alpha_mitigation_generic(self):
        """Test that mitigation works on generic."""

        self.check_markdown(
            R'''
            /// fancylists | start=9 type=a
            #.  Workaround

                Workaround

            #. Workaround
            ///
            ''',
            R'''
            <ol start="9" type="a">
            <li>
            <p>Workaround</p>
            <p>Workaround</p>
            </li>
            <li>
            <p>Workaround</p>
            </li>
            </ol>
            ''',
            True
        )

    def test_alpha_mitigation_generic_no_start(self):
        """Test that mitigation works on generic with no start."""

        self.check_markdown(
            R'''
            /// fancylists | type=a
            #.  Workaround

                Workaround

            #. Workaround
            ///
            ''',
            R'''
            <ol type="a">
            <li>
            <p>Workaround</p>
            <p>Workaround</p>
            </li>
            <li>
            <p>Workaround</p>
            </li>
            </ol>
            ''',
            True
        )

    def test_mitigation_no_force_alpha(self):
        """Test case that can't be forced."""

        self.check_markdown(
            R'''
            /// fancylists | type=a
            1. Can't force
            ///
            ''',
            R'''
            <ol type="a">
            <li>Can't force</li>
            </ol>
            ''',
            True
        )

    def test_mitigation_bad_type(self):
        """Test bad type in mitigation."""

        self.check_markdown(
            R'''
            /// fancylists | type=j

            1. Can't force
            ///
            ''',
            R'''
            <p>/// fancylists | type=j</p>
            <ol type="1">
            <li>Can't force
            ///</li>
            </ol>
            ''',
            True
        )

    def test_mitigation_no_type(self):
        """Test no type in mitigation."""

        self.check_markdown(
            R'''
            /// fancylists |

            a. Can't force
            ///
            ''',
            R'''
            <p>/// fancylists |</p>
            <ol type="a">
            <li>Can't force
            ///</li>
            </ol>
            ''',
            True
        )

    def test_mitigation_only_start(self):
        """Test no type in mitigation."""

        self.check_markdown(
            R'''
            /// fancylists | start=5

            a. item 5
            ///
            ''',
            R'''
            <ol start="5" type="1">
            <li>item 5</li>
            </ol>
            ''',
            True
        )


class TestFancyListsStyle(util.MdCase):
    """Test fancy lists."""

    extension = ['pymdownx.fancylists', 'pymdownx.saneheaders']
    extension_configs = {
        'pymdownx.fancylists': {
            'inject_style': True
        }
    }

    def test_inject_style(self):
        """Test injecting styles."""

        self.check_markdown(
            R'''
            i. Item i
            ''',
            R'''
            <ol style="list-style-type: lower-roman;" type="i">
            <li>Item i</li>
            </ol>
            ''',
            True
        )

    def test_inject_style_force(self):
        """Test injecting styles in forced lists."""

        self.check_markdown(
            R'''
            /// fancylists | type=i
            v. Item v
            ///
            ''',
            R'''
            <ol start="5" style="list-style-type: lower-roman;" type="i">
            <li>Item v</li>
            </ol>
            ''',
            True
        )


class TestFancyListsClass(util.MdCase):
    """Test fancy lists."""

    extension = ['pymdownx.fancylists', 'pymdownx.saneheaders']
    extension_configs = {
        'pymdownx.fancylists': {
            'inject_class': True
        }
    }

    def test_inject_class(self):
        """Test injecting class."""

        self.check_markdown(
            R'''
            i. Item i
            ''',
            R'''
            <ol class="fancylists-lower-roman" type="i">
            <li>Item i</li>
            </ol>
            ''',
            True
        )

    def test_inject_class_force(self):
        """Test injecting class in forced lists."""

        self.check_markdown(
            R'''
            /// fancylists | type=i
            v. Item v
            ///
            ''',
            R'''
            <ol class="fancylists-lower-roman" start="5" type="i">
            <li>Item v</li>
            </ol>
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

    def test_no_alpha_force(self):
        """Test attempting to force alphabetical when they are disabled."""

        self.check_markdown(
            R'''
            /// fancylists | type=a

            i. item 1
            j. item 2
            ///
            ''',
            R'''
            <p>/// fancylists | type=a</p>
            <ol type="i">
            <li>item 1
            j. item 2
            ///</li>
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

    def test_no_roman_force(self):
        """Test attempting to force Roman numerals when they are disabled."""

        self.check_markdown(
            R'''
            /// fancylists | type=i

            v. item 1
            vi. item 2
            ///
            ''',
            R'''
            <p>/// fancylists | type=i</p>
            <ol start="22" type="a">
            <li>item 1
            vi. item 2
            ///</li>
            </ol>
            ''',
            True
        )
