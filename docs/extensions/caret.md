# Caret {: .doctitle}
Additional caret based syntax.

---

## Overview
Caret optionally adds two different features which are syntactically built around the `^` character: **insert** which inserts `#!html <ins></ins>` tags and **superscript** which inserts `#!html <sup></sup>` tags.  Syntax behavior for smart and non-smart variants of **insert** models that of [betterem](betterem.md#differences).

## Options

| Option    | Type | Default |  Description |
|-----------|------|---------|--------------|
| smart_insert | bool | True |Use smart logic with insert characters: `^^underline^^me^^` --> ^^underline^^me^^. |
| insert | bool | True | Enable insert feature. |
| superscript | bool | True |Enable superscript feature. |

## Examples
The first feature adds underline emphasis (`ins` tags) when inline text is surrounded by double carets: `^^underline me^^` --> ^^underline me^^.  It can optionally be configured to use smart logic: `^^underline^^me^^` --> ^^underline^^me^^.

The second feature adds superscript using single carets: `H^2^0` --> H^2^0.  It uses Pandoc style logic, so if your superscript needs to have spaces, you must escape the spaces: `text^a\ superscript^` --> text^a\ superscript^.
