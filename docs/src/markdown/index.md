# PyMdown Extensions

## Overview

PyMdown Extensions is a collection of extensions for Python Markdown. They were originally written to make writing
documentation more enjoyable. They cover a wide range of solutions, and while not every extension is needed by all
people, there is usually at least one useful extension for everybody.

## Usage

All extensions are found under the module namespace of `pymdownx`.  Assuming we wanted to specify the use of the
MagicLink extension, we would include it in Python Markdown like so:

```pycon3
>>> import markdown
>>> text = "A link https://google.com"
>>> html = markdown.markdown(text, extensions=['pymdownx.magiclink'])
'<p>A link <a href="https://google.com">https://google.com</a></p>'
```

Check out documentation on each extension to learn more about how to configure and use each one.

!!! danger "Reminder"
    Please read the [Usage Notes](usage_notes.md) for information on extension compatibility and general notes to be
    aware of when using these extensions.

## Extensions

!!! summary "Arithmatex"
    [Arithmatex](extensions/arithmatex.md) is an extension that preserves LaTeX math equations ($\frac{\sqrt x}{y^3}$)
    during the Markdown conversion process so that they can be used with [MathJax][mathjax].

!!! summary "B64"
    [B64](extensions/b64.md) converts all local images in a document to base64 encoding and embeds them in the document.

!!! summary "BetterEm"
    [BetterEm](extensions/betterem.md) is a different approach to **emphasis** than Python Markdown's default.  It works
    similar but handles certain corner cases differently.

!!! summary "Caret"
    [Caret](extensions/caret.md) is an extension that is syntactically built around the `^` character. It adds support
    for inserting super^scripts^ and adds an easy way to place ^^text^^ in an `#!html <ins>` tag.

!!! summary "Critic"
    [Critic](extensions/critic.md) adds handling and support of [Critic Markup][critic-markup].

!!! summary "Details"
    [Details](extensions/details.md) creates collapsible elements with `#!html <details><summary>` tags.

    ??? note "Click Me!"
        Thanks!

!!! summary "Emoji"
    [Emoji](extensions/emoji.md) makes adding emoji via Markdown easy :smile:.

!!! summary "EscapeAll"
    [EscapeAll](extensions/escapeall.md) allows the escaping of any character, some with additional effects.  Check it
    out to learn more.

!!! summary "Extra"
    [Extra](extensions/extra.md) is just like Python Markdown's Extra package except it uses PyMdown Extensions to
    substitute similar extensions.

!!! summary "Highlight"
    [Highlight](extensions/highlight.md) allows you to configure the syntax highlighting of
    [SuperFences](extensions/superfences.md) and [InlineHilite](extensions/inlinehilite.md).  Also passes standard
    Markdown indented code blocks through the syntax highlighter.

!!! summary "InlineHilite"
    [InlineHilite](extensions/inlinehilite.md) highlights inline code: `#!py3 from module import function as func`.

!!! summary "Keys"
    [Keys](extensions/keys.md) makes inserting key inputs into documents as easy as pressing ++ctrl+alt+delete++.

!!! summary "MagicLink"
    [MagicLink](extensions/magiclink.md) linkafies URL and email links without having to wrap them in Markdown syntax.
    Also, shortens repository issue, pull request, and commit links automatically for popular code hosting providers.
    You can even use special shorthand syntax to link to issues, diffs, and even mention people

!!! summary "Mark"
    [Mark](extensions/mark.md) allows you to ==mark== words easily.

!!! summary "PathConverter"
    [PathConverter](extensions/pathconverter.md) converts paths to absolute or relative to a given base path.

!!! summary "ProgressBar"
    [ProgressBar](extensions/progressbar.md) creates progress bars quick and easy.

    [== 80%]{: .candystripe .candystripe-animate}

!!! summary "SaneHeaders"
    [SaneHeaders](extensions/saneheaders.md) modifies hash headers to only be evaluated if the starting hash symbols are
    followed by at least one space. This is useful if you use other extensions that also use the hash symbol (like our
    own MagicLink extension).

!!! summary "SmartSymbols"
    [SmartSymbols](extensions/smartsymbols.md) inserts commonly used Unicode characters via simple ASCII
    representations: `=/=` --> =/=.

!!! summary "Snippets"
    [Snippets](extensions/snippets.md) include other Markdown or HTML snippets into the current Markdown file being
    parsed.

!!! summary "StripHTML"
    [StripHTML](extensions/striphtml.md) can strip out HTML comments and specific tag attributes.

!!! summary "SuperFences"
    [SuperFences](extensions/superfences.md) is like Python Markdown's fences, but better. Nest fences under lists,
    admonitions, and other syntaxes. You can even create special custom fences for content like UML.

    === "Output"

        ```diagram
        graph TB
            c1-->a2
            subgraph one
            a1-->a2
            end
            subgraph two
            b1-->b2
            end
            subgraph three
            c1-->c2
            end
        ```

    === "Markdown"

        ````
        ```diagram
        graph TB
            c1-->a2
            subgraph one
            a1-->a2
            end
            subgraph two
            b1-->b2
            end
            subgraph three
            c1-->c2
            end
        ```
        ````

!!! summary "Tabbed"
    [Tabbed](extensions/tabbed.md) allows for tabbed Markdown content:

    === "Tab 1"
        Markdown **content**.

    === "Tab 2"
        More Markdown **content**.

!!! summary "Tasklist"
    [Tasklist](extensions/tasklist.md) allows inserting lists with check boxes.

    - [x] eggs
    - [x] bread
    - [ ] milk

!!! summary "Tilde"
    [Tilde](extensions/tilde.md) is syntactically built around the `~` character. It adds support for inserting
    sub~scripts~ and adds an easy way to place ~~text~~ in a `#!html <del>` tag.
