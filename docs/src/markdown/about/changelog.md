# Changelog

## 10.1

-   **NEW**: Add new `combine_header_slug` option in legacy Tabbed extension and new Block Tab extension that will
    prefix a content tab's slug with the parent header's slug. This allows for content tab slugs that are scoped to the
    header they are under.

## 10.0.1

-   **FIX**: Regression related to snippets nested deeply under specified base path.

## 10.0

-   **Break**: Snippets: snippets will restrict snippets to ensure they are under the `base_path` preventing snippets
    relative to the `base_path` but not explicitly under it. `restrict_base_path` can be set to `False` for legacy
    behavior.

## 9.11

-   **NEW**: Emoji: Update to new CDN and use Twemoji 14.1.2.
-   **NEW**: Snippets: Ignore nested snippet section syntax when including a section.

## 9.10

-   **NEW**: Blocks: Add new experimental general purpose blocks that provide a framework for creating fenced block
    containers for specialized parsing. A number of extensions utilizing general purpose blocks are included and are
    meant to be an alternative to (and maybe one day replace): Admonitions, Details, Definition Lists, and Tabbed. Also
    adds a new HTML plugin for quick wrapping of content with arbitrary HTML elements.
-   **NEW**: Highlight: When enabling line spans and/or line anchors, if a code block has an ID associated with it, line
    ids will be generated using that code ID instead of the code block count.
-   **NEW**: Snippets: Expand section syntax to allow section names with `-` and `_`.
-   **NEW**: Snippets: When `check_paths` is enabled, and a specified section is not found, raise an error.
-   **NEW**: Snippets: Add new experimental feature `dedent_sections` that will de-indent (remove any common leading
    whitespace from every line in text) from that block of text.
-   **NEW**: MagicLink: Update GitLab links to match recent changes and to be more correct.
-   **NEW**: MagicLink: Relax required hash length when performing link shortening.

## 9.9.3

-   **FIX**: Highlight: Remove extraneous new lines from end of indented code blocks when using
    `#!py use_pygments = False`.

## 9.9.2

-   **FIX**: Snippets syntax can break in XML comments as XML comments do not allow `--`. Relax Snippets syntax such
    that `-8<-` (single `-`) are allowed.

## 9.9.1

-   **FIX**: Use a different CDN for Twemoji icons as MaxCDN is no longer available.

## 9.9

-   **ENHANCE**: BetterEm: Further improvements to strong/emphasis handling:
    -   Ensure that one or more consecutive `*` or `_` surrounded by whitespace are not considered as a token.
-   **ENHANCE**: Caret: Apply recent BetterEm improvements to Caret:
    -   Fix case where `^^` nested between `^` would be handled in an unexpected way.
    -   Ensure that one or more consecutive `^` surrounded by whitespace are not considered as a token.
-   **ENHANCE**: Tilde: Apply recent BetterEm improvements to Tilde:
    -   Fix case where `~~` nested between `~` would be handled in an unexpected way.
    -   Ensure that one or more consecutive `~` surrounded by whitespace are not considered a token.
-   **ENHANCE**: Mark: Apply recent BetterEm improvements to Mark:
    -   Ensure that one or more consecutive `=` surrounded by whitespace are not considered a token.

## 9.8

-   **NEW**: Formally declare support for Python 3.11.
-   **FIX**: BetterEm: Fix case where `**` nested between `*` would be handled in an unexpected way.

## 9.7

-   **NEW**: Tabbed: Add new syntax to allow forcing a specific tab to be select by default.
-   **NEW**: Snippets: Add new option to pass arbitrary HTTP headers.
-   **NEW**: Snippets: Allow specifying sections in a snippet and including just the specified section.

## 9.6

-   **NEW**: Highlight: Allow greater granularity of specifying where language guessing takes place via `guess_lang`
    option (e.g. `block` vs `inline`).
-   **NEW**: Tabbed: Add options for generating tab IDs from tab titles.
-   **NEW**: Snippets: Add support for specifying specific lines for Snippets.
-   **NEW**: Snippets: Commenting out files in block format no longer requires a space directly after `;`.
-   **NEW**: Snippets: A new sane way to escape snippets is now available.

## 9.5

-   **NEW**: InlineHilite: Custom inline code block formatters can now be forced to raise an exception by raising a
    `InlineHiliteException`.
-   **NEW**: Snippets: Add new options to handle importing snippets from URL.
-   **NEW**: Snippets: Snippets will only swallow missing file errors (unless `check_paths` is enabled), all other
    errors will be propagated up.
-   **NEW**: Snippets: When a file or URL is missing, raise `SnippetMissingError` instead of `IOError`.
-   **FIX**: Snippets: Small issues related to recursive inclusion of snippets.

## 9.4

-   **NEW**: Highlight: Changes in order to support Pygments 2.12+. If using Pygments and a version less than 2.12 is
    installed, Highlight will raise an exception.

## 9.3

-   **NEW**: B64: Allow SVG to be encoded and inlined.
-   **NEW**: PathConverter: Add option to use `file://` prefix on absolute paths.
-   **FIX**: Highlight: Ensure that `extend_pygments_lang` is not case sensitive regarding language names.

## 9.2

-   **NEW**: Drop Python 3.6 support and formally add Python 3.10 support.
-   **NEW**: Highlight: Add `pygments_lang_option` to enable attaching language classes to Pygments code blocks.
-   **NEW**: SuperFences: Custom fence validators and formatters can now be forced to raise an exception by raising a
    `SuperFencesException`.
-   **NEW**: Keys: Add `power` and `fingerprint` keys.
-   **FIX**: SuperFences: Fix case where custom fence in a blockquote was not gracefully handled.
-   **FIX**: Arithmatex: fix issue where if you limit the inline or block syntax to specific input types, access to
    certain matched groups could cause an error.

## 9.1

-   **NEW**: Highlight: If `linenums` is enabled globally via the `highlight` extension, and a code block specifies a
    line number of zero (e.g. SuperFences), disable line numbers for that code block.
-   **FIX**: Snippets: Add missing documentation for `auto_append` feature that was added in 8.2.
-   **FIX**: Highlight: When `attr_list` is enabled, attributes were not properly added to Pygments code blocks in the
    `table` format. (#1505)

## 9.0

Please see [Migration Notes](./releases/9.0.md#9.0) for details on upgrading to 9.0.

-   **NEW**: Arithmatex: Wrap MathJax "script" format (non-preview) with a container element just like all other
    Arithmatex output formats.
-   **NEW**: Arithmatex: MathJax (non-generic) form's container element now has the `arithmatex` class added just like
    everywhere else.
-   **NEW**: Arithmatex: Add options to override HTML element container type of inline and block math.
-   **NEW**: Arithmatex: Add new formatter functions intended to replace old math fenced/inline block formatters. New
    formatter functions are configurable. All others are marked as deprecated and will be removed at some future date.
-   **NEW**: Emoji: Upgraded Twitter emoji database to support latest emoji. It is a known issue that Twitter has
    `:man_in_santa_hat:` and `:mx_claus:` backwards -- same for `:mrs_claus:` and `:woman_in_santa_hat:`. That is on
    Twitter's side, not ours.
-   **NEW**: Highlight: Add support for the Pygments option `linespans`.
-   **NEW**: Highlight: Add support for Pygments option `lineanchors`.
-   **NEW**: Highlight: Add support for Pygments option `anchorlinenos`.
-   **NEW**: Highlight: Remove `legacy_no_wrap_code` option.
-   **NEW**: Add support for generating title headers pulled from the Pygments lexer for code blocks. Feature can be
    enabled via the new `auto_title` option. If a specific name is not preferred, these names can be overridden via
    a user defined mapping called `auto_title_map`.
-   **NEW**: SuperFences: Allow setting a title, or overriding an auto title via the new `title` option in a fenced code
    header.
-   **NEW**: SuperFences: Allow adding ID and arbitrary `data-` attributes on Pygments code blocks. The latter requires
    the `attr_list` extension to be enabled.
-   **NEW**: SuperFences: Removed old deprecated option `highlight_code` which no longer did anything.
-   **NEW**: SuperFences: Remove legacy code meant to help with transitioning to new custom fence function format.
-   **NEW**: Tabbed: New alternate style that allows for a scrollable tabs if they overflow. Feature is experimental,
    see docs for more information.
-   **NEW**: Slugs: Add new configurable `slugify` function that aims to replace all other slugify methods. Deprecate
    `uslugify`, `uslugify_encoded`, `uslugify_case`, `uslugify_case_encoded`, `gfm`, and `gfm_encoded`. `slugify` takes
    parameters returning a function that performs the desired slug handling. `slugify` adds new options `case="fold"`
    for case folding and `normalize='<normalize format here>'` (uses `NFC` by default).
-   **FIX**: BetterEm: Fix some complex cases related to "smart" logic. (#1413)
-   **FIX**: EscapeAll: Fix issue where an escaped HTML entity may end up with incorrect slug and incorrect table of
    content entry.
-   **FIX**: Highlight: Fix issue that occurs when showing only nth line numbers and using `pymdownx-inline`. Lines not
    showing a line number would not render with the proper leading space.

## 8.2

-   **NEW**: Snippets: now accepts a list of base paths which will be resolved in the order they are specified.
    Compatibility is present with legacy behavior, and a single string path will still be accepted.
-   **NEW**: Snippets: allow for specifying certain snippets to auto-append to every file. Useful for appending
    abbreviations, reference links, etc.
-   **NEW**: Snippets: a snippet base path can be a full path to a file. When a base path is a full path to a file, only
    that file will be included from the specified folder. This allows for targeting a one off file outside of the normal
    snippet paths(s).
-   **NEW**: MagicLink: add GitHub Discussions support to MagicLink. Can now use `?<num>` to link discussions. Full
    discussion links will also be shortened if shortening is enabled. (#1187)
-   **NEW**: MagicLink: add new `normalize_issue_symbols` option to make issues, pull request, and discussion links all
    render with `#` instead of `#`, `!`, and `?` respectively. Input syntax is still the same. Great if you want a
    GitHub style look where all issue types are just rendered with `#`.
-   **FIX**: MagicLink: documentation will not render links with special icons added via CSS so as not to confuse users
    that may think that is part of MagicLink. While possible with CSS, MagicLink provides no CSS automatically.
-   **FIX**: Tabbed &amp; Details: Fix corner case with lists. (#1225)
-   **FIX**: Fix issue with unescaping logic in code blocks.

## 8.1.1

-   **FIX**: Ensure content immediately before Details content or Tabbed content gets preserved.
-   **FIX**: StripHTML: Fix some corner cases related to stripping comments.

## 8.1

-   **NEW**: Drop support for Python 3.5.
-   **NEW**: Officially support Python 3.9.
-   **NEW**: Tabbed titles can now have simple Markdown in them which can be parsed and rendered (like emoji, bold,
    etc.).
-   **FIX**: Avoid parsing script tags in PathConverter and B64 extensions.

## 8.0.1

-   **FIX**: Fix issue with `pymdownx-inline` an Pygments 2.7+.

## 8.0

Please see [Migration Notes](./releases/8.0.md#8.0) for details on upgrading to 8.0.

-   **NEW**: Added SaneHeaders extension.
-   **NEW**: SuperFences \& InlineHilite: gracefully handle failing custom formatters and/or validators. Users should
    add their own debug code to their formatter/validator if they suspect it isn't working.
-   **NEW**: SuperFences: if a custom fence validator fails, try the next custom fence until all are exhausted.
-   **NEW**: SuperFences: no longer allow custom options in the form `key=` (no value). Only keys with values or keys
    with no value and no `=` are accepted. Keys with no value will now assume the value to be the key name.
-   **NEW**: SuperFences: if `attr_list` extension is enabled, fenced code that use brace attribute list style headers
    (` ```{lang #id .class attr=value}`) will attach arbitrary attributes that are included in the header to the code
    element.
-   **NEW**: SuperFences: when Pygments is disabled, options (such as `linenums`) included in fenced code headers no
    longer do anything. If `attr_list` is enabled, and the brace header is used, such options will be treated as HTML
    attributes. JavaScript highlighter options should be defined in the brace header form with `attr_list` enabled in
    order to generate appropriate, compatible HTML with the chosen JavaScript highlighter.
-   **NEW**: SuperFences: backwards incompatible changes where made to custom fence API. See
    [Migration Notes](./releases/8.0.md#8.0) for instructions on how to migrate to the new API. Some temporary support
    for most of the old format is in place, but is deprecated.
-   **NEW**: SuperFences: has removed legacy code tab feature. Associated `legacy_tab_classes` option has been removed.
    Please use the Tabbed extension to create general purpose tabs for code blocks or other content.
-   **NEW**: Highlight: add new option `language_prefix` which controls the prefix applied to language classes when
    Pygments is not being used.
-   **NEW**: Highlight: A new option called `code_attr_on_pre` was added to the Highlight extension and controls whether
    language classes, and any ids, attributes, and classes that are defined in fenced code attribute list style headers,
    are attached to the code element or pre element. This has effect when using Pygments.
-   **NEW**: Highlight: option `linenums` now defaults to `None` and accepts `None`, `True`, or `False`. `None` is
    disabled by default, but can be enabled per code block. `True` enables line numbers globally. `False` disables
    globally and cannot be enabled manually per code block.
-   **NEW**: ExtraRawHTML: remove extension.
-   **FIX**: Fix issues with complex emphasis combinations in BetterEm.
-   **FIX**: Details: fix corner cases related to extension and lists.
-   **FIX**: Tabbed: fix corner cases related to extension and lists.
-   **FIX**: EscapeAll: Handle HTML entities special.
-   **FIX**: SuperFences: Fix parameter unpacking bug.

## 7.1

-   **NEW**: SuperFences will now allow number ranges in `hl_lines` option. (#878)
-   **NEW**: Emoji extension now requires custom emoji indexes to take an `options` and `md` argument. The old
    non-argument format is deprecated and still accepted, but support for indexes with no arguments will be removed at a
    future time.
-   **NEW**: Highlight now allows the specifying of a custom line number class when not using Pygments.
-   **FIX**: Better Arithmatex patterns. Fix issue #888 which caused a hang due to a regular expression typo. Also
    ensure `#!tex $$..$$` and `#!tex begin{}...end{}` patterns properly don't match if the tail markers are escaped.

## 7.0

Please see [Migration Notes](./releases/7.0.md#7.0) for details on upgrading to 7.0.

-   **NEW**: MagicLink will now shorten user name and repository links when link shortening is enabled.
-   **NEW**: Added MagicLink options `social_url_shortener` and `shortener_user_exclude` were added.
-   **NEW**: UML examples are now demonstrated with Mermaid in documentation.
-   **NEW**: SuperFences, if using the attribute list format (` ``` {.lang .additional_class, linenums="1"} `) allows
    adding additional classes. IDs can be added as well, though Pygments generated code blocks do not have a mechanism
    to actually insert IDs. The first provided class will always be treated as the language class.
-   **NEW**: Custom SuperFences' formatters should now also include the keyword parameters`classes` and `id_value` to
    allow injecting classes and IDs via the now supported attribute list format. If a code block defines no additional
    IDs and classes, the old form will be used. Formatters should include `**kwargs` at the end to future proof them
    from future changes.
-   **NEW**: Deprecate the SuperFences `highight_code` option. As SuperFences syntax has language classes built right
    in, disabling the `highlight_code` option makes little sense. While `highlight_code` is still accepted, it currently
    does nothing and will be removed at some future time.
-   **NEW**: If a custom fence (SuperFences) or inline (InlineHilite) is given the name of `*`, it will override the
    default fence logic.
-   **NEW**: SuperFences and InlineHilite no longer sync settings from CodeHilite.
-   **NEW**: Add new Tabbed extension for general purpose tabbed content in Markdown.
-   **NEW**: Deprecate old SuperFences tabbed content feature. This will be removed in 8.0.
-   **NEW**: SuperFences' tabbed content classes have changed from `supferfences-tabs` and `superfences-content` to
    `tabbed-set` and `tabbed-content` respectively. Old style classes can be enabled with the `legacy_tab_classes`
    option in SuperFences. This new option will be retired with SuperFences tabbed content feature in 8.0.
-   **NEW**: Upgrade to Twemoji 12.1.5.
-   **NEW**: New key codes and key code changes in Keys extension:
      -   Added `super`, `left-super`, and `right-super` key codes as an alternative to `meta`. Aliases `lsuper` and
          `rsuper` were also added.
      -   Added the `alt-graph` key code with `altgr` alias.
      -   Added the following new aliases: `lwindows` and `rwindows` for consistency.
      -   Added new codes `left-meta` and `right-meta` for consistency with other modifiers. Aliases `lmeta` and `rmeta`
          were also added.
      -   Added `left-option`, `right-option`, `left-command`, `right-command`, `left-meta`, and `right-meta` codes for
          consistency across similar modifier keys. Additional aliases were added as well: `loption`, `roption`, `lopt`,
          `ropt`, `left-opt`, `right-opt`, `lcommand`, `rcommand`, `lcmd`, `rcmd`, `left-cmd`, `right-cmd`, `lmeta`, and
          `rmeta`.
      -   `alt` no longer uses `menu`, `lmenu`, and `rmenu` as key aliases. `context-menu` now uses the alias `menu`.
          `context-menu` will display with `Menu` now.
-   **FIX**: Numerous deprecation warnings associated with the recent release of Python Markdown 3.2.
-   **FIX**: Ensure ExtraRawHTML raises a deprecation warning.

## 6.3

-   **NEW**: `pymdownx.extrarawhtml` is now deprecated in favor of Python Markdown's `md_in_html` extension found in the
    3.2 release.
-   **NEW**: When using Pygments 2.4+, code under `pre` elements will also be wrapped in `code` blocks:
    `#!html <pre><code></code></pre>`. `legacy_no_wrap_code` option has been provided as a temporary way to get the old
    behavior during the transition period, the option will be removed in the future.
-   **NEW**: Remove deprecated `version` and `version_info`.
-   **FIX**: Allow single word hostnames in MagicLink auto-link.

## 6.2.1

-   **FIX**: Fix issue in PathConverter where Windows path conversion from relative to absolute doesn't always work in
    all browsers.

## 6.2

-   **NEW**: Upgrade Twemoji to use 12.1.3.
-   **NEW**: Downgrade and lock EmojiOne version 2.2.7. 2.2.7 is the last truly free version of EmojiOne. This is the
    safest version that users should use. EmojiOne will not be updated anymore as they are now JoyPixels and have a
    license that is not that permissible. We've reverted support for any version greater than 2.2.7 to ensure we don't
    accidentally cause a user to improperly use JoyPixels' assets.
-   **NEW**: Drop specialized `to_awesome` generator for EmojiOne.
-   **FIX**: MagicLink: match the auto-link pattern in the current Markdown package.
-   **FIX**: Fix fenced math escape issue when using MathJax script output format.

## 6.1

-   **NEW**: Upgrade Twemoji to 12.1.2 using the latest JoyPixels' (formally EmojiOne) short name index in
    @JoyPixels/emoji-toolkit 5.0.4.
-   **NEW**: Upgrade EmojiOne to 4.5.0 to the last release in the 4+ series. EmojiOne was rebranded as JoyPixels, but
    while the index is licensed under MIT, the image assets are no longer as permissible as they once were. The Emoji
    extension will only reference the last release under the older more permissible license (4.5.0). The option to use
    the CDN with EmojiOne 2.7 is still available as well which used an even more permissible license.
-   **NEW**: Upgrade Gemoji to 3.0.1.
-   **NEW**: `version` and `version_info` are now accessible via the more standard form `__version__` and
    `_version_info__`. The old format, while available, is now deprecated.
-   **FIX**: Fix GitHub emoji CDN links to use their latest.
-   **FIX**: Fix issue where entities in the form `&#35;` would trigger MagicLink's shorthand for issues.
-   **FIX**: Don't install tests when installing package.
-   **FIX**: Fix for BetterEm case `**Strong*em,strong***`.
-   **FIX**: Fixes for non-word character boundary cases in BetterEm, Caret, Mark, and Tilde extensions.

## 6.0

Please see [Migration Notes](./releases/6.0.md#6.0) for details on upgrading to 6.0.0.

-   **NEW**: Allow custom inline highlight code blocks. (!380)
-   **NEW**: SuperFences now has one custom format convention which now also accepts the markdown class object to allow
    access to meta.
-   **NEW**: SuperFences no longer adds `flow` and `sequence` as default custom fences. Users will need to configure
    them themselves.
-   **NEW**: Add new SuperFences formatters in Arithmatex that are compatible with SuperFences' custom fence feature and
    InlineHilite's custom inline feature. (!380)
-   **NEW**: Requires Python Markdown 3.0.1 and utilizes the new priority registry when adding extensions and uses the
    new inline processor API instead of the old methodology.
-   **NEW**: Better aliases for Twemoji specific emoji.
-   **NEW**: Upgrade support for EmojiOne to 4.0.0 and Twemoji to 11.2.0.
-   **FIX**: Fixes to SuperFences behavior of "preserve tabs" vs "normal" operations.
-   **FIX**: Fixes to PathConverter's output. (#392)
-   **FIX**: Remove unnecessary path code in B64.
-   **FIX**: Fix issues with double escaping entities in code blocks after Python Markdown 3.0 update.

## 5.0

-   **NEW**: Add validator to custom fences so custom options can be used. (!350)
-   **NEW**: Add global `linenums_special` option to Highlight extension. Can be overridden per fence in SuperFences.
    (!360)
-   **NEW**: Add `linenums_style` option to set line number output to Pygments `table` or `inline` format.  Also provide
    a custom `pymdownx-inline` format for more sane inline output in regards to copy and paste. See Highlight
    documentation for more info. (!360)
-   **NEW**: Remove deprecated Github and PlainHTML extension. Remove deprecated Arithmatex option `insert_as_script`
    and deprecated MagicLink option `base_repo_url`.
-   **FIX**: Add workaround in Highlight extension for line number alignment issues in Pygments with certain `step`
    values. (!360)

## 4.12

-   **NEW**: Add option to fail if specified snippet isn't found. (#335)
-   **FIX**: Windows issue with `preserve_tabs` option in SuperFences. (#328)

## 4.11

-   **NEW**: Allow Arithmatex's "smart dollar" logic to be turned off via setting the option `smart_dollar` to `False`.
    (#297)
-   **NEW**: Add support for tabbed groups in SuperFences.

## 4.10.2

-   **FIX**: Failure with code highlight when guessing is enabled, but a bad language name is provided.

## 4.10.1

-   **FIX**: Update Twemoji to 2.6.0 and EmojiOne 3.1.3.

## 4.10

-   **NEW**: SuperFences now adds experimental support for preserving tabs in fenced code blocks. (#276)

## 4.9.2

-   **FIX**: Issues with task lists that span multiple lines. (#267)
-   **FIX**: Require latest Python Markdown.

## 4.9.1

-   **FIX**: Output issue when no user and/or repository is specified.

## 4.9

-   **NEW**: Add option to make task lists editable. (!249)
-   **FIX**: Remove internal references to deprecated options.

## 4.8

-   **NEW**: Set progress bar class level increments via `progress_increment` instead of using the hard coded value of
    `20`.
-   **FIX**: Compatibility changes for next Markdown release.

## 4.7

-   **NEW**: Bring back generic output for Arithmatex. Now under the `generic` option. (#185)
-   **FIX**: StripHTML should allow space before close of opening tag.
-   **FIX**: MagicLink should not auto-link inside a link. (#151)

## 4.6

-   **NEW**: Arithmatex now *just* uses the script wrapper output as it is the most reliable output, and now previews
    can be achieved by providing a span with class `MathJax_Preview` that gets auto hidden when the math is rendered.
    `insert_as_script`, `tex_inline_wrap`, and `tex_block_wrap` have all been deprecated as they are now entirely
    unnecessary. A new option has been added called `preview` that controls whether the script output generates a
    preview or not when the rendered math output is loading. Users no longer need to configure `tex2jax.js` in there
    MathJax configuration anymore. (#171)
-   **NEW**: PlainHTML has been renamed to StripHTML. `strip_attributes` is now a list instead of a string with a
    default of `[]`. `pymdownx.plainhtml` is still available with the old convention for backwards compatibility, but
    will be removed for version 5.0. (!176)
-   **FIX**: PlainHTML has better script and style content avoidance to keep from stripping HTML tags and attributes
    from style and script content. (!174)
-   **FIX**: PlainHTML can strip attributes that are not quoted. (!174)

## 4.5.1

-   **FIX**: If an invalid provider is given, default to `github`. If no `user` or `repo` is specified, do not convert
    links that depend on those default values. (#169)

## 4.5

-   **NEW**: Add GitLab style compare link shorthand and link shortening. (#160)
-   **NEW**: Deprecate GitHub extension. It is now recommended to just include the extensions you want to create a
    GitHub feel instead of relying on a an extension to package something close-ish. (#159)

## 4.4

-   **NEW**: Add social media mentions -- Twitter only right now. (#156)
-   **FIX**: Use correct regular expression for GitLab and Bitbucket.

## 4.3

-   **NEW**: Shorthand format for referencing non-default provider commits, issues, pulls, and mentions. (!147)
-   **NEW**: Shorthand format for mentioning a repo via `@user/repo`. (!149)
-   **NEW**: Add repository provider specific classes. (!149)
-   **NEW**: Make repository labels configurable. (!149)
-   **FIX**: Adjust pattern boundaries auto-links.

## 4.2

-   **NEW**: MagicLink can now auto-link a GitHub like shorthand for repository references. (!139)
-   **NEW**: MagicLink now renders pull request links with a slightly different output from issues. (!139)
-   **NEW**: Deprecate `base_repo_url` in MagicLink in favor of the new `provider`, `user`, and `repo`. (!139)
-   **NEW**: MagicLink now adds classes to repository links. (!139)
-   **NEW**: MagicLink now adds title to repository links. (!139)
-   **NEW**: MagicLink no longer styles repository commit hashes as code. (!143)
-   **FIX**: MagicLink repository link outputs now better reflect default user and repository context. (!143)
-   **FIX**: PlainHTML should not strip tags that are part of JavaScript code. (!140)

## 4.1

-   **NEW**: Details can now have multiple classes defined.

## 4.0

-   **NEW**: Details extension will now derive a title from the class if only a class is provided. (#107)
-   **NEW**: Remove deprecated legacy emoji generator format.
-   **NEW**: Remove deprecated `use_codehilite_settings`.
-   **NEW**: Remove deprecated `spoilers` extension redirect.
-   **NEW**: Update emoji databases: EmojiOne (3.1.2) and Twemoji to .(2.5.0)

## 3.5

-   **NEW**: Add new slugs to preserve case. (!103)
-   **NEW**: Add new GFM specific slug (both percent encoded and normal) that only lowercases ASCII chars just like GFM
    does. (#101)
-   **FIX**: PathConverter should not try and convert obscured email address (with HTML entities). (#100)
-   **FIX**: Don't normalize Unicode in slugs with `NFKD`, use `NFC` instead. (#98)
-   **FIX**: Don't let EscapeAll escape CriticMarkup placeholders.  EscapeAll will no longer escape `STX` and `ETX`;
    they will just pass through. (#95)
-   **FIX**: Replace CriticMarkup placeholders after replacing raw HTML placeholders. (#95)

## 3.4

-   **NEW**: Renamed Spoilers to Details
-   **NEW**: No longer attach the `spoilers` class to `details` tags.
-   **NEW**: Provide better example of UML script in documents.

## 3.3

-   **NEW**: Added support for pull request link shortening in MagicLink. (!88)
-   **NEW**: Added new Spoilers extension. (#85)

## 3.2.1

-   **FIX**: Cannot set Highlight's CSS class.

## 3.2

-   **NEW**: Add support for Twemoji 2.3.5.
-   **NEW**: Update to EmojiOne 3.0.2.
-   **NEW**: Emoji generators now also take `category` which is also no included in all indexes.
-   **FIX**: Excessive new lines at end of code blocks.

## 3.1

-   **NEW**: Highlight extension now runs normal indented code blocks through highlighter.
-   **FIX**: When Pygments is disabled, `linenums` class was attached to code blocks even if `linenums` was disabled and
    not enabled via fence headers.

## 3.0

-   **NEW**: Added Keys extension.
-   **NEW**: Generalized custom fences (#60). `flow` and `sequence` fence are now just custom fences and can be disabled
    simply by overwriting the `custom_fences` setting.
-   **NEW**: Remove deprecated `no_nl2br` in GitHub extension. (#24)
-   **NEW**: Remove deprecated HeaderAnchor extension. (#24)
-   **NEW**: Remove deprecated PyMdown extension. (#24)
-   **NEW**: Remove deprecated GitHubEmoji extension. (#24)
-   **NEW**: Remove deprecated `nested` option in SuperFences. (#24)
-   **NEW**: Wrapper extensions (such as GitHub and Extra) can now allow setting the included sub extensions settings
    (#61). Workaround settings that directly set specific extensions settings has been removed.
-   **NEW**: Deprecated `use_codehilite_settings` in SuperFences and InlineHilite and now does nothing.  The settings
    will be removed in the future.  If `pymdownx.highlight` is used, it's settings will be used instead of CodeHilite.
    Eventually, the both SuperFences and InlineHilite will require `pymdownx.highlight` to be used and will have
    CodeHilite support stripped.
-   **FIX**: Fix MathJax CDN references and usage in documentation.  MathJax CDN is shutting down and must now use
    Cloudflare CDN. (#63)

## 2.0

-   **NEW**: SuperFences and InlineHilite can be configured via the new Highlight extension.
-   **NEW**: InlineHilite now has all highlighting features pushed to the Highlight extension.  This removes all the
    CodeHilite code that used to be in it and instead relocates it to Highlight.
-   **NEW**: Deprecate the nesting option in SuperFences.  Nesting is default and the only acceptable behavior moving
    forward.  The ability to turn off nesting will be removed in 3.0.

## 1.8

-   **NEW**: MagicLink special repository link shortener for GitHub, GitLab, and Bitbucket. (#49)
-   **FIX**: GitHub asterisk emphasis should never have had smart enabled for it. (#50)
-   **FIX**: MagicLink fix for compatibility with wrapped symbols like `~`, `*` etc. which are commonly used.
-   **FIX**: MagicLink encodes emails like Python Markdown does for consistency.
-   **FIX**: MagicLink doesn't allow Unicode for email and does allow Unicode in a URL. (#53)
-   **FIX**: InlineHilite now returns a proper `etree` element so that the `attr_list` extension and function properly
    with it. (#48)
-   **FIX**: InlineHilite will no longer break if Pygments is not installed (478b410a2199d55f3e70b452516511d3810c61a5).

## 1.7

-   **NEW**: Arithmatex now supports `\(...\)`, `\[...\]`, and `\begin{}...\end{}`.
-   **NEW**: Arithmatex has an option to embed the math code in MathJax script tags.
-   **FIX**: Unfortunately the wrap option is now run through an HTML escaper and HTML tags can no longer be fed in this
    way.  Arithmatex also now wraps "wrapped" content with spans to containerize content and keep one equation from
    bleeding into the next.
-   **FIX**: Better handling of escaped Arithmatex inline tokens.
-   **FIX**: Better handling of escaped InlineHilite tokens.
-   **FIX**: Update InlineHilite and SuperFences so that the language option can accept things like `c#` and `.net` etc.
-   **FIX**: Snippets now removes carriage returns from imported files to prevent breakage.

## 1.6.1

-   **FIX**: Don't install tools or tests folder when installing from Pypi.

## 1.6

-   **NEW**: EscapeAll has the option to perform more like Pandoc in that you can enable escaped newlines to be
    `hardbreaks`, and escaped spaces to be `nbsp`.
-   **NEW**: Rework poorly thought out snippets format to require quoting file names with single line format.  Add a
    block format.  Allow commenting out lines temporarily.  And allow a way to escape them by placing a space after
    them.
-   **FIX**: Fix documentation issues.

## 1.5

-   **NEW**: New EscapeAll extension.
-   **NEW**: New Snippets extension for including external files into a Markdown file.
-   **NEW**: Arithmatex now has configurable output wrapper.
-   **NEW**: PathConverter no longer verifies existence of path to allow it more flexible usage.
-   **NEW**: PathConverter now only converts relative paths when converting to a relative or absolute location.
-   **NEW**: Improved support for path path identification for PathConverter and B64.
-   **FIX**: Fixed issue where Arithmatex was un-escaping `$` within math region.
-   **FIX**: Fixed issue where plugins would append globally changing the escape list opposed to just in the in the
    Markdown instance.
-   **FIX**: Fixed logic issue where the `mark`, `caret`, and `tilde` extension weren't quite modeling `betterem` inline
    behavior.
-   **FIX**: Critics shouldn't allow escaping critic marks as it is not in the spec.

## 1.4

-   **NEW**: HeaderAnchor extension is now deprecated.  It will be removed in a future version.
-   **NEW**: HeaderAnchor is no longer included in the `pymdownx.github` extension.
-   **NEW**: Slugify functions are moved to `pymdownx.slug` in preparation of HeaderAnchor removal.
-   **FIX**: GitHubEmoji is not "pending" deprecation, but is actually deprecated.

## 1.3

-   **NEW**: New Emoji extension that aims to replace GitHubEmoji.  By default it is configured for EmojiOne and Gemoji
    (GitHub's emoji).
-   **NEW**: GitHubEmoji is deprecated. Please use the Emoji extension instead.
-   **NEW**: PyMdown extension is deprecated.  PyMdown extension was just a wrapper, please configure the desired
    individual extension(s) instead of relying on PyMdown.
-   **NEW**: `github` extension now turns off `nl2br` by default in order properly emulate recent changes in GFM.
    `no_nl2br` option is deprecated and will be removed in the future as it no longer reflects GFM behavior.

## 1.2

-   **NEW**: Add option to output task lists in a more customizable way.

## 1.1

-   **NEW**: Add pypi 3.5 info in setup
-   **NEW**: Add option to MagicLink extension to allow the stripping of link protocols (`http://` etc.).
-   **NEW**: Add option to `github` extension to disable the use of `nl2br` to reflect recent changes to GitHub Flavored
    Markdown.  Currently the default is the legacy (uses `nl2br`), but a warning will be displayed.  In the future, the
    option will be defaulted to not use `nl2br`.

## 1.0.1

-   **FIX**: Ordinal number 11th, 12th, and 13th

## 1.0.0

-   **NEW**: Initial release.
