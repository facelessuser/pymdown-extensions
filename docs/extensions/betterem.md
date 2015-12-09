# BetterEm {: .doctitle}
Better Emphasis.

---

## Overview
BetterEm is an extension that aims to improve emphasis (bold and italic) handling.  It provides two modes for both asterisk's and underscore's bold and italic: **smart** when `smart_enable` is turned on and normal if `smart_enable` is turned off.  BetterEm overrides all the current bold and italic rules in Python Markdown with its own.  When **smart** is enabled for either asterisks and/or underscores, it is enabled for all variants: single, double, and triple.  When **smart** is enabled, the behavior will be very similar in feel to GFM bold and italic (but not necessarily exact).

!!! Caution "Reminder"
    Remember to read the [Usage Notes](../usage_notes.md) for information that may be relevant when using this extension!

## Differences

!!! Note "Note"
    For all examples on this page, underscores are __smart__ and asterisks are not.

BetterEm requires that non-whitespace characters follow the opening token(s) and precede the closing token(s).

| Test | Result |
|------|---------|
|`* Won't highlight *` | * Won't be italic * |
|`*Will highlight*` | *Will be italic* |

BetterEm allows for a more natural nested token feel.

| Test | Result |
|------|---------|
|`***I'm italic and bold* I am just bold.**` | ***I'm italic and bold* I am just bold.** |
|`***I'm bold and italic!** I am just italic.*` | ***I'm bold and italic!** I am just italic.* |

BetterEm will ensure smart mode doesn't terminate in scenarios where there are a large amount of consecutive tokens inside.

| Test | Result |
|------|---------|
|`___A lot of underscores____________is okay___` | ___A lot of underscores____________is okay___ |

BetterEm will also ensure that smart mode breaks proper when an inner like token signifies an end.

| Test | Result |
|------|---------|
|`__This will all be bold __because of the placement of the center underscores.__` | __This will all be bold __because of the placement of the center underscores.__ |
|`__This will all be bold __ because of the placement of the center underscores.__` | __This will all be bold __ because of the placement of the center asterisks.__ |
|`__This will NOT all be bold__ because of the placement of the center underscores.__` | __This will NOT all be bold__ because of the placement of the center underscores.__ |
|`__This will all be bold_ because of the token is less than that of the surrounding.__` | __This will all be bold_ because the token count is less than that of the surrounding.__ |

BetterEm will allow non-smart emphasis to contain "floating" like tokens.

| Test | Result |
|------|---------|
| `*All will * be italic*` | *All will * be italic* |
| `*All will *be italic*`  | *All will *be italic*  |
| `*All will not* be italic*` | *All will not* be italic* |
| `*All will not ** be italic*` | *All will not ** be italic* |
| `**All will * be bold**` | **All will * be bold** |
| `*All will *be bold**`  | **All will *be bold**  |
| `**All will not*** be bold**` | **All will not*** be bold** |
| `**All will not *** be bold**` | **All will not ***be bold** |


## Options

| Option    | Type | Default |Description |
|-----------|------|---------|------------|
| smart_enable | string | 'underscore' | A string that specifies whether smart should be enabled for `all`, `asterisk`, `underscore`, or `none`. |

Examples
```
Usage is the __same__ as usual.  Just keep in mind the _differences_.  Markdown is un**freaking**believable :smile:.
```

Usage is the __same__ as usual.  Just keep in mind the _differences_.  Markdown is un**freaking**believable :smile:.

*[GFM]:  Github Flavored Markdown
