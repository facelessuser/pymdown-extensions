## Overview

InlineHilite is an inline version of [CodeHilite][codehilite] which adds inline code highlighting.  Borrowing from CodeHilite's existing syntax, InlineHilite utilizes the following syntax to insert inline highlighted code: `` `:::language mycode` `` or `` `#!language mycode` ``.  In CodeHilite, ` #! ` means "use line numbers", but line numbers will not be used in inline code regardless of which form is used; syntax choice is purely personal preference.  We will call these specifiers (` #! ` and ` ::: `) mock shebangs.

When using the colon mock shebang, 3 or more colons can be used.  Mock shebangs must come **immediately** after the opening backtick(s) and must be followed by at least one space.  If you need to escape a mock shebang at the start of a code block, just put a space before it and it will be treated as part of the code.

!!! tip "Tip"
    If using [Pygments][pygments], the elements should be highlighted just fine, but you may need to adjust CSS to get the general style of the inline block the way you like it.

    If you are using a JavaScript highlighter such as [`highlight.js`][highlightjs] you will most likely need to construct a JavaScript method to target the inline blocks.  You may also find it useful to tag inline blocks with a different class than what is used for block highlighted code so you can also target and style them with CSS differently.  InlineHilite allows you to have a different `css_class` than what is used by block code (if CodeHilite is not used as the settings source).

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
