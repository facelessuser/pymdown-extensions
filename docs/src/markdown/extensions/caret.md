---
icon: lucide/superscript
---
[:octicons-file-code-24:][_caret]{: .source-link }

# Caret

## Overview

> [!new] New in 12.0
> Caret was rewritten from the ground up. Some subtle difference may be observed compared to older versions, but these
> changes were made to align better with expected nesting conventions in the majority of parsers and to improve
> performance.

Caret optionally adds two different features which are syntactically built around the `^` character. The first is
**insert** which inserts `#!html <ins></ins>` tags.  The second is **superscript** which inserts `#!html <sup></sup>`
tags.

The Caret extension can be included in Python Markdown by using the following:

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.caret'])
```

## Insert

To wrap content in an **insert** tag, simply surround the text with double `^`. You can also enable `smart_insert` in
the [options](#options). Smart behavior of **insert** models that of [BetterEm](betterem.md).

```text title="Insert"
^^Insert me^^
```

/// html | div.result
^^Insert me^^
///

## Superscript

To denote a superscript, you can surround the desired content in single `^`.  It uses Pandoc style logic, so if your
superscript needs to have spaces, you must escape the spaces.

```text title="Superscript"
X^2^ + 4x - 8

text^a\ superscript^
```

/// html | div.result
X^2^ + 4x - 8

text^a\ superscript^
///

If desired, the Pandoc requirement of "no spaces", unless they are escaped, can be disabled via the `no_space`
[option](#options).

```text title="Superscript"
X^2^ + 4x - 8

text^a superscript^
```

/// html | div.result
text^a superscript^
///

> [!new] New in 12.0
> `no_space` is new in 12.0.

## Options

Option         | Type | Default      | Description
-------------- | ---- | ------------ | -----------
`smart_insert` | bool | `#!py3 False`| Use smart logic with insert characters.
`insert`       | bool | `#!py3 True` | Enable insert feature.
`superscript`  | bool | `#!py3 True` | Enable superscript feature.
`no_space`     | bool | `#!py3 True` | Enable Pandoc style requirement of "no unescaped spaces".
