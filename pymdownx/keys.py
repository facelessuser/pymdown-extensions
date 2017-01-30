"""
Keys.

pymdownx.keys

MIT license.

Extension to input keys with ease.

Idea by Adam Twardoch and coded by Isaac Muse.

Copyright (c) 2017 Isaac Muse <isaacmuse@gmail.com>
"""
from __future__ import unicode_literals
from markdown import Extension
from markdown.inlinepatterns import Pattern
from markdown import util as md_util
from . import util
from . import keymap_db as keymap
import re

RE_KBD = r'''(?x)
(?:
    # Escape
    (?<!\\)(?P<escapes>(?:\\{2})+)(?=\+)|
    # Key
    (?<!\\)\+{2}
    (
        (?:(?:[\w\-]+|"(?:\\.|[^"])+"|\'(?:\\.|[^\'])+\')\+)*?
        (?:[\w\-]+|"(?:\\.|[^"])+"|\'(?:\\.|[^\'])+\')
    )
    \+{2}
)
'''

ESCAPE_RE = re.compile(r'''(?<!\\)(?:\\\\)*\\(.)''')
UNESCAPED_PLUS = re.compile(r'''(?<!\\)(?:\\\\)*(\+)''')
ESCAPED_BSLASH = '%s%s%s' % (md_util.STX, ord('\\'), md_util.ETX)
DOUBLE_BSLASH = '\\\\'


class KeysPattern(Pattern):
    """Return kbd tag."""

    def __init__(self, pattern, config, md):
        """Initialize."""

        self.ksep = config['separator']
        self.markdown = md
        self.strict = config['strict']
        self.classes = config['class'].split(' ')
        self.html_parser = util.HTMLParser()
        self.map = self.merge(keymap.keymap, config['key_map'])
        self.aliases = keymap.aliases
        self.camel = config['camel_case']
        super(KeysPattern, self).__init__(pattern)

    def merge(self, x, y):
        """Given two dicts, merge them into a new dict."""

        z = x.copy()
        z.update(y)
        return z

    def normalize(self, key):
        """Normalize the value."""

        if not self.camel:
            return key

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

    def process_key(self, key):
        """Process key."""

        if key.startswith(('"', "'")):
            value = (None, self.html_parser.unescape(ESCAPE_RE.sub(r'\1', key[1:-1])).strip())
        else:
            norm_key = self.normalize(key)
            canonical_key = self.aliases.get(norm_key, norm_key)
            name = self.map.get(canonical_key, None)
            value = (canonical_key, name) if name else None
        return value

    def handleMatch(self, m):
        """Hanlde kbd pattern matches."""

        if m.group(2):
            return m.group('escapes').replace(DOUBLE_BSLASH, ESCAPED_BSLASH)
        content = [self.process_key(key) for key in UNESCAPED_PLUS.split(m.group(3)) if key != '+']

        if None in content:
            return

        el = md_util.etree.Element(
            ('kbd' if self.strict else 'span'),
            ({'class': ' '.join(self.classes)} if self.classes else {})
        )

        last = None
        for item_class, item_name in content:
            classes = []
            if item_class:
                classes.append('key-' + item_class)
            if last is not None and self.ksep:
                span = md_util.etree.SubElement(el, 'span')
                span.text = md_util.AtomicString(self.ksep)
            attr = {}
            if classes:
                attr['class'] = ' '.join(classes)
            kbd = md_util.etree.SubElement(el, 'kbd', attr)
            kbd.text = md_util.AtomicString(item_name)
            last = kbd

        return el


class KeysExtension(Extension):
    """Add KBD extension to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'separator': ['+', "Provide a keyboard separator - Default: \"+\""],
            'strict': [False, "Format keys and menus according to HTML5 spec - Default: False"],
            'class': ['keys', "Provide class(es) for the kbd elements - Default: kbd"],
            'camel_case': [False, 'Allow camle case conversion for key names PgDn -> pg-dn - Default: False'],
            'key_map': [{}, 'Additional keys to include or keys to override - Default: {}']
        }
        super(KeysExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """Add support for emojis."""

        util.escape_chars(md, ['+'])
        md.inlinePatterns.add("keys", KeysPattern(RE_KBD, self.getConfigs(), md), "<escape")


def makeExtension(*args, **kwargs):
    """Return extension."""

    return KeysExtension(*args, **kwargs)
