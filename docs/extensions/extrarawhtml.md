# ExtraRawHtml {: .doctitle}
PHP Markdown Extra's raw HTML parsing.

---

## Overview
Python Markdown provides an `extra` extension to provide features similar to PHP Markdown Extra.  For reasons covered in [pymdownx.extra](./extra.md), PyMdown Extensions implements its own `extra` extension.  In order to accomplish this, Python Markdown's raw HTML parsing functionality, which is used to parse nested markdown inside HTML blocks, had to be split out of the `extra` implementation.  Afterwards, it was decided to leave it completely separate to allow people who maybe didn't want to use all of the features found in `extra`, but still wanted to use the parsing of nested Markdown inside of HTML blocks.  This is basically a wrapper around Python Markdown's `extra` extension, but it only implements the raw HTML parsing.  For more info see [Python Markdown's Extra documentation](https://pythonhosted.org/Markdown/extensions/extra.html#nested-markdown-inside-html-blocks).
