# PyMdown Extensions

## Usage

PyMdown Extensions is a collection of extensions for Python Markdown.  Keep in mind, the PyMdown extensions were designed to work with the default extensions, so your mileage may vary in regards to compatibility when paired with other 3rd party extensions.

All extensions are found under `pymdownx`.  Assuming we wanted to specify the use of the MagicLink extension, we would include it in Python Markdown like so:

```
import markdown
text = "A link https://google.com"
html = markdown.markdown(text, ['pymdownx.magiclink'])
```

Check out documentation on each extension to learn more about how to configure and use each one.

!!! danger "Reminder"
    Please read the [Usage Notes](usage_notes.md) for information on extension compatibility and general notes to be aware of when using these extensions.

## Extensions

??? summary "Arithmatex"
    [Arithmatex](extensions/arithmatex.md) is an extension that preserves LaTeX math equations ($\frac{\sqrt x}{y^3}$) during the Markdown conversion process so that they can be used with [MathJax][mathjax].

??? summary "B64"
    [B64](extensions/b64.md) converts all local images in a document to base64 encoding and embeds them in the document.

??? summary "BetterEm"
    [BetterEm](extensions/betterem.md) is a different approach to **emphasis** than Python Markdown's default.  It works similar but handles certain corner cases differently.

??? summary "Caret"
    [Caret](extensions/caret.md) is an extension that is syntactically built around the `^` character. It adds support for inserting super^scripts^ and adds an easy way to place ^^text^^ in an `#!html <ins>` tag.

??? summary "Critic"
    [Critic](extensions/critic.md) adds handling and support of [Critic Markup][critic-markup].

??? summary "Details"
    [Details](extensions/details.md) creates collapsible elements with `#!html <details><summary>` tags.

    ??? note "Click Me!"
        Thanks!

??? summary "Emoji"
    [Emoji](extensions/emoji.md) makes adding emoji via Markdown easy :smile:.

??? summary "EscapeAll"
    [EscapeAll](extensions/escapeall.md) allows the escaping of any character, some with additional effects.  Check it out to learn more.

??? summary "Extra"
    [Extra](extensions/extra.md) is just like Python Markdown's Extra package except it uses PyMdown Extensions to substitute similar extensions.

??? summary "ExtraRawHTML"
    [ExtraRawHTML](extensions/extrarawhtml.md) exposes Python Markdown's feature of parsing markdown in HTML blocks. No longer do you have to include all of Extra when all you want to do is parse Markdown in HTML blocks.

??? summary "GitHub"
    [GitHub](extensions/github.md) uses extensions from Python Markdown and PyMdown Extensions to give a GitHub-ish feel.

??? summary "Highlight"
    [Highlight](extensions/highlight.md) allows you to configure the syntax highlighting of SuperFences and InlineHilite.  Also passes standard Markdown indented code blocks through the syntax highlighter.

??? summary "Keys"
    [Keys](extensions/keys.md) makes inserting key inputs into documents as easy as pressing ++ctrl+alt+delete++.

??? summary "MagicLink"
    [MagicLink](extensions/magiclink.md) linkafies URL and email links without having to wrap them in Markdown syntax.

??? summary "Mark"
    [Mark](extensions/mark.md) allows you to ==mark== words easily.

??? summary "ProgressBar"
    [ProgressBar](extensions/progressbar.md) creates progress bars quick and easy.

    [== 75%]{: .success}

??? summary "SmartSymbols"
    [SmartSymbols](extensions/smartsymbols.md) inserts commonly used Unicode characters via simple ASCII representations: `=/=` --> =/=.

??? summary "Snippets"
    [Snippets](extensions/snippets.md) include other Markdown or HTML snippets into the current Markdown file being parsed.

??? summary "SuperFences"
    [SuperFences](extensions/superfences.md) is like Python Markdown's fences, but better. Nest fences under lists, admonitions, and other syntaxes. Also create special custom fences for content like UML.

    ```sequence
    Title: Here is a title
    A->B: Normal line
    B-->C: Dashed line
    C->>D: Open arrow
    D-->>A: Dashed open arrow
    ```

??? summary "Tasklist"
    [Tasklist](extensions/tasklist.md) allows inserting lists with check boxes.

    - [x] eggs
    - [x] bread
    - [ ] milk

??? summary "Tilde"
    [Tilde](extensions/tilde.md) is syntactically built around the `~` character. It adds support for inserting sub^scripts^ and adds an easy way to place ~~text~~ in a `#!html <del>` tag.

??? summary "InlineHilite"
    [InlineHilite](extensions/inlinehilite.md) highlights inline code: `#!py from module import function as func`.

??? summary "PathConverter"
    [PathConverter](extensions/pathconverter.md) convert paths to absolute or relative to a base path.

??? summary "PlainHTML"
    [PlainHTML](extensions/plainhtml.md) can strip out HTML comments and specific tag attributes.

--8<--
refs.md

uml.md

mathjax.md
--8<--
