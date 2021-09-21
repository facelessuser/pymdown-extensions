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

## Alternate Style

!!! new "New 9.0"

!!! warning "Experimental Feature"

The original idea behind the Tabbed extension was to provide a tabbed interface in Markdown that could be driven purely
by CSS. If JavaScript was disabled or unavailable, tab functionality would remain.

@squidfunk (Martin Donath), the author and maintainer of the [MkDocs Material theme][mkdocs-material], who originally
collaborated on the first Tabbed style, approached us again with a newer style.

The aim was to solve one big problem, namely that on narrower screen sizes (like mobile), tabs are broken onto separate
lines, like here for example. And this is indeed a real issue that is presented with the current style. The bonuses of
the current style is that it needs absolutely no JavaScript and is driven by CSS alone. It supports as many tabs as you
can throw at it but the downside is that when all the tabs do not fit on a single line, they'll wrap which is not
aesthetically pleasing in all themes or interfaces.

So, a new style was proposed and we once again worked to hammer out the details, and in the end, we think we have
something that is better in many ways. The new style works with only CSS and does not actually need any JavaScript to be
functional, but it is ideally enhanced with a little JavaScript. The reason why is that when too many tabs are on a
single line, you can overflow them with CSS and make the tab container scrollable. This can provide a much more
aesthetically pleasing interface. There are two caveats though:

1. When tabs overflow, if you want a visual indicator that there are more tabs, it requires a little JavaScript.
2. The number of tabs is limited by how many tabs you define in the CSS.

As for the first point, this seems an acceptable restraint. When JavaScript is available, you will get a nice visual
indicator, but if JavaScript is ever not available, or disabled, tab functionality will still work, just without the
indicators.

As for the second point, this also seems acceptable as most pages will usually have some upper limit of tabs that are
ever used. Pages can become quite cluttered when using too many tabs, and it seems reasonable that most would limit them
to some practical number.

Below is an testable example. Simply copy it into an HTML file and try it out in a browser.

??? example "Example HTML with CSS and JS"
    ```html
    ```

## Options

Option            | Type | Default       | Description
----------------- | ---- | ------------- | -----------
`alternate_style` | bool | `#!py3 False` | Use the experimental, alternative style.

--8<-- "refs.txt"
