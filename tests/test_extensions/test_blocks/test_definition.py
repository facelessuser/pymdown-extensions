"""Test cases for Blocks (define)."""
from ... import util


class TestBlocksDefinition(util.MdCase):
    """Test Blocks admonitions cases."""

    extension = ['pymdownx.blocks.definition', 'pymdownx.blocks.html']

    def test_def(self):
        """Test definition."""

        self.check_markdown(
            R'''
            /// define
            Apple

            - Pomaceous fruit of plants of the genus Malus in
              the family Rosaceae.

            ///
            ''',
            R'''
            <dl>
            <dt>Apple</dt>
            <dd>Pomaceous fruit of plants of the genus Malus in
              the family Rosaceae.</dd>
            </dl>
            ''',  # noqa: E501
            True
        )

    def test_multi_def(self):
        """Test multiple definitions."""

        self.check_markdown(
            R'''
            /// define
            Apple

            - Pomaceous fruit of plants of the genus Malus in
              the family Rosaceae.

            Orange

            - The fruit of an evergreen tree of the genus Citrus.

            ///
            ''',
            R'''
            <dl>
            <dt>Apple</dt>
            <dd>Pomaceous fruit of plants of the genus Malus in
              the family Rosaceae.</dd>
            <dt>Orange</dt>
            <dd>The fruit of an evergreen tree of the genus Citrus.</dd>
            </dl>
            ''',  # noqa: E501
            True
        )

    def test_multi_term(self):
        """Test definitions with multiple terms."""

        self.check_markdown(
            R'''
            /// define
            Term 1

            Term 2

            - Definition a

            Term 3

            - Definition b
            ///
            ''',
            r'''
            <dl>
            <dt>Term 1</dt>
            <dt>Term 2</dt>
            <dd>Definition a</dd>
            <dt>Term 3</dt>
            <dd>Definition b</dd>
            </dl>
            ''',  # noqa: E501
            True
        )

    def test_handling_of_dt_dd(self):
        """Test that we ignore `dt` and `dd` tags."""

        self.check_markdown(
            R'''
            /// define
            //// html | dt
            term
            ////

            //// html | dd
            Some description.
            ////
            ///
            ''',
            R'''
            <dl>
            <dt>term</dt>
            <dd>Some description.</dd>
            </dl>
            ''',  # noqa: E501
            True
        )

    def test_non_paragraph_block(self):
        """Test that we sanely handle a non-paragraph term."""

        self.check_markdown(
            R'''
            /// define

            > A non non-paragraph term

            - description

            ///
            ''',
            R'''
            <dl>
            <dt>
            <blockquote>
            <p>A non non-paragraph term</p>
            </blockquote>
            </dt>
            <dd>description</dd>
            </dl>
            ''',  # noqa: E501
            True
        )
