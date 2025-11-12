[:octicons-file-code-24:][_betterem]{: .source-link }

# BetterEm

## Overview

BetterEm is an extension that aims to improve emphasis (bold and italic) handling.

BetterEm provides a **smart** which controls whether emphasis is processed mid-word or not. When `smart_enable` is
enabled, mid-word emphasis is intelligently ignored. This can be applied to asterisk and underscore emphasis, but since
it usually only desireable to avoid mid-word emphasis in with underscores, it is only enabled for underscores by
default.

With the default behavior, the feel will be very similar to GFM bold and italic, within the bounds of what Python
Markdown is capable of.

The BetterEm extension can be included in Python Markdown by using the following:

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.betterem'])
```

/// danger | Reminder
Remember to read the [Usage Notes](../usage_notes.md) for information that may be relevant when using this
extension!
///

## Rules

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
```

/// html | div.result
*I'm italic. **I'm bold and italic.** I'm also just italic.*
///


BetterEm will ensure smart mode doesn't terminate in scenarios where there are a large amount of consecutive tokens
inside.

```text title="Consecutive Token"
___A lot of underscores____________is okay___
```

/// html | div.result
___A lot of underscores____________is okay___
///

BetterEm will also ensure that smart mode breaks properly when an inner like token signifies an end.

```text title="Smart Break"
__This will all be bold __because of the placement of the center underscores.__

__This will all be bold __ because of the placement of the center underscores.__

__This will NOT all be bold__ because of the placement of the center underscores.__

__This will all be bold_ because of the token is less than that of the surrounding.__
```

/// html | div.result
__This will all be bold __because of the placement of the center underscores.__

__This will all be bold __ because of the placement of the center underscores.__

__This will NOT all be bold__ because of the placement of the center underscores.__

__This will all be bold_ because the token count is less than that of the surrounding.__
///

BetterEm will allow non-smart emphasis to contain "floating" like tokens.

```text title="Floating Token"
*All will * be italic*

*All will *be italic*

*All will not* be italic*

*All will not ** be italic*

**All will * be bold**

**All will *be bold**

**All will not*** be bold**

**All will not *** be bold**
```

/// html | div.result
*All will * be italic*

*All will *be italic*

*All will not* be italic*

*All will ** be italic*

**All will * be bold**

**All will *be bold**

**All will not*** be bold**

**All will not ***be bold**
///

## Options

Option         | Type   | Default             | Description
-------------- | ------ | ------------------- | -----------
`smart_enable` | string | `#!py3 'underscore'` | A string that specifies whether smart should be enabled for `all`, `asterisk`, `underscore`, or `none`.
