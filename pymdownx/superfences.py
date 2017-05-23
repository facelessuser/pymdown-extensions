"""
Superfences.

pymdownx.superfences
Neseted Fenced Code Blocks

This is a modification of the original Fenced Code Extension.
Algorithm has been rewritten to allow for fenced blocks in blockquotes,
lists, etc.  And also , allow for special UML fences like 'flow' for flowcharts
and `sequence` for sequence diagrams.

Modified: 2014 - 2017 Isaac Muse <isaacmuse@gmail.com>
---

Fenced Code Extension for Python Markdown
=========================================

This extension adds Fenced Code Blocks to Python-Markdown.

See <https://pythonhosted.org/Markdown/extensions/fenced_code_blocks.html>
for documentation.

Original code Copyright 2007-2008 [Waylan Limberg](http://achinghead.com/).


All changes Copyright 2008-2014 The Python Markdown Project

License: [BSD](http://www.opensource.org/licenses/bsd-license.php)
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.blockprocessors import CodeBlockProcessor
from markdown import util as md_util
from . import highlight as hl
from .util import PymdownxDeprecationWarning
import warnings
import re

NESTED_FENCE_START = r'''(?x)
(?:^(?P<ws>[\> ]*)(?P<fence>~{3,}|`{3,}))[ ]*                         # Fence opening
(\{?                                                                  # Language opening
\.?(?P<lang>[\w#.+-]*))?[ ]*                                          # Language
(?:
(hl_lines=(?P<quot>"|')(?P<hl_lines>\d+(?:[ ]+\d+)*)(?P=quot))?[ ]*|  # highlight lines
(linenums=(?P<quot2>"|')                                              # Line numbers
    (?P<linestart>[\d]+)                                              #   Line number start
    (?:[ ]+(?P<linestep>[\d]+))?                                      #   Line step
    (?:[ ]+(?P<linespecial>[\d]+))?                                   #   Line special
(?P=quot2))?[ ]*
){,2}
}?[ ]*$                                                               # Language closing
'''
NESTED_FENCE_END = r'^[\> ]*%s[ ]*$'

WS = r'^([\> ]{0,%d})(.*)'

RE_FENCE = re.compile(
    r'''(?xsm)
    (?P<fence>^(?:~{3,}|`{3,}))[ ]*                                       # Opening
    (\{?\.?(?P<lang>[\w#.+-]*))?[ ]*                                      # Optional {, and lang
    (?:
    (hl_lines=(?P<quot>"|')(?P<hl_lines>\d+(?:[ ]+\d+)*)(?P=quot))?[ ]*|  # Optional highlight lines option
    (linenums=(?P<quot2>"|')                                              # Line numbers
        (?P<linestart>[\d]+)                                              #   Line number start
        (?:[ ]+(?P<linestep>[\d]+))?                                      #   Line step
        (?:[ ]+(?P<linespecial>[\d]+))?                                   #   Line special
    (?P=quot2))?[ ]*
    ){,2}
    }?[ ]*\n                                                              # Optional closing }
    (?P<code>.*?)(?<=\n)                                                  # Code
    (?P=fence)[ ]*$                                                       # Closing
    '''
)


def _escape(txt):
    """Basic html escaping."""

    txt = txt.replace('&', '&amp;')
    txt = txt.replace('<', '&lt;')
    txt = txt.replace('>', '&gt;')
    txt = txt.replace('"', '&quot;')
    return txt


class CodeStash(object):
    """
    Stash code for later retrieval.

    Store original fenced code here in case we were
    too greedy and need to restore in an indented code
    block.
    """

    def __init__(self):
        """Initialize."""

        self.stash = {}

    def __len__(self):  # pragma: no cover
        """Length of stash."""

        return len(self.stash)

    def get(self, key, default=None):
        """Get the code from the key."""

        code = self.stash.get(key, default)
        return code

    def remove(self, key):
        """Remove the stashed code."""

        del self.stash[key]

    def store(self, key, code, indent_level):
        """Store the code in the stash."""

        self.stash[key] = (code, indent_level)

    def clear_stash(self):
        """Clear the stash."""

        self.stash = {}


def fence_code_format(source, language, css_class):
    """Format source as code blocks."""

    return '<pre class="%s"><code>%s</code></pre>' % (css_class, _escape(source))


def fence_div_format(source, language, css_class):
    """Format source as div."""

    return '<div class="%s">%s</div>' % (css_class, _escape(source))


class SuperFencesCodeExtension(Extension):
    """Superfences code block extension."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.superfences = []
        self.config = {
            'disable_indented_code_blocks': [False, "Disable indented code blocks - Default: False"],
            'uml_flow': [True, "Enable flowcharts - Default: True"],
            'uml_sequence': [True, "Enable sequence diagrams - Default: True"],
            'custom_fences': [
                [
                    {'name': 'flow', 'class': 'uml-flowchart'},
                    {'name': 'sequence', 'class': 'uml-sequence-diagram'}
                ],
                'Specify custom fences. Default: See documentation.'
            ],
            'highlight_code': [True, "Highlight code - Default: True"],
            'use_codehilite_settings': [
                None,
                "Deprecatd and does nothing. "
                "- Default: None"
            ],
            'css_class': [
                '',
                "Set class name for wrapper element. The default of CodeHilite or Highlight will be used"
                "if nothing is set. - "
                "Default: ''"
            ]
        }
        super(SuperFencesCodeExtension, self).__init__(*args, **kwargs)

    def extend_super_fences(self, name, formatter):
        """Extend superfences with the given name, language, and formatter."""

        self.superfences.append(
            {
                "name": name,
                "test": lambda l, language=name: language == l,
                "formatter": formatter
            }
        )

    def extendMarkdown(self, md, md_globals):
        """Add FencedBlockPreprocessor to the Markdown instance."""

        # Not super yet, so let's make it super
        md.registerExtension(self)
        config = self.getConfigs()

        # Default fenced blocks
        self.superfences.insert(
            0,
            {
                "name": "superfences",
                "test": lambda language: True,
                "formatter": None
            }
        )

        if config.get('use_codehilite_settings'):  # pragma: no coverage
            warnings.warn(
                "'use_codehilite_settings' is deprecated and does nothing.\n"
                "\nCodeHilite settings will only be used if CodeHilite is configured\n"
                " and 'pymdownx.highlight' is not configured.\n"
                "Please discontinue use of this setting as it will be removed in the future.",
                PymdownxDeprecationWarning
            )

        # UML blocks
        custom_fences = config.get('custom_fences', [])
        for custom in custom_fences:
            name = custom.get('name')
            class_name = custom.get('class')
            fence_format = custom.get('format', fence_code_format)
            if name is not None and class_name is not None:
                self.extend_super_fences(
                    name,
                    lambda s, l, c=class_name, f=fence_format: f(s, l, c)
                )

        self.markdown = md
        self.patch_fenced_rule()
        for entry in self.superfences:
            entry["stash"] = CodeStash()

    def patch_fenced_rule(self):
        """
        Patch Python Markdown with our own fenced block extension.

        We don't attempt to protect against a user loading the `fenced_code` extension with this.
        Most likely they will have issues, but they shouldn't have loaded them together in the first place :).
        """

        config = self.getConfigs()
        fenced = SuperFencesBlockPreprocessor(self.markdown)
        indented_code = SuperFencesCodeBlockProcessor(self)
        fenced.config = config
        fenced.extension = self
        indented_code.config = config
        indented_code.markdown = self.markdown
        indented_code.extension = self
        self.superfences[0]["formatter"] = fenced.highlight
        self.markdown.parser.blockprocessors['code'] = indented_code
        self.markdown.preprocessors.add('fenced_code_block', fenced, ">normalize_whitespace")

    def reset(self):
        """Clear the stash."""

        for entry in self.superfences:
            entry["stash"].clear_stash()


class SuperFencesBlockPreprocessor(Preprocessor):
    """
    Preprocessor to find fenced code blocks.

    Because this is done as a preprocessor, it might be too greedy.
    We will stash the blocks code and restore if we mistakenly processed
    text from an indented code block.
    """

    fence_start = re.compile(NESTED_FENCE_START)
    CODE_WRAP = '<pre%s><code%s>%s</code></pre>'

    def __init__(self, md):
        """Initialize."""

        super(SuperFencesBlockPreprocessor, self).__init__(md)
        self.markdown = md
        self.checked_hl_settings = False
        self.codehilite_conf = {}

    def rebuild_block(self, lines):
        """Deindent the fenced block lines."""

        return '\n'.join([line[self.ws_len:] for line in lines])

    def get_hl_settings(self):
        """Check for code hilite extension to get its config."""

        if not self.checked_hl_settings:
            self.checked_hl_settings = True
            self.highlight_code = self.config['highlight_code']

            config = hl.get_hl_settings(self.markdown)
            css_class = self.config['css_class']
            self.css_class = css_class if css_class else config['css_class']

            self.extend_pygments_lang = config.get('extend_pygments_lang', None)
            self.guess_lang = config['guess_lang']
            self.pygments_style = config['pygments_style']
            self.use_pygments = config['use_pygments']
            self.noclasses = config['noclasses']
            self.linenums = config['linenums']

    def clear(self):
        """Reset the class variables."""

        self.ws = None
        self.ws_len = 0
        self.fence = None
        self.lang = None
        self.hl_lines = None
        self.linestart = None
        self.linestep = None
        self.linespecial = None
        self.quote_level = 0
        self.code = []
        self.empty_lines = 0
        self.whitespace = None
        self.fence_end = None

    def eval(self, m, start, end):
        """Evaluate a normal fence."""

        if m.group(0).strip() == '':
            # Empty line is okay
            self.empty_lines += 1
            self.code.append(m.group(0))
        elif len(m.group(1)) != self.ws_len and m.group(2) != '':
            # Not indented enough
            self.clear()
        elif self.fence_end.match(m.group(0)) is not None and not m.group(2).startswith(' '):
            # End of fence
            self.process_nested_block(m, start, end)
        else:
            # Content line
            self.empty_lines = 0
            self.code.append(m.group(0))

    def eval_quoted(self, m, quote_level, start, end):
        """Evaluate fence inside a blockquote."""

        if quote_level > self.quote_level:
            # Quote level exceeds the starting quote level
            self.clear()
        elif quote_level <= self.quote_level:
            if m.group(2) == '':
                # Empty line is okay
                self.code.append(m.group(0))
                self.empty_lines += 1
            elif len(m.group(1)) < self.ws_len:
                # Not indented enough
                self.clear()
            elif self.empty_lines and quote_level < self.quote_level:
                # Quote levels don't match and we are signified
                # the end of the block with an empty line
                self.clear()
            elif self.fence_end.match(m.group(0)) is not None:
                # End of fence
                self.process_nested_block(m, start, end)
            else:
                # Content line
                self.empty_lines = 0
                self.code.append(m.group(0))

    def process_nested_block(self, m, start, end):
        """Process the contents of the nested block."""

        self.last = m.group(0)
        code = None
        for entry in reversed(self.extension.superfences):
            if entry["test"](self.lang):
                code = entry["formatter"](self.rebuild_block(self.code), self.lang)
                break

        if code is not None:
            self._store('\n'.join(self.code) + '\n', code, start, end, entry)
        self.clear()

    def parse_hl_lines(self, hl_lines):
        """Parse the lines to highlight."""

        return list(map(int, hl_lines.strip().split())) if hl_lines else []

    def parse_line_start(self, linestart):
        """Parse line start."""

        return int(linestart) if linestart else -1

    def parse_line_step(self, linestep):
        """Parse line start."""

        step = int(linestep) if linestep else -1

        return step if step > 1 else -1

    def parse_line_special(self, linespecial):
        """Parse line start."""

        return int(linespecial) if linespecial else -1

    def search_nested(self, lines):
        """Search for nested fenced blocks."""

        count = 0
        for line in lines:
            if self.fence is None:
                # Found the start of a fenced block.
                m = self.fence_start.match(line)
                if m is not None:
                    start = count
                    self.first = m.group(0)
                    self.ws = m.group('ws') if m.group('ws') else ''
                    self.ws_len = len(self.ws)
                    self.quote_level = self.ws.count(">")
                    self.empty_lines = 0
                    self.fence = m.group('fence')
                    self.lang = m.group('lang')
                    self.hl_lines = m.group('hl_lines')
                    self.linestart = m.group('linestart')
                    self.linestep = m.group('linestep')
                    self.linespecial = m.group('linespecial')
                    self.fence_end = re.compile(NESTED_FENCE_END % self.fence)
                    self.whitespace = re.compile(WS % self.ws_len)
            else:
                # Evaluate lines
                # - Determine if it is the ending line or content line
                # - If is a content line, make sure it is all indentend
                #   with the opening and closing lines (lines with just
                #   whitespace will be stripped so those don't matter).
                # - When content lines are inside blockquotes, make sure
                #   the nested block quote levels make sense according to
                #   blockquote rules.
                m = self.whitespace.match(line)
                if m:
                    end = count + 1
                    quote_level = m.group(1).count(">")

                    if self.quote_level:
                        # Handle blockquotes
                        self.eval_quoted(m, quote_level, start, end)
                    elif quote_level == 0:
                        # Handle all other cases
                        self.eval(m, start, end)
                    else:
                        # Looks like we got a blockquote line
                        # when not in a blockquote.
                        self.clear()
                else:  # pragma: no cover
                    # I am 99.9999% sure we will never hit this line.
                    # But I am too chicken to pull it out :).
                    self.clear()
            count += 1

        # Now that we are done iterating the lines,
        # let's replace the original content with the
        # fenced blocks.
        while len(self.stack):
            fenced, start, end = self.stack.pop()
            lines = lines[:start] + [fenced] + lines[end:]
        return lines

    def highlight(self, src, language):
        """
        Syntax highlight the code block.

        If config is not empty, then the codehlite extension
        is enabled, so we call into it to highlight the code.
        """

        if self.highlight_code:
            linestep = self.parse_line_step(self.linestep)
            linestart = self.parse_line_start(self.linestart)
            linespecial = self.parse_line_special(self.linespecial)
            hl_lines = self.parse_hl_lines(self.hl_lines)

            el = hl.Highlight(
                guess_lang=self.guess_lang,
                pygments_style=self.pygments_style,
                use_pygments=self.use_pygments,
                noclasses=self.noclasses,
                linenums=self.linenums,
                extend_pygments_lang=self.extend_pygments_lang
            ).highlight(
                src,
                language,
                self.css_class,
                hl_lines=hl_lines,
                linestart=linestart,
                linestep=linestep,
                linespecial=linespecial
            )
        else:
            # Format as a code block.
            el = self.CODE_WRAP % ('', '', _escape(src))
        return el

    def _store(self, source, code, start, end, obj):
        """
        Store the fenced blocks in the stack to be replaced when done iterating.

        Store the original text in case we need to restore if we are too greedy.
        """
        # Save the fenced blocks to add once we are done iterating the lines
        placeholder = self.markdown.htmlStash.store(code, safe=True)
        self.stack.append(('%s%s' % (self.ws, placeholder), start, end))
        if not self.disabled_indented:
            # If an indented block consumes this placeholder,
            # we can restore the original source
            obj["stash"].store(
                placeholder[1:-1],
                "%s\n%s%s" % (self.first, source, self.last),
                self.ws_len
            )

    def run(self, lines):
        """Search for fenced blocks."""

        self.get_hl_settings()
        self.clear()
        self.stack = []
        self.disabled_indented = self.config.get("disable_indented_code_blocks", False)

        lines = self.search_nested(lines)

        return lines


class SuperFencesCodeBlockProcessor(CodeBlockProcessor):
    """Process idented code blocks to see if we accidentaly processed its content as a fenced block."""

    FENCED_BLOCK_RE = re.compile(
        r'^([\> ]*)%s(%s)%s$' % (
            md_util.HTML_PLACEHOLDER[0],
            md_util.HTML_PLACEHOLDER[1:-1] % r'([0-9]+)',
            md_util.HTML_PLACEHOLDER[-1]
        )
    )

    def test(self, parent, block):
        """Test method that is one day to be deprecated."""

        return True

    def reindent(self, text, pos, level):
        """Reindent the code to where it is supposed to be."""

        indented = []
        for line in text.split('\n'):
            index = pos - level
            indented.append(line[index:])
        return '\n'.join(indented)

    def revert_greedy_fences(self, block):
        """Revert a prematurely converted fenced block."""

        new_block = []
        for line in block.split('\n'):
            m = self.FENCED_BLOCK_RE.match(line)
            if m:
                key = m.group(2)
                indent_level = len(m.group(1))
                original = None
                for entry in self.extension.superfences:
                    stash = entry["stash"]
                    original, pos = stash.get(key)
                    if original is not None:
                        code = self.reindent(original, pos, indent_level)
                        new_block.append(code)
                        stash.remove(key)
                        break
                if original is None:  # pragma: no cover
                    # Too much work to test this. This is just a fall back in case
                    # we find a placeholder, and we went to revert it and it wasn't in our stash.
                    # Most likely this would be caused by someone else. We just want to put it
                    # back in the block if we can't revert it.  Maybe we can do a more directed
                    # unit test in the future.
                    new_block.append(line)
            else:
                new_block.append(line)
        return '\n'.join(new_block)

    def run(self, parent, blocks):
        """Look for and parse code block."""

        handled = False

        if not self.config.get("disable_indented_code_blocks", False):
            handled = CodeBlockProcessor.test(self, parent, blocks[0])
            if handled:
                if self.config.get("nested", True):
                    blocks[0] = self.revert_greedy_fences(blocks[0])
                handled = CodeBlockProcessor.run(self, parent, blocks) is not False
        return handled


def makeExtension(*args, **kwargs):
    """Return extension."""

    return SuperFencesCodeExtension(*args, **kwargs)
