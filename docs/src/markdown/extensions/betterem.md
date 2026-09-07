---
icon: lucide/asterisk
---
[:octicons-file-code-24:][_betterem]{: .source-link }

# BetterEm

## Overview

> [!new] New in 12.0
> BetterEm was rewritten from the ground up. Results should be the closest to CommonMark parsing that is possible within
> Python Markdown. Some subtle difference may be observed compared to older versions, but these changes were made to
> align better with expected nesting conventions in the majority of parsers and to improve performance.

BetterEm is an extension that aims to improve emphasis (bold and italic) handling over the standard Python Markdown
handling. In general, parsing behavior should be much closer to other parsers, within the bounds of what Python Markdown
is capable of.

BetterEm provides a **smart** which controls whether emphasis is processed mid-word or not. When `smart_enable` is
enabled, mid-word emphasis is intelligently ignored. This can be applied to asterisk and underscore emphasis, but since
it usually only desirable to avoid mid-word emphasis in with underscores, it is only enabled for underscores by
default.

With the default behavior, the feel will be very similar to GFM bold and italic, within the bounds of what Python
Markdown is capable of.

The BetterEm extension can be included in Python Markdown by using the following:

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.betterem'])
```

/// important | Reminder
Remember to read the [Usage Notes](../usage_notes.md) for information that may be relevant when using this
extension!
///

/// note | Note
For all examples on this page, underscores are __smart__ and asterisks are not.
///

BetterEm requires that non-whitespace characters follow the opening token(s) and precede the closing token(s).

```text title="Whitespace"
This * won't emphasize *

This *will emphasize*
```

/// html | div.result
This * won't emphasize *

This *will emphasize*
///

BetterEm allows for a more natural nested token feel.

```text title="Nested Token"
***I'm italic and bold* I am just bold.**

***I'm bold and italic!** I am just italic.*
```

/// html | div.result
***I'm italic and bold* I am just bold.**

***I'm bold and italic!** I am just italic.*
///

BetterEm will try to prioritize the more sane option when nesting bold (`**`) between italic (`*`).

```text title="Prioritize Best"
*I'm italic. **I'm bold and italic.** I'm also just italic.*

**I'm bold. *I'm bold and italic.* I'm also just bold.**
```

/// html | div.result
*I'm italic. **I'm bold and italic.** I'm also just italic.*

**I'm bold. *I'm bold and italic.* I'm also just bold.**
///

## Options

Option         | Type   | Default             | Description
-------------- | ------ | ------------------- | -----------
`smart_enable` | string | `#!py3 'underscore'` | A string that specifies whether smart should be enabled for `all`, `asterisk`, `underscore`, or `none`.
