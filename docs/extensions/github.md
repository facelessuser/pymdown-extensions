## Overview
The Github extension is a convenience extension to load up and configure the minimum extensions needed to get a GFM feel.  It is not a 1:1 emulation, but some aspects are pretty close.  There is no desire to make it exact, but the feel is nice if you like GFM feel; some things may differ slightly.

!!! Tip "Tip"
    For code highlighting, you will also need to load the `markdown.extensions.codehilite` extension yourself as well with `guess_lang=False`. You will also need to provide your preferred Pygments style (or configure a JavaScript highlighter).  Though there is no Github style included with this extension, you are most likely able to find a suitable theme online by searching. There are Github styles found at the [pymdown-styles](https://github.com/facelessuser/pymdown-styles/tree/master/pymdown_styles) repo; it contains the original Pygments Github style (github) and the Github 2014 style (github2014) which Github used before they ditched Pygments for their own in-house highlighter.

!!! danger "Reminder"
    Remember to read the [Usage Notes](../usage_notes.md) for information that may be relevant when using this extension!

Extensions that get loaded by default:

| Extension | Options | Name   |
|-----------|---------|--------|
| [Tables](https://pythonhosted.org/Markdown/extensions/tables.html) | | markdown.extensions.tables |
| [magiclink](./magiclink.md)      | | pymdownx.magiclink |
| [betterem](./betterem.md)        | `#!python {"smart_enable": 'all' }` | pymdownx.betterem |
| [tilde](./tilde.md)              | `#!python {"subscript": False }` | pymdownx.tilde |
| [emoji](./emoji.md)  | see [Github Emoji Configuration](#github-emoji-configuration) | pymdownx.emoji |
| [tasklist](./tasklist.md) | | pymdownx.tasklist |
| [superfences](./superfences.md) | | pymdownx.superfences |

!!! warning "Output Change"
    HeaderAnchor is no longer included starting in version `1.4.0` as it wasn't really part of the GFM syntax, and HeaderAnchor is now deprecated.  HeaderAnchor is an unnecessary extension, and the same end result can be achieved with `markdown.extensions.toc` (with the `permalink` option enabled) and some custom CSS.  This extension was more about the syntax than it was about styling.  If you are not ready to give up the extension, you can manually include the `pymdownx.headeranchor` extension in addition to `pymdownx.github`. But in the future, the HeaderAnchor extension will be removed from Pymdown Extensions.

### Github Emoji Configuration
This is the full, default setup used to get Github emoji images.  This is valid at the time of writing this. Github constantly tweaks how they do things, so in time this may render differently than what they actually do. But this should provide emojis for as long as the CDNs are valid.

```python
import pymdownx.emoji

extension_configs = {
    "pymdownx.emoji": {
        "emoji_index": pymdownx.emoji.gemoji,
        "emoji_generator": pymdownx.emoji.to_png,
        "alt": "short",
        "options": {
            "attributes": {
                "align": "absmiddle",
                "height": "20px",
                "width": "20px"
            },
            "image_path": "https://assets-cdn.github.com/images/icons/emoji/unicode/",
            "non_standard_image_path": "https://assets-cdn.github.com/images/icons/emoji/"
        }
    }
}
```

## Options
| Option    | Type | Default |Description |
|-----------|------|---------|------------|
| no_nl2br | bool | True | If `False`, this includes the [nl2br](https://pythonhosted.org/Markdown/extensions/nl2br.html) extension. |

!!! warning "Deprecated Option"
    In version `1.3.0`, the setting `no_nl2br` is now `True` by default and the setting is deprecated and will be removed in the future. Github's GFM (which we are emulating) no longer converts new lines to `<br>`.  If you prefer having nl2br enabled, you can enable the `markdown.extensions.nl2br` extension separately.

*[GFM]:  Github Flavored Markdown
