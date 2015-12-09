# Extension Usage Notes {: .doctitle}
Notes about compatibility and usage.

---

## Incompatible Extensions
PyMdown Extensions includes three extensions that are meant to **replace** their counterpart in the default Python Markdown extensions.  You need to either use the PyMdown Extensions version or use the Python Markdown version; **they cannot be loaded at the same time**.

- `pymdownx.superfences` replaces `markdown.extensions.fenced_code`.
- `pymdownx.betterem` replaces `markdown.extensions.smartstrong`.
- `pymdownx.extra` replaces `markdown.extensions.extra`.
- `pymdownx.github` and `pymdownx.pymdown` serve a similar function as `pydmown.extra` so either one would also be used in place of `markdown.extensions.extra`.
- `pymdownx.extra`, `pymdownx.github`, `pymdownx.pymdown` are all convenience extensions that batch include a number of extensions; **do not mix these with each other** as they will cause certain extensions to be included multiple times.

## Include Extensions Only Once
In general, you shouldn't include an extension more than once.  PyMdown Extensions provides three extensions that batch include a number of extensions for convenience: `pymdownx.extra`, `pymdownx.github`, and `pymdownx.pymdown`.  If you try to include more than one of these convenience extensions at the same time, you will include certain extensions multiple times possibly leading to unexpected results.  Also, be aware of what extensions these convenience extensions include and do not accidentally re-include them individually or unexpected issues my arise.
