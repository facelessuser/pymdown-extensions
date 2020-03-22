path: tree/master
source: pymdownx/extrarawhtml.py

# ExtraRawHTML

## Overview

!!! warning "Deprecated 6.3"
    ExtraRawHTML has been deprecated in 6.3.

    As of Python Markdown release 3.2, raw HTML handling has been broken out into a separate extensions called
    `md_in_html`. This change makes the existence of `extrarawhtml` redundant. It is advised that all users use
    `md_in_html` moving forward. `extrarawhtml` will be removed in a future version.

Python Markdown provides an `extra` extension that has features similar to PHP Markdown Extra.  For reasons covered in
[`pymdownx.extra`](./extra.md), PyMdown Extensions implements its own `extra` extension.  In order to accomplish this,
Python Markdown's raw HTML parsing functionality, which is used to parse nested Markdown inside HTML blocks, had to be
split out of the `extra` implementation.  Afterwards, it was decided to expose it as an independent extension to allow
people who maybe didn't want to use all of the features found in `extra`, but still wanted to use the parsing of nested
Markdown inside of HTML blocks.  This is basically a wrapper around Python Markdown's `extra` extension's raw HTML
parsing.  For more info see [Python Markdown's Extra documentation][nested-markdown].

!!! example "Raw HTML Example"

    === "HTML"
        ```html
        <div class="some-class"><p>Some <em>Markdown</em>! <img alt="😄" class="emojione" src="https://cdn.jsdelivr.net/emojione/assets/3.1/png/64/1f604.png" title=":smile:">
        </p></div>
        ```

    === "Markdown"
        ```html
        <div class="some-class" markdown="1">

        Some *Markdown*! :smile:
        </div>
        ```

The ExtraRawHTML extension can be included in Python Markdown by using the following:

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.extrarawhtml'])
```

--8<-- "links.txt"
