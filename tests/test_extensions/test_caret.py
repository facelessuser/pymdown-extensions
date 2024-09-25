"""Test caret."""
from .. import util


class TestCaretSmart(util.MdCase):
    """Test escaping cases for Caret with smart enabled."""

    extension = [
        'pymdownx.caret'
    ]
    extension_configs = {
        "pymdownx.caret": {
            "smart_insert": True
        }
    }

    def test_case_1(self):
        """Test case 1."""

        self.check_markdown(
            R"x^2^ + y^2^ = 4",
            "<p>x<sup>2</sup> + y<sup>2</sup> = 4</p>",
            True
        )

    def test_case_2(self):
        """Test case 2."""

        self.check_markdown(
            R"Text^superscript^",
            "<p>Text<sup>superscript</sup></p>",
            True
        )

    def test_case_3(self):
        """Test case 3."""

        self.check_markdown(
            R"Text^superscript failed^",
            "<p>Text^superscript failed^</p>",
            True
        )

    def test_case_4(self):
        """Test case 4."""

        self.check_markdown(
            R"Text^superscript\ success^",
            "<p>Text<sup>superscript success</sup></p>",
            True
        )

    def test_case_5(self):
        """Test case 5."""

        self.check_markdown(
            R"Test: ^^ Won't insert ^^",
            "<p>Test: ^^ Won't insert ^^</p>",
            True
        )

    def test_case_6(self):
        """Test case 6."""

        self.check_markdown(
            R"Test: ^^Will insert^^",
            "<p>Test: <ins>Will insert</ins></p>",
            True
        )

    def test_case_7(self):
        """Test case 7."""

        self.check_markdown(
            R"Test: \^\^Escaped\^\^",
            "<p>Test: ^^Escaped^^</p>",
            True
        )

    def test_case_8(self):
        """Test case 8."""

        self.check_markdown(
            R"Test: ^^This will all be inserted ^^because of the placement of the center carets.^^",
            "<p>Test: <ins>This will all be inserted ^^because of the placement of the center carets.</ins></p>",
            True
        )

    def test_case_9(self):
        """Test case 9."""

        self.check_markdown(
            R"Test: ^^This will all be inserted ^^ because of the placement of the center carets.^^",
            "<p>Test: <ins>This will all be inserted ^^ because of the placement of the center carets.</ins></p>",
            True
        )

    def test_case_10(self):
        """Test case 10."""

        self.check_markdown(
            R"Test: ^^This will NOT all be inserted^^ because of the placement of the center caret.^^",
            "<p>Test: <ins>This will NOT all be inserted</ins> because of the placement of the center caret.^^</p>",
            True
        )

    def test_case_11(self):
        """Test case 11."""

        self.check_markdown(
            R"Test: ^^This will all be inserted^ because of the token is less than that of the caret.^^",
            "<p>Test: <ins>This will all be inserted^ because of the token is less than that of the caret.</ins></p>",
            True
        )

    def test_complex_sup_ins_under(self):
        """Test `^text ^^text^^^`."""

        self.check_markdown(
            R"^I'm\ sup.\ ^^I'm\ sup\ and\ insert.^^^",
            "<p><sup>I'm sup. <ins>I'm sup and insert.</ins></sup></p>"
        )

    def test_complex_del_sup_inser(self):
        """Test `^^text ^text^^^`."""

        self.check_markdown(
            R"^^I'm insert. ^I'm\ sup\ and\ insert.^^^",
            "<p><ins>I'm insert. <sup>I'm sup and insert.</sup></ins></p>"
        )


class TestCaretNoSmart(util.MdCase):
    """Test escaping cases for Caret without smart enabled."""

    extension = [
        'pymdownx.caret'
    ]
    extension_configs = {
        "pymdownx.caret": {
            "smart_insert": False
        }
    }

    def test_case_1(self):
        """Test case 1."""

        self.check_markdown(
            R"x^2^ + y^2^ = 4",
            "<p>x<sup>2</sup> + y<sup>2</sup> = 4</p>",
            True
        )

    def test_case_2(self):
        """Test case 2."""

        self.check_markdown(
            R"Text^superscript^",
            "<p>Text<sup>superscript</sup></p>",
            True
        )

    def test_case_3(self):
        """Test case 3."""

        self.check_markdown(
            R"Text^superscript failed^",
            "<p>Text^superscript failed^</p>",
            True
        )

    def test_case_4(self):
        """Test case 4."""

        self.check_markdown(
            R"Text^superscript\ success^",
            "<p>Text<sup>superscript success</sup></p>",
            True
        )

    def test_case_5(self):
        """Test case 5."""

        self.check_markdown(
            R"Test: ^^ Won't insert ^^",
            "<p>Test: ^^ Won't insert ^^</p>",
            True
        )

    def test_case_6(self):
        """Test case 6."""

        self.check_markdown(
            R"Test: ^^Will insert^^",
            "<p>Test: <ins>Will insert</ins></p>",
            True
        )

    def test_case_7(self):
        """Test case 7."""

        self.check_markdown(
            R"Test: \^\^Escaped\^\^",
            "<p>Test: ^^Escaped^^</p>",
            True
        )

    def test_case_8(self):
        """Test case 8."""

        self.check_markdown(
            R"Test: ^^All will ^ be insert^^",
            "<p>Test: <ins>All will ^ be insert</ins></p>",
            True
        )

    def test_case_9(self):
        """Test case 9."""

        self.check_markdown(
            R"Test: ^^All will^\^^ be insert with superscript in middle^^",
            "<p>Test: <ins>All will<sup>^</sup> be insert with superscript in middle</ins></p>",
            True
        )

    def test_case_10(self):
        """Test case 10."""

        self.check_markdown(
            R"Test: ^^All will ^\^^ be insert with superscript in middle^^",
            "<p>Test: <ins>All will <sup>^</sup> be insert with superscript in middle</ins></p>",
            True
        )

    def test_complex_sup_ins_under(self):
        """Test `^text ^^text^^^`."""

        self.check_markdown(
            R"^I'm\ sup.\ ^^I'm\ sup\ and\ insert.^^^",
            "<p><sup>I'm sup. <ins>I'm sup and insert.</ins></sup></p>"
        )

    def test_complex_del_sup_inser(self):
        """Test `^^text ^text^^^`."""

        self.check_markdown(
            R"^^I'm insert. ^I'm\ sup\ and\ insert.^^^",
            "<p><ins>I'm insert. <sup>I'm sup and insert.</sup></ins></p>"
        )
