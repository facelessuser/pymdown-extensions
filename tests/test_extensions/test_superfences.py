"""Test cases for SuperFences."""
from .. import util
import unittest
import markdown
import pymdownx.arithmatex as arithmatex
from pymdownx.util import PymdownxDeprecationWarning
import warnings


def custom_format(source, language, class_name, md, options=None, classes=None, value_id='', **kwargs):
    """Custom format."""

    return '<div lang="%s" class_name="class-%s", option="%s">%s</div>' % (language, class_name, options['opt'], source)


def default_format(source, language, class_name, md, options=None, classes=None, value_id='', **kwargs):
    """Default format."""

    return '<custom lang="%s" class_name="class-%s">%s</custom>' % (language, class_name, source)


def custom_validator(language, md, values, options, attrs):
    """Custom validator."""

    okay = True
    for k in values.keys():
        if k != 'opt':
            okay = False
            break
    if okay:
        if values['opt'] != "A":
            okay = False
        else:
            options['opt'] = values['opt']

    return okay


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
