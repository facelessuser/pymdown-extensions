# PyMdown Extensions

## Overview

PyMdown Extensions is a collection of extensions for Python Markdown. They were originally written to make writing
documentation more enjoyable. They cover a wide range of solutions, and while not every extension is needed by all
people, there is usually at least one useful extension for everybody.

## Usage

All extensions are found under the module namespace of `pymdownx`.  Assuming we wanted to specify the use of the
MagicLink extension, we would include it in Python Markdown like so:

```pycon3
>>> import markdown
>>> text = "A link https://google.com"
>>> html = markdown.markdown(text, extensions=['pymdownx.magiclink'])
'<p>A link <a href="https://google.com">https://google.com</a></p>'
```

Check out documentation on each extension to learn more about how to configure and use each one.

/// danger | Reminder
Please read the [Usage Notes](usage_notes.md) for information on extension compatibility and general notes to be
aware of when using these extensions.
///

## Extensions

&nbsp;                                       | Extensions                               | &nbsp;
-------------------------------------------- | ---------------------------------------- | ------
[Arithmatex](extensions/arithmatex.md)       | [B64](extensions/b64.md)                 | [BetterEm](extensions/betterem.md)
[Blocks](extensions/blocks/index.md)         | [Caret](extensions/caret.md)             | [Critic](extensions/critic.md)
[Details](extensions/details.md)             | [Emoji](extensions/emoji.md)             | [EscapeAll](extensions/escapeall.md)
[Extra](extensions/extra.md)                 | [Highlight](extensions/highlight.md)     | [InlineHilite](extensions/inlinehilite.md)
[Keys](extensions/keys.md)                   | [MagicLink](extensions/magiclink.md)     | [Mark](extensions/mark.md)
[PathConverter](extensions/pathconverter.md) | [ProgressBar](extensions/progressbar.md) | [SaneHeaders](extensions/saneheaders.md)
[SmartSymbols](extensions/smartsymbols.md)   | [Snippets](extensions/snippets.md)       | [StripHTML](extensions/striphtml.md)
[SuperFences](extensions/superfences.md)     | [Tabbed](extensions/tabbed.md)           | [Tasklist](extensions/tasklist.md)
[Tilde](extensions/tilde.md)                 |                                          |
