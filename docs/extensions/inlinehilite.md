## Overview

InlineHilite is an inline code highlighter inspired by [CodeHilite][codehilite]. Borrowing from CodeHilite's existing syntax, InlineHilite utilizes the following syntax to insert inline highlighted code: `` `:::language mycode` `` or `` `#!language mycode` ``.  In CodeHilite, ` #! ` means "use line numbers", but line numbers will never be used in inline code regardless of which form is used. Use of one form or the other is purely for personal preference. As this feature is discussed further, we will call these specifiers (` #! ` and ` ::: `) mock shebangs.

When using the colon mock shebang, 3 or more colons can be used.  Mock shebangs must come **immediately** after the opening backtick(s) and must be followed by at least one space.  If you need to escape a mock shebang at the start of a code block, just put a space before it and it will be treated as part of the code.

## Using JavaScript Highlighters

If using [Pygments][pygments], the elements will be highlighted without issues, but you may need to adjust CSS to get the general style of the inline block the way you like it.

If you are using a JavaScript highlighter, such as [`highlight.js`][highlightjs], you will most likely need to construct a JavaScript method to target the inline blocks as these may not be targeted out of the box. You may also find it useful to tag inline code with a different class than what is used for block code so you can also process and style them differently. The CSS class used can be configured independently for inline code in the options if using `pymdownx.highight` instead of CodeHilite.

## Options

By default, syntax highlighting settings will be sourced from [CodeHilite][codehilite] if it is configured and `use_codehilite_settings` is enabled, but InlineHilite's highlighting can be configure without and/or independently from CodeHilite. If CodeHilite is not configured, or if `use_codehilite_settings` is disabled, default settings will be used and can be configured via [`pymdownx.highlight`](./highlight.md).  CodeHilite support will most likely be abandoned in the future, so keep that in mind when configuring.

Option                    | Type   | Default                   | Description
------------------------- | ------ | ------------------------- | -----------
`style_plain_text`        | bool   | `#!py False`              | When `guess_lang` is set to `#!py False`, InlineHilite will avoid applying classes to code blocks that do not explicitly set a language. If it is desired to have plain text styled like code, enable this to inject classes so that they can all be styled the same.
`use_codehilite_settings` | bool   | `#!py True`               | Get applicable highlight settings from CodeHilite (if currently configured). CodeHilite's settings will be applied to `css_class` and additional behavioral options will be applied. Otherwise, use `css_class`, and configure settings via `pymdownx.highlight`.
`css_class`               | string | `#!python 'highlight'` | Set's the class name that will be injected into inline code tags when they are processed.

## Example

```
Here is some code: `#!js function pad(v){return ('0'+v).split('').reverse().splice(0,2).reverse().join('')}`.

The mock shebang will be treated like text here: ` #!js var test = 0; `.
```

Here is some code: `#!js function pad(v){return ('0'+v).split('').reverse().splice(0,2).reverse().join('')}`

The mock shebang will be treated like text here: ` #!js var test = 0; `.

--8<-- "links.md"
