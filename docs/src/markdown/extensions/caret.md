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

> [!tip]
> PyMdown Extensions uses one delimiter processor for emphasis, deletions, insertions, subscripts, superscripts and
> marks via [BetterEm](betterem.md), [Tilde](tilde.md), Caret, and [Mark](mark.md). This allows all delimiter to be parsed
> simultaneously providing the best nesting logic. So for best results, pair Caret with [BetterEm](betterem.md).
>
> ```py3
> import markdown
> md = markdown.Markdown(extensions=['pymdownx.betterem', 'pymdownx.caret'])
> ```

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

> [!new] 12.2 CommonMark Punctuation Rule Change
> 12.0 introduced a rewrite of emphasis handling which brought emphasis handling into alignment with CommonMark rules.
> Caret, being based on the same core logic, inherits the same CommonMark rules.
>
> It was found that specifically the CommonMark punctuation rules were somewhat surprising for some when dealing with
> superscripts. In 12.2, for backwards compatibility, Caret now disables CommonMark punctuation rules any time
> superscript is enabled. If superscript is not enabled, insert notations will follow CommonMark punctuation rules.
>
> If it is desired to force CommonMark punctuation rules in superscript, [`punctuation`](#options) can be enabled in the
> options. You will need to escape punctuation any time it conflicts with CommonMark rules.

## Options

Option         | Type | Default      | Description
-------------- | ---- | ------------ | -----------
`smart_insert` | bool | `#!py3 False`| Use smart logic with insert characters.
`insert`       | bool | `#!py3 True` | Enable insert feature.
`superscript`  | bool | `#!py3 True` | Enable superscript feature.
`no_space`     | bool | `#!py3 True` | Enable Pandoc style requirement of "no unescaped spaces".
`punctuation`  | bool | `#!py3 False`| Enable CommonMark punctuation rules even when subscript tags are enabled".
