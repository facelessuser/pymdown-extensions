# Caret

## Overview

Caret optionally adds two different features which are syntactically built around the `^` character. The first is **insert** which inserts `#!html <ins></ins>`.  The second is **superscript** which inserts `#!html <sup></sup>` tags.

## Insert

To wrap content in an **insert** tag, simply surround the text with double `^`. You can also enable `smart_insert` in the [options](#options). Smart behavior of **insert** models that of [BetterEm](betterem.md#differences).

???+ example "Insert Example"

    ```
    ^^Insert me^^
    ```

    ^^Insert me^^

## Superscript

To denote a superscript, you can surround the desired content in single `^`.  It uses Pandoc style logic, so if your superscript needs to have spaces, you must escape the spaces.

!!! example "Superscript Example"

    ```
    H^2^0

    text^a\ superscript^
    ```

    H^2^0

    text^a\ superscript^

## Options

Option         | Type | Default | Description
-------------- | ---- | ------- | -----------
`smart_insert` | bool | True    |Use smart logic with insert characters.
`insert`       | bool | True    | Enable insert feature.
`superscript`  | bool | True    |Enable superscript feature.
