"""
Inline Highlighting.

pymdownx.inlinehilite

An alternative inline code extension that highlights code.  Can
use CodeHilite to source its settings or pymdownx.highlight.

`:::javascript var test = 0;`

- or -

`#!javascript var test = 0;`

Copyright 2014 - 2017 Isaac Muse <isaacmuse@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals
from markdown import Extension
from markdown.inlinepatterns import Pattern
from markdown import util as md_util
from . import highlight as hl

ESCAPED_BSLASH = '%s%s%s' % (md_util.STX, ord('\\'), md_util.ETX)
DOUBLE_BSLASH = '\\\\'
BACKTICK_CODE_RE = r'''(?x)
(?:
(?<!\\)(?P<escapes>(?:\\{2})+)(?=`+) |  # Process code escapes before code
(?<!\\)(?P<tic>`+)
((?:\:{3,}|\#!)(?P<lang>[\w#.+-]*)\s+)? # Optional language
(?P<code>.+?)                           # Code
(?<!`)(?P=tic)(?!`)                     # Closing
)
'''


def _escape(txt):
    """Basic html escaping."""

    txt = txt.replace('&', '&amp;')
    txt = txt.replace('<', '&lt;')
    txt = txt.replace('>', '&gt;')
    txt = txt.replace('"', '&quot;')
    return txt


class InlineHilitePattern(Pattern):
    """Handle the inline code patterns."""

    def __init__(self, pattern, md):
        """Initialize."""

        Pattern.__init__(self, pattern)
        self.markdown = md
        self.get_hl_settings = False

    def get_settings(self):
        """Check for CodeHilite extension and gather its settings."""

        if not self.get_hl_settings:
            self.get_hl_settings = True
            self.style_plain_text = self.config['style_plain_text']

            config = hl.get_hl_settings(self.markdown)
            css_class = self.config['css_class']
            self.css_class = css_class if css_class else config['css_class']

            self.extend_pygments_lang = config.get('extend_pygments_lang', None)
            self.guess_lang = config['guess_lang']
            self.pygments_style = config['pygments_style']
            self.use_pygments = config['use_pygments']
            self.noclasses = config['noclasses']

    def highlight_code(self, language, src):
        """Syntax highlight the inline code block."""

        process_text = self.style_plain_text or language or self.guess_lang

        if process_text:
            el = hl.Highlight(
                guess_lang=self.guess_lang,
                pygments_style=self.pygments_style,
                use_pygments=self.use_pygments,
                noclasses=self.noclasses,
                extend_pygments_lang=self.extend_pygments_lang
            ).highlight(src, language, self.css_class, inline=True)
            el.text = self.markdown.htmlStash.store(el.text, safe=True)
        else:
            el = md_util.etree.Element('code')
            el.text = self.markdown.htmlStash.store(_escape(src), safe=True)
        return el

    def handleMatch(self, m):
        """Handle the pattern match."""

        if m.group('escapes'):
            return m.group('escapes').replace(DOUBLE_BSLASH, ESCAPED_BSLASH)
        else:
            lang = m.group('lang') if m.group('lang') else ''
            src = m.group('code').strip()
            self.get_settings()
            return self.highlight_code(lang, src)


class InlineHiliteExtension(Extension):
    """Add inline highlighting extension to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'style_plain_text': [
                False,
                "Process inline code even when a language is not specified "
                "or langauge is specified as 'text'. "
                "When 'False', no classes will be added to 'text' code blocks"
                "and no scoping will performed. The content will just be escaped."
                "- Default: False"
            ],
            'css_class': [
                '',
                "Set class name for wrapper element. The default of CodeHilite or Highlight will be used"
                "if nothing is set. - "
                "Default: ''"
            ]
        }
        super(InlineHiliteExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """Add support for `:::language code` and `#!language code` highlighting."""

        config = self.getConfigs()
        inline_hilite = InlineHilitePattern(BACKTICK_CODE_RE, md)
        inline_hilite.config = config
        md.inlinePatterns['backtick'] = inline_hilite


def makeExtension(*args, **kwargs):
    """Return extension."""

    return InlineHiliteExtension(*args, **kwargs)
