# FAQ

## Function References in YAML

> How do I specify function references in YAML if I am using a module like [MkDocs][mkdocs]?

Pymdown Extensions has a number of extensions that expose customization via options that take function references. If
you are using a project like [MkDocs][mkdocs], which allows a user to configure Python Markdown extensions via YAML,
specifying function references may not be intuitive.

Keep in mind that the following examples specifically reference YAML configurations that are implemented via
[PyYAML][pyyaml] and are configured to allow Python objects.

When specifying a function reference in PyYAML, you must prepend the function with `#!yaml !!python/name:`. For
instance, to specify Python Markdown's Toc extension to use one of PyMdown Extensions' slugs in MkDocs:

```yaml
markdown_extensions:
  - markdown.extensions.toc:
      slugify: !!python/name:pymdownx.slugs.uslugify
      permalink: "\ue157"
```

To specify a particular emoji generator in the Emoji extension:

```yaml
markdown_extensions:
  - pymdownx.emoji:
      emoji_generator: !!python/name:pymdownx.emoji.to_png
```

## GitHub-ish Configurations

> How do I get GitHub Flavored Markdown?

A recommended GitHub configuration is provided below to emulate a setup that gives a GitHub feel.

For GitHub issue, commit, pull request, and mention shorthand syntax, you will also need to specify a `provider`, `user`
and `repo` in MagicLink's options below. This gives relative context for shorthand links (like `#1`) so that links can
properly be generated.  In the example below, we will use `facelessuser` and `pymdown-extensions` as the user and
repository respectively. See [MagicLink](./extensions/magiclink.md) for more details.

!!! tip
    If you are attempting to configure these options in a YAML based configuration (like in [MkDocs][mkdocs]), please
    see the related [FAQ question](#function-references-in-yaml) to see how to specify function references in YAML.

```py3
from pymdownx import emoji

extensions = [
    'markdown.extensions.tables',
    'pymdownx.magiclink',
    'pymdownx.betterem',
    'pymdownx.tilde',
    'pymdownx.emoji',
    'pymdownx.tasklist',
    'pymdownx.superfences',
    'pymdownx.saneheaders'
]

extension_configs = {
    "pymdownx.magiclink": {
        "repo_url_shortener": True,
        "repo_url_shorthand": True,
        "provider": "github",
        "user": "facelessuser",
        "repo": "pymdown-extensions"
    },
    "pymdownx.tilde": {
        "subscript": False
    },
    "pymdownx.emoji": {
        "emoji_index": emoji.gemoji,
        "emoji_generator": emoji.to_png,
        "alt": "short",
        "options": {
            "attributes": {
                "align": "absmiddle",
                "height": "20px",
                "width": "20px"
            },
            "image_path": "https://assets-cdn.github.com/images/icons/emoji/unicode/",
            "non_standard_image_path": "https://assets-cdn.github.com/images/icons/emoji/"
        }
    }
}
```

--8<-- "refs.txt"
