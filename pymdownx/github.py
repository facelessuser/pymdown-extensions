"""
Github.

pymdown.github
Load up extension to get a Github Flavored Markdown feel.

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
from __future__ import unicode_literals
from markdown import Extension
from . import emoji

extensions = [
    'markdown.extensions.tables',
    'pymdownx.magiclink',
    'pymdownx.betterem',
    'pymdownx.tilde',
    'pymdownx.emoji',
    'pymdownx.tasklist',
    'pymdownx.superfences'
]


class GithubExtension(Extension):
    """Add various extensions to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {}

        self.extension_configs = {
            "pymdownx.tilde": {
                "subscript": False
            },
            "pymdownx.emoji": {
                "emoji_index": emoji.gemoji,
                "alt": "unicode",
                "options": {
                    "attributes": {
                        "align": "absmiddle",
                        "height": "20px",
                        "width": "20px"
                    }
                }
            }
        }

        for ext in extensions:
            if ext in kwargs:
                self.extension_configs[ext] = kwargs.pop(ext)
        super(GithubExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """Register extension instances."""

        md.registerExtensions(extensions, self.extension_configs)


def makeExtension(*args, **kwargs):
    """Return extension."""

    return GithubExtension(*args, **kwargs)
