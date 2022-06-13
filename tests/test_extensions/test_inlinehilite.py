"""Test cases for Highlight."""
from .. import util
import pymdownx.arithmatex as arithmatex
from pymdownx.inlinehilite import InlineHiliteException
import warnings


def _format(src, language, class_name, md):
    """Inline math formatter."""

    return '<span class="lang-%s %s">%s</span>' % (language, class_name, src)


def _default_format(src, language, class_name, md):
    """Inline math formatter."""

    return '<custom class="lang-%s %s">%s</custom>' % (language, class_name, src)


def _format_exploder(src, language, class_name, md):
    """Inline math formatter."""

    raise Exception('Boom!')


def _format_exploder_fail(src, language, class_name, md):
    """Inline math formatter."""

    raise InlineHiliteException('Boom!')


class TestInlineHilite(util.MdCase):
    """Test general cases for inline highlight."""

    extension = [
        'markdown.extensions.attr_list',
        'pymdownx.highlight',
        'pymdownx.inlinehilite',
    ]
    extension_configs = {
        'pymdownx.inlinehilite': {
            'style_plain_text': True,
            'css_class': 'inlinehilite'
        }
    }

    def test_language(self):
        """Test language handling."""

        # Test #! original syntax
        self.check_markdown(
            r'`#!python import module`.',
            r'<p><code class="inlinehilite"><span class="kn">import</span> <span class="nn">module</span></code>.</p>'
        )

        # Test ::: syntax
        self.check_markdown(
            r'`:::python import module`.',
            r'<p><code class="inlinehilite"><span class="kn">import</span> <span class="nn">module</span></code>.</p>'
        )

        # Test escaping language with space
        self.check_markdown(
            r'` #!python import module`.',
            r'<p><code class="inlinehilite">#!python import module</code>.</p>'
        )

        # Test bad language
        self.check_markdown(
            r'`#!bad import module`.',
            r'<p><code class="inlinehilite">import module</code>.</p>'
        )

    def test_escape(self):
        """Test backtick escape logic."""

        self.check_markdown(
            r'`Code`',
            r'<p><code class="inlinehilite">Code</code></p>'
        )

        self.check_markdown(
            r'\`Not code`',
            r'<p>`Not code`</p>'
        )

        self.check_markdown(
            r'\\`Code`',
            r'<p>\<code class="inlinehilite">Code</code></p>'
        )

        self.check_markdown(
            r'\\\`Not code`',
            r'<p>\`Not code`</p>'
        )

        self.check_markdown(
            r'\\\\`Code`',
            r'<p>\\<code class="inlinehilite">Code</code></p>'
        )

    def test_attributes(self):
        """Test with attribute extension."""

        self.check_markdown(
            r'`#!python import module`{: .test}',
            r'<p><code class="inlinehilite test">'
            r'<span class="kn">import</span> <span class="nn">module</span>'
            r'</code></p>'
        )


class TestInlineHilitePlainText(util.MdCase):
    """Test inline highlight when not styling plain text."""

    extension = [
        'pymdownx.highlight',
        'pymdownx.inlinehilite',
    ]
    extension_configs = {
        'pymdownx.inlinehilite': {
            'style_plain_text': False
        }
    }

    def test_unstyled_plaintext(self):
        """Test unstyled plain text."""

        self.check_markdown(
            r'Lets test inline highlight no guessing and no text styling `import module`.',
            r'<p>Lets test inline highlight no guessing and no text styling <code>import module</code>.</p>'
        )


class TestInlineHiliteNoClass(util.MdCase):
    """Test with no class."""

    extension = [
        'pymdownx.highlight',
        'pymdownx.inlinehilite',
    ]
    extension_configs = {
        'pymdownx.highlight': {
            'css_class': ''
        }
    }

    def test_no_class(self):
        """Test with no class."""

        self.check_markdown(
            r'Lets test inline highlight no guessing and no text styling `#!python import module`.',
            r'<p>Lets test inline highlight no guessing and no text styling <code><span class="kn">import</span> <span class="nn">module</span></code>.</p>'  # noqa: E501
        )


class TestInlineHiliteNoClassNoPygments(util.MdCase):
    """Test with no class and no Pygments."""

    extension = [
        'pymdownx.highlight',
        'pymdownx.inlinehilite',
    ]
    extension_configs = {
        'pymdownx.highlight': {
            'css_class': '',
            'use_pygments': False
        }
    }

    def test_no_class_no_pygments(self):
        """Test with no class and no Pygments."""

        self.check_markdown(
            r'Lets test inline highlight no guessing and no text styling `#!python import module`.',
            r'<p>Lets test inline highlight no guessing and no text styling <code class="language-python">import module</code>.</p>'  # noqa: E501
        )


class TestInlineHiliteNoPygments(util.MdCase):
    """Test inline highlight without Pygments."""

    extension = [
        'pymdownx.highlight',
        'pymdownx.inlinehilite',
    ]
    extension_configs = {
        'pymdownx.highlight': {
            'use_pygments': False
        },
        'pymdownx.inlinehilite': {
            'css_class': 'inlinehilite'
        }
    }

    def test_no_pygments(self):
        """Ensure proper behavior when disabling Pygments."""

        self.check_markdown(
            r'`#!python import module`.',
            r'<p><code class="language-python inlinehilite">import module</code>.</p>'
        )


class TestInlineHiliteGuess(util.MdCase):
    """Test inline highlight with guessing."""

    extension = [
        'pymdownx.highlight',
        'pymdownx.inlinehilite',
    ]
    extension_configs = {
        'pymdownx.highlight': {
            'guess_lang': True
        },
        'pymdownx.inlinehilite': {
            'css_class': 'inlinehilite',
            'style_plain_text': True
        }
    }

    def test_guessing(self):
        """Ensure guessing can be enabled."""

        self.check_markdown(
            r'`import module`.',
            r'<p><code class="inlinehilite"><span class="kn">import</span> <span class="nn">module</span></code>.</p>'
        )


class TestInlineHiliteGuessInline(util.MdCase):
    """Test inline highlight with guessing set to be inline only."""

    extension = [
        'pymdownx.highlight',
        'pymdownx.inlinehilite',
        'pymdownx.superfences'
    ]
    extension_configs = {
        'pymdownx.highlight': {
            'guess_lang': 'inline'
        },
        'pymdownx.inlinehilite': {
            'css_class': 'inlinehilite',
            'style_plain_text': True
        }
    }

    def test_guessing_inline(self):
        """Ensure guessing can be enabled for inline only."""

        self.check_markdown(
            r'`import module`.',
            r'<p><code class="inlinehilite"><span class="kn">import</span> <span class="nn">module</span></code>.</p>'
        )

    def test_no_guessing_block(self):
        """Ensure block is not guessed when set as inline only."""

        self.check_markdown(
            r'''
            ```
            <!DOCTYPE html>
            <html>
            <body>
            <h1>My great test</h1>
            <p>Thou shalt be re-educated through labour should this test ever fails.</p>
            </body>
            </html>
            ```
            ''',
            r'''
            <div class="highlight"><pre><span></span><code>&lt;!DOCTYPE html&gt;
            &lt;html&gt;
            &lt;body&gt;
            &lt;h1&gt;My great test&lt;/h1&gt;
            &lt;p&gt;Thou shalt be re-educated through labour should this test ever fails.&lt;/p&gt;
            &lt;/body&gt;
            &lt;/html&gt;
            </code></pre></div>
            ''',
            True
        )


class TestInlineHiliteCodeHilite(util.MdCase):
    """Test inline highlight with CodeHilite."""

    extension = [
        'markdown.extensions.codehilite',
        'pymdownx.inlinehilite',
    ]
    extension_configs = {
        'markdown.extensions.codehilite': {
            'guess_lang': False
        },
        'pymdownx.inlinehilite': {
            'style_plain_text': True
        }
    }

    def test_codehilite(self):
        """Test CodeHilite."""

        # Test #! original syntax
        self.check_markdown(
            r'`#!python import module`.',
            r'<p><code class="highlight"><span class="kn">import</span> <span class="nn">module</span></code>.</p>'
        )

        # Test ::: syntax
        self.check_markdown(
            r'`:::python import module`.',
            r'<p><code class="highlight"><span class="kn">import</span> <span class="nn">module</span></code>.</p>'
        )

        # Test escaping language with space
        self.check_markdown(
            r'` #!python import module`.',
            r'<p><code class="highlight">#!python import module</code>.</p>'
        )

        # Test bad language
        self.check_markdown(
            r'`#!bad import module`.',
            r'<p><code class="highlight">import module</code>.</p>'
        )


class TestInlineHiliteCustom1(util.MdCase):
    """Test custom InlineHilite cases."""

    extension = [
        'pymdownx.highlight',
        'pymdownx.inlinehilite',
    ]
    extension_configs = {
        'pymdownx.inlinehilite': {
            'css_class': 'inlinehilite',
            'custom_inline': [
                {
                    'name': 'math',
                    'class': 'arithmatex',
                    'format': arithmatex.arithmatex_inline_format(mode='mathjax')
                }
            ]
        }
    }

    def test_arithmatex(self):
        """Test Arithmatex."""

        self.check_markdown(
            r'`#!math 3 + 3`',
            r'''
            <p><span class="arithmatex"><script type="math/tex">3 + 3</script></span></p>
            ''',
            True
        )


class TestLegacyInlineHiliteCustom1(util.MdCase):
    """Test custom InlineHilite cases."""

    extension = [
        'pymdownx.highlight',
        'pymdownx.inlinehilite',
    ]
    extension_configs = {
        'pymdownx.inlinehilite': {
            'css_class': 'inlinehilite',
            'custom_inline': [
                {
                    'name': 'math',
                    'class': 'arithmatex',
                    'format': arithmatex.inline_mathjax_format
                }
            ]
        }
    }

    def test_legacy_arithmatex(self):
        """Test Arithmatex."""

        with warnings.catch_warnings(record=True) as w:
            self.check_markdown(
                r'`#!math 3 + 3`',
                r'''
                <p><span class="arithmatex"><script type="math/tex">3 + 3</script></span></p>
                ''',
                True
            )
            self.assertTrue(len(w) == 1)
            self.assertTrue(issubclass(w[-1].category, DeprecationWarning))


class TestInlineHiliteCustom2(util.MdCase):
    """Test custom InlineHilite cases."""

    extension = [
        'pymdownx.highlight',
        'pymdownx.inlinehilite',
    ]
    extension_configs = {
        'pymdownx.inlinehilite': {
            'css_class': 'inlinehilite',
            'custom_inline': [
                {
                    'name': 'math',
                    'class': 'arithmatex',
                    'format': arithmatex.arithmatex_inline_format(mode="mathjax", preview=True)
                }
            ]
        }
    }

    def test_preview_arithmatex(self):
        """Test preview Arithmatex."""

        self.check_markdown(
            r'`#!math 3 + 3`',
            r'<p><span class="arithmatex"><span class="MathJax_Preview">3 + 3</span>'
            r'<script type="math/tex">3 + 3</script></span></p>'
        )


class TestLegacyInlineHiliteCustom2(util.MdCase):
    """Test custom InlineHilite cases."""

    extension = [
        'pymdownx.highlight',
        'pymdownx.inlinehilite',
    ]
    extension_configs = {
        'pymdownx.inlinehilite': {
            'css_class': 'inlinehilite',
            'custom_inline': [
                {
                    'name': 'math',
                    'class': 'arithmatex',
                    'format': arithmatex.inline_mathjax_preview_format
                }
            ]
        }
    }

    def test_legacy_preview_arithmatex(self):
        """Test preview Arithmatex."""

        with warnings.catch_warnings(record=True) as w:
            self.check_markdown(
                r'`#!math 3 + 3`',
                r'<p><span class="arithmatex"><span class="MathJax_Preview">3 + 3</span>'
                r'<script type="math/tex">3 + 3</script></span></p>'
            )
            self.assertTrue(len(w) == 1)
            self.assertTrue(issubclass(w[-1].category, DeprecationWarning))


class TestInlineHiliteCustom3(util.MdCase):
    """Test custom InlineHilite cases."""

    extension = [
        'pymdownx.highlight',
        'pymdownx.inlinehilite',
    ]
    extension_configs = {
        'pymdownx.inlinehilite': {
            'css_class': 'inlinehilite',
            'custom_inline': [
                {
                    'name': 'math',
                    'class': 'arithmatex',
                    'format': arithmatex.arithmatex_inline_format(mode="generic")
                }
            ]
        }
    }

    def test_arithmatex_generic(self):
        """Test generic Arithmatex."""

        self.check_markdown(
            r'`#!math 3 + 3`',
            r'<p><span class="arithmatex">\(3 + 3\)</span></p>'
        )


class TestLegacyInlineHiliteCustom3(util.MdCase):
    """Test custom InlineHilite cases."""

    extension = [
        'pymdownx.highlight',
        'pymdownx.inlinehilite',
    ]
    extension_configs = {
        'pymdownx.inlinehilite': {
            'css_class': 'inlinehilite',
            'custom_inline': [
                {
                    'name': 'math',
                    'class': 'arithmatex',
                    'format': arithmatex.inline_generic_format
                }
            ]
        }
    }

    def test_legacy_arithmatex_generic(self):
        """Test generic Arithmatex."""

        with warnings.catch_warnings(record=True) as w:
            self.check_markdown(
                r'`#!math 3 + 3`',
                r'<p><span class="arithmatex">\(3 + 3\)</span></p>'
            )
            self.assertTrue(len(w) == 1)
            self.assertTrue(issubclass(w[-1].category, DeprecationWarning))


class TestInlineHiliteCustom4(util.MdCase):
    """Test custom InlineHilite cases."""

    extension = [
        'pymdownx.highlight',
        'pymdownx.inlinehilite',
    ]
    extension_configs = {
        'pymdownx.inlinehilite': {
            'css_class': 'inlinehilite',
            'custom_inline': [
                {
                    'name': 'test',
                    'class': 'class-test',
                    'format': _format
                }
            ]
        }
    }

    def test_custom(self):
        """Test custom formatter."""

        self.check_markdown(
            r'`#!test src test`',
            r'<p><span class="lang-test class-test">src test</span></p>'
        )


class TestInlineHiliteCustom5(util.MdCase):
    """Test custom InlineHilite cases."""

    extension = [
        'pymdownx.highlight',
        'pymdownx.inlinehilite',
    ]
    extension_configs = {
        'pymdownx.inlinehilite': {
            'css_class': 'inlinehilite',
            'custom_inline': [
                {
                    'name': '*',
                    'class': 'overwrite',
                    'format': _default_format
                },
                {
                    'name': 'test',
                    'class': 'class-test',
                    'format': _format
                }
            ]
        }
    }

    def test_custom(self):
        """Test custom formatter."""

        self.check_markdown(
            r'`#!test src test` `#!python src test`',
            r'<p><span class="lang-test class-test">src test</span> <custom class="lang-python overwrite">src test</custom></p>'  # noqa: E501
        )


class TestInlineHiliteCustomBrokenFormatter(util.MdCase):
    """Test custom broken InlineHilite cases."""

    extension = [
        'pymdownx.highlight',
        'pymdownx.inlinehilite',
    ]
    extension_configs = {
        'pymdownx.inlinehilite': {
            'custom_inline': [
                {
                    'name': 'test',
                    'class': 'test',
                    'format': _format_exploder
                }
            ]
        }
    }

    def test_broken(self):
        """Test custom broken formatter."""

        self.check_markdown(
            r'`#!test boom`',
            r'<p>`#!test boom`</p>'  # noqa: E501
        )


class TestInlineHiliteCustomBrokenFormatterFail(util.MdCase):
    """Test custom broken InlineHilite cases fails."""

    extension = [
        'pymdownx.highlight',
        'pymdownx.inlinehilite',
    ]
    extension_configs = {
        'pymdownx.inlinehilite': {
            'custom_inline': [
                {
                    'name': 'test',
                    'class': 'test',
                    'format': _format_exploder_fail
                }
            ]
        }
    }

    def test_broken(self):
        """Test custom broken formatter."""

        with self.assertRaises(InlineHiliteException):
            self.check_markdown(
                r'`#!test boom`',
                r''  # noqa: E501
            )
