# Mark

## Overview

Mark adds the ability to insert `#!html <mark></mark>` tags.  The syntax requires the text to be surrounded by double equal signs. It can optionally be configured to use smart logic. Syntax behavior for smart and non-smart variants of **mark** models that of [BetterEm](betterem.md#differences).

To Mark some text, simply surround the text with double `=`.

!!! example "Mark Example"

    ```
    ==mark me==

    ==smart==mark==
    ```

    ==mark me==

    ==smart==mark==

## Options

Option       | Type | Default     | Description
------------ | ---- | ----------- |------------
`smart_mark` | bool | `#!py3 True` | Use smart logic with mark characters.
