## Incompatible Extensions

PyMdown Extensions includes three extensions that are meant to **replace** their counterpart in the default Python Markdown extensions.  You need to either use the PyMdown Extensions version or use the Python Markdown version; **they cannot be loaded at the same time**.

- `pymdownx.superfences` replaces `markdown.extensions.fenced_code`.
- `pymdownx.betterem` replaces `markdown.extensions.smartstrong`.
- `pymdownx.extra` replaces `markdown.extensions.extra`.

A few convenience extensions that include multiple extensions in one shot are also provided and should not be mixed.  And none of them should be mixed with `markdown.extensions.extra` or `pymdownx.extra`. This is to prevent multiples of an extension from getting included.

- `pymdownx.github`
- `pymdownx.pymdown`

## Include Extensions Only Once

In general, you shouldn't include an extension more than once. If you try to include more than one of the aforementioned convenience extensions at the same time, you will include certain extensions multiple times possibly leading to unexpected results.  Also, be aware of what extensions these convenience extensions include and do not accidentally re-include them individually.
