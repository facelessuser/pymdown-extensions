"""KBD."""
from __future__ import unicode_literals
from markdown import Extension
from markdown.inlinepatterns import Pattern
from . import util
from . import keymap_db as keymap
import re

RE_KBD = r'''(?x)
\+{2}(
    (?:(?:[\w\-]+|"(?:\\.|[^"])+"|\'(?:\\.|[^\'])+\')\+)*?
    (?:[\w\-]+|"(?:\\.|[^"])+"|\'(?:\\.|[^\'])+\')
)\+{2}
'''
KBD = '<kbd class="%(class)s-key %(key)s">%(name)s</kbd>'
KBD_SEP = '<span class="%(class)s-sep">%(sep)s</span>'
KBD_WRAP = '<kbd class="%(class)s">%(keys)s</kbd>'
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

        sep = config['separator']
        self.markdown = md
        self.wrap_kbd = config['wrap_kbd']
        self.classes = config['class']
        self.separator = (KBD_SEP % {'class': self.classes, 'sep': sep}) if sep else ''
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

    def process_key(self, key):
        """Process key."""

        if key.startswith(('"', "'")):
            value = (None, ESCAPE_RE.sub(r'\1', key[1:-1]))
        else:
            norm_key = self.normalize(key)
            canonical_key = keymap.aliases.get(norm_key, norm_key)
            name = keymap.keymap.get(canonical_key, None)
            value = (canonical_key, _escape(name)) if name else None
        return value

    def handleMatch(self, m):
        """Hanlde kbd pattern matches."""

        keys = [self.process_key(key) for key in m.group(2).split('+')]

        if None in keys:
            return

        html = []
        for key_class, key_name in keys:
            html.append(
                KBD % {
                    'class': self.classes,
                    'key': ('key-' + key_class if key_class else '' ),
                    'name': key_name
                }
            )

        if self.wrap_kbd:
            kbd = KBD_WRAP % {'class': self.classes, 'keys': self.separator.join(html)}
        else:
            kbd = self.separator.join(html)

        return self.markdown.htmlStash.store(kbd, safe=True)


class KbdExtension(Extension):
    """Add KBD extension to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'separator': ['+', "Provide a separator - Default: \"+\""],
            'wrap_kbd': [False, "Wrap kbds in another kbd according to HTML5 spec - Default: False"],
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
