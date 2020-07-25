[:octicons-file-code-24:][_tabbed]{: .source-link }

# Tabbed

## Overview

!!! new "New 7.0"
    Tabbed has been newly added in 7.0.

Tabbed provides a syntax to easily add tabbed Markdown content. The Tabbed extension can be included in Python Markdown
by using the following:

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.tabbed'])
```

## Syntax

Tabs start with `===` to signify a tab followed by a quoted title. Consecutive tabs are grouped into a tab set.

!!! example "Example Tabs"

    === "Output"
        === "Tab 1"
            Markdown **content**.

            Multiple paragraphs.

        === "Tab 2"
            More Markdown **content**.

            - list item a
            - list item b

    === "Markdown"
        ```
        === "Tab 1"
            Markdown **content**.

            Multiple paragraphs.

        === "Tab 2"
            More Markdown **content**.

            - list item a
            - list item b
        ```

In the rare case that you want to follow two separate tab sets right after each other, you can explicitly mark the start
of a new tab set with `!`.


!!! example "Example Tab Breaks"

    === "Output"
        === "Tab 1"
            Markdown **content**.

            Multiple paragraphs.

        === "Tab 2"
            More Markdown **content**.

            - list item a
            - list item b

        ===! "Tab A"
            Different tab set.

        === "Tab B"
            ```
            More content.
            ```

    === "Markdown"

        ```
        === "Tab 1"
            Markdown **content**.

            Multiple paragraphs.

        === "Tab 2"
            More Markdown **content**.

            - list item a
            - list item b

        ===! "Tab A"
            Different tab set.

        === "Tab B"
            ```
            More content.
            ```
        ```

## Styling with CSS

In order to use tabbed blocks, some additional CSS is needed. You can check out the configuration below which will
show the CSS and the HTML it targets. Keep in mind the CSS is just the minimum to get you started. You can tweak it and
modify it to get it how you like it.

In general, tabbed controls are wrapped in a `#!html <div>` with the class `tabbed-set`. They contain an
`#!html <input>` with an ID of `__tabbed_<tab_set_number>_<tab_number>`. All the `#!html <input>` elements from a
specific tab set will use the name `__tabbed_<tab_set_number>`. Particularly, a user should be mindful of the ID to keep
from explicitly using a conflicting ID. Auto-generated slugs shouldn't conflict though.

??? settings "Tabbed Code Setup"
    === "HTML"
        ```HTML
        <div class="tabbed-set">
        <input name="__tabbed_1" type="radio" id="__tabbed_1_1" checked="checked">
        <label for="__tabbed_1_1">Tab 0</label>
        <div class="tabbed-content">...</div>
        ...
        <input name="__tabbed_1" type="radio" id="__tabbed_1_X" checked="checked">
        <label for="__tabbed_1_X">Tab X</label>
        <div class="tabbed-content">...</div>
        ...
        </div>
        ```

    === "CSS"
        ```CSS
        .tabbed-set {
          display: flex;
          position: relative;
          flex-wrap: wrap;
        }

        .tabbed-set .highlight {
          background: #ddd;
        }

        .tabbed-set .tabbed-content {
          display: none;
          order: 99;
          width: 100%;
        }

        .tabbed-set label {
          width: auto;
          margin: 0 0.5em;
          padding: 0.25em;
          font-size: 120%;
          cursor: pointer;
        }

        .tabbed-set input {
          position: absolute;
          opacity: 0;
        }

        .tabbed-set input:nth-child(n+1) {
          color: #333333;
        }

        .tabbed-set input:nth-child(n+1):checked + label {
            color: #FF5252;
        }

        .tabbed-set input:nth-child(n+1):checked + label + .tabbed-content {
            display: block;
        }
        ```

--8<-- "links.txt"
