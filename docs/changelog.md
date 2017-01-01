# Changelog {: .doctitle}
Changes between versions.

---

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
- **NEW**: Add option to github extension to disable the use of nl2br to reflect recent changes to Github Flavored Markdown.  Currently the default is the legacy (uses nl2br), but a warning will be displayed.  In the future, the option will be defaulted to not use nl2br.


## 1.0.1
> Released Dec 10, 2015

- **FIX**: Ordinal number 11th, 12th, and 13th

## 1.0.0
> Released Dec 8, 2015

- **NEW**: Initial release.
