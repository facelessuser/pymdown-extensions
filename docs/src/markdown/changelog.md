# Changelog

## 6.1.0

- **NEW**: `version` and `version_info` are now accessible via the more standard form `__version__` and `_version_info__`. The old format, while available, is now deprecated.
- **FIX**: Fix issue where entities in the form `&#35;` would trigger MagicLink's shorthand for issues.
- **FIX**: Don't install tests when installing package.
- **FIX**: Fix for BetterEm case `**Strong*em,strong***`.

## 6.0.0

Please see [Release Notes](./release.md) for details on upgrading to 6.0.0.

- **NEW**: Allow custom inline highlight code blocks. (!380)
- **NEW**: SuperFences now has one custom format convention which now also accepts the markdown class object to allow access to meta.
- **NEW**: SuperFences no longer adds `flow` and `sequence` as default custom fences. Users will need to configure them themselves.
- **NEW**: Add new SuperFences formatters in Arithmatex that are compatible with SuperFences' custom fence feature and InlineHilite's custom inline feature. (!380)
- **NEW**: Requires Python Markdown 3.0.1 and utilizes the new priority registry when adding extensions and uses the new inline processor API instead of the old methodology.
- **NEW**: Better aliases for Twemoji specific emoji.
- **NEW**: Upgrade support for EmojiOne to 4.0.0 and Twemoji to 11.2.0.
- **FIX**: Fixes to SuperFences behavior of "preserve tabs" vs "normal" operations.
- **FIX**: Fixes to PathConverter's output. (#392)
- **FIX**: Remove unnecessary path code in B64.
- **FIX**: Fix issues with double escaping entities in code blocks after Python Markdown 3.0 update.

## 5.0.0

- **NEW**: Add validator to custom fences so custom options can be used. (!350)
- **NEW**: Add global `linenums_special` option to Highlight extension. Can be overridden per fence in SuperFences. (!360)
- **NEW**: Add `linenums_style` option to set line number output to Pygments `table` or `inline` format.  Also provide a custom `pymdownx-inline` format for more sane inline output in regards to copy and paste. See Highlight documentation for more info. (!360)
- **NEW**: Remove deprecated Github and PlainHTML extension. Remove deprecated Arithmatex option `insert_as_script` and deprecated MagicLink option `base_repo_url`.
- **FIX**: Add workaround in Highlight extension for line number alignment issues in Pygments with certain `step` values. (!360)

## 4.12.0

- **NEW**: Add option to fail if specified snippet isn't found. (#335)
- **FIX**: Windows issue with `preserve_tabs` option in SuperFences. (#328)

## 4.11.0

Jun 10, 2018

- **NEW**: Allow Arithmatex's "smart dollar" logic to be turned off via setting the option `smart_dollar` to `False`. (#297)
- **NEW**: Add support for tabbed groups in SuperFences.

## 4.10.2

May 17, 2018

- **FIX**: Failure with code highlight when guessing is enabled, but a bad language name is provided.

## 4.10.1

Apr 29, 2018

- **FIX**: Update Twemoji to 2.6.0 and EmojiOne 3.1.3.

## 4.10.0

Apr 18, 2018

- **NEW**: SuperFences now adds experimental support for preserving tabs in fenced code blocks. (#276)

## 4.9.2

Mar 26, 2018

- **FIX**: Issues with task lists that span multiple lines. (#267)
- **FIX**: Require latest Python Markdown.

## 4.9.1

Mar 18, 2018

- **FIX**: Output issue when no user and/or repository is specified.

## 4.9.0

Mar 3, 2018

- **NEW**: Add option to make task lists editable. (!249)
- **FIX**: Remove internal references to deprecated options.

## 4.8.0

Jan 17, 2018

- **NEW**: Set progress bar class level increments via `progress_increment` instead of using the hard coded value of `20`.
- **FIX**: Compatibility changes for next Markdown release.

## 4.7.0

Dec 8, 2017

- **NEW**: Bring back generic output for Arithmatex. Now under the `generic` option. (#185)
- **FIX**: StripHTML should allow space before close of opening tag.
- **FIX**: MagicLink should not auto-link inside a link. (#151)

## 4.6.0

Dec 2, 2017

- **NEW**: Arithmatex now *just* uses the script wrapper output as it is the most reliable output, and now previews can be achieved by providing a span with class `MathJax_Preview` that gets auto hidden when the math is rendered. `insert_as_script`, `tex_inline_wrap`, and `tex_block_wrap` have all been deprecated as they are now entirely unnecessary. A new option has been added called `preview` that controls whether the script output generates a preview or not when the rendered math output is loading. Users no longer need to configure `tex2jax.js` in there MathJax configuration anymore. (#171)
- **NEW**: PlainHTML has been renamed to StripHTML. `strip_attributes` is now a list instead of a string with a default of `[]`. `pymdownx.plainhtml` is still available with the old convention for backwards compatibility, but will be removed for version 5.0. (!176)
- **FIX**: PlainHTML has better script and style content avoidance to keep from stripping HTML tags and attributes from style and script content. (!174)
- **FIX**: PlainHTML can strip attributes that are not quoted. (!174)

## 4.5.1

Nov 28, 2017

- **FIX**: If an invalid provider is given, default to `github`. If no `user` or `repo` is specified, do not convert links that depend on those default values. (#169)

## 4.5.0

Nov 26, 2017

- **NEW**: Add GitLab style compare link shorthand and link shortening. (#160)
- **NEW**: Deprecate GitHub extension. It is now recommended to just include the extensions you want to create a GitHub feel instead of relying on a an extension to package something close-ish. (#159)

## 4.4.0

Nov 23, 2017

- **NEW**: Add social media mentions -- Twitter only right now. (#156)
- **FIX**: Use correct regular expression for GitLab and Bitbucket.

## 4.3.0

Nov 14, 2017

- **NEW**: Shorthand format for referencing non-default provider commits, issues, pulls, and mentions. (!147)
- **NEW**: Shorthand format for mentioning a repo via `@user/repo`. (!149)
- **NEW**: Add repository provider specific classes. (!149)
- **NEW**: Make repository labels configurable. (!149)
- **FIX**: Adjust pattern boundaries auto-links.

## 4.2.0

Nov 13, 2017

- **NEW**: MagicLink can now auto-link a GitHub like shorthand for repository references. (!139)
- **NEW**: MagicLink now renders pull request links with a slightly different output from issues. (!139)
- **NEW**: Deprecate `base_repo_url` in MagicLink in favor of the new `provider`, `user`, and `repo`. (!139)
- **NEW**: MagicLink now adds classes to repository links. (!139)
- **NEW**: MagicLink now adds title to repository links. (!139)
- **NEW**: MagicLink no longer styles repository commit hashes as code. (!143)
- **FIX**: MagicLink repository link outputs now better reflect default user and repository context. (!143)
- **FIX**: PlainHTML should not strip tags that are part of JavaScript code. (!140)

## 4.1.0

Oct 11, 2017

- **NEW**: Details can now have multiple classes defined.

## 4.0.0

Aug 29, 2017

- **NEW**: Details extension will now derive a title from the class if only a class is provided. (#107)
- **NEW**: Remove deprecated legacy emoji generator format.
- **NEW**: Remove deprecated `use_codehilite_settings`.
- **NEW**: Remove deprecated `spoilers` extension redirect.
- **NEW**: Update emoji databases: EmojiOne (3.1.2) and Twemoji to .(2.5.0)

## 3.5.0

Jun 13, 2017

- **NEW**: Add new slugs to preserve case. (!103)
- **NEW**: Add new GFM specific slug (both percent encoded and normal) that only lowercases ASCII chars just like GFM does. (#101)
- **FIX**: PathConverter should not try and convert obscured email address (with HTML entities). (#100)
- **FIX**: Don't normalize Unicode in slugs with `NFKD`, use `NFC` instead. (#98)
- **FIX**: Don't let EscapeAll escape CriticMarkup placeholders.  EscapeAll will no longer escape `STX` and `ETX`; they will just pass through. (#95)
- **FIX**: Replace CriticMarkup placeholders after replacing raw HTML placeholders. (#95)

## 3.4.0

Jun 1, 2017

- **NEW**: Renamed Spoilers to Details
- **NEW**: No longer attach the `spoilers` class to `details` tags.
- **NEW**: Provide better example of UML script in documents.

## 3.3.0

May 26, 2017

- **NEW**: Added support for pull request link shortening in MagicLink. (!88)
- **NEW**: Added new Spoilers extension. (#85)

## 3.2.1

May 23, 2017

- **FIX**: Cannot set Highlight's CSS class.

## 3.2.0

May 15, 2017

- **NEW**: Add support for Twemoji 2.3.5.
- **NEW**: Update to EmojiOne 3.0.2.
- **NEW**: Emoji generators now also take `category` which is also no included in all indexes.
- **FIX**: Excessive new lines at end of code blocks.

## 3.1.0

May 7, 2017

- **NEW**: Highlight extension now runs normal indented code blocks through highlighter.
- **FIX**: When Pygments is disabled, `linenums` class was attached to code blocks even if `linenums` was disabled and not enabled via fence headers.

## 3.0.0

Apr 16, 2017

- **NEW**: Added Keys extension.
- **NEW**: Generalized custom fences (#60). `flow` and `sequence` fence are now just custom fences and can be disabled simply by overwriting the `custom_fences` setting.
- **NEW**: Remove deprecated `no_nl2br` in GitHub extension. (#24)
- **NEW**: Remove deprecated HeaderAnchor extension. (#24)
- **NEW**: Remove deprecated PyMdown extension. (#24)
- **NEW**: Remove deprecated GitHubEmoji extension. (#24)
- **NEW**: Remove deprecated `nested` option in SuperFences. (#24)
- **NEW**: Wrapper extensions (such as GitHub and Extra) can now allow setting the included sub extensions settings (#61). Workaround settings that directly set specific extensions settings has been removed.
- **NEW**: Deprecated `use_codehilite_settings` in SuperFences and InlineHilite and now does nothing.  The settings will be removed in the future.  If `pymdownx.highlight` is used, it's settings will be used instead of CodeHilite. Eventually, the both SuperFences and InlineHilite will require `pymdownx.highlight` to be used and will have CodeHilite support stripped.
- **FIX**: Fix MathJax CDN references and usage in documentation.  MathJax CDN is shutting down and must now use Cloudflare CDN. (#63)

## 2.0.0

Feb 12, 2017

- **NEW**: SuperFences and InlineHilite can be configured via the new Highlight extension.
- **NEW**: InlineHilite now has all highlighting features pushed to the Highlight extension.  This removes all the CodeHilite code that used to be in it and instead relocates it to Highlight.
- **NEW**: Deprecate the nesting option in SuperFences.  Nesting is default and the only acceptable behavior moving forward.  The ability to turn off nesting will be removed in 3.0.

## 1.8.0

Jan 27, 2017

- **NEW**: MagicLink special repository link shortener for GitHub, GitLab, and Bitbucket. (#49)
- **FIX**: GitHub asterisk emphasis should never have had smart enabled for it. (#50)
- **FIX**: MagicLink fix for compatibility with wrapped symbols like `~`, `*` etc. which are commonly used.
- **FIX**: MagicLink encodes emails like Python Markdown does for consistency.
- **FIX**: MagicLink doesn't allow Unicode for email and does allow Unicode in a URL. (#53)
- **FIX**: InlineHilite now returns a proper `etree` element so that the `attr_list` extension and function properly with it. (#48)
- **FIX**: InlineHilite will no longer break if Pygments is not installed (478b410a2199d55f3e70b452516511d3810c61a5).

## 1.7.0

Jan 21, 2017

- **NEW**: Arithmatex now supports `\(...\)`, `\[...\]`, and `\begin{}...\end{}`.
- **NEW**: Arithmatex has an option to embed the math code in MathJax script tags.
- **FIX**: Unfortunately the wrap option is now run through an HTML escaper and HTML tags can no longer be fed in this way.  Arithmatex also now wraps "wrapped" content with spans to containerize content and keep one equation from bleeding into the next.
- **FIX**: Better handling of escaped Arithmatex inline tokens.
- **FIX**: Better handling of escaped InlineHilite tokens.
- **FIX**: Update InlineHilite and SuperFences so that the language option can accept things like `c#` and `.net` etc.
- **FIX**: Snippets now removes carriage returns from imported files to prevent breakage.

## 1.6.1

Jan 16, 2017

- **FIX**: Don't install tools or tests folder when installing from Pypi.

## 1.6.0

Jan 15, 2017

- **NEW**: EscapeAll has the option to perform more like Pandoc in that you can enable escaped newlines to be `hardbreaks`, and escaped spaces to be `nbsp`.
- **NEW**: Rework poorly thought out snippets format to require quoting file names with single line format.  Add a block format.  Allow commenting out lines temporarily.  And allow a way to escape them by placing a space after them.
- **FIX**: Fix documentation issues.

## 1.5.0

Jan 13, 2017

- **NEW**: New EscapeAll extension.
- **NEW**: New Snippets extension for including external files into a Markdown file.
- **NEW**: Arithmatex now has configurable output wrapper.
- **NEW**: PathConverter no longer verifies existence of path to allow it more flexible usage.
- **NEW**: PathConverter now only converts relative paths when converting to a relative or absolute location.
- **NEW**: Improved support for path path identification for PathConverter and B64.
- **FIX**: Fixed issue where Arithmatex was un-escaping `$` within math region.
- **FIX**: Fixed issue where plugins would append globally changing the escape list opposed to just in the in the Markdown instance.
- **FIX**: Fixed logic issue where the `mark`, `caret`, and `tilde` extension weren't quite modeling `betterem` inline behavior.
- **FIX**: Critics shouldn't allow escaping critic marks as it is not in the spec.

## 1.4.0

Jan 5, 2017

- **NEW**: HeaderAnchor extension is now deprecated.  It will be removed in a future version.
- **NEW**: HeaderAnchor is no longer included in the `pymdownx.github` extension.
- **NEW**: Slugify functions are moved to `pymdownx.slug` in preparation of HeaderAnchor removal.
- **FIX**: GitHubEmoji is not "pending" deprecation, but is actually deprecated.

## 1.3.0

Jan 1, 2017

- **NEW**: New Emoji extension that aims to replace GitHubEmoji.  By default it is configured for EmojiOne and Gemoji (GitHub's emoji).
- **NEW**: GitHubEmoji is deprecated. Please use the Emoji extension instead.
- **NEW**: PyMdown extension is deprecated.  PyMdown extension was just a wrapper, please configure the desired individual extension(s) instead of relying on PyMdown.
- **NEW**: `github` extension now turns off `nl2br` by default in order properly emulate recent changes in GFM.  `no_nl2br` option is deprecated and will be removed in the future as it no longer reflects GFM behavior.

## 1.2.0

Nov 1, 2016

- **NEW**: Add option to output task lists in a more customizable way.

## 1.1.0

Mar 1, 2016

- **NEW**: Add pypi 3.5 info in setup
- **NEW**: Add option to MagicLink extension to allow the stripping of link protocols (`http://` etc.).
- **NEW**: Add option to `github` extension to disable the use of `nl2br` to reflect recent changes to GitHub Flavored Markdown.  Currently the default is the legacy (uses `nl2br`), but a warning will be displayed.  In the future, the option will be defaulted to not use `nl2br`.

## 1.0.1

Dec 10, 2015

- **FIX**: Ordinal number 11th, 12th, and 13th

## 1.0.0

Dec 8, 2015

- **NEW**: Initial release.

--8<-- "refs.txt"
