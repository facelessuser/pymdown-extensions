"""Test cases for SuperFences."""
from __future__ import unicode_literals
from .. import util


def custom_format(source, language, class_name, options):
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


class TestSuperFencesCustom(util.MdCase):
    """Test Details."""

    extension = ['pymdownx.superfences']
    extension_configs = {
        'pymdownx.superfences': {
            'custom_fences': [
                {'name': 'test', 'class': 'test', 'format': custom_format, 'validator': custom_validator}
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
