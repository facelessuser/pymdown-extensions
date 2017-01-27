"""
Slugs.

Additional slug outputs.

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
import sys
import re
import unicodedata
from . import util
PY3 = sys.version_info >= (3, 0) and sys.version_info < (4, 0)

RE_TAGS = re.compile(r'''</?[^>]*>''', re.UNICODE)
RE_WORD = re.compile(r'''[^\w\- ]''', re.UNICODE)


def uslugify(text, sep):
    """Unicode slugify (utf-8)."""

    # Normalize, Strip html tags, strip leading and trailing whitespace, and lower
    tag_id = RE_TAGS.sub('', unicodedata.normalize('NFKD', text)).strip().lower()
    # Remove non word characters, non spaces, and non dashes, and convert spaces to dashes.
    return RE_WORD.sub('', tag_id).replace(' ', sep)


def uslugify_encoded(text, sep):
    """Custom slugify (percent encoded)."""

    # Strip html tags and lower
    tag_id = RE_TAGS.sub('', unicodedata.normalize('NFKD', text)).lower()
    # Remove non word characters or non spaces and dashes
    # Then convert spaces to dashes
    tag_id = RE_WORD.sub('', tag_id).replace(' ', sep)
    # Encode anything that needs to be
    return util.quote(tag_id.encode('utf-8'))
