"""KBD."""
from __future__ import unicode_literals
from markdown import Extension
from markdown.inlinepatterns import Pattern
from . import util
from . import keymap_db as keymap
import re

RE_KBD = r'''(?x)
\+{2}
    # Menu
    (?::
        (
            (?:(?:"(?:\\.|[^"])+"|\'(?:\\.|[^\'])+\')\+)*?
            (?:"(?:\\.|[^"])+"|\'(?:\\.|[^\'])+\')
        ) |
    # Key
        (
            (?:(?:[\w\-]+|"(?:\\.|[^"])+"|\'(?:\\.|[^\'])+\')\+)*?
            (?:[\w\-]+|"(?:\\.|[^"])+"|\'(?:\\.|[^\'])+\')
        )
    )
\+{2}
'''
KBD_OUTPUT = '<samp class="%(class)s%(state)s">%(name)s</samp>'
KBD_INPUT = '<kbd class="%(class)s%(state)s %(key)s">%(name)s</kbd>'
SEP = '<span class="%(class)s%(state)s-sep">%(sep)s</span>'
KBD_WRAP = '<kbd class="%(class)s %(state)s">%(keys)s</kbd>'
ESCAPE_RE = re.compile(r'''(?<!\\)(?:\\\\)*\\(.)''')


def _escape(txt):
    """Basic html escaping."""

    txt = txt.replace('&', '&amp;')
    txt = txt.replace('<', '&lt;')
    txt = txt.replace('>', '&gt;')
    txt = txt.replace('"', '&quot;')
    return txt


class KbdPattern(Pattern):
    """Return kbd tag."""

    def __init__(self, pattern, config, md):
        """Initialize."""

        ksep = config['keyboard_separator']
        msep = config['menu_separator']
        self.markdown = md
        self.wrap_kbd = config['strict']
        self.classes = config['class']
        self.html_parser = util.HTMLParser()

        # Keyboard separator
        if ksep and not self.wrap_kbd:
            self.ksep =  SEP % {'class': self.classes + ' ', 'state': 'keyboard', 'sep': ksep}
        elif ksep:
            self.ksep =  SEP % {'class': '', 'state': 'keyboard', 'sep': ksep}
        else:
            self.ksep = ''

        # Menu separator
        if msep and not self.wrap_kbd:
            self.msep =  SEP % {'class': self.classes + ' ', 'state': 'menu', 'sep': msep}
        elif msep:
            self.msep =  SEP % {'class': '', 'state': 'menu', 'sep': msep}
        else:
            self.msep = ''

        # Menu format
        if self.wrap_kbd:
            self.menu = KBD_OUTPUT
        else:
            self.menu = KBD_INPUT

        # Keyboard format
        self.keyboard = KBD_INPUT
        Pattern.__init__(self, pattern)

    def normalize(self, key):
        """Normalize the value."""

        norm_key = []
        last = ''
        for c in key:
            if c.isupper():
                if not last or last == '-':
                    norm_key.append(c.lower())
                else:
                    norm_key.extend(['-', c.lower()])
            else:
                norm_key.append(c)
            last = c
        return ''.join(norm_key)

    def process_menu(self, key):
        """Process menu."""

        return (None, _escape(self.html_parser.unescape(ESCAPE_RE.sub(r'\1', key[1:-1]))))

    def process_key(self, key):
        """Process key."""

        if key.startswith(('"', "'")):
            value = (None, _escape(self.html_parser.unescape(ESCAPE_RE.sub(r'\1', key[1:-1]))))
        else:
            norm_key = self.normalize(key)
            canonical_key = keymap.aliases.get(norm_key, norm_key)
            name = keymap.keymap.get(canonical_key, None)
            value = (canonical_key, _escape(name)) if name else None
        return value

    def handleMatch(self, m):
        """Hanlde kbd pattern matches."""

        if m.group(3):
            is_key = True
            content = [self.process_key(key) for key in m.group(3).split('+')]
        else:
            is_key = False
            content = [self.process_menu(menu) for menu in m.group(2).split('+')]

        if None in content:
            return

        html = []
        for item_class, item_name in content:
            html.append(
                (self.keyboard if is_key else self.menu) % {
                    'class': (self.classes + ' ' if not self.wrap_kbd else ''),
                    'state': ('keyboard' if is_key else 'menu'),
                    'key': ('key-' + item_class if item_class else '' ),
                    'name': item_name
                }
            )

        separator = self.ksep if is_key else self.msep

        if self.wrap_kbd:
            kbd = KBD_WRAP % {'class': self.classes, 'keys': separator.join(html)}
        else:
            kbd = separator.join(html)

        return self.markdown.htmlStash.store(kbd, safe=True)


class KbdExtension(Extension):
    """Add KBD extension to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'keyboard_separator': ['+', "Provide a keyboard separator - Default: \"+\""],
            'menu_separator': ['\u2192', "Provide a menu separator - Default: \"\u2192\""],
            'strict': [False, "Format keys and menus according to HTML5 spec - Default: False"],
            'class': ['kbd', "Provide class(es) for the kbd elements - Default: kbd"]
        }
        super(KbdExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """Add support for emojis."""

        util.escape_chars(md, ['+'])

        md.inlinePatterns.add(
            "kbd",
            KbdPattern(RE_KBD, self.getConfigs(), md),
            "<escape"
        )


###################
# Make Available
###################
def makeExtension(*args, **kwargs):
    """Return extension."""

    return KbdExtension(*args, **kwargs)
