# Extra

## Overview

Python Markdown has an `extra` extension that provides features similar to PHP Markdown Extra.  PyMdown Extensions aims to provide not only new features, but to improve behavior in Python Markdown's existing feature set.  Some of these things can be at odds.  Python Markdown's `smartstrong` and `fenced_code` are not compatible with PyMdown Extensions' `betterem` and `superfences`.  `smartstong` should never be loaded at the same time as `betterem`, and `superfences` should not be loaded at the same time as `fenced_code`.  Because of this, it is not possible to use Python Markdown's `extra` and PyMdown's `superfences` and `betterem`. To make this less frustrating, PyMdown Extensions provides it's own implementation of `extra`.

PyMdown's `extra` is just like Python Markdown's extra except `smartstrong` is replaced by `betterem` and `fenced_code` is replaced by `superfences`.  All other features and extensions should be identical because we are using the same ones.

This extension is a convenience extension, and it currently provides no other additional features.  But remember **don't use `pymdownx.extra` while also using `markdown.extensions.extra`**!

!!! danger "Reminder"
    Remember to read the [Usage Notes](../usage_notes.md) for information that may be relevant when using this extension!

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
[ExtraRawHTML](./extrarawhtml.md)  | `pymdownx.extrarawhtml`

## Options

If you wish to configure the individual extensions included via this extensions, you can configure them by placing that sub extension's settings under a setting value that equals the sub extensions name.

```py
extension_configs = {
    'pymdownx.extra': {
        'markdown.extensions.footnotes': {
            'BACKLINK_TEXT': 'link'
        }
    }
}
```

--8<-- "links.md"
