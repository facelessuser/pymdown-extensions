"""Test cases for BracketSpan."""
from .. import util


class TestBracketSpan(util.MdCase):
    """Test BracketSpan."""

    extension = ['pymdownx.bracketspan', 'attr_list']
    extension_configs = {}

    def test_bracketspan(self):
        """Test bracket span."""

        self.check_markdown(
            """
            [test]{.class}

            [test [nesting]{#id} spans]{.class}

            [test [more]{#id} [nesting]{.class} cases and no attribute]{}

            [test [deep [nested]{.multiple .class} [spans]{#id .class}]{.more} and [make]{} sure they]{} work

            []{}

            [test [another]{#id}com[pli[cated_test_case[with]{.class} a lot of [nesting]{attr="value"}

            [will not match]

            [will not match

            [example]{.no-span}

            [example]: https://example.com
            """,
            """
            <p><span class="class">test</span></p>
            <p><span class="class">test <span id="id">nesting</span> spans</span></p>
            <p><span>test <span id="id">more</span> <span class="class">nesting</span> cases and no attribute</span></p>
            <p><span>test <span class="more">deep <span class="multiple class">nested</span> <span class="class" id="id">spans</span></span> and <span>make</span> sure they</span> work</p>
            <p><span></span></p>
            <p>[test <span id="id">another</span>com[pli[cated_test_case<span class="class">with</span> a lot of <span attr="value">nesting</span></p>
            <p>[will not match]</p>
            <p>[will not match</p>
            <p><a class="no-span" href="https://example.com">example</a></p>
            """,  # noqa: E501
            True
        )


class TestBracketSpanNoAttrList(util.MdCase):
    """Test BracketSpan with no `attr_list`."""

    extension = ['pymdownx.bracketspan']
    extension_configs = {}

    def test_bracketspan_no_attr_list(self):
        """Test no attribute list."""

        self.check_markdown(
            """
            [test]{.class}
            """,
            """
            <p>[test]{.class}</p>
            """,
            True
        )
