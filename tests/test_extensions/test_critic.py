"""Test critic."""
from .. import util
from pymdownx import critic

class TestCriticViewMode(util.MdCase):
    """Test view mode."""

    extension = [
        'pymdownx.critic'
    ]
    extension_configs = {
        "pymdownx.critic": {
            "mode": 'view'
        }
    }

    def test_view(self):
        """Test view mode."""

        self.check_markdown(
            R"""
            Here is some {--*incorrect*--} Markdown.  I am adding this{++ here.++}.  Here is some more {--text
            that I am removing--}text.  And here is even more {++text that I
            am ++}adding.{~~

            ~>  ~~}Paragraph was deleted and replaced with some spaces.{~~  ~>

            ~~}Spaces were removed and a paragraph was added.

            And here is a comment on {==some
             ==text== ==}{>>This works quite well. I just wanted to comment on it.<<}. Substitutions {~~is~>are~~} great!

            General block handling.

            {--

            * test
            * test
            * test
                * test
            * test

            --}

            {++

            * test
                * test
            * test
            * test
            * test

            ++}
            """,  # noqa: E501
            """
            <p>Here is some <del class="critic"><em>incorrect</em></del> Markdown.  I am adding this<ins class="critic"> here.</ins>.  Here is some more <del class="critic">text
            that I am removing</del>text.  And here is even more <ins class="critic">text that I
            am </ins>adding.<del class="critic break">&nbsp;</del><ins class="critic">  </ins>Paragraph was deleted and replaced with some spaces.<del class="critic">  </del></p>
            <ins class="critic break">&nbsp;</ins>
            <p>Spaces were removed and a paragraph was added.</p>
            <p>And here is a comment on <mark class="critic">some
             ==text== </mark><span class="critic comment">This works quite well. I just wanted to comment on it.</span>. Substitutions <del class="critic">is</del><ins class="critic">are</ins> great!</p>
            <p>General block handling.</p>
            <del class="critic block">
            <ul>
            <li>test</li>
            <li>test</li>
            <li>test<ul>
            <li>test</li>
            </ul>
            </li>
            <li>test</li>
            </ul>
            </del>
            <ins class="critic block">
            <ul>
            <li>test<ul>
            <li>test</li>
            </ul>
            </li>
            <li>test</li>
            <li>test</li>
            <li>test</li>
            </ul>
            </ins>
            """,  # noqa: E501
            True
        )


class TestCriticAcceptMode(util.MdCase):
    """Test accept mode."""

    extension = [
        'pymdownx.critic'
    ]
    extension_configs = {
        "pymdownx.critic": {
            "mode": 'accept'
        }
    }

    def test_accept(self):
        """Test accept mode."""

        self.check_markdown(
            R"""
            Here is some {--*incorrect*--} Markdown.  I am adding this{++ here.++}.  Here is some more {--text
            that I am removing--}text.  And here is even more {++text that I
            am ++}adding.{~~

            ~>  ~~}Paragraph was deleted and replaced with some spaces.{~~  ~>

            ~~}Spaces were removed and a paragraph was added.

            And here is a comment on {==some
             ==text== ==}{>>This works quite well. I just wanted to comment on it.<<}. Substitutions {~~is~>are~~} great!

            General block handling.

            {--

            * test
            * test
            * test
                * test
            * test

            --}

            {++

            * test
                * test
            * test
            * test
            * test

            ++}
            """,  # noqa: E501
            """
            <p>Here is some  Markdown.  I am adding this here..  Here is some more text.  And here is even more text that I
            am adding.  Paragraph was deleted and replaced with some spaces.</p>
            <p>Spaces were removed and a paragraph was added.</p>
            <p>And here is a comment on some
             ==text== . Substitutions are great!</p>
            <p>General block handling.</p>
            <ul>
            <li>test<ul>
            <li>test</li>
            </ul>
            </li>
            <li>test</li>
            <li>test</li>
            <li>test</li>
            </ul>
            """,  # noqa: E501
            True
        )


class TestCriticRejectMode(util.MdCase):
    """Test reject mode."""

    extension = [
        'pymdownx.critic'
    ]
    extension_configs = {
        "pymdownx.critic": {
            "mode": 'reject'
        }
    }

    def test_reject(self):
        """Test reject mode."""

        self.check_markdown(
            R"""
            Here is some {--*incorrect*--} Markdown.  I am adding this{++ here.++}.  Here is some more {--text
            that I am removing--}text.  And here is even more {++text that I
            am ++}adding.{~~

            ~>  ~~}Paragraph was deleted and replaced with some spaces.{~~  ~>

            ~~}Spaces were removed and a paragraph was added.

            And here is a comment on {==some
             ==text== ==}{>>This works quite well. I just wanted to comment on it.<<}. Substitutions {~~is~>are~~} great!

            General block handling.

            {--

            * test
            * test
            * test
                * test
            * test

            --}

            {++

            * test
                * test
            * test
            * test
            * test

            ++}
            """,  # noqa: E501
            """
            <p>Here is some <em>incorrect</em> Markdown.  I am adding this.  Here is some more text
            that I am removingtext.  And here is even more adding.</p>
            <p>Paragraph was deleted and replaced with some spaces.  Spaces were removed and a paragraph was added.</p>
            <p>And here is a comment on some
             ==text== . Substitutions is great!</p>
            <p>General block handling.</p>
            <ul>
            <li>test</li>
            <li>test</li>
            <li>test<ul>
            <li>test</li>
            </ul>
            </li>
            <li>test</li>
            </ul>
            """,
            True
        )


class TestCriticEscapeAll(util.MdCase):
    """Test critic with escaping."""

    extension = [
        'pymdownx.critic',
        'pymdownx.escapeall'
    ]
    extension_configs = {
        "pymdownx.critic": {
            "mode": 'view'
        }
    }

    def test_escape(self):
        """Test with escapes."""

        self.check_markdown(
            R"""
            We shouldn't escape STX and ETX characters:

            Don't escape crtiic placeholder: \{>>comment<<}
            """,
            """
            <p>We shouldn't escape STX and ETX characters:</p>
            <p>Don't escape crtiic placeholder: <span class="critic comment">comment</span></p>
            """,
            True
        )


class TestCriticScanner(util.MdCase):
    """Test the critic scanner."""

    extension = [
        'pymdownx.critic'
    ]
    extension_configs = {
        "pymdownx.critic": {
            "mode": 'view'
        }
    }

    def scan(self, text):
        """Scan text and return the found marks."""

        return [(text[s:e], k, c, sc) for s, e, k, c, sc in critic.find_critics(text)]

    def test_marks(self):
        """Test that each mark type is found."""

        self.assertEqual(
            self.scan('a {++ins++} b {--del--} c {==mark==} d {>>com<<} e {~~old~>new~~} f'),
            [
                ('{++ins++}', critic.INS, 'ins', None),
                ('{--del--}', critic.DEL, 'del', None),
                ('{==mark==}', critic.MARK, 'mark', None),
                ('{>>com<<}', critic.COMMENT, 'com', None),
                ('{~~old~>new~~}', critic.SUB, 'old', 'new')
            ]
        )

    def test_edge_cases(self):
        """Test closers that overlap openers and other boundary cases."""

        # The closer can't share characters with the opener
        self.assertEqual(self.scan('{++}'), [])
        self.assertEqual(self.scan('{+++}'), [])
        self.assertEqual(self.scan('{++++}'), [('{++++}', critic.INS, '', None)])
        self.assertEqual(self.scan('{~~~>~~}'), [('{~~~>~~}', critic.SUB, '', '')])
        self.assertEqual(self.scan('{~~~~}'), [])
        self.assertEqual(self.scan('{~~a~>b}'), [])
        # Marks span lines and are not nested
        self.assertEqual(self.scan('{++a\n{--b--}\nc++}'), [('{++a\n{--b--}\nc++}', critic.INS, 'a\n{--b--}\nc', None)])
        # Braces that don't start a mark are skipped, including those directly before a real opener or at the end
        self.assertEqual(self.scan('{ {+a+} {x {{++a++} {'), [('{++a++}', critic.INS, 'a', None)])
        self.assertEqual(self.scan('{{{--a--}'), [('{--a--}', critic.DEL, 'a', None)])
        self.assertEqual(self.scan('{'), [])
        self.assertEqual(self.scan('{+'), [])
        # An unclosed mark does not prevent later marks of other kinds, or of the same kind, from being found
        self.assertEqual(
            self.scan('{++ {--a--} {==b==}'),
            [('{--a--}', critic.DEL, 'a', None), ('{==b==}', critic.MARK, 'b', None)]
        )
        self.assertEqual(self.scan('{~~a {++b++}'), [('{++b++}', critic.INS, 'b', None)])

    def test_unclosed_output(self):
        """Test that unclosed marks are left untouched."""

        self.check_markdown(
            "{++ a {-- b {== c {>> d {~~ e ~> f",
            "<p>{++ a {-- b {== c {&gt;&gt; d {~~ e ~&gt; f</p>"
        )

    def test_unclosed_large(self):
        """
        Test large inputs with unclosed marks.

        Previously, these would take quadratic (or in the case of substitutions, cubic) time and
        inputs of this size would effectively never finish. We only check the results, not the time.
        """

        n = 100000
        payloads = [
            '{++' * n,
            '{--' * n,
            '{==' * n,
            '{>>' * n,
            '{~~' * n,
            '{~~' + '~>' * n,
            '{~~a~>b' * n,
            '++}' + '{++' * n,
            ''.join(m * n for m in ('{++', '{--', '{==', '{>>', '{~~a~>b'))
        ]

        for payload in payloads:
            self.assertEqual(list(critic.find_critics(payload)), [])

        # A large number of valid marks is also fine
        self.assertEqual(len(list(critic.find_critics('{~~a~>b~~} {++a++} ' * n))), n * 2)
