---
icon: lucide/subscript
---
[:octicons-file-code-24:][_tilde]{: .source-link }

# Tilde

## Overview

> [!new] New in 12.0
> Tilde was rewritten from the ground up. Some subtle difference may be observed compared to older versions, but these
> changes were made to align better with expected nesting conventions in the majority of parsers and to improve
> performance.

Tilde optionally adds two different features which are syntactically built around the `~` character: **delete** which
inserts `#!html <del></del>` tags and **subscript** which inserts `#!html <sub></sub>` tags.

The Tilde extension can be included in Python Markdown by using the following:

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.tilde'])
```

> [!tip]
> PyMdown Extensions uses one delimiter processor for emphasis, deletions, insertions, subscripts, superscripts and
> marks via [BetterEm](betterem.md), Tilde, [Caret](caret.md), and [Mark](mark.md). This allows all delimiter to be parsed
> simultaneously providing the best nesting logic. So for best results, pair Tilde with [BetterEm](betterem.md).
>
> ```py3
> import markdown
> md = markdown.Markdown(extensions=['pymdownx.betterem', 'pymdownx.tilde'])
> ```

## Delete

To wrap content in a **delete** tag, simply surround the text with double `~`. You can also enable `smart_delete` in the
[options](#options). Smart behavior of **delete** models that of [BetterEm](betterem.md).

```text title="Delete"
~~Delete me~~
```

/// html | div.result
~~Delete me~~
///

## Subscript

To denote a subscript, you can surround the desired content in single `~`.  It uses Pandoc style logic, so if your
subscript needs to have spaces, you must escape the spaces.

```text title="Subscript"
CH~3~CH~2~OH

text~a\ subscript~
```

/// html | div.result
CH~3~CH~2~OH

text~a\ subscript~
///

If desired, the Pandoc requirement of "no spaces", unless they are escaped, can be disabled via the `no_space`
[option](#options).

```text title="Superscript"
text~a subscript~
```

/// html | div.result
text~a subscript~
///

> [!new] New in 12.0
> `no_space` is new in 12.0.

> [!new] 12.2 CommonMark Punctuation Rule Change
> 12.0 introduced a rewrite of emphasis handling which brought emphasis handling into alignment with CommonMark rules.
> Tilde, being based on the same core logic, inherits the same CommonMark rules.
>
> It was found that specifically the CommonMark punctuation rules were somewhat surprises for some when dealing with
> subscripts. In 12.2, for backwards compatibility, Tilde now disables CommonMark punctuation rules any time subscript
> is enabled. If subscript is not enabled, delete notations will follow CommonMark punctuation rules.
>
> If it is desired to force CommonMark punctuation rules in subscript, [`punctuation`](#options) can be enabled in the
> options. You will need to escape punctuation any time it conflicts with CommonMark rules.

## Options

Option         | Type | Default      | Description
-------------- | ---- | ------------ | -----------
`smart_delete` | bool | `#!py3 False`| Use smart logic with delete characters.
`delete`       | bool | `#!py3 True` | Enable delete feature.
`subscript`    | bool | `#!py3 True` | Enable subscript feature.
`no_space`     | bool | `#!py3 True` | Enable Pandoc style requirement of "no unescaped spaces".
`punctuation`  | bool | `#!py3 False`| Enable CommonMark punctuation rules even when subscript tags are enabled".
