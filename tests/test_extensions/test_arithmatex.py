"""Test cases for Arithmatex."""
from .. import util


class TestArithmatexLimit(util.MdCase):
    """Test limiting Arithmatex inline and block inputs."""

    extension = [
        'pymdownx.arithmatex'
    ]
    extension_configs = {'pymdownx.arithmatex': {'inline_syntax': ['round'], 'block_syntax': ['square']}}

    def test_round_only(self):
        """Test round only."""

        self.check_markdown(
            "\\(1 + 2 + 3\\)",
            """<p><span class="arithmatex"><span class="MathJax_Preview">1 + 2 + 3</span><script type="math/tex">1 + 2 + 3</script></span></p>"""  # noqa: E501
        )

    def test_square_only(self):
        """Test square only."""

        self.check_markdown(
            r"""
            \[
            1 + 2 + 3
            \]
            """,
            r"""
            <div class="arithmatex">
            <div class="MathJax_Preview">
            1 + 2 + 3
            </div>
            <script type="math/tex; mode=display">
            1 + 2 + 3
            </script>
            </div>
            """,
            True
        )


class TestArithmatexBlockEscapes(util.MdCase):
    """Test escaping cases for Arithmatex blocks."""

    extension = [
        'pymdownx.arithmatex'
    ]
    extension_configs = {}

    def test_escaped_dollar_block(self):
        """Test escaping a dollar."""

        self.check_markdown(
            r'''
            $$3+2\$$
            ''',
            r'''
            <p>$<span class="arithmatex"><span class="MathJax_Preview">3+2\$</span><script type="math/tex">3+2\$</script></span></p>
            ''',  # noqa: E501
            True
        )

    def test_escaped_dollar_dollar_block(self):
        """Test escaping both dollars."""

        self.check_markdown(
            r'''
            $$3+2\$\$
            ''',
            r'''
            <p>$$3+2$$</p>
            ''',
            True
        )

    def test_double_escaped_dollar_block(self):
        """Test double escaping a dollar."""

        self.check_markdown(
            r'''
            $$3+2\\$$
            ''',
            r'''
            <div class="arithmatex">
            <div class="MathJax_Preview">3+2\\</div>
            <script type="math/tex; mode=display">3+2\\</script>
            </div>
            ''',
            True
        )

    def test_escaped_end_block(self):
        """Test escaping an end."""

        self.check_markdown(
            r'''
            \begin{align}3+2\\end{align}
            ''',
            r'''
            <p>\begin{align}3+2\end{align}</p>
            ''',
            True
        )

    def test_double_escaped_end_block(self):
        """Test double escaping an end."""

        self.check_markdown(
            r'''
            \begin{align}3+2\\\end{align}
            ''',
            r'''
            <div class="arithmatex">
            <div class="MathJax_Preview">\begin{align}3+2\\\end{align}</div>
            <script type="math/tex; mode=display">\begin{align}3+2\\\end{align}</script>
            </div>
            ''',
            True
        )

    def test_escaped_bracket_block(self):
        """Test escaping a bracket."""

        self.check_markdown(
            r'''
            \[3+2\\]
            ''',
            r'''
            <p>[3+2\]</p>
            ''',
            True
        )

    def test_double_escaped_bracket_block(self):
        """Test double escaping a bracket."""

        self.check_markdown(
            r'''
            \[3+2\\\]
            ''',
            r'''
            <div class="arithmatex">
            <div class="MathJax_Preview">3+2\\</div>
            <script type="math/tex; mode=display">3+2\\</script>
            </div>
            ''',
            True
        )


class TestArithmatexHang(util.MdCase):
    """Test hang cases."""

    def test_hang_dollar(self):
        """
        We are just making sure this works.

        Previously this pattern would hang. It isn't supposed to match due to the space before the last dollar,
        but it definitely shouldn't hang the process.
        """

        self.check_markdown(
            r'''
            $z^{[1]} = \begin{bmatrix}w^{[1]T}_1 \\ w^{[1]T}_2 \\ w^{[1]T}_3 \\ w^{[1]T}_4 \end{bmatrix} \begin{bmatrix}x_1 \\ x_2 \\ x_3 \end{bmatrix} + \begin{bmatrix}b^{[1]}_1 \\ b^{[1]}_2 \\ b^{[1]}_3 \\ b^{[1]}_4 \end{bmatrix}= \begin{bmatrix}w^{[1]T}_1 x + b^{[1]}_1 \\ w^{[1]T}_2 x + b^{[1]}_2\\ w^{[1]T}_3 x + b^{[1]}_3 \\ w^{[1]T}_4 x + b^{[1]}_4 \end{bmatrix} $
            ''',  # noqa: E501
            r'''
            <p>$z^{[1]} = \begin{bmatrix}w^{[1]T}_1 \ w^{[1]T}_2 \ w^{[1]T}_3 \ w^{[1]T}_4 \end{bmatrix} \begin{bmatrix}x_1 \ x_2 \ x_3 \end{bmatrix} + \begin{bmatrix}b^{[1]}_1 \ b^{[1]}_2 \ b^{[1]}_3 \ b^{[1]}_4 \end{bmatrix}= \begin{bmatrix}w^{[1]T}_1 x + b^{[1]}_1 \ w^{[1]T}_2 x + b^{[1]}_2\ w^{[1]T}_3 x + b^{[1]}_3 \ w^{[1]T}_4 x + b^{[1]}_4 \end{bmatrix} $</p>
            ''',  # noqa: E501
            True
        )
