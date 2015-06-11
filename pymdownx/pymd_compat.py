"""
Fallback methods to remain compatible with Python Markdown's default.

Table of Contents Extension for Python-Markdown
===============================================
See <https://pythonhosted.org/Markdown/extensions/toc.html>
for documentation.
Oringinal code Copyright 2008 [Jack Miller](http://codezen.org)
All changes Copyright 2008-2014 The Python Markdown Project
License: [BSD](http://www.opensource.org/licenses/bsd-license.php)
"""
import re
import unicodedata
from markdown import util
IDCOUNT_RE = re.compile(r'^(.*)_([0-9]+)$')


def slugify(value, separator):
    """Slugify a string, to make it URL friendly."""

    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = re.sub('[^\w\s-]', '', value.decode('ascii')).strip().lower()
    return re.sub('[%s\s]+' % separator, separator, value)


def unique(id, ids):
    """Ensure id is unique in set of ids. Append '_1', '_2'... if not."""

    while id in ids or not id:
        m = IDCOUNT_RE.match(id)
        if m:
            id = '%s_%d' % (m.group(1), int(m.group(2)) + 1)
        else:
            id = '%s_%d' % (id, 1)
    ids.add(id)
    return id


def stashedHTML2text(text, md):
    """Extract raw HTML from stash, reduce to plain text and swap with placeholder."""

    def _html_sub(m):
        """Substitute raw html with plain text."""

        try:
            raw, safe = md.htmlStash.rawHtmlBlocks[int(m.group(1))]
        except (IndexError, TypeError):  # pragma: no cover
            return m.group(0)
        if md.safeMode and not safe:  # pragma: no cover
            return ''
        # Strip out tags and entities - leaveing text
        return re.sub(r'(<[^>]+>)|(&[\#a-zA-Z0-9]+;)', '', raw)

    return util.HTML_PLACEHOLDER_RE.sub(_html_sub, text)
