"""Test cases for Highlight."""
from .. import util


class TestHighlightInline(util.MdCase):
    """Test highlight inline."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences']
    extension_configs = {
        'pymdownx.highlight': {
            'linenums_style': 'pymdownx-inline'
        }
    }

    def test_pymdownx_inline(self):
        """Test new inline mode."""

        self.check_markdown(
            r'''
            ```python linenums="1"
            import test
            test.test()
            ```
            ''',
            r'''
            <div class="highlight"><pre><span></span><code><span class="lineno" data-linenos="1 "></span><span class="kn">import</span> <span class="nn">test</span>
            <span class="lineno" data-linenos="2 "></span><span class="n">test</span><span class="o">.</span><span class="n">test</span><span class="p">()</span>
            </code></pre></div>
            ''',  # noqa: E501
            True
        )


class TestNoClass(util.MdCase):
    """Test no class."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences', 'markdown.extensions.attr_list']
    extension_configs = {
        'pymdownx.highlight': {
            'css_class': ''
        }
    }

    def test_no_class(self):
        """Test with no class."""

        self.check_markdown(
            r'''
            ```python
            import test
            test.test()
            ```
            ''',
            r'''
            <div><pre><span></span><code><span class="kn">import</span> <span class="nn">test</span>
            <span class="n">test</span><span class="o">.</span><span class="n">test</span><span class="p">()</span>
            </code></pre></div>
            ''',  # noqa: E501
            True
        )

    def test_no_class_and_user_class(self):
        """Test with no class and user class."""

        self.check_markdown(
            r'''
            ```{.python .more}
            import test
            test.test()
            ```
            ''',
            r'''
            <div class="more"><pre><span></span><code><span class="kn">import</span> <span class="nn">test</span>
            <span class="n">test</span><span class="o">.</span><span class="n">test</span><span class="p">()</span>
            </code></pre></div>
            ''',  # noqa: E501
            True
        )

    def test_no_class_and_user_class_linenums(self):
        """Test with no class and user class and table format."""

        self.check_markdown(
            r'''
            ```{.python .more linenums="1"}
            import test
            test.test()
            ```
            ''',
            r'''
            <table class="more table"><tr><td class="linenos"><div class="linenodiv"><pre><span></span>1
            2</pre></div></td><td class="code"><div class="more "><pre><span></span><code><span class="kn">import</span> <span class="nn">test</span>
            <span class="n">test</span><span class="o">.</span><span class="n">test</span><span class="p">()</span>
            </code></pre></div>
            </td></tr></table>
            ''',  # noqa: E501
            True
        )


class TestNoClassNoPygments(util.MdCase):
    """Test no class."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences']
    extension_configs = {
        'pymdownx.highlight': {
            'css_class': '',
            'use_pygments': False
        }
    }

    def test_no_class_no_pygments(self):
        """Test with no class and no Pygments."""

        self.check_markdown(
            r'''
            ```python
            import test
            test.test()
            ```
            ''',
            r'''
            <pre><code class="language-python">import test
            test.test()</code></pre>
            ''',  # noqa: E501
            True
        )


class TestCustomLangPrefixNoPygments(util.MdCase):
    """Test custom language prefix."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences', 'pymdownx.inlinehilite']
    extension_configs = {
        'pymdownx.highlight': {
            'language_prefix': 'lang-',
            'use_pygments': False
        }
    }

    def test_custom_prefix_no_pygments(self):
        """Test with custom prefix and no Pygments."""

        self.check_markdown(
            r'''
            ```python
            import test
            test.test()
            ```
            ''',
            r'''
            <pre class="highlight"><code class="lang-python">import test
            test.test()</code></pre>
            ''',  # noqa: E501
            True
        )

    def test_custom_prefix_no_pygments_inline(self):
        """Test with custom prefix and no Pygments with inline code."""

        self.check_markdown(
            '`#!python import test`',
            '<p><code class="lang-python highlight">import test</code></p>'
        )


class TestNoPygments(util.MdCase):
    """Test no Pygments."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences']
    extension_configs = {
        'pymdownx.highlight': {
            'use_pygments': False
        }
    }

    def test_no_pygments(self):
        """Test with no Pygments."""

        self.check_markdown(
            r'''
            ```python
            import test
            test.test()
            ```
            ''',
            r'''
            <pre class="highlight"><code class="language-python">import test
            test.test()</code></pre>
            ''',
            True
        )

    def test_no_pygments_linenums(self):
        """Test with no Pygments and line numbers."""

        self.check_markdown(
            r'''
            ```python linenums="1"
            import test
            test.test()
            ```
            ''',
            r'''
            <p><code>python linenums="1"
            import test
            test.test()</code></p>
            ''',
            True
        )


class TestNoPygmentsCustomLineClass(util.MdCase):
    """Test no Pygments with custom line number class."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences']
    extension_configs = {
        'pymdownx.highlight': {
            'use_pygments': False,
            'linenums_class': 'line-numbers',
            'linenums': True
        }
    }

    def test_no_pygments_linenums_custom_class(self):
        """Test with no Pygments and line numbers."""

        self.check_markdown(
            r'''
            Text

                import test
                test.test()

            Text
            ''',
            r'''
            <p>Text</p>
            <pre class="highlight"><code>import test
            test.test()
            </code></pre>

            <p>Text</p>
            ''',
            True
        )

    def test_no_pygments_linenums_custom_class_fences(self):
        """Test with no Pygments and line numbers in fences."""

        self.check_markdown(
            r'''
            ```python
            import test
            test.test()
            ```
            ''',
            r'''
            <pre class="highlight"><code class="language-python">import test
            test.test()</code></pre>
            ''',
            True
        )


class TestHighlightSpecial(util.MdCase):
    """Test highlight global special."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences']
    extension_configs = {
        'pymdownx.highlight': {
            'linenums_style': 'pymdownx-inline',
            'linenums_special': 2
        }
    }

    def test_special(self):
        """Test global special mode."""

        self.check_markdown(
            r'''
            ```python linenums="1"
            import test
            test.test()
            ```
            ''',
            r'''
            <div class="highlight"><pre><span></span><code><span class="lineno" data-linenos="1 "></span><span class="kn">import</span> <span class="nn">test</span>
            <span class="lineno special" data-linenos="2 "></span><span class="n">test</span><span class="o">.</span><span class="n">test</span><span class="p">()</span>
            </code></pre></div>
            ''',  # noqa: E501
            True
        )

    def test_special_override(self):
        """Test global special mode override."""

        self.check_markdown(
            r'''
            ```python linenums="1 1 1"
            import test
            test.test()
            ```
            ''',
            r'''
            <div class="highlight"><pre><span></span><code><span class="lineno special" data-linenos="1 "></span><span class="kn">import</span> <span class="nn">test</span>
            <span class="lineno special" data-linenos="2 "></span><span class="n">test</span><span class="o">.</span><span class="n">test</span><span class="p">()</span>
            </code></pre></div>
            ''',  # noqa: E501
            True
        )


class TestDisabledLinenums(util.MdCase):
    """Test with line numbers globally disabled."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences']
    extension_configs = {
        'pymdownx.highlight': {
            'linenums': False
        }
    }

    def test_global_disable(self):
        """Test with line numbers globally disabled."""

        self.check_markdown(
            r'''
            ```python linenums="1"
            import test
            test.test()
            ```
            ''',
            r'''
            <div class="highlight"><pre><span></span><code><span class="kn">import</span> <span class="nn">test</span>
            <span class="n">test</span><span class="o">.</span><span class="n">test</span><span class="p">()</span>
            </code></pre></div>
            ''',  # noqa: E501
            True
        )


class TestDisabledLinenumsNoPygments(util.MdCase):
    """Test with line numbers globally disabled with no Pygments."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences']
    extension_configs = {
        'pymdownx.highlight': {
            'linenums': False,
            'use_pygments': False
        }
    }

    def test_global_disable(self):
        """Test with line numbers globally disabled and no Pygments."""

        self.check_markdown(
            r'''
            ```python linenums="1"
            import test
            test.test()
            ```
            ''',
            r'''
            <p><code>python linenums="1"
            import test
            test.test()</code></p>
            ''',  # noqa: E501
            True
        )
