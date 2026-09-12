"""Test caret."""
from .. import util
import markdown
import pytest


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
            R"Test: ^^This will NOT all be inserted ^^because of the placement of the center carets.^^",
            "<p>Test: ^^This will NOT all be inserted <ins>because of the placement of the center carets.</ins></p>",
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

    def test_case12(self):
        """Test case 12."""

        self.check_markdown(
            R"^^^a^^b^^c ^ d^^",
            "<p><ins><sup>a</sup><sup>b</sup>^c ^ d</ins></p>"
        )

    def test_case13(self):
        """Test case 13."""

        self.check_markdown(
            R"^^^a^a^b^c ^ d^^",
            "<p><ins><sup>a</sup>a<sup>b</sup>c ^ d</ins></p>"
        )

    def test_case14(self):
        """Test case 14."""

        self.check_markdown(
            R"^^^ a a^ b^^^",
            "<p>^^^ a a^ b^^^</p>"
        )

    def test_case15(self):
        """Test case 15."""

        self.check_markdown(
            R"^^^aa^ b^^^",
            "<p><ins><sup>aa</sup> b</ins>^</p>"
        )

    def test_case16(self):
        """Test case 16."""

        self.check_markdown(
            R"^^^aaa^^ ^b^ c^",
            "<p>^<ins>aaa</ins> <sup>b</sup> c^</p>"
        )

    def test_case17(self):
        """Test case 17."""

        self.check_markdown(
            R"^^^aaa^^^b^^c c^",
            "<p><sup><ins>aaa</ins></sup>b^^c c^</p>"
        )

    def test_case18(self):
        """Test case 18."""

        self.check_markdown(
            R"^^^aaa^^^^b^^ ^c c^",
            "<p><sup><ins>aaa</ins></sup><sup>b</sup>^ ^c c^</p>"
        )

    def test_case19(self):
        """Test case 19."""

        self.check_markdown(
            R"^^^a b^ c^^",
            "<p>^<ins>a b^ c</ins></p>"
        )

    def test_case20(self):
        """Test case 20."""

        self.check_markdown(
            "^a ^^b^^",
            '<p>^a <ins>b</ins></p>'
        )

    def test_case21(self):
        """Test case 21."""

        self.check_markdown(
            "^^^a ^b^^",
            '<p>^<ins>a ^b</ins></p>'
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

    def test_case12(self):
        """Test case 12."""

        self.check_markdown(
            R"^^^a^^b^^c ^ d^^",
            "<p>^<ins>a</ins>b<ins>c ^ d</ins></p>"
        )

    def test_case13(self):
        """Test case 13."""

        self.check_markdown(
            R"^^^a^a^b^c ^ d^^",
            "<p><ins><sup>a</sup>a<sup>b</sup>c ^ d</ins></p>"
        )

    def test_case14(self):
        """Test case 14."""

        self.check_markdown(
            R"^^^ a a^ b^^^",
            "<p>^^^ a a^ b^^^</p>"
        )

    def test_case15(self):
        """Test case 15."""

        self.check_markdown(
            R"^^^aa^ b^^^",
            "<p><ins><sup>aa</sup> b</ins>^</p>"
        )

    def test_case16(self):
        """Test case 16."""

        self.check_markdown(
            R"^^^aaa^^ ^b^ c^",
            "<p>^<ins>aaa</ins> <sup>b</sup> c^</p>"
        )

    def test_case17(self):
        """Test case 17."""

        self.check_markdown(
            R"^^^aaa^^^b^^c c^",
            "<p><sup><ins>aaa</ins></sup>b^^c c^</p>"
        )

    def test_case18(self):
        """Test case 18."""

        self.check_markdown(
            R"^^^aaa^^^^b^^ ^c c^",
            "<p><sup><ins>aaa</ins></sup><sup>b</sup>^ ^c c^</p>"
        )

    def test_case19(self):
        """Test case 19."""

        self.check_markdown(
            R"^^^a b^ c^^",
            "<p>^<ins>a b^ c</ins></p>"
        )

    def test_case20(self):
        """Test case 20."""

        self.check_markdown(
            "^a ^^b^^",
            '<p>^a <ins>b</ins></p>'
        )

    def test_case21(self):
        """Test case 21."""

        self.check_markdown(
            "^^^a ^b^^",
            '<p>^<ins>a ^b</ins></p>'
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


class TestCaretNoSmartNoSup(util.MdCase):
    """Test cases for Caret without smart enabled and no superscript."""

    extension = [
        'pymdownx.caret'
    ]
    extension_configs = {
        "pymdownx.caret": {
            "smart_insert": False,
            "superscript": False
        }
    }

    def test_complex_cases(self):
        """Test some complex cases."""

        self.check_markdown(
            R"""
            Test: ^^ Won't insert ^^

            Test: ^^Will insert^^

            Test: \^\^Escaped\^\^

            Test: ^^All will ^ be insert^^

            Test: ^^All will^^^ not be insert^^

            Test: ^^All will ^^^ be insert^^
            """,
            """
            <p>Test: ^^ Won't insert ^^</p>
            <p>Test: <ins>Will insert</ins></p>
            <p>Test: ^^Escaped^^</p>
            <p>Test: <ins>All will ^ be insert</ins></p>
            <p>Test: <ins>All will</ins>^ not be insert^^</p>
            <p>Test: <ins>All will ^^^ be insert</ins></p>
            """,
            True
        )


class TestCaretNoInsert(util.MdCase):
    """Test cases for Caret without insert."""

    extension = [
        'pymdownx.caret'
    ]
    extension_configs = {
        "pymdownx.caret": {
            "insert": False
        }
    }

    def test_complex_cases(self):
        """Test some complex cases."""

        self.check_markdown(
            R"""
            x^2^ + y^2^ = 4

            Text^superscript^

            Text^superscript failed^

            Text^superscript\ success^

            Test: ^^Won't insert^^
            """,
            """
            <p>x<sup>2</sup> + y<sup>2</sup> = 4</p>
            <p>Text<sup>superscript</sup></p>
            <p>Text^superscript failed^</p>
            <p>Text<sup>superscript success</sup></p>
            <p>Test: ^<sup>Won't insert</sup>^</p>
            """,
            True
        )


class TestCaretNoSup(util.MdCase):
    """Test cases for Caret without superscript."""

    extension = [
        'pymdownx.caret'
    ]
    extension_configs = {
        "pymdownx.caret": {
            "superscript": False
        }
    }

    def test_complex_cases(self):
        """Test some complex cases."""

        self.check_markdown(
            R"""
            Test: ^^ Won't insert ^^

            Test: ^^Will insert^^

            Test: \^\^Escaped\^\^

            Test: ^^This will NOT all be inserted ^^because of the placement of the center carets.^^

            Test: ^^This will all be inserted ^^ because of the placement of the center carets.^^

            Test: ^^This will NOT all be inserted^^ because of the placement of the center caret.^^

            Test: ^^This will all be inserted^ because of the token is less than that of the caret.^^
            """,
            """
            <p>Test: ^^ Won't insert ^^</p>
            <p>Test: <ins>Will insert</ins></p>
            <p>Test: ^^Escaped^^</p>
            <p>Test: ^^This will NOT all be inserted <ins>because of the placement of the center carets.</ins></p>
            <p>Test: <ins>This will all be inserted ^^ because of the placement of the center carets.</ins></p>
            <p>Test: <ins>This will NOT all be inserted</ins> because of the placement of the center caret.^^</p>
            <p>Test: <ins>This will all be inserted^ because of the token is less than that of the caret.</ins></p>
            """,
            True
        )


class TestCaretSpaces(util.MdCase):
    """Test Caret with spaces allowed."""

    extension = [
        'pymdownx.caret'
    ]
    extension_configs = {
        "pymdownx.caret": {
            "no_space": False
        }
    }

    def test_spaces(self):
        """Test allowed spaces."""

        self.check_markdown(
            R"""
            ^^^I'm sup and ins^ I am just ins.^^

            ^^^I'm sup and ins!^^ I am just ins.^

            ^ins and ^^ins sup^^^ and ^ins^

            ^^sup and ^ins sup^^^ and ^ins^

            ^^^I'm ins and sup^ I am just sup.^^ ^ins^

            ^^^I'm sup and ins!^^ I am just ins.^ ^ins^

            ^ins and ^^ins sup^^^ and not ins^

            ^^sup and ^ins sup^^^ and not sup^

            ^ins and ^^ins sup^^^

            ^^sup and ^ins sup^^^

            ^ins ^^ins sup^^ ins^

            ^^^ins and sup^ sup^^: foo bar ^^ins^^

            ^^^ins and sup^^ ins^ foo bar ^^ins^^

            ^ins and ^^ins sup^^^ ^^ins^^

            ^^sup and ^ins sup^^^ ^^ins^^

            ^^sup^ins sup^^^
            """,
            """
            <p><ins><sup>I'm sup and ins</sup> I am just ins.</ins></p>
            <p><sup><ins>I'm sup and ins!</ins> I am just ins.</sup></p>
            <p><sup>ins and <ins>ins sup</ins></sup> and <sup>ins</sup></p>
            <p><ins>sup and <sup>ins sup</sup></ins> and <sup>ins</sup></p>
            <p><ins><sup>I'm ins and sup</sup> I am just sup.</ins> <sup>ins</sup></p>
            <p><sup><ins>I'm sup and ins!</ins> I am just ins.</sup> <sup>ins</sup></p>
            <p><sup>ins and <ins>ins sup</ins></sup> and not ins^</p>
            <p><ins>sup and <sup>ins sup</sup></ins> and not sup^</p>
            <p><sup>ins and <ins>ins sup</ins></sup></p>
            <p><ins>sup and <sup>ins sup</sup></ins></p>
            <p><sup>ins <ins>ins sup</ins> ins</sup></p>
            <p><ins><sup>ins and sup</sup> sup</ins>: foo bar <ins>ins</ins></p>
            <p><sup><ins>ins and sup</ins> ins</sup> foo bar <ins>ins</ins></p>
            <p><sup>ins and <ins>ins sup</ins></sup> <ins>ins</ins></p>
            <p><ins>sup and <sup>ins sup</sup></ins> <ins>ins</ins></p>
            <p><ins>sup<sup>ins sup</sup></ins></p>
            """,
            True
        )


@pytest.mark.parametrize("space", [" ", "\n", "\u00a0", "\u2003"])
def test_reject_unescaped_whitespace(space):
    """Test that all white spaces are handled."""

    source = f"^a{space}b^"
    assert markdown.markdown(source, extensions=['pymdownx.tilde']) == f"<p>{source}</p>"
