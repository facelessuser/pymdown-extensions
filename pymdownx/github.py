"""
Github.

pymdown.github
Load up extension to get a Github Flavored Markdown feel.

MIT license.

Copyright (c) 2014 - 2015 Isaac Muse <isaacmuse@gmail.com>

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
import warnings

extensions = [
    'markdown.extensions.tables',
    'pymdownx.magiclink',
    'pymdownx.betterem',
    'pymdownx.tilde',
    'pymdownx.githubemoji',
    'pymdownx.tasklist',
    'pymdownx.headeranchor',
    'pymdownx.superfences'
]

legacy_extensions = [
    'markdown.extensions.nl2br'
]

extension_configs = {
    "pymdownx.tilde": {
        "subscript": False
    },
    "pymdownx.betterem": {
        "smart_enable": "all"
    }
}

legacy_extension_configs = {}


class GithubExtension(Extension):
    """Add various extensions to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'no_nl2br': [
                False,
                "Don't use nl2br extension.  Latest Github Flavored Markdown"
                " no longer uses the equivalent of nl2br.  In the future, this will be"
                " defaulted to 'True'. - Default: False"
            ]
        }
        super(GithubExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """Register extension instances."""

        no_nl2br = self.getConfigs()["no_nl2br"]
        if not no_nl2br:
            warnings.warn(
                "The pymdown.github extension has added a new config "
                "'no_nl2br' which will be defaulted to 'True' in the future."
                "\nThis is to be compliant with recent Github Flavored Markdown.",
                FutureWarning
            )

        exts = extensions if no_nl2br else extensions + legacy_extensions
        exts_config = extension_configs.copy()
        if not no_nl2br:
            exts_config.update(legacy_extension_configs)

        md.registerExtensions(exts, exts_config)


def makeExtension(*args, **kwargs):
    """Return extension."""

    return GithubExtension(*args, **kwargs)
