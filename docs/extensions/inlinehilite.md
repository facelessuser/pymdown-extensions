# InlineHilite {: .doctitle}
Inline syntax highlighting.

---

## Overview
InlineHilite extends [CodeHilite](https://pythonhosted.org/Markdown/extensions/code_hilite.html) to add inline code highlighting.  Borrowing from CodeHilite's existing syntax, InlineHilite utilizes the following syntax to insert inline  highlighted code: `` `:::language mycode` `` or `` `#!language mycode` ``.  We will call these specifiers mock shebangs.

When using the colon mock shebang, 3 or more colons can be used.  Mock shebangs must come **immediately** after the opening backtick(s) and must be followed by at least one space.  If you need to escape a mock shebang at the start of a code block, just put a space before it and it will be treated as part of the code.

!!! tip "Tip"
    If using Pygments, the elements should be highlighted just fine, but you may need to adjust CSS to get the general style of the inline block the way you like it.

    If you are using a JavaScript highlighter such as `highlight.js` you will most likely need to construct a JavaScript method to target the inline blocks.  You may also find it useful to tag inline blocks with a different class than the normal highlighted blocks so you can also target and style them with CSS differently.  InlineHilite allows you to have a different `css_class` than what is used by `CodeHilite`.

## Options
By default, InlineHilite will use CodeHilite's settings if it is being used, but InlineHilite can be run without CodeHilite, and if desired, it can be run along side it and ignore CodeHilite's settings.

| Option    | Type | Default |Description |
|-----------|------|---------|------------|
| style_plain_text | bool | False | By default, InlineHilite will ignore a code block with no language specified or the `text` language specified.  No classes or style will be applied, the code block will be styled as normal.  If this is set true, text blocks will be processed and have classes injected into them even though only the plain text lexer is applied. |
| use_codehilite_settings | bool | True | Determine whether CodeHilite's settings should be used, or if InlineHilite should use a different set. |
| guess_lang | bool | True | If ignoring CodeHilite's settings, determine whether InlineHilite should try to guess a code block's language if not specified. |
| css_class | string | 'inlinehilite' | If ignoring CodeHilite's settings, this is the class name that will be injected into code tags when they are processed. |
| pygments_style | string | 'default' | If ignoring CodeHilite's settings, this is the pygments style to use.  When using Python Markdown, this really only has an effect when using `noclasses`. |
| noclasses | bool | False | If ignoring CodeHilite's settings, this will cause the styles to directly be written to the tag's style attribute instead of requiring a stylesheet. |
| use_pygments | bool | True | If Pygments is available, and if ignoring CodeHilite's settings, this will control whether Pygements is used on the code block, or if the block's content will just be escaped and prepped for a JavaScript syntax highlighter. |

## Example

```
Here is some code: `#!js function pad(v){return ('0'+v).split('').reverse().splice(0,2).reverse().join('')}`.

The mock shebang will be treated like text here: ` #!js var test = 0; `.
```

Here is some code: `#!js function pad(v){return ('0'+v).split('').reverse().splice(0,2).reverse().join('')}`

The mock shebang will be treated like text here: ` #!js var test = 0; `.
