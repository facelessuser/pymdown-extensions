"""Test cases for BetterEm."""
from .. import util


class TestBetterNoSmart(util.MdCase):
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

    def test_nested(self):
        """Test nested."""

        self.check_markdown(
            '**test *text text**',
            '<p>*<em>test <em>text text</em></em></p>'
        )

    def test_heavily_nested(self):
        """Test heavily nested."""

        self.check_markdown(
            '***test **test *text text** test* test***',
            '<p><strong><em>test <em><em>test <em>text text</em></em> test</em> test</em></strong></p>'
        )

    def test_absurdly_nested(self):
        """Test absurdly nested."""

        self.check_markdown(
            '*test **test **test **test **test **test*',
            '<p>*test **test **test **test **test *<em>test</em></p>'
        )

    def test_tripple_nested(self):
        """Test triple nested."""

        self.check_markdown(
            '***test **test *test test* test** test***',
            '<p><strong><em>test <strong>test <em>test test</em> test</strong> test</em></strong></p>'
        )

    def test_nested_case_with_complex_element_wrapping(self):
        """Test element building when elements are wrapped in complex ways."""

        self.check_markdown(
            "***test **test *test test* test** test *test* test***",
            "<p><strong><em>test <strong>test <em>test test</em> test</strong> test <em>test</em> test</em></strong></p>"  # noqa: E501
        )

    def test_deep_nested_triple_case(self):
        """Test deep nested triple case."""

        self.check_markdown(
            "***a ***b c** d* e***",
            "<p><strong><em>a <em><strong>b c</strong> d</em> e</em></strong></p>"
        )

    def test_nested_underscore(self):
        """Test nested."""

        self.check_markdown(
            '__test _text text__',
            '<p>_<em>test <em>text text</em></em></p>'
        )

    def test_heavily_nested_underscore(self):
        """Test heavily nested."""

        self.check_markdown(
            '___test __test _text text__ test_ test___',
            '<p><strong><em>test <em><em>test <em>text text</em></em> test</em> test</em></strong></p>'
        )

    def test_absurdly_nested_underscore(self):
        """Test absurdly nested."""

        self.check_markdown(
            '_test __test __test __test __test __test_',
            '<p>_test __test __test __test __test _<em>test</em></p>'
        )

    def test_tripple_nested_underscore(self):
        """Test triple nested."""

        self.check_markdown(
            '___test __test _test test_ test__ test___',
            '<p><strong><em>test <strong>test <em>test test</em> test</strong> test</em></strong></p>'
        )

    def test_nested_case_with_complex_element_wrapping_underscore(self):
        """Test element building when elements are wrapped in complex ways."""

        self.check_markdown(
            "___test __test _test test_ test__ test _test_ test___",
            "<p><strong><em>test <strong>test <em>test test</em> test</strong> test <em>test</em> test</em></strong></p>"  # noqa: E501
        )

    def test_deep_nested_triple_case_underscore(self):
        """Test deep nested triple case."""

        self.check_markdown(
            "___a ___b c__ d_ e___",
            "<p><strong><em>a <em><strong>b c</strong> d</em> e</em></strong></p>"
        )

    def test_complex_cases_star(self):
        """Test some complex cases for asterisks."""

        self.check_markdown(
            '''
            ***I'm italic and bold* I am just bold.**

            ***I'm bold and italic!** I am just italic.*

            *italic and **italic bold*** and *italic*

            **bold and *italic bold*** and *italic*

            ***I'm italic and bold* I am just bold.** *italic*

            ***I'm bold and italic!** I am just italic.* *italic*

            *italic and **italic bold*** and italic*

            **bold and *italic bold*** and bold*

            *italic and **italic bold***

            **bold and *italic bold***

            *italic **italic bold** italic*

            ***italic and bold* bold**: foo bar **italic**

            ***italic and bold** italic* foo bar **italic**

            *italic and **italic bold*** **italic**

            **bold and *italic bold*** **italic**

            **bold*italic bold***
            ''',
            '''
            <p><strong><em>I'm italic and bold</em> I am just bold.</strong></p>
            <p><em><strong>I'm bold and italic!</strong> I am just italic.</em></p>
            <p><em>italic and <strong>italic bold</strong></em> and <em>italic</em></p>
            <p><strong>bold and <em>italic bold</em></strong> and <em>italic</em></p>
            <p><strong><em>I'm italic and bold</em> I am just bold.</strong> <em>italic</em></p>
            <p><em><strong>I'm bold and italic!</strong> I am just italic.</em> <em>italic</em></p>
            <p><em>italic and <strong>italic bold</strong></em> and italic*</p>
            <p><strong>bold and <em>italic bold</em></strong> and bold*</p>
            <p><em>italic and <strong>italic bold</strong></em></p>
            <p><strong>bold and <em>italic bold</em></strong></p>
            <p><em>italic <strong>italic bold</strong> italic</em></p>
            <p><strong><em>italic and bold</em> bold</strong>: foo bar <strong>italic</strong></p>
            <p><em><strong>italic and bold</strong> italic</em> foo bar <strong>italic</strong></p>
            <p><em>italic and <strong>italic bold</strong></em> <strong>italic</strong></p>
            <p><strong>bold and <em>italic bold</em></strong> <strong>italic</strong></p>
            <p><strong>bold<em>italic bold</em></strong></p>
            ''',
            True
        )

    def test_complex_cases_underscore(self):
        """Test some complex cases for underscore."""

        self.check_markdown(
            '''
            ___I'm italic and bold_ I am just bold.__

            ___I'm bold and italic!__ I am just italic._

            _italic and __italic bold___ and _italic_

            __bold and _italic bold___ and _italic_

            ___I'm italic and bold_ I am just bold.__ _italic_

            ___I'm bold and italic!__ I am just italic._ _italic_

            _italic and __italic bold___ and italic_

            __bold and _italic bold___ and bold_

            _italic and __italic bold___

            __bold and _italic bold___

            _italic __italic bold__ italic_

            ___italic and bold_ bold__: foo bar __italic__

            ___italic and bold__ italic_ foo bar __italic__

            _italic and __italic bold___ __italic__

            __bold and _italic bold___ __italic__

            __bold_italic bold___
            ''',
            '''
            <p><strong><em>I'm italic and bold</em> I am just bold.</strong></p>
            <p><em><strong>I'm bold and italic!</strong> I am just italic.</em></p>
            <p><em>italic and <strong>italic bold</strong></em> and <em>italic</em></p>
            <p><strong>bold and <em>italic bold</em></strong> and <em>italic</em></p>
            <p><strong><em>I'm italic and bold</em> I am just bold.</strong> <em>italic</em></p>
            <p><em><strong>I'm bold and italic!</strong> I am just italic.</em> <em>italic</em></p>
            <p><em>italic and <strong>italic bold</strong></em> and italic_</p>
            <p><strong>bold and <em>italic bold</em></strong> and bold_</p>
            <p><em>italic and <strong>italic bold</strong></em></p>
            <p><strong>bold and <em>italic bold</em></strong></p>
            <p><em>italic <strong>italic bold</strong> italic</em></p>
            <p><strong><em>italic and bold</em> bold</strong>: foo bar <strong>italic</strong></p>
            <p><em><strong>italic and bold</strong> italic</em> foo bar <strong>italic</strong></p>
            <p><em>italic and <strong>italic bold</strong></em> <strong>italic</strong></p>
            <p><strong>bold and <em>italic bold</em></strong> <strong>italic</strong></p>
            <p><strong>bold<em>italic bold</em></strong></p>
            ''',
            True
        )


class TestBetterSmartAll(util.MdCase):
    """Test escaping cases for BetterEm with smart enabled everywhere."""

    extension = [
        'pymdownx.betterem'
    ]
    extension_configs = {
        "pymdownx.betterem": {
            "smart_enable": "all"
        }
    }

    def test_nested(self):
        """Test nested."""

        self.check_markdown(
            '**test *text text**',
            '<p>*<em>test <em>text text</em></em></p>'
        )

    def test_heavily_nested(self):
        """Test heavily nested."""

        self.check_markdown(
            '***test **test *text text** test* test***',
            '<p><strong><em>test <em><em>test <em>text text</em></em> test</em> test</em></strong></p>'
        )

    def test_absurdly_nested(self):
        """Test absurdly nested."""

        self.check_markdown(
            '*test **test **test **test **test **test*',
            '<p>*test **test **test **test **test *<em>test</em></p>'
        )

    def test_tripple_nested(self):
        """Test triple nested."""

        self.check_markdown(
            '***test **test *test test* test** test***',
            '<p><strong><em>test <strong>test <em>test test</em> test</strong> test</em></strong></p>'
        )

    def test_nested_case_with_complex_element_wrapping(self):
        """Test element building when elements are wrapped in complex ways."""

        self.check_markdown(
            "***test **test *test test* test** test *test* test***",
            "<p><strong><em>test <strong>test <em>test test</em> test</strong> test <em>test</em> test</em></strong></p>"  # noqa: E501
        )

    def test_deep_nested_triple_case(self):
        """Test deep nested triple case."""

        self.check_markdown(
            "***a ***b c** d* e***",
            "<p><strong><em>a <em><strong>b c</strong> d</em> e</em></strong></p>"
        )

    def test_nested_underscore(self):
        """Test nested."""

        self.check_markdown(
            '__test _text text__',
            '<p>_<em>test <em>text text</em></em></p>'
        )

    def test_heavily_nested_underscore(self):
        """Test heavily nested."""

        self.check_markdown(
            '___test __test _text text__ test_ test___',
            '<p><strong><em>test <em><em>test <em>text text</em></em> test</em> test</em></strong></p>'
        )

    def test_absurdly_nested_underscore(self):
        """Test absurdly nested."""

        self.check_markdown(
            '_test __test __test __test __test __test_',
            '<p>_test __test __test __test __test _<em>test</em></p>'
        )

    def test_tripple_nested_underscore(self):
        """Test triple nested."""

        self.check_markdown(
            '___test __test _test test_ test__ test___',
            '<p><strong><em>test <strong>test <em>test test</em> test</strong> test</em></strong></p>'
        )

    def test_nested_case_with_complex_element_wrapping_underscore(self):
        """Test element building when elements are wrapped in complex ways."""

        self.check_markdown(
            "___test __test _test test_ test__ test _test_ test___",
            "<p><strong><em>test <strong>test <em>test test</em> test</strong> test <em>test</em> test</em></strong></p>"  # noqa: E501
        )

    def test_deep_nested_triple_case_underscore(self):
        """Test deep nested triple case."""

        self.check_markdown(
            "___a ___b c__ d_ e___",
            "<p><strong><em>a <em><strong>b c</strong> d</em> e</em></strong></p>"
        )

    def test_complex_cases_star(self):
        """Test some complex cases for asterisks."""

        self.check_markdown(
            '''
            ***I'm italic and bold* I am just bold.**

            ***I'm bold and italic!** I am just italic.*

            *italic and **italic bold*** and *italic*

            **bold and *italic bold*** and *italic*

            ***I'm italic and bold* I am just bold.** *italic*

            ***I'm bold and italic!** I am just italic.* *italic*

            *italic and **italic bold*** and not italic*

            **bold and *italic bold*** and not italic*

            *italic and **italic bold***

            **bold and *italic bold***

            *italic **italic bold** italic*

            ***italic and bold* bold**: foo bar **bold**

            ***italic and bold** italic* foo bar **bold**

            *italic and **italic bold*** **bold**

            **bold and *italic bold*** **bold**

            **bold*and bold***
            ''',
            '''
            <p><strong><em>I'm italic and bold</em> I am just bold.</strong></p>
            <p><em><strong>I'm bold and italic!</strong> I am just italic.</em></p>
            <p><em>italic and <strong>italic bold</strong></em> and <em>italic</em></p>
            <p><strong>bold and <em>italic bold</em></strong> and <em>italic</em></p>
            <p><strong><em>I'm italic and bold</em> I am just bold.</strong> <em>italic</em></p>
            <p><em><strong>I'm bold and italic!</strong> I am just italic.</em> <em>italic</em></p>
            <p><em>italic and <strong>italic bold</strong></em> and not italic*</p>
            <p><strong>bold and <em>italic bold</em></strong> and not italic*</p>
            <p><em>italic and <strong>italic bold</strong></em></p>
            <p><strong>bold and <em>italic bold</em></strong></p>
            <p><em>italic <strong>italic bold</strong> italic</em></p>
            <p><strong><em>italic and bold</em> bold</strong>: foo bar <strong>bold</strong></p>
            <p><em><strong>italic and bold</strong> italic</em> foo bar <strong>bold</strong></p>
            <p><em>italic and <strong>italic bold</strong></em> <strong>bold</strong></p>
            <p><strong>bold and <em>italic bold</em></strong> <strong>bold</strong></p>
            <p><strong>bold*and bold</strong>*</p>
            ''',
            True
        )

    def test_complex_cases_underscore(self):
        """Test some complex cases for underscore."""

        self.check_markdown(
            '''
            ___I'm italic and bold_ I am just bold.__

            ___I'm bold and italic!__ I am just italic._

            _italic and __italic bold___ and _italic_

            __bold and _italic bold___ and _italic_

            ___I'm italic and bold_ I am just bold.__ _italic_

            ___I'm bold and italic!__ I am just italic._ _italic_

            _italic and __italic bold___ and not italic_

            __bold and _italic bold___ and not italic_

            _italic and __italic bold___

            __bold and _italic bold___

            _italic __italic bold__ italic_

            ___italic and bold_ bold__: foo bar __bold__

            ___italic and bold__ italic_ foo bar __bold__

            _italic and __italic bold___ __bold__

            __bold and _italic bold___ __bold__

            __bold_and bold___
            ''',
            '''
            <p><strong><em>I'm italic and bold</em> I am just bold.</strong></p>
            <p><em><strong>I'm bold and italic!</strong> I am just italic.</em></p>
            <p><em>italic and <strong>italic bold</strong></em> and <em>italic</em></p>
            <p><strong>bold and <em>italic bold</em></strong> and <em>italic</em></p>
            <p><strong><em>I'm italic and bold</em> I am just bold.</strong> <em>italic</em></p>
            <p><em><strong>I'm bold and italic!</strong> I am just italic.</em> <em>italic</em></p>
            <p><em>italic and <strong>italic bold</strong></em> and not italic_</p>
            <p><strong>bold and <em>italic bold</em></strong> and not italic_</p>
            <p><em>italic and <strong>italic bold</strong></em></p>
            <p><strong>bold and <em>italic bold</em></strong></p>
            <p><em>italic <strong>italic bold</strong> italic</em></p>
            <p><strong><em>italic and bold</em> bold</strong>: foo bar <strong>bold</strong></p>
            <p><em><strong>italic and bold</strong> italic</em> foo bar <strong>bold</strong></p>
            <p><em>italic and <strong>italic bold</strong></em> <strong>bold</strong></p>
            <p><strong>bold and <em>italic bold</em></strong> <strong>bold</strong></p>
            <p><strong>bold_and bold</strong>_</p>
            ''',
            True
        )


class TestBetterEmMixedSmart(util.MdCase):
    """Tests BetterEm with mixed smart approach."""

    extension = [
        'pymdownx.betterem'
    ]
    extension_configs = {}

    def test_legacy(self):
        """Test normal smart mode."""

        self.check_markdown(
            """
            Test: * Won't highlight *

            Test: *Will highlight*

            Test: ***I'm italic and bold* I am just bold.**

            Test: ***I'm bold and italic!** I am just italic.*

            Test: ___A lot of underscores____________is okay___

            Test: __This will NOT all be bold __because of the placement of the center underscores.__

            Test: __This will all be bold __ because of the placement of the center underscores.__

            Test: __This will NOT all be bold__ because of the placement of the center underscores.__

            Test: __This will all be italic_ because the token is less than that of the surrounding.__

            Test: This is text __bold _italic bold___ with more text

            Test: *All will * be italic*

            Test: *All will NOT *be italic*

            Test: *All will not* be italic*

            Test: *All will not ** be italic*

            Test: **All will * be bold**

            Test: *All will *be italic**

            Test: **All will not*** be bold**

            Test: **All will not *** be bold**

            Test: This is text **bold *italic bold*** with more text

            Test: **test *test* *test* test**

            Test: ***test* test *test***

            Test: *test * test*

            Test: **test ** test**

            Test: __test _test_ _test_ test__

            Test: ___test_ test _test___

            Test: _test _ test_

            Test: __test __ test__

            Test: **test *(test)* test**

            Test: __test _(test)_ test__

            One asterisk: *

            One underscore: _

            Two asterisks: **

            With spaces: * *

            Two underscores __

            with spaces: _ _

            three asterisks: ***

            with spaces: * * *

            three underscores: ___

            with spaces: _ _ _

            One char: _a_
            """,
            """
            <p>Test: * Won't highlight *</p>
            <p>Test: <em>Will highlight</em></p>
            <p>Test: <strong><em>I'm italic and bold</em> I am just bold.</strong></p>
            <p>Test: <em><strong>I'm bold and italic!</strong> I am just italic.</em></p>
            <p>Test: <strong><em>A lot of underscores____________is okay</em></strong></p>
            <p>Test: __This will NOT all be bold <strong>because of the placement of the center underscores.</strong></p>
            <p>Test: <strong>This will all be bold __ because of the placement of the center underscores.</strong></p>
            <p>Test: <strong>This will NOT all be bold</strong> because of the placement of the center underscores.__</p>
            <p>Test: <em><em>This will all be italic</em> because the token is less than that of the surrounding.</em>_</p>
            <p>Test: This is text <strong>bold <em>italic bold</em></strong> with more text</p>
            <p>Test: <em>All will * be italic</em></p>
            <p>Test: *All will NOT <em>be italic</em></p>
            <p>Test: <em>All will not</em> be italic*</p>
            <p>Test: <em>All will not ** be italic</em></p>
            <p>Test: <strong>All will * be bold</strong></p>
            <p>Test: <em>All will <em>be italic</em></em></p>
            <p>Test: <strong>All will not</strong>* be bold**</p>
            <p>Test: <strong>All will not *** be bold</strong></p>
            <p>Test: This is text <strong>bold <em>italic bold</em></strong> with more text</p>
            <p>Test: <strong>test <em>test</em> <em>test</em> test</strong></p>
            <p>Test: <strong><em>test</em> test <em>test</em></strong></p>
            <p>Test: <em>test * test</em></p>
            <p>Test: <strong>test ** test</strong></p>
            <p>Test: <strong>test <em>test</em> <em>test</em> test</strong></p>
            <p>Test: <strong><em>test</em> test <em>test</em></strong></p>
            <p>Test: <em>test _ test</em></p>
            <p>Test: <strong>test __ test</strong></p>
            <p>Test: <strong>test <em>(test)</em> test</strong></p>
            <p>Test: <strong>test <em>(test)</em> test</strong></p>
            <p>One asterisk: *</p>
            <p>One underscore: _</p>
            <p>Two asterisks: **</p>
            <p>With spaces: * *</p>
            <p>Two underscores __</p>
            <p>with spaces: _ _</p>
            <p>three asterisks: ***</p>
            <p>with spaces: * * *</p>
            <p>three underscores: ___</p>
            <p>with spaces: _ _ _</p>
            <p>One char: <em>a</em></p>
            """,  # noqa: E501
            True
        )


class TestBetterEmReverseMixed(util.MdCase):
    """Tests BetterEm with smart mode reversed."""

    extension = [
        'pymdownx.betterem'
    ]
    extension_configs = {
        "pymdownx.betterem": {
            "smart_enable": "asterisk"
        }
    }

    def test_complex_cases(self):
        """Test smart mode reversed."""

        self.check_markdown(
            """
            Test: _ Won't highlight _

            Test: _Will highlight_

            Test: ___I'm italic and bold_ I am just bold.__

            Test: ___I'm bold and italic!__ I am just italic._

            Test: ***A lot of asterisks************is okay***

            Test: **This will NOT all be bold **because of the placement of the center asterisk.**

            Test: **This will all be bold ** because of the placement of the center asterisk.**

            Test: **This will NOT all be bold** because of the placement of the center asterisk.**

            Test: **This will all be italic* because the token is less than that of the surrounding.**

            Test: This is text **bold *italic bold*** with more text

            Test: _All will _ be italic_

            Test: _All will NOT _be italic_

            Test: _All will not_ be italic_

            Test: _All will not __ be italic_

            Test: __All will _ be bold__

            Test: _All will _be italic__

            Test: __All will not___ be bold__

            Test: __All will not ___ be bold__

            Test: This is text __bold _italic bold___ with more text

            Test: **test *test* *test* test**

            Test: ***test* test *test***

            Test: *test * test*

            Test: **test ** test**

            Test: __test _test_ _test_ test__

            Test: ___test_ test _test___

            Test: _test _ test_

            Test: __test __ test__

            Test: **test *(test)* test**

            Test: __test _(test)_ test__
            """,
            """
            <p>Test: _ Won't highlight _</p>
            <p>Test: <em>Will highlight</em></p>
            <p>Test: <strong><em>I'm italic and bold</em> I am just bold.</strong></p>
            <p>Test: <em><strong>I'm bold and italic!</strong> I am just italic.</em></p>
            <p>Test: <strong><em>A lot of asterisks************is okay</em></strong></p>
            <p>Test: **This will NOT all be bold <strong>because of the placement of the center asterisk.</strong></p>
            <p>Test: <strong>This will all be bold ** because of the placement of the center asterisk.</strong></p>
            <p>Test: <strong>This will NOT all be bold</strong> because of the placement of the center asterisk.**</p>
            <p>Test: <em><em>This will all be italic</em> because the token is less than that of the surrounding.</em>*</p>
            <p>Test: This is text <strong>bold <em>italic bold</em></strong> with more text</p>
            <p>Test: <em>All will _ be italic</em></p>
            <p>Test: _All will NOT <em>be italic</em></p>
            <p>Test: <em>All will not</em> be italic_</p>
            <p>Test: <em>All will not __ be italic</em></p>
            <p>Test: <strong>All will _ be bold</strong></p>
            <p>Test: <em>All will <em>be italic</em></em></p>
            <p>Test: <strong>All will not</strong>_ be bold__</p>
            <p>Test: <strong>All will not ___ be bold</strong></p>
            <p>Test: This is text <strong>bold <em>italic bold</em></strong> with more text</p>
            <p>Test: <strong>test <em>test</em> <em>test</em> test</strong></p>
            <p>Test: <strong><em>test</em> test <em>test</em></strong></p>
            <p>Test: <em>test * test</em></p>
            <p>Test: <strong>test ** test</strong></p>
            <p>Test: <strong>test <em>test</em> <em>test</em> test</strong></p>
            <p>Test: <strong><em>test</em> test <em>test</em></strong></p>
            <p>Test: <em>test _ test</em></p>
            <p>Test: <strong>test __ test</strong></p>
            <p>Test: <strong>test <em>(test)</em> test</strong></p>
            <p>Test: <strong>test <em>(test)</em> test</strong></p>
            """,  # noqa: E501
            True

        )


class TestBetterCached(util.MdCase):
    """Tests BetterEm with cached cases."""

    extension = [
        'pymdownx.betterem'
    ]
    extension_configs = {}


    def test_cache(self):
        """Test an explicit case that requires caching."""

        self.check_markdown(
            '*a **b** *c **d** *e **f**',
            '<p>*a <strong>b</strong> *c <strong>d</strong> *e <strong>f</strong></p>'
        )
