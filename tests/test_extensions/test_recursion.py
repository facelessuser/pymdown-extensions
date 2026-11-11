"""Test that extensions that recursively parse content stop short of the recursion limit."""
import os
import sys
import tempfile
import unittest
import markdown
import xml.etree.ElementTree as etree
from markdown import util as mutil

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


class TestDeepTree(unittest.TestCase):
    """
    Test constructs that recurse do not start when the element tree is already deep.

    Lists and blocks nest without recursing, so the tree can be very deep while the call stack is shallow. The tree is
    walked recursively later, so a construct that only looked at the call stack would keep nesting on top of it, and
    the tree would become too deep. These need a limit that is large for the problem to be reachable, as the margin
    we stop short of the limit hides it when the limit is small.
    """

    def deep_tree(self, md, depth):
        """Make the parser think it has already built a tree of the given depth and return the deepest parent."""

        root = etree.Element('div')
        node = root
        for _ in range(depth):
            node = etree.SubElement(node, 'div')
        md.parser.root = root
        return node

    def check_processor(self, extension, name, block):
        """Check a processor starts normally, but not when the tree is deep and the call stack is not."""

        md = markdown.Markdown(extensions=[extension])
        processor = md.parser.blockprocessors[name]

        self.assertTrue(processor.test(self.deep_tree(md, 10), block))

        parent = self.deep_tree(md, sys.getrecursionlimit() - 100)
        # The call stack alone says there is plenty of room, which is the problem
        self.assertFalse(mutil.nearing_recursion_limit())
        self.assertFalse(processor.test(parent, block))

    def test_quotes(self):
        """Test quotes."""

        self.check_processor('pymdownx.quotes', 'quote', '> quote')

    def test_details(self):
        """Test legacy details."""

        self.check_processor('pymdownx.details', 'details', '??? note "Title"')

    def test_tabbed(self):
        """Test legacy tabbed."""

        self.check_processor('pymdownx.tabbed', 'tabbed', '=== "Title"')

    def check_after_lists(self, source, extensions, configs=None):
        """Convert content that builds a deep tree with lists, and then nests more, with a realistically large limit."""

        limit = sys.getrecursionlimit()
        sys.setrecursionlimit(stack_depth() + 800)
        try:
            markdown.Markdown(extensions=extensions, extension_configs=configs or {}).convert(source)
        except RecursionError:  # pragma: no cover
            self.fail('Recursion limit was reached')
        finally:
            sys.setrecursionlimit(limit)

    def test_quotes_after_lists(self):
        """Test quotes that start inside a list that is already deep."""

        self.check_after_lists(
            nest('- item', 320) + '    ' * 320 + '> ' * 300 + 'x\n',
            ['pymdownx.quotes', 'pymdownx.fancylists']
        )

    def test_tabbed_after_lists(self):
        """Test tabs that start inside a list that is already deep."""

        self.check_after_lists(
            nest('- item', 300) + ''.join(f'{"    " * (300 + i)}=== "Tab"\n\n' for i in range(150)) + 'x\n',
            ['pymdownx.tabbed', 'pymdownx.fancylists'],
            {'pymdownx.tabbed': {'alternate_style': True}}
        )
