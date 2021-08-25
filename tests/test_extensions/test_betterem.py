"""Test cases for BetterEm."""
from .. import util


class TestBetterEmNoSmart(util.MdCase):
    """Test escaping cases for BetterEm without smart enabled."""

    extension = [
        'pymdownx.betterem'
    ]
    extension_configs = {
        "pymdownx.betterem": {
            "smart_enable": "none"
        }
    }

    def test_complex_multple_emphasis_type(self):
        """Test complex case where `**text*text***` may be detected on accident."""

        self.check_markdown(
            'traced ***along*** bla **blocked** if other ***or***',
            '<p>traced <strong><em>along</em></strong> bla <strong>blocked</strong> if other <strong><em>or</em></strong></p>'  # noqa: E501
        )

    def test_complex_multple_emphasis_type_variant2(self):
        """Test another complex case where `**text*text***` may be detected on accident."""

        self.check_markdown(
            'on the **1-4 row** of the AP Combat Table ***and*** receive',
            '<p>on the <strong>1-4 row</strong> of the AP Combat Table <strong><em>and</em></strong> receive</p>'
        )

    def test_complex_multple_underscore_type(self):
        """Test complex case where `__text_text___` may be detected on accident."""

        self.check_markdown(
            'traced ___along___ bla __blocked__ if other ___or___',
            '<p>traced <strong><em>along</em></strong> bla <strong>blocked</strong> if other <strong><em>or</em></strong></p>'  # noqa: E501
        )

    def test_complex_multple_underscore_type_variant2(self):
        """Test another complex case where `__text_text___` may be detected on accident."""

        self.check_markdown(
            'on the __1-4 row__ of the AP Combat Table ___and___ receive',
            '<p>on the <strong>1-4 row</strong> of the AP Combat Table <strong><em>and</em></strong> receive</p>'
        )


class TestBetterSmartAll(util.MdCase):
    """Test escaping cases for BetterEm with smart enabled everywhere."""

    def test_smart_complex_cases_star(self):
        """Test some complex cases with star."""

        self.check_markdown(
            '''
            ***I'm italic and bold* I am just bold.**

            ***I'm bold and italic!** I am just italic.*
            ''',
            '''
            <p><strong><em>I'm italic and bold</em> I am just bold.</strong></p>
            <p><em><strong>I'm bold and italic!</strong> I am just italic.</em></p>
            ''',
            True
        )

    def test_smart_complex_cases_underscore(self):
        """Test some complex cases with underscore."""

        self.check_markdown(
            '''
            ___I'm italic and bold_ I am just bold.__

            ___I'm bold and italic!__ I am just italic._
            ''',
            '''
            <p><strong><em>I'm italic and bold</em> I am just bold.</strong></p>
            <p><em><strong>I'm bold and italic!</strong> I am just italic.</em></p>
            ''',
            True
        )
