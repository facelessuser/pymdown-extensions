"""Test cases for Highlight."""
from .. import util


class TestHighlightGuess(util.MdCase):
    """Test that highlighting works with guessing."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences']
    extension_configs = {
        'pymdownx.highlight': {
            'guess_lang': True
        }
    }

    def test_guess(self):
        """Test guessing."""

        self.check_markdown(
            r'''
            ```
            import test
            test.test()
            ```
            ''',
            '''
            <div class="highlight"><pre><span></span><code><span class="kn">import</span> <span class="nn">test</span>
            <span class="n">test</span><span class="o">.</span><span class="n">test</span><span class="p">()</span>
            </code></pre></div>
            ''',
            True
        )


class TestHighlightGuessBlock(util.MdCase):
    """Test that highlighting works with guessing for block."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences']
    extension_configs = {
        'pymdownx.highlight': {
            'guess_lang': "block"
        }
    }

    def test_guess_block(self):
        """Test guessing for block."""

        self.check_markdown(
            r'''
            ```
            import test
            test.test()
            ```
            ''',
            '''
            <div class="highlight"><pre><span></span><code><span class="kn">import</span> <span class="nn">test</span>
            <span class="n">test</span><span class="o">.</span><span class="n">test</span><span class="p">()</span>
            </code></pre></div>
            ''',
            True
        )

    def test_no_guess_inline(self):
        """Test inline code is not language guessed."""
        self.check_markdown(
            r'''
            `int i = std::numeric_limits<int>::min();`
            ''',
            '''
            <p><code>int i = std::numeric_limits&lt;int&gt;::min();</code></p>
            ''',
            True
        )


class TestHighlightAutoTitle(util.MdCase):
    """Test title cases."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences']
    extension_configs = {
        'pymdownx.highlight': {
            'auto_title': True
        }
    }

    def test_auto_tile(self):
        """Test auto title."""

        self.check_markdown(
            r'''
            ```pycon
            >>> import test
            ```
            ''',
            r'''
            <div class="highlight"><span class="filename">Python Console Session</span><pre><span></span><code><span class="gp">&gt;&gt;&gt; </span><span class="kn">import</span> <span class="nn">test</span>
            </code></pre></div>
            ''',  # noqa: E501
            True
        )


class TestHighlightAutoTitleMap(util.MdCase):
    """Test title cases."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences']
    extension_configs = {
        'pymdownx.highlight': {
            'auto_title': True,
            "auto_title_map": {
                "Python Console Session": "Python"
            }
        }
    }

    def test_auto_tile_map(self):
        """Test auto title."""

        self.check_markdown(
            r'''
            ```pycon
            >>> import test
            ```
            ''',
            r'''
            <div class="highlight"><span class="filename">Python</span><pre><span></span><code><span class="gp">&gt;&gt;&gt; </span><span class="kn">import</span> <span class="nn">test</span>
            </code></pre></div>
            ''',  # noqa: E501
            True
        )


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
            <div class="highlight"><pre><span></span><code><span class="linenos" data-linenos="1 "></span><span class="kn">import</span> <span class="nn">test</span>
            <span class="linenos" data-linenos="2 "></span><span class="n">test</span><span class="o">.</span><span class="n">test</span><span class="p">()</span>
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
            <div class="more"><table class="table"><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal">1</span>
            <span class="normal">2</span></pre></div></td><td class="code"><div><pre><span></span><code><span class="kn">import</span> <span class="nn">test</span>
            <span class="n">test</span><span class="o">.</span><span class="n">test</span><span class="p">()</span>
            </code></pre></div></td></tr></table></div>
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
            <div class="highlight"><pre><span></span><code><span class="linenos" data-linenos="1 "></span><span class="kn">import</span> <span class="nn">test</span>
            <span class="linenos special" data-linenos="2 "></span><span class="n">test</span><span class="o">.</span><span class="n">test</span><span class="p">()</span>
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
            <div class="highlight"><pre><span></span><code><span class="linenos special" data-linenos="1 "></span><span class="kn">import</span> <span class="nn">test</span>
            <span class="linenos special" data-linenos="2 "></span><span class="n">test</span><span class="o">.</span><span class="n">test</span><span class="p">()</span>
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


class TestGlobalLinenums(util.MdCase):
    """Test global line number cases."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences']
    extension_configs = {
        'pymdownx.highlight': {
            'linenums': True
        }
    }

    def test_global_line_numbers(self):
        """Test that global line numbers works."""

        self.check_markdown(
            r'''
            ```python
            import test
            test.test()
            ```
            ''',
            r'''
            <div class="highlight"><table class="highlighttable"><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal">1</span>
            <span class="normal">2</span></pre></div></td><td class="code"><div><pre><span></span><code><span class="kn">import</span> <span class="nn">test</span>
            <span class="n">test</span><span class="o">.</span><span class="n">test</span><span class="p">()</span>
            </code></pre></div></td></tr></table></div>
            ''',  # noqa: E501
            True
        )

    def test_global_disabling_of_line_numbers(self):
        """Test that global line numbers can be disabled."""

        self.check_markdown(
            r'''
            ```{.python linenums="0"}
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


class TestPygmentsLangClass(util.MdCase):
    """Test no Pygments with custom line number class."""

    extension = ['pymdownx.highlight', 'pymdownx.inlinehilite', 'pymdownx.superfences']
    extension_configs = {
        'pymdownx.highlight': {
            'pygments_lang_class': True
        }
    }

    def test_superfences(self):
        """Test language classes with SuperFences."""

        self.check_markdown(
            r'''
            ```python
            import test
            ```
            ''',
            r'''
            <div class="language-python highlight"><pre><span></span><code><span class="kn">import</span> <span class="nn">test</span>
            </code></pre></div>
            ''',  # noqa: E501
            True
        )

    def test_inlinehilite(self):
        """Test language classes with InlineHilite."""

        self.check_markdown(
            '''
            `#!python import test`
            ''',
            '''
            <p><code class="language-python highlight"><span class="kn">import</span> <span class="nn">test</span></code></p>
            ''',  # noqa: E501
            True
        )


class TestExtendedLang(util.MdCase):
    """Test extended language cases."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences', 'pymdownx.inlinehilite']
    extension_configs = {
        'pymdownx.highlight': {
            'extend_pygments_lang': [
                {'name': 'php-inline', 'lang': 'php', 'options': {'startinline': True}}
            ]
        }
    }

    def test_extended_lang_inlinehilite(self):
        """Test extended language in InlineHilite."""

        self.check_markdown(
            '''
            `#!php-inline $a = array("foo" => 0, "bar" => 1);`
            ''',
            '''
            <p><code class="highlight"><span class="nv">$a</span> <span class="o">=</span> <span class="k">array</span><span class="p">(</span><span class="s2">&quot;foo&quot;</span> <span class="o">=&gt;</span> <span class="mi">0</span><span class="p">,</span> <span class="s2">&quot;bar&quot;</span> <span class="o">=&gt;</span> <span class="mi">1</span><span class="p">);</span></code></p>
            ''',  # noqa: E501
            True
        )

    def test_extended_lang_superfences(self):
        """Test extended language in SuperFences."""

        self.check_markdown(
            '''
            ```php-inline
            $a = array("foo" => 0, "bar" => 1);
            ```
            ''',
            '''
            <div class="highlight"><pre><span></span><code><span class="nv">$a</span> <span class="o">=</span> <span class="k">array</span><span class="p">(</span><span class="s2">&quot;foo&quot;</span> <span class="o">=&gt;</span> <span class="mi">0</span><span class="p">,</span> <span class="s2">&quot;bar&quot;</span> <span class="o">=&gt;</span> <span class="mi">1</span><span class="p">);</span>
            </code></pre></div>
            ''',  # noqa: E501
            True
        )

    def test_extended_lang_case(self):
        """Test extended language in SuperFences."""

        self.check_markdown(
            '''
            ```PHP-Inline
            $a = array("foo" => 0, "bar" => 1);
            ```
            ''',
            '''
            <div class="highlight"><pre><span></span><code><span class="nv">$a</span> <span class="o">=</span> <span class="k">array</span><span class="p">(</span><span class="s2">&quot;foo&quot;</span> <span class="o">=&gt;</span> <span class="mi">0</span><span class="p">,</span> <span class="s2">&quot;bar&quot;</span> <span class="o">=&gt;</span> <span class="mi">1</span><span class="p">);</span>
            </code></pre></div>
            ''',  # noqa: E501
            True
        )
