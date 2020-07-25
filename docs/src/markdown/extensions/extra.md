[:octicons-file-code-24:][_extra]{: .source-link }

# Extra

## Overview

Python Markdown has an `extra` extension that provides features similar to PHP Markdown Extra.  PyMdown Extensions aims
to provide not only new features, but to improve behavior in Python Markdown's existing feature set.  Some of these
things can be at odds.Python Markdown's `smartstrong` and `fenced_code` are not compatible with PyMdown Extensions'
`betterem` and `superfences`.  `smartstong` should never be loaded at the same time as `betterem`, and `superfences`
should not be loaded at the same time as `fenced_code`.  For these reasons, it is not possible to use Python Markdown's
`extra` and PyMdown Extensions' `superfences` and `betterem` at the same time. To make this less frustrating, PyMdown
Extensions provides it's own implementation of `extra`.

PyMdown Extensions' `extra` is just like Python Markdown's extra except `smartstrong` is replaced by `betterem` and
`fenced_code` is replaced by `superfences`.  All other features and extensions should be identical because we are using
the same ones.

This extension is a convenience extension, and it currently provides no other additional features.  But remember **don't
use `pymdownx.extra` while also using `markdown.extensions.extra`**!

!!! danger "Reminder"
    Remember to read the [Usage Notes](../usage_notes.md) for information that may be relevant when using this
    extension!

Extensions:

Extension                          | Name
---------------------------------- |--------
[BetterEm](./betterem.md)          | `pymdownx.betterem`
[SuperFences](./superfences.md)    | `pymdownx.superfences`
[Footnotes][footnotes]             | `markdown.extensions.footnotes`
[Attribute Lists][attr-list]       | `markdown.extensions.attr_list`
[Definition Lists][def-list]       | `markdown.extensions.def_list`
[Tables][tables]                   | `markdown.extensions.tables`
[Abbreviations][abbreviations]     | `markdown.extensions.abbr`
[Markdown in HTML][md-in-html]     | `markdown.extensions.md_in_html`

The Extra extension can be included in Python Markdown by using the following:

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.extra'])
```

## Options

If you wish to configure the individual extensions included via this extensions, you can configure them by placing that
sub extension's settings under a setting value that equals the sub extensions name.

```py3
extension_configs = {
    'pymdownx.extra': {
        'markdown.extensions.footnotes': {
            'BACKLINK_TEXT': 'link'
        }
    }
}
```

--8<-- "links.txt"
