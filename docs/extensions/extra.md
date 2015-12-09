# Extra {: .doctitle}
PHP Markdown Extra extensions.

---

## Overview
Python Markdown provides an `extra` extension to provide features similar to PHP Markdown Extra.  PyMdown Extensions aims to provide not only new features, but to improve behavior in Python Markdown's existing feature set.  Some of these things can be at odds.  Python Markdown's `smartstrong` and `fenced_code` are not compatible with PyMdown Extensions' `betterem` and `superfences`.  `smartstong` should never be loaded at the same time as `betterem`, and `superfences` should not be loaded at the same time as `fenced_code`.  Because of this, it is not possible to use Python Markdown's `extra` and PyMdown's `superfences` and `betterem`. To make this less frustrating, PyMdown provides it's own implementation of `extra`.

PyMdown's `extra` is just like Python Markdown's extra except `smartstrong` is replaced by `betterem` and `fenced_code` is replaced by `superfences`.  All other features and extensions should be identical because we are using the same ones.

This extension is a convenience extension, and it currently provides no other additional features.  But remember **don't use `pymdownx.extra` while also using `markdown.extensions.extra`**!

!!! Caution "Reminder"
    Remember to read the [Usage Notes](../usage_notes.md) for information that may be relevant when using this extension!

Extensions:

| Extension | Options | Name   |
|-----------|---------|--------|
| [betterem](./betterem.md)                                                              | | pymdownx.betterem |
| [superfences](./superfences.md)                                                        | | pymdownx.superfences |
| [Footnotes](https://pythonhosted.org/Markdown/extensions/footnotes.html)               | | markdown.extensions.footnotes |
| [Attribute Lists](https://pythonhosted.org/Markdown/extensions/attr_list.html)         | | markdown.extensions.attr_list |
| [Definition Lists](https://pythonhosted.org/Markdown/extensions/definition_lists.html) | | markdown.extensions.def_list |
| [Tables](https://pythonhosted.org/Markdown/extensions/tables.html)                     | | markdown.extensions.tables |
| [Abbreviations](https://pythonhosted.org/Markdown/extensions/abbreviations.html)       | | markdown.extensions.abbr |
| [extrarawhtml](./extrarawhtml.md)                                                      | | pymdownx.extrarawhtml |
