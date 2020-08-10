"""Test cases for SuperFences."""
from .. import util
import unittest
import markdown
import pymdownx.arithmatex as arithmatex
import pymdownx.superfences as superfences
from pymdownx.util import PymdownxDeprecationWarning
import warnings


def custom_format(source, language, class_name, options, md, **kwargs):
    """Custom format."""

    return '<div lang="%s" class_name="class-%s", option="%s">%s</div>' % (language, class_name, options['opt'], source)


def default_format(source, language, class_name, options, md, **kwargs):
    """Default format."""

    return '<custom lang="%s" class_name="class-%s">%s</custom>' % (language, class_name, source)


def custom_exploder(source, language, class_name, options, md, **kwargs):
    """Broken format."""

    raise Exception('Boom!')


def custom_validater_exploder(language, inputs, options, attrs, md):
    """Broken validator."""

    raise Exception('Boom!')


def custom_validator(language, inputs, options, attrs, md):
    """Custom validator."""

    okay = True
    for k in inputs.keys():
        if k != 'opt':
            okay = False
            break
    if okay:
        if inputs['opt'] != "A":
            okay = False
        else:
            options['opt'] = inputs['opt']

    return okay


def custom_validator_legacy(language, options):
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


class TestSuperFencesClassesIds(util.MdCase):
    """Test classes and ids without attribute lists."""

    extension = ['pymdownx.superfences']
    extension_configs = {}

    def test_classes(self):
        """Test extra classes."""

        self.check_markdown(
            r'''
            ```{.python .more}
            import test
            ```
            ''',
            r'''
            <div class="more highlight"><pre><span></span><code><span class="kn">import</span> <span class="nn">test</span>
            </code></pre></div>
            ''',  # noqa: E501
            True
        )

    def test_id(self):
        """Test extra id."""

        self.check_markdown(
            r'''
            ```{.python #id}
            import test
            ```
            ''',
            r'''
            <div class="highlight"><pre><span></span><code><span class="kn">import</span> <span class="nn">test</span>
            </code></pre></div>
            ''',
            True
        )

    def test_attr(self):
        """Test extra attributes."""

        self.check_markdown(
            r'''
            ```{.python #id attr="test"}
            import test
            ```
            ''',
            r'''
            <div class="highlight"><pre><span></span><code><span class="kn">import</span> <span class="nn">test</span>
            </code></pre></div>
            ''',
            True
        )


class TestSuperFencesClassesIdsAttrList(util.MdCase):
    """Test fence ids and classes with attribute lists."""

    extension = ['pymdownx.superfences', 'markdown.extensions.attr_list']
    extension_configs = {}

    def test_classes(self):
        """Test extra classes."""

        self.check_markdown(
            r'''
            ```{.python .more}
            import test
            ```
            ''',
            r'''
            <div class="more highlight"><pre><span></span><code><span class="kn">import</span> <span class="nn">test</span>
            </code></pre></div>
            ''',  # noqa: E501
            True
        )

    def test_id(self):
        """Test extra id."""

        self.check_markdown(
            r'''
            ```{.python #id}
            import test
            ```
            ''',
            r'''
            <div class="highlight"><pre><span></span><code><span class="kn">import</span> <span class="nn">test</span>
            </code></pre></div>
            ''',
            True
        )

    def test_attr(self):
        """Test extra attributes."""

        self.check_markdown(
            r'''
            ```{.python #id attr="test"}
            import test
            ```
            ''',
            r'''
            <div class="highlight"><pre><span></span><code><span class="kn">import</span> <span class="nn">test</span>
            </code></pre></div>
            ''',
            True
        )


class TestSuperFencesClassesIdsAttrListNoPygments(util.MdCase):
    """Test fence ids and classes with attribute lists and with no Pygments."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences', 'markdown.extensions.attr_list']
    extension_configs = {
        "pymdownx.highlight": {
            "use_pygments": False
        }
    }

    def test_classes(self):
        """Test extra classes."""

        self.check_markdown(
            r'''
            ```{.python .more}
            import test
            ```
            ''',
            r'''
            <pre class="highlight"><code class="language-python more">import test</code></pre>
            ''',  # noqa: E501
            True
        )

    def test_id(self):
        """Test extra id."""

        self.check_markdown(
            r'''
            ```{.python #id}
            import test
            ```
            ''',
            r'''
            <pre class="highlight"><code id="id" class="language-python">import test</code></pre>
            ''',
            True
        )

    def test_attr(self):
        """Test extra attributes."""

        self.check_markdown(
            r'''
            ```{.python #id attr="test"}
            import test
            ```
            ''',
            r'''
            <pre class="highlight"><code id="id" class="language-python" attr="test">import test</code></pre>
            ''',
            True
        )


class TestSuperFencesClassesIdsAttrListNoPygmentsOnPre(util.MdCase):
    """Test fence ids and classes with attribute lists and with no Pygments and classes and ids on pre."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences', 'markdown.extensions.attr_list']
    extension_configs = {
        "pymdownx.highlight": {
            "use_pygments": False,
            "code_attr_on_pre": True
        }
    }

    def test_classes(self):
        """Test extra classes."""

        self.check_markdown(
            r'''
            ```{.python .more}
            import test
            ```
            ''',
            r'''
            <pre class="language-python highlight more"><code>import test</code></pre>
            ''',  # noqa: E501
            True
        )

    def test_id(self):
        """Test extra id."""

        self.check_markdown(
            r'''
            ```{.python #id}
            import test
            ```
            ''',
            r'''
            <pre id="id" class="language-python highlight"><code>import test</code></pre>
            ''',
            True
        )

    def test_attr(self):
        """Test extra attributes."""

        self.check_markdown(
            r'''
            ```{.python #id attr="test"}
            import test
            ```
            ''',
            r'''
            <pre id="id" class="language-python highlight" attr="test"><code>import test</code></pre>
            ''',
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

    def test_legacy_validator_code(self):
        """Test legacy validator."""

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
                                'format': custom_format,
                                'validator': custom_validator_legacy
                            }
                        ]
                    }
                }
            ).convert('```\ntest\n```\n')

            self.assertTrue(len(w) == 1)
            self.assertTrue(issubclass(w[-1].category, PymdownxDeprecationWarning))


class TestSuperFencesBad(util.MdCase):
    """Test bad options."""

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


class TestSuperFencesCustomLegacy(util.MdCase):
    """Test custom legacy validator."""

    extension = ['pymdownx.superfences']
    extension_configs = {
        'pymdownx.superfences': {
            'custom_fences': [
                {
                    'name': 'test',
                    'class': 'test',
                    'format': custom_format,
                    'validator': custom_validator_legacy
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


class TestSuperFencesCustom(util.MdCase):
    """Test custom validator and format."""

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
        """Test bad option."""

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
        """Test option with bad value."""

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

    def test_bad_option_no_value(self):
        """Test option with no value."""

        self.check_markdown(
            r'''
            ```test opt
            test
            ```
            ''',
            r'''
            <p><code>test opt
            test</code></p>
            ''',
            True
        )

    def test_custom_options(self):
        """Test option with correct value."""

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


class TestSuperFencesCustomDefaultValidator(util.MdCase):
    """Test custom format with default validator."""

    extension = ['pymdownx.superfences', 'markdown.extensions.attr_list']
    extension_configs = {
        'pymdownx.superfences': {
            'custom_fences': [
                {
                    'name': 'test',
                    'class': 'test',
                    'format': superfences.fence_div_format,
                    'validator': superfences.default_validator
                }
            ]
        }
    }

    def test_default_validator(self):
        """Test default validator."""

        self.check_markdown(
            r'''
            ```{.test opt="A"}
            test
            ```
            ''',
            r'''
            <div class="test" opt="A">test</div>
            ''',
            True
        )


class TestSuperFencesCustomArithmatex(util.MdCase):
    """Test custom Arithmatex format."""

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


class TestSuperFencesCustomArithmatexPreview(util.MdCase):
    """Test custom Arithmatex preview format."""

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


class TestSuperFencesCustomArithmatexGeneric(util.MdCase):
    """Test custom Arithmatex generic format."""

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


class TestSuperFencesCustomDefault(util.MdCase):
    """Test overriding the default format."""

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


class TestSuperFencesCustomBroken(util.MdCase):
    """Test custom formatter that is broken."""

    extension = ['pymdownx.superfences']
    extension_configs = {
        'pymdownx.superfences': {
            'custom_fences': [
                {
                    'name': 'test',
                    'class': 'test',
                    'format': custom_exploder,
                }
            ]
        }
    }

    def test_broken(self):
        """Test broken fence."""

        self.check_markdown(
            '''
            ```test
            doesn't matter
            ```
            ''',
            '''
            <p><code>test
            doesn't matter</code></p>
            ''',
            True
        )


class TestSuperFencesCustomValidatorBroken(util.MdCase):
    """Test custom legacy validator that is broken."""

    extension = ['pymdownx.superfences']
    extension_configs = {
        'pymdownx.superfences': {
            'custom_fences': [
                {
                    'name': 'test',
                    'class': 'test',
                    'format': custom_format,
                    'validator': custom_validater_exploder
                }
            ]
        }
    }

    def test_broken(self):
        """Test broken fence."""

        self.check_markdown(
            '''
            ```test
            doesn't matter
            ```
            ''',
            '''
            <div class="highlight"><pre><span></span><code>doesn&#39;t matter
            </code></pre></div>
            ''',
            True
        )

    def test_broken_brace(self):
        """Test broken fence."""

        self.check_markdown(
            '''
            ```{.test}
            doesn't matter
            ```
            ''',
            '''
            <div class="highlight"><pre><span></span><code>doesn&#39;t matter
            </code></pre></div>
            ''',
            True
        )
