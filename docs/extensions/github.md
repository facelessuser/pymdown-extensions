## Overview

The GitHub extension is a convenience extension to load up and configure the minimum extensions needed to get a GFM feel.  It is not a 1:1 emulation, but some aspects are pretty close.  There is no desire to make it exact, but the feel is nice if you like GFM feel; some things may differ slightly.

!!! Tip "Tip"
    For code highlighting, you will also need to load the `markdown.extensions.codehilite` extension yourself as well with `guess_lang=False`. You will also need to provide your preferred Pygments style (or configure a JavaScript highlighter).  Though there is no GitHub style included with this extension, you are most likely able to find a suitable theme online by searching. There are GitHub styles found at the [`pymdown-styles`][pymdown-styles] repository; it contains the original Pygments GitHub style (`github`) and the GitHub 2014 style (`github2014`) which GitHub used before they ditched Pygments for their own in-house highlighter.

!!! danger "Reminder"
    Remember to read the [Usage Notes](../usage_notes.md) for information that may be relevant when using this extension!

Extensions that get loaded by default:

Extension | Options | Name   |
----------|---------|--------|
[Tables][tables]                | | `markdown.extensions.tables`
[MagicLink](./magiclink.md)     | | `pymdownx.magiclink`
[BetterEm](./betterem.md)       | `#!py {"smart_enable": 'all' }` | `pymdownx.betterem`
[Tilde](./tilde.md)             | `#!py {"subscript": False }` | `pymdownx.tilde`
[Emoji](./emoji.md)             | see [GitHub Emoji Configuration](#github-emoji-configuration) | `pymdownx.emoji`
[Tasklist](./tasklist.md)       | | `pymdownx.tasklist`
[SuperFences](./superfences.md) | | `pymdownx.superfences`

!!! warning "Output Change"
    HeaderAnchor is no longer included starting in version `1.4.0` as it wasn't really part of the GFM syntax, and HeaderAnchor is now deprecated.  HeaderAnchor is an unnecessary extension, and the same end result can be achieved with `markdown.extensions.toc` (with the `permalink` option enabled) and some custom CSS.  This extension was more about the syntax than it was about styling.  If you are not ready to give up the extension, you can manually include the `pymdownx.headeranchor` extension in addition to `pymdownx.github`. But in the future, the HeaderAnchor extension will be removed from PyMdown Extensions.

### GitHub Emoji Configuration

This is the full, default setup used to get GitHub emoji images.  This is valid at the time of writing this. GitHub constantly tweaks how they do things, so in time this may render differently than what they actually do. But this should provide emojis for as long as the CDNs are valid.

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

Option     | Type | Default     | Description
---------- | ---- | ----------- | -----------
`no_nl2br` | bool | `#!py True` | If `False`, this includes the [New-Line-to-Break][nl2br] extension.

!!! warning "Deprecated Option"
    In version `1.3.0`, the setting `no_nl2br` is now `True` by default and the setting is deprecated and will be removed in the future. GitHub's GFM (which we are emulating) no longer converts new lines to `<br>`.  If you prefer having New-Line-to-Break enabled, you can enable the `markdown.extensions.nl2br` extension separately.

--8<-- "refs.md"
