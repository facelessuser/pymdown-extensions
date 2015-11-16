# SmartSymbols {: .doctitle}
Auto-convert special symbols.

---

## Overview
SmartSymbols adds syntax for creating special characters such as trademarks, arrows, fractions, etc.  It basically allows for more "smarty-pants" type replacements.  It is meant to be used along side the Python Markdown's `smarty` extension.

## Options
| Option          | Type | Default | Description |
|-----------------|------|---------|-------------|
| trademark       | bool | True | Add syntax for tradmark symbol.   |
| copyright       | bool | True | Add syntax for copyright symbol.  |
| registered      | bool | True | Add syntax for registered symbol. |
| care_of         | bool | True | Add syntax for care / of.         |
| plusminus       | bool | True | Add syntax for plus / minus.      |
| arrows          | bool | True | Add syntax for creating arrows.   |
| notequal        | bool | True | Add syntax for not equal symbol.  |
| fractions       | bool | True | Add syntax for common fractions.  |
| ordinal_numbers | bool | True | Add syntax for ordinal numbers.   |

## Examples

| Markdown      | Result     |
|---------------|------------|
| `(tm)`        | (tm)       |
| `(c)`         | (c)        |
| `(r)`         | (r)        |
| `c/o`         | c/o        |
| `+/-`         | +/-        |
| `-->`         | -->        |
| `<--`         | <--        |
| `<-->`        | <-->       |
| `=/=`         | =/=        |
| `1/4, etc.`   | 1/4, etc.  |
| `1st 2nd etc.`|1st 2nd etc.|
