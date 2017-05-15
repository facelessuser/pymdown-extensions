# Usage Notes

## Incompatible Extensions

PyMdown Extensions includes three extensions that are meant to **replace** their counterpart in the default Python Markdown extensions. You don't have to use all of PyMdown's extensions, but if you choose to use one of the packages below, you should use it instead of the Python Markdown one; **they cannot be loaded at the same time**.

Also, you shouldn't include an extension more than once. If you try to include more than one extension at the same time, you may get unexpected results.  Also, be aware of that some of the extensions are convenience extensions that include multiple extensions; be aware of what they include so you do not accidentally re-include them individually.

- `pymdownx.superfences` replaces `markdown.extensions.fenced_code`.

- `pymdownx.betterem` replaces `markdown.extensions.smartstrong`.

- `pymdownx.extra` replaces `markdown.extensions.extra`, but remember, `pymdown.extra` is a convenience extension which is just a wrapper and includes a number of extensions. Remember to avoid including this and then including conflicting extensions or doubles of extensions.  Here is the full list of included extensions:

    ```
    'markdown.extensions.tables',
    'pymdownx.magiclink',
    'pymdownx.betterem',
    'pymdownx.tilde',
    'pymdownx.emoji',
    'pymdownx.tasklist',
    'pymdownx.superfences'
    ```

- `pymdownx.github` doesn't replace any extensions and is just a convenience extensions to include most of the extensions needed to get a GitHub-ish feel.  Remember to avoid including this and then including conflicting extensions or doubles of extensions.  Here is the full list of included extensions:

    ```
    'markdown.extensions.tables',
    'pymdownx.magiclink',
    'pymdownx.betterem',
    'pymdownx.tilde',
    'pymdownx.emoji',
    'pymdownx.tasklist',
    'pymdownx.superfences'
    ```
