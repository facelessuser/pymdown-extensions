"""
Highlight.

A library for managing code highlighting.

All Changes Copyright 2014-2017 Isaac Muse.

---

CodeHilite Extension for Python-Markdown
========================================

Adds code/syntax highlighting to standard Python-Markdown code blocks.

See <https://pythonhosted.org/Markdown/extensions/code_hilite.html>
for documentation.

Original code Copyright 2006-2008 [Waylan Limberg](http://achinghead.com/).

All changes Copyright 2008-2014 The Python Markdown Project

License: [BSD](http://www.opensource.org/licenses/bsd-license.php)
"""
import re
from markdown import Extension
from markdown.treeprocessors import Treeprocessor
import xml.etree.ElementTree as etree
import copy
from collections import OrderedDict
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, guess_lexer
    from pygments.formatters import find_formatter_class
    HtmlFormatter = find_formatter_class('html')
    pygments = True
except ImportError:  # pragma: no cover
    pygments = False

CODE_WRAP = '<pre%s><code%s%s%s>%s</code></pre>'
CODE_WRAP_ON_PRE = '<pre%s%s%s><code>%s</code></pre>'
CLASS_ATTR = ' class="%s"'
ID_ATTR = ' id="%s"'
DEFAULT_CONFIG = {
    'use_pygments': [
        True,
        'Use Pygments to highlight code blocks. '
        'Disable if using a JavaScript library. '
        'Default: True'
    ],
    'guess_lang': [
        False,
        "Automatic language detection - Default: False"
    ],
    'css_class': [
        'highlight',
        "CSS class to apply to wrapper element."
    ],
    'pygments_style': [
        'default',
        'Pygments HTML Formatter Style '
        '(color scheme) - Default: default'
    ],
    'noclasses': [
        False,
        'Use inline styles instead of CSS classes - '
        'Default false'
    ],
    'linenums': [
        None,
        'Display line numbers in block code output (not inline) - Default: False'
    ],
    'linenums_style': [
        'table',
        'Line number style -Default: "table"'
    ],
    'linenums_special': [
        -1,
        'Globally make nth line special - Default: -1'
    ],
    'linenums_class': [
        "linenums",
        "Control the linenums class name when not using Pygments - Default: 'linenums'"
    ],
    'extend_pygments_lang': [
        [],
        'Extend pygments language with special language entry - Default: {}'
    ],
    'legacy_no_wrap_code': [
        False,
        'Do not wrap block code under pre elements with code elements - Default: False'
    ],
    'language_prefix': [
        'language-',
        'Controls the language prefix for non-Pygments code blocks. - Defaults: "language-"'
    ],
    'code_attr_on_pre': [
        False,
        "Attach attribute list values on pre element instead of code element - Default: False"
    ],
    '_enabled': [
        True,
        'Used internally to communicate if extension has been explicitly enabled - Default: False'
    ]
}

if pygments:
    class InlineHtmlFormatter(HtmlFormatter):
        """Format the code blocks."""

        def wrap(self, source, outfile):
            """Overload wrap."""

            return self._wrap_code(source)

        def _wrap_code(self, source):
            """Return source, but do not wrap in inline <code> block."""

            yield 0, ''
            for i, t in source:
                yield i, t.strip()
            yield 0, ''

    class BlockHtmlFormatter(HtmlFormatter):
        """Adds ability to output line numbers in a new way."""

        # Capture `<span class="lineno">   1 </span>`
        RE_SPAN_NUMS = re.compile(r'(<span[^>]*?)(class="[^"]*\blinenos?\b[^"]*)"([^>]*)>([^<]+)(</span>)')
        # Capture `<pre>` that is not followed by `<span></span>`
        RE_TABLE_NUMS = re.compile(r'(<pre[^>]*>)(?!<span></span>)')

        def __init__(self, **options):
            """Initialize."""

            self.pymdownx_inline = options.get('linenos', False) == 'pymdownx-inline'
            if self.pymdownx_inline:
                options['linenos'] = 'inline'
            HtmlFormatter.__init__(self, **options)

        def _format_custom_line(self, m):
            """Format the custom line number."""

            # We've broken up the match in such a way that we not only
            # move the line number value to `data-linenos`, but we could
            # wrap the gutter number in the future with a highlight class.
            # The decision to do this has still not be made.
            return (
                m.group(1) +
                m.group(2) +
                '"' +
                m.group(3) +
                ' data-linenos="' + m.group(4).rstrip() + ' ">' +
                m.group(5)
            )

        def _wrap_customlinenums(self, inner):
            """
            Wrapper to handle block inline line numbers.

            For our special inline version, don't display line numbers via `<span>  1</span>`,
            but include as `<span data-linenos="  1"></span>` and use CSS to display them:
            `[data-linenos]:before {content: attr(data-linenos);}`.  This allows us to use
            inline and copy and paste without issue.
            """

            for t, line in inner:
                if t:
                    line = self.RE_SPAN_NUMS.sub(self._format_custom_line, line)
                yield t, line

        def wrap(self, source, outfile):
            """Wrap the source code."""

            if self.linenos == 2 and self.pymdownx_inline:
                source = self._wrap_customlinenums(source)
            return HtmlFormatter.wrap(self, source, outfile)

        def _wrap_tablelinenos(self, inner):
            """
            Wrapper to handle line numbers better in table.

            Pygments currently has a bug with line step where leading blank lines collapse.
            Use the same fix Pygments uses for code content for code line numbers.
            This fix should be pull requested on the Pygments repository.
            """

            for t, line in HtmlFormatter._wrap_tablelinenos(self, inner):
                yield t, self.RE_TABLE_NUMS.sub(r'\1<span></span>', line)


class Highlight(object):
    """Highlight class."""

    def __init__(
        self, guess_lang=False, pygments_style='default', use_pygments=True,
        noclasses=False, extend_pygments_lang=None, linenums=None, linenums_special=-1,
        linenums_style='table', linenums_class='linenums', wrapcode=True, language_prefix='language-',
        code_attr_on_pre=False
    ):
        """Initialize."""

        self.guess_lang = guess_lang
        self.pygments_style = pygments_style
        self.use_pygments = use_pygments
        self.noclasses = noclasses
        self.linenums = linenums
        self.linenums_style = linenums_style
        self.linenums_special = linenums_special
        self.linenums_class = linenums_class
        self.wrapcode = wrapcode
        self.language_prefix = language_prefix
        self.code_attr_on_pre = code_attr_on_pre

        if extend_pygments_lang is None:  # pragma: no cover
            extend_pygments_lang = []
        self.extend_pygments_lang = {}
        for language in extend_pygments_lang:
            if isinstance(language, (dict, OrderedDict)):
                name = language.get('name')
                if name is not None and name not in self.extend_pygments_lang:
                    self.extend_pygments_lang[name] = [
                        language.get('lang'),
                        language.get('options', {})
                    ]

    def get_extended_language(self, language):
        """Get extended language."""

        return self.extend_pygments_lang.get(language, (language, {}))

    def get_lexer(self, src, language):
        """Get the Pygments lexer."""

        if language:
            language, lexer_options = self.get_extended_language(language)
        else:
            lexer_options = {}

        # Try and get lexer by the name given.
        try:
            lexer = get_lexer_by_name(language, **lexer_options)
        except Exception:
            lexer = None

        if lexer is None:
            if self.guess_lang:
                try:
                    lexer = guess_lexer(src)
                except Exception:  # pragma: no cover
                    pass
        if lexer is None:
            lexer = get_lexer_by_name('text')
        return lexer

    def escape(self, txt):
        """Basic HTML escaping."""

        txt = txt.replace('&', '&amp;')
        txt = txt.replace('<', '&lt;')
        txt = txt.replace('>', '&gt;')
        return txt

    def highlight(
        self, src, language, css_class='highlight', hl_lines=None,
        linestart=-1, linestep=-1, linespecial=-1, inline=False, classes=None, id_value='', attrs=None
    ):
        """Highlight code."""

        if attrs is None:
            attrs = {}
        class_names = classes[:] if classes else []
        linenums_enabled = (self.linenums or (self.linenums is not False and linestart >= 0)) and not inline > 0

        # Convert with Pygments.
        if pygments and self.use_pygments:
            # Setup language lexer.
            lexer = self.get_lexer(src, language)
            linenums = self.linenums_style if linenums_enabled else False

            if class_names:
                css_class = ' {}'.format('' if not css_class else css_class)
                css_class = ' '.join(class_names) + css_class
                stripped = css_class.strip()

                if not isinstance(linenums, str) or linenums != 'table':
                    css_class = stripped

            # Setup line specific settings.
            if not linenums or linestep < 1:
                linestep = 1
            if not linenums or linestart < 1:
                linestart = 1
            if self.linenums_special >= 0 and linespecial < 0:
                linespecial = self.linenums_special
            if not linenums or linespecial < 0:
                linespecial = 0
            if hl_lines is None or inline:
                hl_lines = []

            # Setup formatter
            html_formatter = InlineHtmlFormatter if inline else BlockHtmlFormatter
            formatter = html_formatter(
                cssclass=css_class,
                linenos=linenums,
                linenostart=linestart,
                linenostep=linestep,
                linenospecial=linespecial,
                style=self.pygments_style,
                noclasses=self.noclasses,
                hl_lines=hl_lines,
                wrapcode=self.wrapcode
            )

            # Convert
            code = highlight(src, lexer, formatter)
            if inline:
                class_str = css_class
                attr_str = ''
                id_str = ''
        elif inline:
            # Format inline code for a JavaScript Syntax Highlighter by specifying language.
            code = self.escape(src)
            if css_class:
                class_names.insert(0, css_class)
            if language:
                class_names.insert(0, self.language_prefix + language)
            class_str = ' '.join(class_names) if class_names else ''
            id_str = id_value
        else:
            # Format block code for a JavaScript Syntax Highlighter by specifying language.
            if self.code_attr_on_pre and css_class:
                class_names.insert(0, css_class)
            if language:
                class_names.insert(0, self.language_prefix + language)
            class_str = CLASS_ATTR % ' '.join(class_names) if class_names else ''
            id_str = ID_ATTR % id_value if id_value else ''
            attr_str = ' ' + ' '.join('{k}="{v}"'.format(k=k, v=v) for k, v in attrs.items()) if attrs else ''
            if not self.code_attr_on_pre:
                highlight_class = (CLASS_ATTR % css_class) if css_class else ''
                code = CODE_WRAP % (highlight_class, id_str, class_str, attr_str, self.escape(src))
            else:
                code = CODE_WRAP_ON_PRE % (id_str, class_str, attr_str, self.escape(src))

        if inline:
            attributes = {}

            if class_str:
                attributes['class'] = class_str

            # This code exists for consistency, but we currently don't
            # ever feed extra ids or attributes for inline code.
            # We let `attr_list` handle this directly, but if we did
            # need this, we would then want to exercise this logic.
            if id_str:  # pragma: no cover
                attributes['id'] = id_str
            for k, v in attrs:  # pragma: no cover
                attributes[k] = v

            el = etree.Element('code', attributes)
            el.text = code
            return el
        else:
            return code.strip()


class HighlightTreeprocessor(Treeprocessor):
    """Highlight source code in code blocks."""

    def __init__(self, md):
        """Initialize."""

        super(HighlightTreeprocessor, self).__init__(md)

    def code_unescape(self, text):
        """Unescape code."""
        text = text.replace("&lt;", "<")
        text = text.replace("&gt;", ">")
        text = text.replace("&amp;", "&")
        return text

    def run(self, root):
        """Find code blocks and store in `htmlStash`."""

        blocks = root.iter('pre')
        for block in blocks:
            if len(block) == 1 and block[0].tag == 'code':
                code = Highlight(
                    guess_lang=self.config['guess_lang'],
                    pygments_style=self.config['pygments_style'],
                    use_pygments=self.config['use_pygments'],
                    noclasses=self.config['noclasses'],
                    linenums=self.config['linenums'],
                    linenums_style=self.config['linenums_style'],
                    linenums_special=self.config['linenums_special'],
                    linenums_class=self.config['linenums_class'],
                    extend_pygments_lang=self.config['extend_pygments_lang'],
                    wrapcode=not self.config['legacy_no_wrap_code'],
                    language_prefix=self.config['language_prefix'],
                    code_attr_on_pre=self.config['code_attr_on_pre']
                )
                placeholder = self.md.htmlStash.store(
                    code.highlight(
                        self.code_unescape(block[0].text),
                        '',
                        self.config['css_class']
                    )
                )

                # Clear code block in `etree` instance
                block.clear()
                # Change to `p` element which will later
                # be removed when inserting raw HTML
                block.tag = 'p'
                block.text = placeholder


class HighlightExtension(Extension):
    """Configure highlight settings globally."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = copy.deepcopy(DEFAULT_CONFIG)
        super(HighlightExtension, self).__init__(*args, **kwargs)

    def get_pymdownx_highlight_settings(self):
        """Get the specified extension."""

        target = None

        if self.enabled:
            target = self.getConfigs()

        if target is None:
            target = {}
            config_clone = copy.deepcopy(DEFAULT_CONFIG)
            for k, v in config_clone.items():
                target[k] = config_clone[k][0]

        return target

    def get_pymdownx_highlighter(self):
        """Get the highlighter."""

        return Highlight

    def extendMarkdown(self, md):
        """Add support for code highlighting."""

        config = self.getConfigs()
        self.md = md
        self.enabled = config.get("_enabled", False)

        if self.enabled:
            ht = HighlightTreeprocessor(self.md)
            ht.config = self.getConfigs()
            self.md.treeprocessors.register(ht, "indent-highlight", 30)

        index = 0
        register = None
        for ext in self.md.registeredExtensions:
            if isinstance(ext, HighlightExtension):
                register = not ext.enabled and self.enabled
                break

        if register is None:
            register = True
            index = -1

        if register:
            if index == -1:
                self.md.registerExtension(self)
            else:
                self.md.registeredExtensions[index] = self


def makeExtension(*args, **kwargs):
    """Return extension."""

    return HighlightExtension(*args, **kwargs)
