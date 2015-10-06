# Mark {: .doctitle}
Mark syntax.

---

## Overview
Mark adds the ability to insert `#!html <mark></mark>` tags.  The syntax requires the text to be surrounded by double equal signs.  Syntax behavior for smart and non-smart variants of **mark** models that of [betterem](betterem.md#differences).

## Options

| Option    | Type | Default | Description |
|-----------|------|---------|-------------|
| smart_mark | bool | True | Use smart logic with mark characters: `==mark==me==` --> ==mark==me==. |

## Examples
Mark adds `mark` tags when inline text is surrounded by double equal signs: `==mark me==` --> ==mark me==.  It can optionally be configured to use smart logic: `==mark==me==` --> ==mark==me==.
