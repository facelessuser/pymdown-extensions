"""Test that extensions that recursively parse content stop short of the recursion limit."""
import os
import sys
import tempfile
import unittest
import markdown

# Number of nested levels to generate. Far more than the headroom we give the interpreter below.
LEVELS = 400
# Headroom above the current stack depth. This keeps the tests fast while still being deep enough to overflow
# if an extension does not stop short of the limit.
HEADROOM = 250


def stack_depth():
    """Get the current stack depth."""

    depth = 0
    frame = sys._getframe(1)
    while frame:
        depth += 1
        frame = frame.f_back
    return depth


def nest(opener, levels=LEVELS, indent='    '):
    """Generate content nested via indentation."""

    return ''.join(f'{indent * i}{opener}\n\n' for i in range(levels)) + f'{indent * levels}x\n'


def fences(name, levels=LEVELS):
    """Generate nested generic blocks (inner blocks use a longer fence)."""

    return (
        ''.join(f'{"/" * (3 + i)} {name}\n\n' for i in range(levels)) +
        'x\n\n' +
        ''.join(f'{"/" * (3 + i)}\n\n' for i in reversed(range(levels)))
    )


class TestRecursion(unittest.TestCase):
    """Test deeply nested content does not raise a `RecursionError`."""

    def setUp(self):
        """Lower the recursion limit so we do not need huge documents to hit it."""

        self.limit = sys.getrecursionlimit()
        sys.setrecursionlimit(stack_depth() + HEADROOM)

    def tearDown(self):
        """Restore the recursion limit."""

        sys.setrecursionlimit(self.limit)

    def check(self, source, extensions, configs=None, keeps_content=True):
        """Convert the source and make sure we gracefully stop short of the recursion limit."""

        md = markdown.Markdown(extensions=extensions, extension_configs=configs or {})
        try:
            html = md.convert(source)
        except RecursionError:  # pragma: no cover
            self.fail('Recursion limit was reached')

        # Content is not lost, we just stop treating it specially once we are too deep.
        if keeps_content:
            self.assertIn('x', html)

    def test_quotes(self):
        """Test quotes."""

        self.check('> ' * LEVELS + 'x', ['pymdownx.quotes'])

    def test_quotes_callouts(self):
        """Test nested quotes with callouts."""

        self.check(
            ''.join(f'{"> " * i}[!note] Title\n' for i in range(1, LEVELS)) + '> ' * LEVELS + 'x',
            ['pymdownx.quotes'],
            {'pymdownx.quotes': {'callouts': True}}
        )

    def test_quotes_after_deep_lists(self):
        """Test quotes that start after a list has already built a deep tree."""

        self.check(
            nest('- item', LEVELS // 4) + '    ' * (LEVELS // 4) + '> ' * LEVELS + 'x\n',
            ['pymdownx.quotes', 'pymdownx.fancylists']
        )

    def test_details(self):
        """Test legacy details."""

        self.check(nest('??? note "Title"'), ['pymdownx.details'])

    def test_tabbed(self):
        """Test legacy tabbed."""

        self.check(nest('=== "Title"'), ['pymdownx.tabbed'])

    def test_tabbed_alternate(self):
        """Test legacy tabbed with alternate style."""

        self.check(nest('=== "Title"'), ['pymdownx.tabbed'], {'pymdownx.tabbed': {'alternate_style': True}})

    def test_fancylists_ordered(self):
        """Test fancy ordered lists."""

        self.check(nest('1. item'), ['pymdownx.fancylists'])

    def test_fancylists_unordered(self):
        """Test fancy unordered lists."""

        self.check(nest('- item'), ['pymdownx.fancylists'])

    def test_blocks_admonition(self):
        """Test admonition blocks."""

        self.check(fences('admonition'), ['pymdownx.blocks.admonition'])

    def test_blocks_details(self):
        """Test details blocks."""

        self.check(fences('details'), ['pymdownx.blocks.details'])

    def test_blocks_tab(self):
        """Test tab blocks."""

        self.check(fences('tab | Title'), ['pymdownx.blocks.tab'])

    def test_blocks_caption(self):
        """Test caption blocks."""

        self.check(fences('figure-caption'), ['pymdownx.blocks.caption'])

    def test_snippets(self):
        """Test snippets nested through many distinct files."""

        with tempfile.TemporaryDirectory() as d:
            for i in range(LEVELS):
                with open(os.path.join(d, f'f{i}.md'), 'w', encoding='utf-8') as f:
                    f.write(f'-8<- "f{i + 1}.md"\n' if i < LEVELS - 1 else 'x\n')

            # Snippets deeper than the limit are skipped, just like those that would cause a cycle.
            self.check(
                '-8<- "f0.md"\n',
                ['pymdownx.snippets'],
                {'pymdownx.snippets': {'base_path': [d]}},
                keeps_content=False
            )

    def test_normal_nesting_unaffected(self):
        """Test that reasonable nesting is still processed normally."""

        md = markdown.Markdown(extensions=['pymdownx.details', 'pymdownx.tabbed', 'pymdownx.fancylists'])
        html = md.convert('1. a\n\n    ??? note "Title"\n\n        === "Tab"\n\n            x\n')
        self.assertIn('<details class="note">', html)
        self.assertIn('<div class="tabbed-set', html)
        self.assertIn('<ol', html)
