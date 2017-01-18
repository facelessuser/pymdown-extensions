"""KBD."""
from __future__ import unicode_literals
from markdown import Extension
from markdown.inlinepatterns import Pattern
from . import util
import re

RE_KBD = r'\+{2}((?:[A-Za-z\d_]+\+)*?[A-Za-z\d_]+)\+{2}'
RE_NORMALIZE = re.compile(r'((?<=[a-z\d])[A-Z])')
KBD = '<kbd class="%(class)s key-%(key)s">%(name)s</kbd>'
WRAPPED_KBD = '<kbd class="%(class)s">' + KBD + '</kbd>'

KEY_MAP = {
    "backspace": "BACKSPACE",
    "tab": "TAB",
    "enter": "ENTER",
    "shift": "SHIFT",
    "ctrl": "CTRL",
    "alt": "ALT",
    "pause": "PAUSE",
    "break": "BREAK",
    "caps-lock": "CAPS LOCK",
    "escape": "ESC",
    "page-up": "PG UP",
    "page-down": "PG DN",
    "end": "END",
    "home": "HOME",
    "left-arrow": "\u2190",
    "up_arrow": "\u2191",
    "right-arrow": "\u2192",
    "down-arrow": "\u2193",
    "insert": "INS",
    "delete": "DEL",
    "0": "0",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    "a": "a",
    "b": "b",
    "c": "c",
    "d": "d",
    "e": "e",
    "f": "f",
    "g": "g",
    "h": "h",
    "i": "i",
    "j": "j",
    "k": "k",
    "l": "l",
    "m": "m",
    "n": "n",
    "o": "o",
    "p": "p",
    "q": "q",
    "r": "r",
    "s": "s",
    "t": "t",
    "u": "u",
    "v": "v",
    "w": "w",
    "x": "x",
    "y": "y",
    "z": "z",
    "windows": "WIN",
    "command": "CMD",
    "function": "FN",
    "num0": "NUM 0",
    "num1": "NUM 1",
    "num2": "NUM 2",
    "num3": "NUM 3",
    "num4": "NUM 4",
    "num5": "NUM 5",
    "num6": "NUM 6",
    "num7": "NUM 7",
    "num8": "NUM 8",
    "num9": "NUM 9",
    "multiply": "*",
    "add": "+",
    "subtract": "-",
    "decimal": ".",
    "divide": "/",
    "f1": "F1",
    "f2": "F2",
    "f3": "F3",
    "f4": "F4",
    "f5": "F5",
    "f6": "F6",
    "f7": "F7",
    "f8": "F8",
    "f9": "F9",
    "f10": "F10",
    "f11": "F11",
    "f12": "F12",
    "num-lock": "NUM LOCK",
    "scroll-lock": "SCROLL LOCK",
    "semicolon": ":;",
    "equal-sign": "+=",
    "comma": "<,",
    "period": ">.",
    "forward-slash": "?/",
    "grave-accent": "`~",
    "open-bracket": "{[",
    "back-slash": "\\",
    "close-braket": "}]",
    "single-quote": "\"'"
}

KEY_ALIAS = {
    "win": "windows",
    "cmd": "command"
}


class KbdPattern(Pattern):
    """Return kbd tag."""

    def __init__(self, pattern, config, md):
        """Initialize."""

        self.markdown = md
        self.wrap_kbd = config['wrap_kbd']
        self.separator = config['separator']
        self.classes = config['classes']
        Pattern.__init__(self, pattern)

    def process_key(self, key):
        """Process key."""

        norm_key = RE_NORMALIZE.sub(r'-\1', key).replace('_', '-').lower()
        canonical_key = KEY_ALIAS.get(norm_key, norm_key)
        name = KEY_MAP.get(canonical_key, None)
        return (canonical_key, name) if name else None

    def handleMatch(self, m):
        """Hanlde kbd pattern matches."""

        keys = [self.process_key(key) for key in m.group(2).split('+')]

        if None in keys:
            return

        html = []
        for key_class, key_name in keys:
            html.append(
                (WRAPPED_KBD if self.wrap_kbd else KBD) % {
                    'class': self.classes,
                    'key': key_class,
                    'name': key_name
                }
            )

        return self.markdown.htmlStash.store(self.separator.join(html), safe=True)


class KbdExtension(Extension):
    """Add KBD extension to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'separator': ['+', "Provide a separator - Default: \"+\""],
            'wrap_kbd': [False, "Wrap kbds in another kbd according to HTML5 spec - Default: False"],
            'classes': ['kbd', "Provide classes for the kbd elements - Default: kbd"]
        }
        super(KbdExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """Add support for emojis."""

        util.escape_chars(md, ['+'])

        md.inlinePatterns.add(
            "kbd",
            KbdPattern(RE_KBD, self.getConfigs(), md),
            "<not_strong"
        )


###################
# Make Available
###################
def makeExtension(*args, **kwargs):
    """Return extension."""

    return KbdExtension(*args, **kwargs)
