"""
---
pymdownx.inlinehilite
Inline codehilite variant

This is a modification of the original CodeHilite extension.
It relies on codehilite's config, and adds a processor that
can highlite backtick regions content if it is preceeded with
a language specifier like so:

    `:::javascript var test = 0;`
            - or -
    `#!javascript var test = 0;`

Modified: 2014 Isaac Muse <isaacmuse@gmail.com>
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

from __future__ import absolute_import
from __future__ import unicode_literals
from markdown import Extension
from markdown.inlinepatterns import Pattern
from markdown.extensions import codehilite
# import traceback
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, guess_lexer
    from pygments.formatters import find_formatter_class
    HtmlFormatter = find_formatter_class('html')
    pygments = True
except ImportError:
    pygments = False

BACKTICK_CODE_RE = r'''(?x)
(?<!\\)(?P<tic>`+)
((?:\:{3,}|\#!)(?P<lang>[a-zA-Z0-9_+-]*)\s+)? # Optional language
(?P<code>.+?)                                 # Code
(?<!`)(?P=tic)(?!`)                           # Closing
'''


class InlineCodeHtmlFormatter(HtmlFormatter):
    def wrap(self, source, outfile):
        """ Overload wrap """
        return self._wrap_code(source)

    def _wrap_code(self, source):
        """ Return source wrapped in simple inline <code> block """
        yield 0, '<code class="%s">' % self.cssclass
        for i, t in source:
            yield i, t.strip()
        yield 0, '</code>'


class InlineHilitePattern(Pattern):
    def __init__(self, pattern, md):
        Pattern.__init__(self, pattern)
        self.markdown = md
        self.checked_for_codehilite = False
        self.guess_lang = False
        self.css_class = 'codehilite'
        self.style = 'default'

    def get_codehilite_settings(self):
        # Check for code hilite extension
        if not self.checked_for_codehilite:
            for ext in self.markdown.registeredExtensions:
                if isinstance(ext, codehilite.CodeHiliteExtension):
                    ext.config
                    self.guess_lang = ext.config['guess_lang'][0]
                    self.css_class = ext.config['css_class'][0]
                    self.style = ext.config['pygments_style'][0]
                    self.use_pygments = ext.config['use_pygments'][0]
                    break
            self.checked_for_codehilite = True

    def codehilite(self, lang, src):
        if codehilite.pygments and pygments and self.use_pygments:
            try:
                lexer = get_lexer_by_name(lang)
            except ValueError:
                try:
                    if self.guess_lang:
                        lexer = guess_lexer(src)
                    else:
                        lexer = get_lexer_by_name('text')
                except ValueError:
                    lexer = get_lexer_by_name('text')

            formatter = InlineCodeHtmlFormatter(style=self.style, cssclass=self.css_class)
            code = highlight(src, lexer, formatter)
        else:
            # Just escape and build markup usable by JS highlighting libs
            txt = src.replace('&', '&amp;')
            txt = txt.replace('<', '&lt;')
            txt = txt.replace('>', '&gt;')
            txt = txt.replace('"', '&quot;')
            classes = [self.css_class]
            if lang:
                classes.append('language-%s' % lang)
            class_str = ''
            if len(classes):
                class_str = ' class="%s"' % ' '.join(classes)
            code = '<code%s>%s</code>' % (class_str, txt)
        placeholder = self.markdown.htmlStash.store(code, safe=True)
        return placeholder

    def handleMatch(self, m):
        lang = m.group('lang') if m.group('lang') else 'text'
        src = m.group('code').strip()
        self.get_codehilite_settings()
        return self.codehilite(lang, src)


class InlineHiliteExtension(Extension):
    """Adds inline-hilite extension to Markdown class."""

    def __init__(self, *args, **kwargs):
        super(InlineHiliteExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """ Add support for :::language`code` code hiliting """
        inline_hilite = InlineHilitePattern(BACKTICK_CODE_RE, md)
        md.inlinePatterns['backtick'] = inline_hilite


def makeExtension(*args, **kwargs):
    return InlineHiliteExtension(*args, **kwargs)
