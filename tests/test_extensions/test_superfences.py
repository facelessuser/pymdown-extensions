"""Test cases for SuperFences."""
from .. import util
import pymdownx.arithmatex as arithmatex
import pymdownx.superfences as superfences
from pymdownx.superfences import SuperFencesException
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


def custom_exploder_fail(source, language, class_name, options, md, **kwargs):
    """Broken format."""

    raise SuperFencesException('Boom!')


def custom_validator_exploder(language, inputs, options, attrs, md):
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


def custom_validator_except(language, inputs, options, attrs, md):
    """Custom validator."""

    okay = True
    try:
        for k in inputs.keys():
            if k != 'opt':
                okay = False
                break
        if okay:
            if inputs['opt'] != "A":
                okay = False
            else:
                options['opt'] = inputs['opt']
    except KeyError as e:
        raise SuperFencesException from e

    return okay


class TestHighlightTitle(util.MdCase):
    """Test title cases."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences']

    def test_title(self):
        """Test auto title."""

        self.check_markdown(
            r'''
            ```pycon title="My title"
            >>> import test
            ```
            ''',
            r'''
            <div class="highlight"><span class="filename">My title</span><pre><span></span><code><span class="gp">&gt;&gt;&gt; </span><span class="kn">import</span> <span class="nn">test</span>
            </code></pre></div>
            ''',  # noqa: E501
            True
        )

    def test_title_table(self):
        """Test auto title."""

        self.check_markdown(
            r'''
            ```pycon title="My title" linenums="1"
            >>> import test
            ```
            ''',
            r'''
            <div class="highlight"><table class="highlighttable"><tr><th colspan="2" class="filename"><span class="filename">My title</span></th></tr><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal">1</span></pre></div></td><td class="code"><div><pre><span></span><code><span class="gp">&gt;&gt;&gt; </span><span class="kn">import</span> <span class="nn">test</span>
            </code></pre></div></td></tr></table></div>
            ''',  # noqa: E501
            True
        )


class TestHighlightAutoTitleOverride(util.MdCase):
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

    def test_auto_tile(self):
        """Test auto title."""

        self.check_markdown(
            r'''
            ```{.python title="My Title"}
            import test
            ```
            ''',
            r'''
            <div class="highlight"><span class="filename">My Title</span><pre><span></span><code><span class="kn">import</span> <span class="nn">test</span>
            </code></pre></div>
            ''',  # noqa: E501
            True
        )

    def test_auto_tile_map(self):
        """Test auto title."""

        self.check_markdown(
            r'''
            ```{.pycon title="My Title"}
            >>> import test
            ```
            ''',
            r'''
            <div class="highlight"><span class="filename">My Title</span><pre><span></span><code><span class="gp">&gt;&gt;&gt; </span><span class="kn">import</span> <span class="nn">test</span>
            </code></pre></div>
            ''',  # noqa: E501
            True
        )


class TestHighlightLineWrapsInline(util.MdCase):
    """Test highlight line wraps."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences']
    extension_configs = {
        'pymdownx.highlight': {
            'line_spans': '__my_span',
            'linenums_style': 'inline'
        }
    }

    def test_linespans(self):
        """Test wrapping a line in line spans."""

        self.check_markdown(
            r'''
            ```python linenums="2"
            import test
            ```
            ''',
            r'''
            <div class="highlight"><pre><span></span><code><span id="__my_span-0-2"><span class="linenos">2</span><span class="kn">import</span> <span class="nn">test</span>
            </span></code></pre></div>
            ''',  # noqa: E501
            True
        )


class TestHighlightLineWrapsPymdownxInline(util.MdCase):
    """Test highlight line wraps."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences']
    extension_configs = {
        'pymdownx.highlight': {
            'line_spans': '__my_span',
            'linenums_style': 'pymdownx-inline'
        }
    }

    def test_linespans(self):
        """Test wrapping a line in line spans."""

        self.check_markdown(
            r'''
            ```python linenums="2"
            import test
            ```
            ''',
            r'''
            <div class="highlight"><pre><span></span><code><span id="__my_span-0-2"><span class="linenos" data-linenos="2 "></span><span class="kn">import</span> <span class="nn">test</span>
            </span></code></pre></div>
            ''',  # noqa: E501
            True
        )


class TestHighlightLineWrapsPymdownsTable(util.MdCase):
    """Test highlight line wraps."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences']
    extension_configs = {
        'pymdownx.highlight': {
            'line_spans': '__my_span',
            'linenums_style': 'table'
        }
    }

    def test_linespans(self):
        """Test wrapping a line in line spans."""

        self.check_markdown(
            r'''
            ```python linenums="2"
            import test
            ```
            ''',
            r'''
            <div class="highlight"><table class="highlighttable"><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal">2</span></pre></div></td><td class="code"><div><pre><span></span><code><span id="__my_span-0-2"><span class="kn">import</span> <span class="nn">test</span>
            </span></code></pre></div></td></tr></table></div>
            ''',  # noqa: E501
            True
        )


class TestHighlightLineAnchorsInline(util.MdCase):
    """Test highlight line wraps."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences']
    extension_configs = {
        'pymdownx.highlight': {
            'line_anchors': '__my_span',
            'linenums_style': 'inline'
        }
    }

    def test_linespans(self):
        """Test wrapping a line in line spans."""

        self.check_markdown(
            r'''
            ```python linenums="2"
            import test
            ```
            ''',
            r'''
            <div class="highlight"><pre><span></span><code><a id="__my_span-0-2" name="__my_span-0-2"></a><span class="linenos">2</span><span class="kn">import</span> <span class="nn">test</span>
            </code></pre></div>
            ''',  # noqa: E501
            True
        )


class TestHighlightLineAnchorsPymdownxInline(util.MdCase):
    """Test highlight line wraps."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences']
    extension_configs = {
        'pymdownx.highlight': {
            'line_anchors': '__my_span',
            'linenums_style': 'pymdownx-inline'
        }
    }

    def test_linespans(self):
        """Test wrapping a line in line spans."""

        self.check_markdown(
            r'''
            ```python linenums="2"
            import test
            ```
            ''',
            r'''
            <div class="highlight"><pre><span></span><code><a id="__my_span-0-2" name="__my_span-0-2"></a><span class="linenos" data-linenos="2 "></span><span class="kn">import</span> <span class="nn">test</span>
            </code></pre></div>
            ''',  # noqa: E501
            True
        )


class TestHighlightLineAnchorsPymdownsTable(util.MdCase):
    """Test highlight line wraps."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences']
    extension_configs = {
        'pymdownx.highlight': {
            'line_anchors': '__my_span',
            'linenums_style': 'table'
        }
    }

    def test_linespans(self):
        """Test wrapping a line in line spans."""

        self.check_markdown(
            r'''
            ```python linenums="2"
            import test
            ```
            ''',
            r'''
            <div class="highlight"><table class="highlighttable"><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal">2</span></pre></div></td><td class="code"><div><pre><span></span><code><a id="__my_span-0-2" name="__my_span-0-2"></a><span class="kn">import</span> <span class="nn">test</span>
            </code></pre></div></td></tr></table></div>
            ''',  # noqa: E501
            True
        )


class TestHighlightAnchorLinenumInline(util.MdCase):
    """Test highlight line wraps."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences']
    extension_configs = {
        'pymdownx.highlight': {
            'anchor_linenums': True,
            'linenums_style': 'inline'
        }
    }

    def test_linespans(self):
        """Test wrapping a line in line spans."""

        self.check_markdown(
            r'''
            ```python linenums="2"
            import test
            ```
            ''',
            r'''
            <div class="highlight"><pre><span></span><code><a id="__codelineno-0-2" name="__codelineno-0-2"></a><a href="#__codelineno-0-2"><span class="linenos">2</span></a><span class="kn">import</span> <span class="nn">test</span>
            </code></pre></div>
            ''',  # noqa: E501
            True
        )


class TestHighlightAnchorLinenumsPymdownxInline(util.MdCase):
    """Test highlight line wraps."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences']
    extension_configs = {
        'pymdownx.highlight': {
            'anchor_linenums': True,
            'linenums_style': 'pymdownx-inline'
        }
    }

    def test_linespans(self):
        """Test wrapping a line in line spans."""

        self.check_markdown(
            r'''
            ```python linenums="2"
            import test
            ```
            ''',
            r'''
            <div class="highlight"><pre><span></span><code><a id="__codelineno-0-2" name="__codelineno-0-2"></a><a href="#__codelineno-0-2"><span class="linenos" data-linenos="2 "></span></a><span class="kn">import</span> <span class="nn">test</span>
            </code></pre></div>
            ''',  # noqa: E501
            True
        )


class TestHighlightAnchorLinenumsPymdownsTable(util.MdCase):
    """Test highlight line wraps."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences']
    extension_configs = {
        'pymdownx.highlight': {
            'anchor_linenums': True,
            'linenums_style': 'table'
        }
    }

    def test_linespans(self):
        """Test wrapping a line in line spans."""

        self.check_markdown(
            r'''
            ```python linenums="2"
            import test
            ```
            ''',
            r'''
            <div class="highlight"><table class="highlighttable"><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal"><a href="#__codelineno-0-2">2</a></span></pre></div></td><td class="code"><div><pre><span></span><code><a id="__codelineno-0-2" name="__codelineno-0-2"></a><span class="kn">import</span> <span class="nn">test</span>
            </code></pre></div></td></tr></table></div>
            ''',  # noqa: E501
            True
        )


class TestHighlightAnchorLinenumNameInline(util.MdCase):
    """Test highlight line wraps."""

    extension = ['pymdownx.highlight', 'pymdownx.superfences']
    extension_configs = {
        'pymdownx.highlight': {
            'anchor_linenums': True,
            'line_anchors': '__my_span',
            'linenums_style': 'inline'
        }
    }

    def test_linespans(self):
        """Test wrapping a line in line spans."""

        self.check_markdown(
            r'''
            ```python linenums="2"
            import test
            ```
            ''',
            r'''
            <div class="highlight"><pre><span></span><code><a id="__my_span-0-2" name="__my_span-0-2"></a><a href="#__my_span-0-2"><span class="linenos">2</span></a><span class="kn">import</span> <span class="nn">test</span>
            </code></pre></div>
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
            <div id="id" class="highlight"><pre><span></span><code><span class="kn">import</span> <span class="nn">test</span>
            </code></pre></div>
            ''',  # noqa: E501
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
            <div id="id" class="highlight"><pre><span></span><code><span class="kn">import</span> <span class="nn">test</span>
            </code></pre></div>
            ''',  # noqa: E501
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
            <div id="id" class="highlight"><pre><span></span><code><span class="kn">import</span> <span class="nn">test</span>
            </code></pre></div>
            ''',  # noqa: E501
            True
        )

    def test_bad_attr(self):
        """Test bad attribute."""

        self.check_markdown(
            r'''
            ```{.python #id attr="test"}
            import test
            ```
            ''',
            r'''
            <div id="id" class="highlight"><pre><span></span><code><span class="kn">import</span> <span class="nn">test</span>
            </code></pre></div>
            ''',  # noqa: E501
            True
        )

    def test_data_attr(self):
        """Test data attributes."""

        self.check_markdown(
            r'''
            ```{.python #id data-attr="test"}
            import test
            ```
            ''',
            r'''
            <div id="id" class="highlight" data-attr="test"><pre><span></span><code><span class="kn">import</span> <span class="nn">test</span>
            </code></pre></div>
            ''',  # noqa: E501
            True
        )

    def test_data_attr_linenums(self):
        """Test data attributes with line numbers enabled."""

        self.check_markdown(
            r'''
            ```{.python #id data-attr="test" linenums="1"}
            import test
            ```
            ''',
            r'''
            <div id="id" class="highlight" data-attr="test"><table class="highlighttable"><tr><td class="linenos"><div class="linenodiv"><pre><span></span><span class="normal">1</span></pre></div></td><td class="code"><div><pre><span></span><code><span class="kn">import</span> <span class="nn">test</span>
            </code></pre></div></td></tr></table></div>
            ''',  # noqa: E501
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

    def test_failure(self):
        """
        Test failure of custom fence.

        Fence failed, gracefully continue with any other fences that can capture this.
        """

        self.check_markdown(
            r'''
            ```test
            test
            ```
            ''',
            r'''
            <div class="highlight"><pre><span></span><code>test
            </code></pre></div>
            ''',
            True
        )

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


class TestSuperFencesCustomException(util.MdCase):
    """Test custom validator and format."""

    extension = ['pymdownx.superfences']
    extension_configs = {
        'pymdownx.superfences': {
            'custom_fences': [
                {
                    'name': 'test',
                    'class': 'test',
                    'format': custom_format,
                    'validator': custom_validator_except
                }
            ]
        }
    }

    def test_custom_fail_exception(self):
        """Test custom fences forced exception."""

        with self.assertRaises(SuperFencesException):
            self.check_markdown(
                r'''
                ```test
                test
                ```
                ''',
                '',
                True
            )


class TestSuperFencesCustomExceptionAttrList(util.MdCase):
    """Test custom validator and format with attribute lists."""

    extension = ['pymdownx.superfences', 'attr_list']
    extension_configs = {
        'pymdownx.superfences': {
            'custom_fences': [
                {
                    'name': 'test',
                    'class': 'test',
                    'format': custom_format,
                    'validator': custom_validator_except
                }
            ]
        }
    }

    def test_custom_fail_exception(self):
        """Test custom fences forced exception with attribute lists."""

        with self.assertRaises(SuperFencesException):
            self.check_markdown(
                r'''
                ```{.test}
                test
                ```
                ''',
                '',
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
                    'format': arithmatex.arithmatex_fenced_format(mode="mathjax")
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
            <div class="arithmatex">
            <script type="math/tex; mode=display">
            E(\mathbf{v}, \mathbf{h}) = -\sum_{i,j}w_{ij}v_i h_j - \sum_i b_i v_i - \sum_j c_j h_j
            </script>
            </div>
            ''',
            True
        )


class TestSuperFencesCustomLegacyArithmatex(util.MdCase):
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

    def test_legacy_arithmatex(self):
        """Test Arithmatex formatter without preview."""

        with warnings.catch_warnings(record=True) as w:
            self.check_markdown(
                r'''
                ```math
                E(\mathbf{v}, \mathbf{h}) = -\sum_{i,j}w_{ij}v_i h_j - \sum_i b_i v_i - \sum_j c_j h_j
                ```
                ''',
                r'''
                <div class="arithmatex">
                <script type="math/tex; mode=display">
                E(\mathbf{v}, \mathbf{h}) = -\sum_{i,j}w_{ij}v_i h_j - \sum_i b_i v_i - \sum_j c_j h_j
                </script>
                </div>
                ''',
                True
            )

            self.assertTrue(len(w) == 1)
            self.assertTrue(issubclass(w[-1].category, DeprecationWarning))


class TestSuperFencesCustomArithmatexPreview(util.MdCase):
    """Test custom Arithmatex preview format."""

    extension = ['pymdownx.superfences']
    extension_configs = {
        'pymdownx.superfences': {
            'custom_fences': [
                {
                    'name': 'math',
                    'class': 'arithmatex',
                    'format': arithmatex.arithmatex_fenced_format(mode='mathjax', preview=True)
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
            <div class="arithmatex">
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


class TestSuperFencesCustomLegacyArithmatexPreview(util.MdCase):
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

    def test_legacy_arithmatex_preview(self):
        """Test Arithmatex formatter with preview."""

        with warnings.catch_warnings(record=True) as w:
            self.check_markdown(
                r'''
                ```math
                E(\mathbf{v}, \mathbf{h}) = -\sum_{i,j}w_{ij}v_i h_j - \sum_i b_i v_i - \sum_j c_j h_j
                ```
                ''',
                r'''
                <div class="arithmatex">
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

            self.assertTrue(len(w) == 1)
            self.assertTrue(issubclass(w[-1].category, DeprecationWarning))


class TestSuperFencesCustomArithmatexGeneric(util.MdCase):
    """Test custom Arithmatex generic format."""

    extension = ['pymdownx.superfences']
    extension_configs = {
        'pymdownx.superfences': {
            'custom_fences': [
                {
                    'name': 'math',
                    'class': 'arithmatex',
                    'format': arithmatex.arithmatex_fenced_format(mode="generic")
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


class TestSuperFencesCustomLegacyArithmatexGeneric(util.MdCase):
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

    def test_legacy_arithmatex_generic(self):
        """Test Arithmatex generic formatter."""

        with warnings.catch_warnings(record=True) as w:
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

            self.assertTrue(len(w) == 1)
            self.assertTrue(issubclass(w[-1].category, DeprecationWarning))


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
                    'format': arithmatex.arithmatex_fenced_format(mode="generic")
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

    def test_broken_blockquote(self):
        """Test broken fence in a blockquote."""

        self.check_markdown(
            '''
            > ```test
            > doesn't matter
            > ```
            ''',
            '''
            <blockquote>
            <p><code>test
            doesn't matter</code></p>
            </blockquote>
            ''',
            True
        )


class TestSuperFencesCustomBrokenFail(util.MdCase):
    """Test custom formatter that is broken and causes a failure."""

    extension = ['pymdownx.superfences']
    extension_configs = {
        'pymdownx.superfences': {
            'custom_fences': [
                {
                    'name': 'test',
                    'class': 'test',
                    'format': custom_exploder_fail,
                }
            ]
        }
    }

    def test_custom_fail_exception(self):
        """Test custom fences forced exception."""

        with self.assertRaises(SuperFencesException):
            self.check_markdown(
                r'''
                ```test
                test
                ```
                ''',
                '',
                True
            )

    def test_custom_fail_exception_blockquote(self):
        """Test custom fences forced exception in a block quote."""

        with self.assertRaises(SuperFencesException):
            self.check_markdown(
                r'''
                > ```test
                > test
                > ```
                ''',
                '',
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
                    'validator': custom_validator_exploder
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
