"""
Critic.

pymdownx.critic
Parses critic markup and outputs the file in a more visual HTML.
Must be the last extension loaded.

MIT license.

Copyright (c) 2014 - 2017 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
from markdown import Extension
from markdown.preprocessors import Preprocessor
from markdown.postprocessors import Postprocessor
from markdown.util import STX, ETX
import re

SOH = '\u0001'  # start
EOT = '\u0004'  # end

CRITIC_KEY = "czjqqkd:%s"
CRITIC_PLACEHOLDER = CRITIC_KEY % r'[0-9]+'
SINGLE_CRITIC_PLACEHOLDER = r'{stx}(?P<key>{key}){etx}'.format(
    key=CRITIC_PLACEHOLDER, stx=STX, etx=ETX
)
CRITIC_PLACEHOLDERS = r'''(?x)
(?:
    (?P<block>\<p\>(?P<block_keys>(?:{stx}{key}{etx})+)\</p\>) |
    {single}
)
'''.format(
    key=CRITIC_PLACEHOLDER, single=SINGLE_CRITIC_PLACEHOLDER,
    stx=STX, etx=ETX
)
# Critic mark types, identified by the two characters following the opening `{`.
INS = '++'
DEL = '--'
MARK = '=='
COMMENT = '>>'
SUB = '~~'

# The sequence that terminates each type of mark (the closing `}` included).
CLOSERS = {
    INS: '++}',
    DEL: '--}',
    MARK: '==}',
    COMMENT: '<<}',
    SUB: '~~}'
}

# Separates the deleted and inserted text of a substitution.
SUB_MID = '~>'

RE_CRITIC_PLACEHOLDER = re.compile(CRITIC_PLACEHOLDERS)
RE_CRITIC_SUB_PLACEHOLDER = re.compile(SINGLE_CRITIC_PLACEHOLDER)
RE_CRITIC_BLOCK = re.compile(r'((?:ins|del|mark)\s+)(class=([\'"]))(.*?)(\3)')
RE_BLOCK_SEP = re.compile(r'^(?:\r?\n){2,}$')


def find_critics(text):
    """
    Find critic marks in the text, yielding `(start, end, kind, text, sub_text)` for each.

    `kind` is one of `INS`, `DEL`, `MARK`, `COMMENT`, or `SUB`. `sub_text` is only set for `SUB` (the inserted text,
    with `text` being the deleted text).

    A mark opens with `{` and a two character type, and closes with the first occurrence of the type's closer
    (`SUB` uses the first `~>` and then the first `~~}` after it). Marks cannot nest, so the scan resumes after
    each mark that is found.

    This is intentionally not a regular expression. Searching for a closer that does not exist fails only after
    scanning to the end of the text, and a regular expression would repeat that scan for every opener (and, for
    substitutions, for every `~>` as well), resulting in quadratic or even cubic time on unclosed input.

    Here, a closer is found with `str.find`, and if none exists after an opener, none can exist after any later
    opener of the same kind. We record that and skip all further openers of that kind. Every character is therefore
    scanned a bounded number of times: either it is consumed by a mark that was found, or it was scanned by the
    single failed search made for its kind.
    """

    find = text.find
    dead = set()
    pos = 0

    while True:
        start = find('{', pos)
        if start == -1:
            break

        kind = text[start + 1:start + 3]
        if kind not in CLOSERS:
            pos = start + 1
            continue

        # The opener is three characters long and can not contain the start of another opener.
        pos = start + 3
        if kind in dead:
            continue

        content = sub_text = None
        end = -1

        if kind == SUB:
            mid = find(SUB_MID, pos)
            if mid != -1:
                close = find(CLOSERS[kind], mid + 2)
                if close != -1:
                    content = text[pos:mid]
                    sub_text = text[mid + 2:close]
                    end = close + 3
        else:
            close = find(CLOSERS[kind], pos)
            if close != -1:
                content = text[pos:close]
                end = close + 3

        if end == -1:
            dead.add(kind)
            # Nothing left that could possibly be found
            if len(dead) == len(CLOSERS):
                break
            continue

        yield start, end, kind, content, sub_text
        pos = end


class CriticStash:
    """Stash critic marks until ready."""

    def __init__(self, stash_key):
        """Initialize."""

        self.stash_key = stash_key
        self.stash = {}
        self.count = 0

    def __len__(self):  # pragma: no cover
        """Get length of stash."""
        return len(self.stash)

    def get(self, key, default=None):
        """Get the specified item from the stash."""

        code = self.stash.get(key, default)
        return code

    def remove(self, key):  # pragma: no cover
        """Remove the specified item from the stash."""

        del self.stash[key]

    def store(self, code):
        """
        Store the code in the stash with the placeholder.

        Return placeholder.
        """
        key = self.stash_key % str(self.count)
        self.stash[key] = code
        self.count += 1
        return SOH + key + EOT

    def clear(self):
        """Clear the stash."""

        self.stash = {}
        self.count = 0


class CriticsPostprocessor(Postprocessor):
    """Handle cleanup on post process for viewing critic marks."""

    def __init__(self, critic_stash):
        """Initialize."""

        super().__init__()
        self.critic_stash = critic_stash

    def subrestore(self, m):
        """Replace all critic tags in the paragraph block `<p>(critic del close)(critic ins close)</p>` etc."""
        content = None
        key = m.group('key')
        if key is not None:
            content = self.critic_stash.get(key)
        return content

    def block_edit(self, m):
        """Handle block edits."""

        if 'break' in m.group(4).split(' '):
            return m.group(0)
        else:
            return m.group(1) + m.group(2) + m.group(4) + ' block' + m.group(5)

    def restore(self, m):
        """Replace placeholders with actual critic tags."""

        content = None
        if m.group('block_keys') is not None:
            content = RE_CRITIC_SUB_PLACEHOLDER.sub(
                self.subrestore, m.group('block_keys')
            )
            if content is not None:
                content = RE_CRITIC_BLOCK.sub(self.block_edit, content)
        else:
            text = self.critic_stash.get(m.group('key'))
            if text is not None:
                content = text
        return content if content is not None else m.group(0)

    def run(self, text):
        """Replace critic placeholders."""

        text = RE_CRITIC_PLACEHOLDER.sub(self.restore, text)

        return text


class CriticViewPreprocessor(Preprocessor):
    """Handle viewing critic marks in Markdown content."""

    def __init__(self, critic_stash):
        """Initialize."""

        super().__init__()
        self.critic_stash = critic_stash

    def _ins(self, text):
        """Handle critic inserts."""

        if RE_BLOCK_SEP.match(text):
            return '\n\n%s\n\n' % self.critic_stash.store('<ins class="critic break">&nbsp;</ins>')
        return (
            self.critic_stash.store('<ins class="critic">') +
            text +
            self.critic_stash.store('</ins>')
        )

    def _del(self, text):
        """Handle critic deletes."""

        if RE_BLOCK_SEP.match(text):
            return self.critic_stash.store('<del class="critic break">&nbsp;</del>')
        return (
            self.critic_stash.store('<del class="critic">') +
            text +
            self.critic_stash.store('</del>')
        )

    def _mark(self, text):
        """Handle critic marks."""

        return (
            self.critic_stash.store('<mark class="critic">') +
            text +
            self.critic_stash.store('</mark>')
        )

    def _comment(self, text):
        """Handle critic comments."""

        return (
            self.critic_stash.store(
                '<span class="critic comment">' +
                self.html_escape(text, strip_nl=True) +
                '</span>'
            )
        )

    def critic_view(self, kind, text, sub_text=None):
        """Insert appropriate HTML to tags to visualize Critic marks."""

        if kind == INS:
            return self._ins(text)
        elif kind == DEL:
            return self._del(text)
        elif kind == SUB:
            return self._del(text) + self._ins(sub_text)
        elif kind == MARK:
            return self._mark(text)
        else:
            return self._comment(text)

    def critic_parse(self, kind, text, sub_text=None):
        """
        Normal critic parser.

        Either removes accepted or rejected critic marks and replaces with the opposite.
        Comments are removed and marks are replaced with their content.
        """

        accept = self.config["mode"] == 'accept'
        if kind == INS:
            return text if accept else ''
        elif kind == DEL:
            return '' if accept else text
        elif kind == MARK:
            return text
        elif kind == COMMENT:
            return ''
        else:
            return sub_text if accept else text

    def html_escape(self, txt, strip_nl=False):
        """Basic html escaping."""

        txt = txt.replace('&', '&amp;')
        txt = txt.replace('<', '&lt;')
        txt = txt.replace('>', '&gt;')
        txt = txt.replace('"', '&quot;')
        txt = txt.replace("\n", "<br>" if not strip_nl else ' ')
        return txt

    def run(self, lines):
        """Process critic marks."""

        # Determine processor type to use
        if self.config['mode'] == "view":
            processor = self.critic_view
        else:
            processor = self.critic_parse

        # Find and process critic marks
        text = '\n'.join(lines)
        result = []
        last = 0
        for start, end, kind, content, sub_text in find_critics(text):
            result.append(text[last:start])
            result.append(processor(kind, content, sub_text))
            last = end
        result.append(text[last:])
        text = ''.join(result)

        return text.split('\n')


class CriticExtension(Extension):
    """Critic extension."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'mode': [
                'view',
                "Critic mode to run in: 'view', 'accept', or 'reject' - Default: view "
            ],
            'raw_view': [False, "Raw view keeps the output as the raw markup for view mode - Default False"]
        }

        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        """Register the extension."""

        md.registerExtension(self)
        self.critic_stash = CriticStash(CRITIC_KEY)
        post = CriticsPostprocessor(self.critic_stash)
        critic = CriticViewPreprocessor(self.critic_stash)
        critic.config = self.getConfigs()
        md.preprocessors.register(critic, "critic", 31.1)
        md.postprocessors.register(post, "critic-post", 25)
        md.registerExtensions(["pymdownx._bypassnorm"], {})

    def reset(self):
        """Clear stash."""

        self.critic_stash.clear()


def makeExtension(*args, **kwargs):
    """Return extension."""

    return CriticExtension(*args, **kwargs)
