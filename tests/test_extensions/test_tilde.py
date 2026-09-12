"""Test tilde."""
import markdown
import pytest
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
            R"Test: ~~This will NOT all be deleted ~~because of the placement of the center tilde.~~",
            "<p>Test: ~~This will NOT all be deleted <del>because of the placement of the center tilde.</del></p>",
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

    def test_case12(self):
        """Test case 12."""

        self.check_markdown(
            R"~~~a~~b~~c ~ d~~",
            "<p><del><sub>a</sub><sub>b</sub>~c ~ d</del></p>"
        )

    def test_case13(self):
        """Test case 13."""

        self.check_markdown(
            R"~~~a~a~b~c ~ d~~",
            "<p><del><sub>a</sub>a<sub>b</sub>c ~ d</del></p>"
        )

    def test_case14(self):
        """Test case 14."""

        self.check_markdown(
            R"~~~ a a~ b~~~",
            "<p>~~~ a a~ b~~~</p>"
        )

    def test_case15(self):
        """Test case 15."""

        self.check_markdown(
            R"~~~aa~ b~~~",
            "<p><del><sub>aa</sub> b</del>~</p>"
        )

    def test_case16(self):
        """Test case 16."""

        self.check_markdown(
            R"~~~aaa~~ ~b~ c~",
            "<p>~<del>aaa</del> <sub>b</sub> c~</p>"
        )

    def test_case17(self):
        """Test case 17."""

        self.check_markdown(
            R"~~~aaa~~~b~~c c~",
            "<p><sub><del>aaa</del></sub>b~~c c~</p>"
        )

    def test_case18(self):
        """Test case 18."""

        self.check_markdown(
            R"~~~aaa~~~~b~~ ~c c~",
            "<p><sub><del>aaa</del></sub><sub>b</sub>~ ~c c~</p>"
        )

    def test_case19(self):
        """Test case 19."""

        self.check_markdown(
            R"~~~a b~ c~~",
            "<p>~<del>a b~ c</del></p>"
        )

    def test_case20(self):
        """Test case 20."""

        self.check_markdown(
            "~a ~~b~~",
            '<p>~a <del>b</del></p>'
        )

    def test_case21(self):
        """Test case 21."""

        self.check_markdown(
            "~~~a ~b~~",
            '<p>~~~a <sub>b</sub>~</p>'
        )

    def test_complex_cases(self):
        """Test some complex cases."""

        self.check_markdown(
            R'''
            ~~~I'm\ delete\ and\ sub~ I am just delete.~~

            ~~~I'm\ delete\ and\ sub!~~\ I\ am\ just\ sub.~

            ~sub\ and\ ~~sub\ delete~~~ and ~sub~

            ~~delete and ~sub\ delete~~~ and ~sub~

            ~~~I'm\ sub\ and\ delete~ I am just delete.~~ ~sub~

            ~~~I'm\ delete\ and\ sub!~~\ I\ am\ just\ sub.~ ~sub~

            ~sub\ and\ ~~sub\ delete~~~ and not sub~

            ~~delete and ~sub\ delete~~~ and not sub~

            ~sub\ and\ ~~sub\ delete~~~

            ~~delete and ~sub\ delete~~~

            ~sub\ ~~sub\ delete~~\ sub~

            ~~~sub\ and\ delete~ delete~~: foo bar ~~delete~~

            ~~~sub\ and\ delete~~\ sub~ foo bar ~~delete~~

            ~sub\ and\ ~~sub\ delete~~~ ~~delete~~

            ~~delete and ~sub\ delete~~~ ~~delete~~
            ''',
            '''
            <p><del><sub>I'm delete and sub</sub> I am just delete.</del></p>
            <p><sub><del>I'm delete and sub!</del> I am just sub.</sub></p>
            <p><sub>sub and <del>sub delete</del></sub> and <sub>sub</sub></p>
            <p><del>delete and <sub>sub delete</sub></del> and <sub>sub</sub></p>
            <p><del><sub>I'm sub and delete</sub> I am just delete.</del> <sub>sub</sub></p>
            <p><sub><del>I'm delete and sub!</del> I am just sub.</sub> <sub>sub</sub></p>
            <p><sub>sub and <del>sub delete</del></sub> and not sub~</p>
            <p><del>delete and <sub>sub delete</sub></del> and not sub~</p>
            <p><sub>sub and <del>sub delete</del></sub></p>
            <p><del>delete and <sub>sub delete</sub></del></p>
            <p><sub>sub <del>sub delete</del> sub</sub></p>
            <p><del><sub>sub and delete</sub> delete</del>: foo bar <del>delete</del></p>
            <p><sub><del>sub and delete</del> sub</sub> foo bar <del>delete</del></p>
            <p><sub>sub and <del>sub delete</del></sub> <del>delete</del></p>
            <p><del>delete and <sub>sub delete</sub></del> <del>delete</del></p>
            ''',
            True
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

    def test_case12(self):
        """Test case 12."""

        self.check_markdown(
            R"~~~a~~b~~c ~ d~~",
            "<p>~<del>a</del>b<del>c ~ d</del></p>"
        )

    def test_case13(self):
        """Test case 13."""

        self.check_markdown(
            R"~~~a~a~b~c ~ d~~",
            "<p><del><sub>a</sub>a<sub>b</sub>c ~ d</del></p>"
        )

    def test_case14(self):
        """Test case 14."""

        self.check_markdown(
            R"~~~ a a~ b~~~",
            "<p>~~~ a a~ b~~~</p>"
        )

    def test_case15(self):
        """Test case 15."""

        self.check_markdown(
            R"~~~aa~ b~~~",
            "<p><del><sub>aa</sub> b</del>~</p>"
        )

    def test_case16(self):
        """Test case 16."""

        self.check_markdown(
            R"~~~aaa~~ ~b~ c~",
            "<p>~<del>aaa</del> <sub>b</sub> c~</p>"
        )

    def test_case17(self):
        """Test case 17."""

        self.check_markdown(
            R"~~~aaa~~~b~~c c~",
            "<p><sub><del>aaa</del></sub>b~~c c~</p>"
        )

    def test_case18(self):
        """Test case 18."""

        self.check_markdown(
            R"~~~aaa~~~~b~~ ~c c~",
            "<p><sub><del>aaa</del></sub><sub>b</sub>~ ~c c~</p>"
        )

    def test_case19(self):
        """Test case 19."""

        self.check_markdown(
            R"~~~a b~ c~~",
            "<p>~<del>a b~ c</del></p>"
        )

    def test_case20(self):
        """Test case 20."""

        self.check_markdown(
            "~a ~~b~~",
            '<p>~a <del>b</del></p>'
        )

    def test_case21(self):
        """Test case 21."""

        self.check_markdown(
            "~~~a ~b~~",
            '<p>~~~a <sub>b</sub>~</p>'
        )

    def test_complex_cases(self):
        """Test some complex cases."""

        self.check_markdown(
            R'''
            ~~~I'm\ delete\ and\ sub~ I am just delete.~~

            ~~~I'm\ delete\ and\ sub!~~\ I\ am\ just\ sub.~

            ~sub\ and\ ~~sub\ delete~~~ and ~sub~

            ~~delete and ~sub\ delete~~~ and ~sub~

            ~~~I'm\ sub\ and\ delete~ I am just delete.~~ ~sub~

            ~~~I'm\ delete\ and\ sub!~~\ I\ am\ just\ sub.~ ~sub~

            ~sub\ and\ ~~sub\ delete~~~ and not sub~

            ~~delete and ~sub\ delete~~~ and not sub~

            ~sub\ and\ ~~sub\ delete~~~

            ~~delete and ~sub\ delete~~~

            ~sub\ ~~sub\ delete~~\ sub~

            ~~~sub\ and\ delete~ delete~~: foo bar ~~delete~~

            ~~~sub\ and\ delete~~\ sub~ foo bar ~~delete~~

            ~sub\ and\ ~~sub\ delete~~~ ~~delete~~

            ~~delete and ~sub\ delete~~~ ~~delete~~
            ''',
            '''
            <p><del><sub>I'm delete and sub</sub> I am just delete.</del></p>
            <p><sub><del>I'm delete and sub!</del> I am just sub.</sub></p>
            <p><sub>sub and <del>sub delete</del></sub> and <sub>sub</sub></p>
            <p><del>delete and <sub>sub delete</sub></del> and <sub>sub</sub></p>
            <p><del><sub>I'm sub and delete</sub> I am just delete.</del> <sub>sub</sub></p>
            <p><sub><del>I'm delete and sub!</del> I am just sub.</sub> <sub>sub</sub></p>
            <p><sub>sub and <del>sub delete</del></sub> and not sub~</p>
            <p><del>delete and <sub>sub delete</sub></del> and not sub~</p>
            <p><sub>sub and <del>sub delete</del></sub></p>
            <p><del>delete and <sub>sub delete</sub></del></p>
            <p><sub>sub <del>sub delete</del> sub</sub></p>
            <p><del><sub>sub and delete</sub> delete</del>: foo bar <del>delete</del></p>
            <p><sub><del>sub and delete</del> sub</sub> foo bar <del>delete</del></p>
            <p><sub>sub and <del>sub delete</del></sub> <del>delete</del></p>
            <p><del>delete and <sub>sub delete</sub></del> <del>delete</del></p>
            ''',
            True
        )


class TestTildeNoSmartNoSub(util.MdCase):
    """Test cases for Tilde without smart enabled and no subscript."""

    extension = [
        'pymdownx.tilde'
    ]
    extension_configs = {
        "pymdownx.tilde": {
            "smart_delete": False,
            "subscript": False
        }
    }

    def test_complex_cases(self):
        """Test some complex cases."""

        self.check_markdown(
            R"""
            Test: ~~ Won't delete ~~

            Test: ~~Will delete~~

            Test: \~\~Escaped\~\~

            Test: ~~All will ~ be deleted~~

            Test: ~~All will~~~ not be deleted~~

            Test: ~~All will ~~~ be deleted~~
            """,
            """
            <p>Test: ~~ Won't delete ~~</p>
            <p>Test: <del>Will delete</del></p>
            <p>Test: ~~Escaped~~</p>
            <p>Test: <del>All will ~ be deleted</del></p>
            <p>Test: <del>All will</del>~ not be deleted~~</p>
            <p>Test: <del>All will ~~~ be deleted</del></p>
            """,
            True
        )


class TestTildeNoDelete(util.MdCase):
    """Test cases for Tilde without delete."""

    extension = [
        'pymdownx.tilde'
    ]
    extension_configs = {
        "pymdownx.tilde": {
            "delete": False
        }
    }

    def test_complex_cases(self):
        """Test some complex cases."""

        self.check_markdown(
            R"""
            CH~3~CH~2~OH

            Text~subscript~

            Text~subscript failed~

            Text~subscript\ success~

            Test: ~~Won't delete~~
            """,
            """
            <p>CH<sub>3</sub>CH<sub>2</sub>OH</p>
            <p>Text<sub>subscript</sub></p>
            <p>Text~subscript failed~</p>
            <p>Text<sub>subscript success</sub></p>
            <p>Test: ~<sub>Won't delete</sub>~</p>
            """,
            True
        )


class TestTildeNoSub(util.MdCase):
    """Test cases for Tilde without subscript enabled."""

    extension = [
        'pymdownx.tilde'
    ]
    extension_configs = {
        "pymdownx.tilde": {
            "subscript": False
        }
    }

    def test_complex_cases(self):
        """Test some complex cases."""

        self.check_markdown(
            R"""
            Test: ~~ Won't delete ~~

            Test: ~~Will delete~~

            Test: \~\~Escaped\~\~

            Test: ~~This will NOT all be deleted ~~because of the placement of the center tilde.~~

            Test: ~~This will all be deleted ~~ because of the placement of the center tilde.~~

            Test: ~~This will NOT all be deleted~~ because of the placement of the center tilde.~~

            Test: ~~This will all be deleted~ because of the token is less than that of the tilde.~~
            """,
            """
            <p>Test: ~~ Won't delete ~~</p>
            <p>Test: <del>Will delete</del></p>
            <p>Test: ~~Escaped~~</p>
            <p>Test: ~~This will NOT all be deleted <del>because of the placement of the center tilde.</del></p>
            <p>Test: <del>This will all be deleted ~~ because of the placement of the center tilde.</del></p>
            <p>Test: <del>This will NOT all be deleted</del> because of the placement of the center tilde.~~</p>
            <p>Test: <del>This will all be deleted~ because of the token is less than that of the tilde.</del></p>
            """,
            True
        )


class TestTildeSpaces(util.MdCase):
    """Test Tilde with spaces allowed."""

    extension = [
        'pymdownx.tilde'
    ]
    extension_configs = {
        "pymdownx.tilde": {
            "no_space": False
        }
    }

    def test_spaces(self):
        """Test allowed spaces."""

        self.check_markdown(
            R"""
            ~~~I'm sub and del~ I am just del.~~

            ~~~I'm sub and del!~~ I am just del.~

            ~del and ~~del sub~~~ and ~del~

            ~~sub and ~del sub~~~ and ~del~

            ~~~I'm del and sub~ I am just sub.~~ ~del~

            ~~~I'm sub and del!~~ I am just del.~ ~del~

            ~del and ~~del sub~~~ and not del~

            ~~sub and ~del sub~~~ and not sub~

            ~del and ~~del sub~~~

            ~~sub and ~del sub~~~

            ~del ~~del sub~~ del~

            ~~~del and sub~ sub~~: foo bar ~~del~~

            ~~~del and sub~~ del~ foo bar ~~del~~

            ~del and ~~del sub~~~ ~~del~~

            ~~sub and ~del sub~~~ ~~del~~

            ~~sub~del sub~~~
            """,
            """
            <p><del><sub>I'm sub and del</sub> I am just del.</del></p>
            <p><sub><del>I'm sub and del!</del> I am just del.</sub></p>
            <p><sub>del and <del>del sub</del></sub> and <sub>del</sub></p>
            <p><del>sub and <sub>del sub</sub></del> and <sub>del</sub></p>
            <p><del><sub>I'm del and sub</sub> I am just sub.</del> <sub>del</sub></p>
            <p><sub><del>I'm sub and del!</del> I am just del.</sub> <sub>del</sub></p>
            <p><sub>del and <del>del sub</del></sub> and not del~</p>
            <p><del>sub and <sub>del sub</sub></del> and not sub~</p>
            <p><sub>del and <del>del sub</del></sub></p>
            <p><del>sub and <sub>del sub</sub></del></p>
            <p><sub>del <del>del sub</del> del</sub></p>
            <p><del><sub>del and sub</sub> sub</del>: foo bar <del>del</del></p>
            <p><sub><del>del and sub</del> del</sub> foo bar <del>del</del></p>
            <p><sub>del and <del>del sub</del></sub> <del>del</del></p>
            <p><del>sub and <sub>del sub</sub></del> <del>del</del></p>
            <p><del>sub<sub>del sub</sub></del></p>
            """,
            True
        )


@pytest.mark.parametrize("space", [" ", "\n", "\u00a0", "\u2003"])
def test_reject_unescaped_whitespace(space):
    """Test that all white spaces are handled."""

    source = f"~a{space}b~"
    assert markdown.markdown(source, extensions=['pymdownx.tilde']) == f"<p>{source}</p>"
