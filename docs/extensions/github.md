# Github {: .doctitle}
Simulation of Github Flavored Markdown.

---

## Overview
The Github extension is a convenience extension to load up and configure the minimum extensions needed to get a GFM feel.  It is not a 1:1 emulation, but some aspects are pretty close.  I don't really have a desire to to make it exact, but the feel is nice if you like GFM feel; some things may differ slightly.

!!! Tip "Tip"
    For code highlighting, you will also need to load the `markdown.extensions.codehilite` extension yourself as well with `guess_lang=False` and your preferred Pygments style (if available or use some other JavaScript highlighter).  Though there is no Github style included with this extension, you are most likely able to find a suitable theme online by searching.  I do have older Github styles found at the [pymdown-styles](https://github.com/facelessuser/pymdown-styles/tree/master/pymdown_styles) repo; it contains the original Pygments Github style (github) and the Github 2014 style (github2014) which Github used before they ditched Pygments for their own in-house highlighter.

!!! Caution "Reminder"
    Remember to read the [Usage Notes](../usage_notes.md) for information that may be relevant when using this extension!

Extensions that get loaded:

| Extension | Options | Name   |
|-----------|---------|--------|
| [Tables](https://pythonhosted.org/Markdown/extensions/tables.html) | | markdown.extensions.tables |
| [New&nbsp;Line&nbsp;to&nbsp;Break](https://pythonhosted.org/Markdown/extensions/nl2br.html)[^nl2br] | | markdown.extensions.nl2b |
| [magiclink](./magiclink.md)      | | pymdownx.magiclink |
| [betterem](./betterem.md)        | `#!python {"smart_enable": 'all' }` | pymdownx.betterem |
| [tilde](./tilde.md)              | `#!python {"subscript": False }` | pymdownx.tilde |
| [githubemoji](./githubemoji.md)  | | pymdownx.githubemoji |
| [tasklist](./tasklist.md) | | pymdownx.tasklist |
| [headeranchor](./headeranchor.md)| | pymdownx.headeranchor |
| [superfences](./superfences.md) | | pymdownx.superfences |

## Options
| Option    | Type | Default |Description |
|-----------|------|---------|------------|
| no_nl2br | bool | True | Don't use `nl2br` extension. |

!!! warning "Deprecated"
    `no_nl2br` is deprecated in version `1.3.0` and will be removed in the future as Github's GFM (which we are emulating) no longer converts new lines to `<br>`.

*[GFM]:  Github Flavored Markdown
