# SmartSymbols

## Overview

SmartSymbols adds syntax for creating special characters such as trademarks, arrows, fractions, etc.  It basically allows for more "smarty-pants" like replacements.  It is meant to be used along side Python Markdown's `smarty` extension not to replace.

## Options

Option            | Type | Default     | Description
----------------- | ---- | ----------- |------------
`trademark`       | bool | `#!py True` | Add syntax for trademark symbol.
`copyright`       | bool | `#!py True` | Add syntax for copyright symbol.
`registered`      | bool | `#!py True` | Add syntax for registered symbol.
`care_of`         | bool | `#!py True` | Add syntax for care / of.
`plusminus`       | bool | `#!py True` | Add syntax for plus / minus.
`arrows`          | bool | `#!py True` | Add syntax for creating arrows.
`notequal`        | bool | `#!py True` | Add syntax for not equal symbol.
`fractions`       | bool | `#!py True` | Add syntax for common fractions.
`ordinal_numbers` | bool | `#!py True` | Add syntax for ordinal numbers.

## Examples

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
