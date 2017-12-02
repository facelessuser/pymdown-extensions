# Tilde

## Overview

Tilde optionally adds two different features which are syntactically built around the `~` character: **delete** which inserts `#!html <del></del>` tags and **subscript** which inserts `#!html <sub></sub>` tags.

## Delete

To wrap content in a **delete** tag, simply surround the text with double `~`. You can also enable `smart_delete` in the [options](#options). Smart behavior of **delete** models that of [BetterEm](betterem.md#differences).

!!! example "Delete Example"

    ```
    ~~Delete me~~
    ```

    ~~Delete me~~

## Subscript

To denote a subscript, you can surround the desired content in single `~`.  It uses Pandoc style logic, so if your subscript needs to have spaces, you must escape the spaces.

!!! example "Subscript Example"

    ```
    CH~3~CH~2~OH

    text~a\ subscript~
    ```

    CH~3~CH~2~OH

    text~a\ subscript~

## Options

Option         | Type | Default     | Description
-------------- | ---- | ----------- | -----------
`smart_delete` | bool | `#!py3 True` | Use smart logic with delete characters.
`delete`       | bool | `#!py3 True` | Enable delete feature.
`subscript`    | bool | `#!py3 True` | Enable subscript feature.
