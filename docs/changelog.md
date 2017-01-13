## 1.5.0

> Released Jan X, 2017

- **NEW**: New EscapeAll extension.
- **NEW**: Arithmatex now has configurable output wrapper.
- **NEW**: PathConverter no longer verifies existence of path to allow it more flexible usage.
- **NEW**: PathConverter now only converts relative paths when converting to a relative or absolute location.
- **NEW**: Improved support for path path identification for PathConverter and B64.
- **FIX**: Fixed issue where Arithmatex was un-escaping `$` within math region.
- **FIX**: Fixed issue where plugins would append globally changing the escape list opposed to just in the in the Markdown instance.
- **FIX**: Fixed logic issue where the `mark`, `caret`, and `tilde` extension weren't quite modeling `betterem` inline behavior.
- **FIX**: Critics shouldn't allow escaping critic marks as it is not in the spec.

## 1.4.0

> Released Jan 5, 2017

- **NEW**: HeaderAnchor extension is now deprecated.  It will be removed in a future version.
- **NEW**: HeaderAnchor is no longer included in the Github extension.
- **NEW**: Slugify functions are moved to `pymdownx.slug` in preparation of HeaderAnchor removal.
- **FIX**: GithubEmoji is not "pending" deprecation, but is actually deprecated.

## 1.3.0

> Released Jan 1, 2017

- **NEW**: New emoji extension that aims to replace githubemoji.  By default it is configured for EmojiOne and Gemoji (Github's emoji).
- **NEW**: Githubemoji is deprecated. Please use the emoji extension instead.
- **NEW**: Pymdown extension is deprecated.  Pymdown extension was just a wrapper, please configure the desired individual extension(s) instead of relying on pymdown.
- **NEW**: Github extension now turns off nl2br by default in order properly emulate recent changes in GFM.  `no_nl2br` option is deprecated and will be removed in the future as it no longer reflects GFM behavior.

## 1.2.0

> Released Nov 1, 2016

- **NEW**: Add option to output tasklists in a more customizable way.

## 1.1.0

> Released Mar 1, 2016

- **NEW**: Add pypi 3.5 info in setup
- **NEW**: Add option to magiclink extension to allow the stripping of link protocols (`http://` etc.).
- **NEW**: Add option to github extension to disable the use of nl2br to reflect recent changes to GitHub Flavored Markdown.  Currently the default is the legacy (uses nl2br), but a warning will be displayed.  In the future, the option will be defaulted to not use nl2br.

## 1.0.1

> Released Dec 10, 2015

- **FIX**: Ordinal number 11th, 12th, and 13th

## 1.0.0

> Released Dec 8, 2015

- **NEW**: Initial release.
