# Tabbed

## Overview

Tabbed provides a syntax to easily add tabbed Markdown content. The Tabbed extension can be included in Python Markdown
by using the following:

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.tabbed'])
```

## Syntax

Tabs start with `===` to signify a tab followed by a quoted title. Consecutive tabs are grouped into a tab set.

```
=== "Tab 1"
    Markdown **content**.

    Multiple paragraphs.

=== "Tab 2"
    More Markdown **content**.

    - list item a
    - list item b
```

This will yield tabbed Markdown content:

=== "Tab 1"
    Markdown **content**.

    Multiple paragraphs.

=== "Tab 2"
    More Markdown **content**.

    - list item a
    - list item b

In the rare case that you want to follow two separate tab sets right after each other, you can explicitly mark the start
of a new tab set with `!`:

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

Which should yield two tab sets.

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
