# InlineHilite

## Overview

InlineHilite is an inline code highlighter inspired by [CodeHilite][codehilite]. Borrowing from CodeHilite's existing syntax, InlineHilite utilizes the following syntax to insert inline highlighted code: `` `:::language mycode` `` or `` `#!language mycode` ``.  In CodeHilite, ` #! ` means "use line numbers", but line numbers will never be used in inline code regardless of which form is used. Use of one form or the other is purely for personal preference. As this feature is discussed further, we will call these specifiers (` #! ` and ` ::: `) mock shebangs.

When using the colon mock shebang, 3 or more colons can be used.  Mock shebangs must come **immediately** after the opening backtick(s) and must be followed by at least one space.  If you need to escape a mock shebang at the start of a code block, just put a space before it and it will be treated as part of the code.

## Code Highlighting

Assuming Pygments is installed, code highlighting will be handled by [Pygments][pygments] by default. If Pygments is not installed, or disabled, code blocks will be output for JavaScript syntax highlighters as `#!html <code class="highlight language-mylanguage"></code>`.

Highlighting can be further controlled if either the `pymdownx.highlight` extension is used or if Python Markdown's CodeHilite is used. If CodeHilite is configured, it's settings will be used to configure highlighting, but CodeHilite support is deprecated and will be removed in the next major release. It is recommended to instead use [`pymdownx.highlight`](./highlight.md) extension. If `pymdownx.highlight` is included and configured, CodeHilite will be ignored.

## Using JavaScript Highlighters

If using [Pygments][pygments], the elements will be highlighted without issues, but you may need to adjust CSS to get the general style of the inline block the way you like it.

If you are using a JavaScript highlighter, such as [`highlight.js`][highlightjs], you will most likely need to construct a JavaScript method to target the inline blocks as these may not be targeted out of the box. You may also find it useful to tag inline code with a different class than what is used for block code so you can also process and style them differently. The CSS class used can be configured independently for inline code in the options if using `pymdownx.highight` instead of CodeHilite.

## Options

Option                    | Type   | Default      | Description
------------------------- | ------ | ------------ | -----------
`css_class`               | string | `#!py ''`    | Class name is applied to the wrapper element of the code. If configured, this setting will override the `css_class` option of either CodeHilite or Highlight. If nothing is configured here or via CodeHilite or Highlight, the class `highlight` will be used.
`style_plain_text`        | bool   | `#!py False` | When `guess_lang` is set to `#!py False`, InlineHilite will avoid applying classes to code blocks that do not explicitly set a language. If it is desired to have plain text styled like code, enable this to inject classes so that they can all be styled the same.

!!! warning "Deprecated 3.0.0"
    The setting `use_codehilite_settings` has been deprecated since `3.0.0` and now does nothing. It is still present to avoid breakage, but will be removed in the future.

## Example

```
Here is some code: `#!js function pad(v){return ('0'+v).split('').reverse().splice(0,2).reverse().join('')}`.

The mock shebang will be treated like text here: ` #!js var test = 0; `.
```

Here is some code: `#!js function pad(v){return ('0'+v).split('').reverse().splice(0,2).reverse().join('')}`

The mock shebang will be treated like text here: ` #!js var test = 0; `.

--8<-- "links.md"
