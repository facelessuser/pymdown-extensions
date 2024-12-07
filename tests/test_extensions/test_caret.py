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

    def test_complex_cases(self):
        """Test some complex cases."""

        self.check_markdown(
            R'''
            ^^^I'm\ insert\ and\ sup^ I am just insert.^^

            ^^^I'm\ insert\ and\ sup!^^\ I\ am\ just\ sup.^

            ^sup\ and\ ^^sup\ insert^^^ and ^sup^

            ^^insert and ^sup\ insert^^^ and ^sup^

            ^^^I'm\ sup\ and\ insert^ I am just insert.^^ ^sup^

            ^^^I'm\ insert\ and\ sup!^^\ I\ am\ just\ sup.^ ^sup^

            ^sup\ and\ ^^sup\ insert^^^ and not sup^

            ^^insert and ^sup\ insert^^^ and not sup^

            ^sup\ and\ ^^sup\ insert^^^

            ^^insert and ^sup\ insert^^^

            ^sup\ ^^sup\ insert^^\ sup^

            ^^^sup\ and\ insert^ insert^^: foo bar ^^insert^^

            ^^^sup\ and\ insert^^\ sup^ foo bar ^^insert^^

            ^sup\ and\ ^^sup\ insert^^^ ^^insert^^

            ^^insert and ^sup\ insert^^^ ^^insert^^
            ''',
            '''
            <p><ins><sup>I'm insert and sup</sup> I am just insert.</ins></p>
            <p><sup><ins>I'm insert and sup!</ins> I am just sup.</sup></p>
            <p><sup>sup and <ins>sup insert</ins></sup> and <sup>sup</sup></p>
            <p><ins>insert and <sup>sup insert</sup></ins> and <sup>sup</sup></p>
            <p><ins><sup>I'm sup and insert</sup> I am just insert.</ins> <sup>sup</sup></p>
            <p><sup><ins>I'm insert and sup!</ins> I am just sup.</sup> <sup>sup</sup></p>
            <p><sup>sup and <ins>sup insert</ins></sup> and not sup^</p>
            <p><ins>insert and <sup>sup insert</sup></ins> and not sup^</p>
            <p><sup>sup and <ins>sup insert</ins></sup></p>
            <p><ins>insert and <sup>sup insert</sup></ins></p>
            <p><sup>sup <ins>sup insert</ins> sup</sup></p>
            <p><ins><sup>sup and insert</sup> insert</ins>: foo bar <ins>insert</ins></p>
            <p><sup><ins>sup and insert</ins> sup</sup> foo bar <ins>insert</ins></p>
            <p><sup>sup and <ins>sup insert</ins></sup> <ins>insert</ins></p>
            <p><ins>insert and <sup>sup insert</sup></ins> <ins>insert</ins></p>
            ''',
            True
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

    def test_complex_cases(self):
        """Test some complex cases."""

        self.check_markdown(
            R'''
            ^^^I'm\ insert\ and\ sup^ I am just insert.^^

            ^^^I'm\ insert\ and\ sup!^^\ I\ am\ just\ sup.^

            ^sup\ and\ ^^sup\ insert^^^ and ^sup^

            ^^insert and ^sup\ insert^^^ and ^sup^

            ^^^I'm\ sup\ and\ insert^ I am just insert.^^ ^sup^

            ^^^I'm\ insert\ and\ sup!^^\ I\ am\ just\ sup.^ ^sup^

            ^sup\ and\ ^^sup\ insert^^^ and not sup^

            ^^insert and ^sup\ insert^^^ and not sup^

            ^sup\ and\ ^^sup\ insert^^^

            ^^insert and ^sup\ insert^^^

            ^sup\ ^^sup\ insert^^\ sup^

            ^^^sup\ and\ insert^ insert^^: foo bar ^^insert^^

            ^^^sup\ and\ insert^^\ sup^ foo bar ^^insert^^

            ^sup\ and\ ^^sup\ insert^^^ ^^insert^^

            ^^insert and ^sup\ insert^^^ ^^insert^^
            ''',
            '''
            <p><ins><sup>I'm insert and sup</sup> I am just insert.</ins></p>
            <p><sup><ins>I'm insert and sup!</ins> I am just sup.</sup></p>
            <p><sup>sup and <ins>sup insert</ins></sup> and <sup>sup</sup></p>
            <p><ins>insert and <sup>sup insert</sup></ins> and <sup>sup</sup></p>
            <p><ins><sup>I'm sup and insert</sup> I am just insert.</ins> <sup>sup</sup></p>
            <p><sup><ins>I'm insert and sup!</ins> I am just sup.</sup> <sup>sup</sup></p>
            <p><sup>sup and <ins>sup insert</ins></sup> and not sup^</p>
            <p><ins>insert and <sup>sup insert</sup></ins> and not sup^</p>
            <p><sup>sup and <ins>sup insert</ins></sup></p>
            <p><ins>insert and <sup>sup insert</sup></ins></p>
            <p><sup>sup <ins>sup insert</ins> sup</sup></p>
            <p><ins><sup>sup and insert</sup> insert</ins>: foo bar <ins>insert</ins></p>
            <p><sup><ins>sup and insert</ins> sup</sup> foo bar <ins>insert</ins></p>
            <p><sup>sup and <ins>sup insert</ins></sup> <ins>insert</ins></p>
            <p><ins>insert and <sup>sup insert</sup></ins> <ins>insert</ins></p>
            ''',
            True
        )
