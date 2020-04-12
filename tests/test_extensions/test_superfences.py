"""Test cases for SuperFences."""
from .. import util
import unittest
import markdown
import pymdownx.arithmatex as arithmatex
from pymdownx.util import PymdownxDeprecationWarning
import warnings


def custom_format_old(source, language, class_name, options, md):
    """Custom format."""

    return '<div lang="%s" class_name="class-%s", option="%s">%s</div>' % (language, class_name, options['opt'], source)


def custom_format(source, language, class_name, options, md, classes=None, value_id='', **kwargs):
    """Custom format."""

    return '<div lang="%s" class_name="class-%s", option="%s">%s</div>' % (language, class_name, options['opt'], source)


def default_format(source, language, class_name, options, md, classes=None, value_id='', **kwargs):
    """Default format."""

    return '<custom lang="%s" class_name="class-%s">%s</custom>' % (language, class_name, source)


def custom_validator(language, options):
    """Custom validator."""

    okay = True
    for k in options.keys():
        if k != 'opt':
            okay = False
            break
    if okay:
        if options['opt'] != "A":
            okay = False
    return okay


class TestLegacyTab(util.MdCase):
    """Test legacy tab cases."""

    extension = ['pymdownx.superfences']
    extension_configs = {
        'pymdownx.superfences': {
            'legacy_tab_classes': True
        }
    }

    def test_legacy_css(self):
        """Test legacy tab CSS classes."""

        self.check_markdown(
            r'''
            ```python tab="Test"
            This will be a tab.
            ```
            ''',
            r'''
            <div class="superfences-tabs" data-tabs="1:1">
            <input name="__tabbed_1" type="radio" id="__tabbed_1_1" checked="checked" /><label for="__tabbed_1_1">Test</label><div class="superfences-content"><div class="highlight"><pre><span></span><code><span class="n">This</span> <span class="n">will</span> <span class="n">be</span> <span class="n">a</span> <span class="n">tab</span><span class="o">.</span>
            </code></pre></div></div>
            </div>
            ''',  # noqa: E501
            True
        )


class TestHighlightLines(util.MdCase):
    """Test line highlighting."""

    extension = ['pymdownx.superfences']
    extension_configs = {}

    def test_highlight_range(self):
        """Test highlight ranges."""

        self.check_markdown(
            r'''
            ```py3 hl_lines="1-2 5 7-8"
            import foo
            import boo.baz
            import foo.bar.baz

            class Foo:
               def __init__(self):
                   self.foo = None
                   self.bar = None
                   self.baz = None
            ```
            ''',
            '''
            <div class="highlight"><pre><span></span><code><span class="hll"><span class="kn">import</span> <span class="nn">foo</span>
            </span><span class="hll"><span class="kn">import</span> <span class="nn">boo.baz</span>
            </span><span class="kn">import</span> <span class="nn">foo.bar.baz</span>

            <span class="hll"><span class="k">class</span> <span class="nc">Foo</span><span class="p">:</span>
            </span>   <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
            <span class="hll">       <span class="bp">self</span><span class="o">.</span><span class="n">foo</span> <span class="o">=</span> <span class="kc">None</span>
            </span><span class="hll">       <span class="bp">self</span><span class="o">.</span><span class="n">bar</span> <span class="o">=</span> <span class="kc">None</span>
            </span>       <span class="bp">self</span><span class="o">.</span><span class="n">baz</span> <span class="o">=</span> <span class="kc">None</span>
            </code></pre></div>
            ''',  # noqa: E501
            True
        )

    def test_highlight_out_of_range(self):
        """Test highlight ranges."""

        self.check_markdown(
            r'''
            ```py3 hl_lines="0 10"
            import foo
            import boo.baz
            import foo.bar.baz

            class Foo:
               def __init__(self):
                   self.foo = None
                   self.bar = None
                   self.baz = None
            ```
            ''',
            '''
            <div class="highlight"><pre><span></span><code><span class="kn">import</span> <span class="nn">foo</span>
            <span class="kn">import</span> <span class="nn">boo.baz</span>
            <span class="kn">import</span> <span class="nn">foo.bar.baz</span>

            <span class="k">class</span> <span class="nc">Foo</span><span class="p">:</span>
               <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
                   <span class="bp">self</span><span class="o">.</span><span class="n">foo</span> <span class="o">=</span> <span class="kc">None</span>
                   <span class="bp">self</span><span class="o">.</span><span class="n">bar</span> <span class="o">=</span> <span class="kc">None</span>
                   <span class="bp">self</span><span class="o">.</span><span class="n">baz</span> <span class="o">=</span> <span class="kc">None</span>
            </code></pre></div>
            ''',  # noqa: E501
            True
        )

    def test_highlight_in_range_only(self):
        """Test highlight ranges."""

        self.check_markdown(
            r'''
            ```py3 hl_lines="0-10"
            import foo
            import boo.baz
            import foo.bar.baz

            class Foo:
               def __init__(self):
                   self.foo = None
                   self.bar = None
                   self.baz = None
            ```
            ''',
            '''
            <div class="highlight"><pre><span></span><code><span class="hll"><span class="kn">import</span> <span class="nn">foo</span>
            </span><span class="hll"><span class="kn">import</span> <span class="nn">boo.baz</span>
            </span><span class="hll"><span class="kn">import</span> <span class="nn">foo.bar.baz</span>
            </span><span class="hll">
            </span><span class="hll"><span class="k">class</span> <span class="nc">Foo</span><span class="p">:</span>
            </span><span class="hll">   <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
            </span><span class="hll">       <span class="bp">self</span><span class="o">.</span><span class="n">foo</span> <span class="o">=</span> <span class="kc">None</span>
            </span><span class="hll">       <span class="bp">self</span><span class="o">.</span><span class="n">bar</span> <span class="o">=</span> <span class="kc">None</span>
            </span><span class="hll">       <span class="bp">self</span><span class="o">.</span><span class="n">baz</span> <span class="o">=</span> <span class="kc">None</span>
            </span></code></pre></div>
            ''',  # noqa: E501
            True
        )


class TestWaringings(unittest.TestCase):
    """Test warnings."""

    def test_highlight_code(self):
        """Test highlight code warning."""

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            markdown.Markdown(
                extensions=['pymdownx.superfences'],
                extension_configs={'pymdownx.superfences': {'highlight_code': False}}
            ).convert('```\ntest\n```\n')

            self.assertTrue(len(w) == 1)
            self.assertTrue(issubclass(w[-1].category, PymdownxDeprecationWarning))

    def test_tab(self):
        """Test tab deprecation."""

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            markdown.Markdown(
                extensions=['pymdownx.superfences']
            ).convert('```tab="Tab 1"\ntest\n```\n')

            self.assertTrue(len(w) == 1)
            self.assertTrue(issubclass(w[-1].category, PymdownxDeprecationWarning))

    def test_format(self):
        """Test warning using old format style."""

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            markdown.Markdown(
                extensions=['pymdownx.superfences'],
                extension_configs={
                    'pymdownx.superfences': {
                        'custom_fences': [
                            {
                                'name': 'test',
                                'class': 'test',
                                'format': custom_format_old,
                                'validator': custom_validator
                            }
                        ]
                    }
                }
            ).convert('```test opt="A"\ncontent\n```\n')

            self.assertTrue(len(w) == 1)
            self.assertTrue(issubclass(w[-1].category, UserWarning))


class TestTabbedFenceWithTabbedExtension(util.MdCase):
    """Test legacy tab cases."""

    extension = ['pymdownx.superfences', 'pymdownx.tabbed']
    extension_configs = {}

    def test_tabbed_together(self):
        """
        Test SuperFences' tabbed implementation along side Tabbed.

        We should calculate the tab set number correctly based off of the biggest Tabbed tab set value.
        """

        self.check_markdown(
            r'''
            === "Test"
                Content

            ```python tab="Test"
            This will be a tab.
            ```
            ''',
            r'''
            <div class="tabbed-set" data-tabs="1:1"><input checked="checked" id="__tabbed_1_1" name="__tabbed_1" type="radio" /><label for="__tabbed_1_1">Test</label><div class="tabbed-content">
            <p>Content</p>
            </div>
            </div>
            <div class="tabbed-set" data-tabs="2:1">
            <input name="__tabbed_2" type="radio" id="__tabbed_2_1" checked="checked" /><label for="__tabbed_2_1">Test</label><div class="tabbed-content"><div class="highlight"><pre><span></span><code><span class="n">This</span> <span class="n">will</span> <span class="n">be</span> <span class="n">a</span> <span class="n">tab</span><span class="o">.</span>
            </code></pre></div></div>
            </div>
            ''',  # noqa: E501
            True
        )


class TestSuperFences(util.MdCase):
    """Test Details."""

    extension = ['pymdownx.superfences']
    extension_configs = {}

    def test_bad_options(self):
        """Test bad options."""

        self.check_markdown(
            r'''
            ```python option="bad"
            import test
            ```
            ''',
            r'''
            <p><code>python option="bad"
            import test</code></p>
            ''',
            True
        )

    def test_bad_option_value(self):
        """Test bad option values."""

        self.check_markdown(
            r'''
            ```python hl_lines="unexpected 3" linenums="1"
            """Some file."""
            import foo.bar
            import boo.baz
            import foo.bar.baz
            ```
            ''',
            r'''
            <p><code>python hl_lines="unexpected 3" linenums="1"
            """Some file."""
            import foo.bar
            import boo.baz
            import foo.bar.baz</code></p>
            ''',
            True
        )


class TestSuperFencesCustom1(util.MdCase):
    """Test Details."""

    extension = ['pymdownx.superfences']
    extension_configs = {
        'pymdownx.superfences': {
            'custom_fences': [
                {
                    'name': 'test',
                    'class': 'test',
                    'format': custom_format,
                    'validator': custom_validator
                }
            ]
        }
    }

    def test_bad_options(self):
        """Test bad options."""

        self.check_markdown(
            r'''
            ```test bad="bad"
            test
            ```
            ''',
            r'''
            <p><code>test bad="bad"
            test</code></p>
            ''',
            True
        )

    def test_bad_option_value(self):
        """Test bad options."""

        self.check_markdown(
            r'''
            ```test opt="B"
            test
            ```
            ''',
            r'''
            <p><code>test opt="B"
            test</code></p>
            ''',
            True
        )

    def test_custom_options(self):
        """Test options."""

        self.check_markdown(
            r'''
            ```test opt="A"
            test
            ```
            ''',
            r'''
            <div lang="test" class_name="class-test", option="A">test</div>
            ''',
            True
        )


class TestSuperFencesCustom2(util.MdCase):
    """Test Details."""

    extension = ['pymdownx.superfences']
    extension_configs = {
        'pymdownx.superfences': {
            'custom_fences': [
                {
                    'name': 'math',
                    'class': 'arithmatex',
                    'format': arithmatex.fence_mathjax_format
                }
            ]
        }
    }

    def test_arithmatex(self):
        """Test Arithmatex formatter without preview."""

        self.check_markdown(
            r'''
            ```math
            E(\mathbf{v}, \mathbf{h}) = -\sum_{i,j}w_{ij}v_i h_j - \sum_i b_i v_i - \sum_j c_j h_j
            ```
            ''',
            r'''
            <script type="math/tex; mode=display">
            E(\mathbf{v}, \mathbf{h}) = -\sum_{i,j}w_{ij}v_i h_j - \sum_i b_i v_i - \sum_j c_j h_j
            </script>
            ''',
            True
        )


class TestSuperFencesCustom3(util.MdCase):
    """Test Details."""

    extension = ['pymdownx.superfences']
    extension_configs = {
        'pymdownx.superfences': {
            'custom_fences': [
                {
                    'name': 'math',
                    'class': 'arithmatex',
                    'format': arithmatex.fence_mathjax_preview_format
                }
            ]
        }
    }

    def test_arithmatex_preview(self):
        """Test Arithmatex formatter with preview."""

        self.check_markdown(
            r'''
            ```math
            E(\mathbf{v}, \mathbf{h}) = -\sum_{i,j}w_{ij}v_i h_j - \sum_i b_i v_i - \sum_j c_j h_j
            ```
            ''',
            r'''
            <div>
            <div class="MathJax_Preview">
            E(\mathbf{v}, \mathbf{h}) = -\sum_{i,j}w_{ij}v_i h_j - \sum_i b_i v_i - \sum_j c_j h_j
            </div>
            <script type="math/tex; mode=display">
            E(\mathbf{v}, \mathbf{h}) = -\sum_{i,j}w_{ij}v_i h_j - \sum_i b_i v_i - \sum_j c_j h_j
            </script>
            </div>
            ''',
            True
        )


class TestSuperFencesCustom4(util.MdCase):
    """Test Details."""

    extension = ['pymdownx.superfences']
    extension_configs = {
        'pymdownx.superfences': {
            'custom_fences': [
                {
                    'name': 'math',
                    'class': 'arithmatex',
                    'format': arithmatex.fence_generic_format
                }
            ]
        }
    }

    def test_arithmatex_generic(self):
        """Test Arithmatex generic formatter."""

        self.check_markdown(
            r'''
            ```math
            E(\mathbf{v}, \mathbf{h}) = -\sum_{i,j}w_{ij}v_i h_j - \sum_i b_i v_i - \sum_j c_j h_j
            ```
            ''',
            r'''
            <div class="arithmatex">\[
            E(\mathbf{v}, \mathbf{h}) = -\sum_{i,j}w_{ij}v_i h_j - \sum_i b_i v_i - \sum_j c_j h_j
            \]</div>
            ''',
            True
        )


class TestSuperFencesCustom5(util.MdCase):
    """Test Details."""

    extension = ['pymdownx.superfences']
    extension_configs = {
        'pymdownx.superfences': {
            'custom_fences': [
                {
                    'name': '*',
                    'class': '',
                    'format': default_format
                },
                {
                    'name': 'math',
                    'class': 'arithmatex',
                    'format': arithmatex.fence_generic_format
                }
            ]
        }
    }

    def test_default_override(self):
        """Test default override."""

        self.check_markdown(
            r'''
            ```math
            E(\mathbf{v}, \mathbf{h}) = -\sum_{i,j}w_{ij}v_i h_j - \sum_i b_i v_i - \sum_j c_j h_j
            ```

            ```python
            test
            ```
            ''',
            r'''
            <div class="arithmatex">\[
            E(\mathbf{v}, \mathbf{h}) = -\sum_{i,j}w_{ij}v_i h_j - \sum_i b_i v_i - \sum_j c_j h_j
            \]</div>

            <p><custom lang="python" class_name="class-">test</custom></p>
            ''',
            True
        )
