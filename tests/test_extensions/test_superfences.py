"""Test cases for SuperFences."""
from __future__ import unicode_literals
from .. import util
import pymdownx.arithmatex as arithmatex


def custom_format(source, language, class_name, options, md):
    """Custom format."""

    return '<div lang="%s" class_name="class-%s", option="%s">%s</div>' % (language, class_name, options['opt'], source)


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
