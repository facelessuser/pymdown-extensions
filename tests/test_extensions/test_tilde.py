"""Test tilde."""
from .. import util


class TestTildeSmart(util.MdCase):
    """Test escaping cases for Tilde with smart enabled."""

    extension = [
        'pymdownx.tilde'
    ]
    extension_configs = {
        "pymdownx.tilde": {
            "smart_delete": True
        }
    }

    def test_case_1(self):
        """Test case 1."""

        self.check_markdown(
            R"CH~3~CH~2~OH",
            "<p>CH<sub>3</sub>CH<sub>2</sub>OH</p>",
            True
        )

    def test_case_2(self):
        """Test case 2."""

        self.check_markdown(
            R"Text~subscript~",
            "<p>Text<sub>subscript</sub></p>",
            True
        )

    def test_case_3(self):
        """Test case 3."""

        self.check_markdown(
            R"Text~subscript failed~",
            "<p>Text~subscript failed~</p>",
            True
        )

    def test_case_4(self):
        """Test case 4."""

        self.check_markdown(
            R"Text~subscript\ success~",
            "<p>Text<sub>subscript success</sub></p>",
            True
        )

    def test_case_5(self):
        """Test case 5."""

        self.check_markdown(
            R"Test: ~~ Won't delete ~~",
            "<p>Test: ~~ Won't delete ~~</p>",
            True
        )

    def test_case_6(self):
        """Test case 6."""

        self.check_markdown(
            R"Test: ~~Will delete~~",
            "<p>Test: <del>Will delete</del></p>",
            True
        )

    def test_case_7(self):
        """Test case 7."""

        self.check_markdown(
            R"Test: \~\~Escaped\~\~",
            "<p>Test: ~~Escaped~~</p>",
            True
        )

    def test_case_8(self):
        """Test case 8."""

        self.check_markdown(
            R"Test: ~~This will all be deleted ~~because of the placement of the center tilde.~~",
            "<p>Test: <del>This will all be deleted ~~because of the placement of the center tilde.</del></p>",
            True
        )

    def test_case_9(self):
        """Test case 9."""

        self.check_markdown(
            R"Test: ~~This will all be deleted ~~ because of the placement of the center tilde.~~",
            "<p>Test: <del>This will all be deleted ~~ because of the placement of the center tilde.</del></p>",
            True
        )

    def test_case_10(self):
        """Test case 10."""

        self.check_markdown(
            R"Test: ~~This will NOT all be deleted~~ because of the placement of the center tilde.~~",
            "<p>Test: <del>This will NOT all be deleted</del> because of the placement of the center tilde.~~</p>",
            True
        )

    def test_case_11(self):
        """Test case 11."""

        self.check_markdown(
            R"Test: ~~This will all be deleted~ because of the token is less than that of the tilde.~~",
            "<p>Test: <del>This will all be deleted~ because of the token is less than that of the tilde.</del></p>",
            True
        )

    def test_complex_sub_del_under(self):
        """Test `~text ~~text~~~`."""

        self.check_markdown(
            R"~I'm\ sub.\ ~~I'm\ sub\ and\ delete.~~~",
            "<p><sub>I'm sub. <del>I'm sub and delete.</del></sub></p>"
        )

    def test_complex_del_sub_under(self):
        """Test `~~text ~text~~~`."""

        self.check_markdown(
            R"~~I'm delete. ~I'm\ sub\ and\ delete.~~~",
            "<p><del>I'm delete. <sub>I'm sub and delete.</sub></del></p>"
        )


class TestTildeNoSmart(util.MdCase):
    """Test escaping cases for Tilde without smart enabled."""

    extension = [
        'pymdownx.tilde'
    ]
    extension_configs = {
        "pymdownx.tilde": {
            "smart_delete": False
        }
    }

    def test_case_1(self):
        """Test case 1."""

        self.check_markdown(
            R"CH~3~CH~2~OH",
            "<p>CH<sub>3</sub>CH<sub>2</sub>OH</p>",
            True
        )

    def test_case_2(self):
        """Test case 2."""

        self.check_markdown(
            R"Text~subscript~",
            "<p>Text<sub>subscript</sub></p>",
            True
        )

    def test_case_3(self):
        """Test case 3."""

        self.check_markdown(
            R"Text~subscript failed~",
            "<p>Text~subscript failed~</p>",
            True
        )

    def test_case_4(self):
        """Test case 4."""

        self.check_markdown(
            R"Text~subscript\ success~",
            "<p>Text<sub>subscript success</sub></p>",
            True
        )

    def test_case_5(self):
        """Test case 5."""

        self.check_markdown(
            R"Test: ~~ Won't delete ~~",
            "<p>Test: ~~ Won't delete ~~</p>",
            True
        )

    def test_case_6(self):
        """Test case 6."""

        self.check_markdown(
            R"Test: ~~Will delete~~",
            "<p>Test: <del>Will delete</del></p>",
            True
        )

    def test_case_7(self):
        """Test case 7."""

        self.check_markdown(
            R"Test: \~\~Escaped\~\~",
            "<p>Test: ~~Escaped~~</p>",
            True
        )

    def test_case_8(self):
        """Test case 8."""

        self.check_markdown(
            R"Test: ~~All will ~ be deleted~~",
            "<p>Test: <del>All will ~ be deleted</del></p>",
            True
        )

    def test_case_9(self):
        """Test case 9."""

        self.check_markdown(
            R"Test: ~~All will~\~~ be deleted with subscript in middle~~",
            "<p>Test: <del>All will<sub>~</sub> be deleted with subscript in middle</del></p>",
            True
        )

    def test_case_10(self):
        """Test case 10."""

        self.check_markdown(
            R"Test: ~~All will ~\~~ be deleted with subscript in middle~~",
            "<p>Test: <del>All will <sub>~</sub> be deleted with subscript in middle</del></p>",
            True
        )

    def test_case_11(self):
        """Test case 11."""

        self.check_markdown(
            R"Test: Subscript ~~~",
            "<p>Test: Subscript ~~~</p>",
            True
        )

    def test_complex_sub_del_under(self):
        """Test `~text ~~text~~~`."""

        self.check_markdown(
            R"~I'm\ sub.\ ~~I'm\ sub\ and\ delete.~~~",
            "<p><sub>I'm sub. <del>I'm sub and delete.</del></sub></p>"
        )

    def test_complex_del_sub_under(self):
        """Test `~~text ~text~~~`."""

        self.check_markdown(
            R"~~I'm delete. ~I'm\ sub\ and\ delete.~~~",
            "<p><del>I'm delete. <sub>I'm sub and delete.</sub></del></p>"
        )
