# Extensions {: .doctitle}
Additional tilde based syntax.

---

## Overview
Tilde optionally adds two different features which are syntactically built around the `~` character: **delete** which inserts `#!html <del></del>` tags and **subscript** which inserts `#!html <sub></sub>` tags.  Syntax behavior for smart and non-smart variants of **delete** models that of [betterem](betterem.md#differences).

## Options

| Option    | Type | Default | Description |
|-----------|------|---------|-------------|
| smart_delete | bool | True | Use smart logic with delete characters: `~~delete~~me~~` --> ~~delete~~me~~. |
| delete | bool | True | Enable delete feature. |
| subscript | bool | True | Enable subscript feature. |

## Examples
The first feature adds delete emphasis (`del` tags) when inline text is surrounded by double tildes: `~~delete me~~` --> ~~delete me~~.  It can optionally be configured to use smart logic: `~~delete~~me~~` --> ~~delete~~me~~.

The second feature adds subscripts using single tildes: `CH~3~CH~2~OH` --> CH~3~CH~2~OH.  It uses Pandoc style logic, so if your subscript needs to have spaces, you must escape the spaces: `text~a\ subscript~` --> text~a\ subscript~.
