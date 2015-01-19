from __future__ import unicode_literals
from markdown import Extension

extensions = [
    'markdown.extensions.tables',
    'pymdownx.magiclink',
    'pymdownx.betterem',
    'pymdownx.tilde',
    'pymdownx.githubemoji',
    'pymdownx.tasklist',
    'pymdownx.headeranchor',
    'pymdownx.superfences',
    'markdown.extensions.nl2br'
]

extension_configs = {
    "pymdownx.tilde": {
        "subscript": False
    }
}


class GithubExtension(Extension):
    """Add various extensions to Markdown class"""

    def extendMarkdown(self, md, md_globals):
        """Register extension instances"""
        md.registerExtensions(extensions, extension_configs)


def makeExtension(*args, **kwargs):
    return GithubExtension(*args, **kwargs)
