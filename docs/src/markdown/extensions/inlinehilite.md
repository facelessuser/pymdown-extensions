# InlineHilite

## Overview

InlineHilite is an inline code highlighter inspired by [CodeHilite][codehilite]. Borrowing from CodeHilite's existing syntax, InlineHilite utilizes the following syntax to insert inline highlighted code: `` `:::language mycode` `` or `` `#!language mycode` ``.  In CodeHilite, ` #! ` means "use line numbers", but line numbers will never be used in inline code regardless of which form is used. Use of one form or the other is purely for personal preference. As this feature is discussed further, we will call these specifiers (` #! ` and ` ::: `) mock shebangs.

!!! example "Inline Highlighted Code Example"

    ```
    Here is some code: `#!js function pad(v){return ('0'+v).split('').reverse().splice(0,2).reverse().join('')}`.

    The mock shebang will be treated like text here: ` #!js var test = 0; `.
    ```

    Here is some code: `#!js function pad(v){return ('0'+v).split('').reverse().splice(0,2).reverse().join('')}`

    The mock shebang will be treated like text here: ` #!js var test = 0; `.

When using the colon mock shebang, 3 or more colons can be used.  Mock shebangs must come **immediately** after the opening backtick(s) and must be followed by at least one space.  If you need to escape a mock shebang at the start of a code block, just put a space before it and it will be treated as part of the code.

## Code Highlighting

Assuming Pygments is installed, code highlighting will be handled by [Pygments][pygments] by default. If Pygments is not installed, or disabled, code blocks will be output for JavaScript syntax highlighters as `#!html <code class="highlight language-mylanguage"></code>`.

Highlighting can be further controlled if either the `pymdownx.highlight` extension is used or if Python Markdown's CodeHilite is used. If CodeHilite is configured, it's settings will be used to configure highlighting, but CodeHilite support is deprecated and will be removed in the next major release. It is recommended to instead use [`pymdownx.highlight`](./highlight.md) extension. If `pymdownx.highlight` is included and configured, CodeHilite will be ignored.

## Using JavaScript Highlighters

If using [Pygments][pygments], the elements will be highlighted without issues, but you may need to adjust CSS to get the general style of the inline block the way you like it.

If you are using a JavaScript highlighter, such as [`highlight.js`][highlightjs], you will most likely need to construct a JavaScript method to target the inline blocks as these may not be targeted out of the box. You may also find it useful to tag inline code with a different class than what is used for block code so you can also process and style them differently. The CSS class used can be configured independently for inline code in the options if using `pymdownx.highight` instead of CodeHilite.

## Custom Inline Blocks

Like [SuperFences](./superfences.md), InlineHilite now provides a support for custom inline blocks.

!!! example "Inline Math"
    ```
    `#!math p(x|y) = \frac{p(y|x)p(x)}{p(y)}`
    ```

    `#!math p(x|y) = \frac{p(y|x)p(x)}{p(y)}`

!!! tip "Math Example"
    For more indepth information on how to reproduce the example above, check out [Arithmatex Documentation](./arithmatex.md#alternative-math-blocks).

Custom inline code blocks are created via the `custom_inline` option.  `custom_inline` takes an array of dictionaries where each dictionary defines a custom inline code block. The dictionaries requires the following keys:

Keys        | Description
----------- | -----------
`name`      | The language name that is specified when using the fence in Markdown.
`class`     | The class name assigned to the HTML element when converting from Markdown to HTML.
`format`    | A function that formats the HTML output.  Should return a either an ElementTree object (preferable) or a string as HTML.

### Formatters

In general, formatters take three parameters: the source found between the backticks, the specified language, and the class name originally defined via the `class` option in the `custom_inline` entry. Should return a either an ElementTree element (preferable) or a string as HTML.

```python
def custom_formatter(source, language, css_class):
    return el
```

## Options

Option                    | Type         | Default       | Description
------------------------- | ------------ | ------------- | -----------
`css_class`               | string       | `#!py3 ''`    | Class name is applied to the wrapper element of the code. If configured, this setting will override the `css_class` option of either CodeHilite or Highlight. If nothing is configured here or via CodeHilite or Highlight, the class `highlight` will be used.
`style_plain_text`        | bool         | `#!py3 False` | When `guess_lang` is set to `#!py3 False`, InlineHilite will avoid applying classes to code blocks that do not explicitly set a language. If it is desired to have plain text styled like code, enable this to inject classes so that they can all be styled the same.
`custom_inline`           | [dictionary] | `#!py3 []`    | Custom inline code blocks.

---8<---
links.txt

mathjax.txt
---8<---
