---
icon: lucide/highlighter
---
[:octicons-file-code-24:][_mark]{: .source-link }

# Mark

## Overview

> [!new] New in 12.0
> Mark was rewritten from the ground up. Some subtle difference may be observed compared to older versions, but these
> changes were made to align better with expected nesting conventions in the majority of parsers and to improve
> performance.

Mark adds the ability to insert `#!html <mark></mark>` tags.  The syntax requires the text to be surrounded by double
equal signs. It can optionally be configured to use smart logic. Syntax behavior for smart and non-smart variants of
**mark** models that of [BetterEm](betterem.md).

To Mark some text, simply surround the text with double `=`.

```text title="Marking"
==mark me==

==smart==mark==
```

/// html | div.result
==mark me==

==smart==mark==
///

The Mark extension can be included in Python Markdown by using the following:

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.mark'])
```

## Options

Option       | Type | Default     | Description
------------ | ---- | ----------- |------------
`smart_mark` | bool | `#!py3 True` | Use smart logic with mark characters.
