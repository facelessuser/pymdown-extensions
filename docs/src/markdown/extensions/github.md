# GitHub

!!! warning "Deprecated 4.5.0"
    4.5.0 has deprecated the GitHub extension and will remove it in version 5.0.0. The GitHub extension has never aimed to give a 1:1 match of GitHub features, and to avoid confusion, it is being discontinued, but all the great extensions can be configured individually to create your own GitHub-ish feel. Please see the [FAQ](../faq.md#github-ish-configurations) to learn how to configure a GitHub-ish feel.

## Overview

The GitHub extension is a convenience extension to load up and configure the minimum extensions needed to get a GFM feel.  It is not a 1:1 emulation, but some aspects are pretty close.  There is no desire to make it exact, but the feel is nice if you like GFM feel.


!!! danger "Reminder"
    Remember to read the [Usage Notes](../usage_notes.md) for information that may be relevant when using this extension!


## Loaded Extensions

Extension                       | Options                                                       | Name
------------------------------- | ------------------------------------------------------------- | ----
[Tables][tables]                |                                                               | `markdown.extensions.tables`
[MagicLink](./magiclink.md)     |                                                               | `pymdownx.magiclink`
[BetterEm](./betterem.md)       |                                                               | `pymdownx.betterem`
[Tilde](./tilde.md)             | `#!py3 {"subscript": False }`                                  | `pymdownx.tilde`
[Emoji](./emoji.md)             | see [GitHub Emoji Configuration](#github-emoji-configuration) | `pymdownx.emoji`
[Tasklist](./tasklist.md)       |                                                               | `pymdownx.tasklist`
[SuperFences](./superfences.md) |                                                               | `pymdownx.superfences`


## Code Highlighting

Code highlighting is usually done via Pygments by including either the `pymdownx.highlight` or `markdown.extensions.codehilite` extension and ensuring the following option is set if not by default: `guess_lang=False`. Optionally, you can use either of these extensions and disable Pygments support to use your preferred JavaScript highlighter.

If using Pygments, you will also need to provide your preferred Pygments style. If using a JavaScript highlighter, you will have to read that highlighter's documentation to learn how to setup and style your code blocks appropriately.

For those looking for a GitHub theme, there is no GitHub style included with this extension. You are most likely able to find a suitable theme online by searching. Presently, there are GitHub styles found at the [`pymdown-styles`][pymdown-styles] repository which contains the original Pygments GitHub style (`github`) and the GitHub 2014 style (`github2014`) which GitHub used before they abandoned Pygments for their own in-house highlighter. The listed themes might not always be available, and may not actually be close to current GitHub syntax highlighting.

## GitHub Like Slugs

The default slugify that Python Markdown uses isn't very much like GitHub's as it just removes all Unicode. But, at the time of writing this, the [`gfm`](../miscellaneous_extras.md#gfm) slugify provided by PyMdown Extensions is pretty close in the way it handles Unicode in slugs. By passing in the `pymdownx.slugs.uslugify` function via Toc's slugify parameter, you can alter the slugs to be GitHub like.

As mentioned before, the GitHub extension does not intend to provide a 1:1 match of GFM. There is one small known difference that may never be directly addressed. GitHub appends a number to duplicate headers with a hyphen: `-1`. Python Markdown (through the Toc extension) appends a number to duplicate headers with an underscore `_1`. Unfortunately, a slug function cannot simply override this duplicate as that behavior is controlled within the Toc extension. There are no plans at this time to write a Toc extension to replace the default one as a 1:1 match in behavior is not the end goal.

## Options

If you wish to configure the individual extensions included via this extensions, you can configure them by placing that sub extension's settings under a setting value that equals the sub extensions name.

```py
extension_configs = {
    'pymdownx.github': {
        'pymdownx.tilde': {
            'subscript': True
        }
    }
}
```

--8<-- "refs.md"
