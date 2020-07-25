[:octicons-file-code-24:][_smartsymbols]{: .source-link }

# SmartSymbols

## Overview

SmartSymbols adds syntax for creating special characters such as trademarks, arrows, fractions, etc.  It basically
allows for more "smarty-pants" like replacements.  It is meant to be used along side Python Markdown's `smarty`
extension not to replace.

Markdown       | Result
-------------- |--------
`(tm)`         | (tm)
`(c)`          | (c)
`(r)`          | (r)
`c/o`          | c/o
`+/-`          | +/-
`-->`          | -->
`<--`          | <--
`<-->`         | <-->
`=/=`          | =/=
`1/4, etc.`    | 1/4, etc.
`1st 2nd etc.` |1st 2nd etc.

The SmartSymbols extension can be included in Python Markdown by using the following:

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.smartsymbols'])
```

## Options

Option            | Type | Default     | Description
----------------- | ---- | ----------- |------------
`trademark`       | bool | `#!py3 True` | Add syntax for trademark symbol.
`copyright`       | bool | `#!py3 True` | Add syntax for copyright symbol.
`registered`      | bool | `#!py3 True` | Add syntax for registered symbol.
`care_of`         | bool | `#!py3 True` | Add syntax for care / of.
`plusminus`       | bool | `#!py3 True` | Add syntax for plus / minus.
`arrows`          | bool | `#!py3 True` | Add syntax for creating arrows.
`notequal`        | bool | `#!py3 True` | Add syntax for not equal symbol.
`fractions`       | bool | `#!py3 True` | Add syntax for common fractions.
`ordinal_numbers` | bool | `#!py3 True` | Add syntax for ordinal numbers.

--8<-- "links.txt"
