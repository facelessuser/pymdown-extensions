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
import warnings
from . import emoji
from .util import PymdownxDeprecationWarning

extensions = [
    'markdown.extensions.tables',
    'pymdownx.magiclink',
    'pymdownx.betterem',
    'pymdownx.tilde',
    'pymdownx.emoji',
    'pymdownx.tasklist',
    'pymdownx.superfences'
]

legacy_extensions = [
    'markdown.extensions.nl2br'
]

extension_configs = {
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
    },
    "pymdownx.magiclink": {}
}

legacy_extension_configs = {}


class GithubExtension(Extension):
    """Add various extensions to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'repo_url_shortener': [
                False,
                "If 'True' repo commit and issue links are shortened - Default: False"
            ],
            'base_repo_url': [
                '',
                'The base repo url to use - Default: ""'
            ],
            'no_nl2br': [
                True,
                "Don't use nl2br extension.  Latest Github Flavored Markdown"
                " no longer uses the equivalent of nl2br.  In the future, this will be"
                " defaulted to 'True'. - Default: False"
            ]
        }
        super(GithubExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """Register extension instances."""

        config = self.getConfigs()
        no_nl2br = config["no_nl2br"]
        if not no_nl2br:
            warnings.warn(
                "The pymdown.github extension does not enable nl2br anymore by default."
                "\nThis is to ensure compliance with recent Github Flavored Markdown."
                "\n'no_nl2br' is deprecated and will be removed in a future version."
                "\nPlease manually include markdown.extensions.nl2br if you wish to continue using.",
                PymdownxDeprecationWarning
            )

        exts = extensions if no_nl2br else extensions + legacy_extensions
        exts_config = extension_configs.copy()
        exts_config['pymdownx.magiclink']['repo_url_shortener'] = config['repo_url_shortener']
        exts_config['pymdownx.magiclink']['base_repo_url'] = config['base_repo_url']
        if not no_nl2br:
            exts_config.update(legacy_extension_configs)

        md.registerExtensions(exts, exts_config)


def makeExtension(*args, **kwargs):
    """Return extension."""

    return GithubExtension(*args, **kwargs)
