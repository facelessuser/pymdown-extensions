[:octicons-file-code-24:][_inlinehilite]{: .source-link }

# InlineHilite

## Overview

InlineHilite is an inline code highlighter inspired by [CodeHilite][codehilite]. Borrowing from CodeHilite's existing
syntax, InlineHilite utilizes the following syntax to insert inline highlighted code: `` `:::language mycode` `` or
`` `#!language mycode` ``.  In CodeHilite, ` #! ` means "use line numbers", but line numbers will never be used in
inline code regardless of which form is used. Use of one form or the other is purely for personal preference. As this
feature is discussed further, we will call these specifiers (` #! ` and ` ::: `) mock shebangs, mainly due to the first
options similar syntax to a real shebang.

!!! example "Inline Highlighted Code Example"

    === "Output"
        Here is some code: `#!py3 import pymdownx; pymdownx.__version__`

        The mock shebang will be treated like text here: ` #!js var test = 0; `.

    === "Markdown"
        ```
        Here is some code: `#!py3 import pymdownx; pymdownx.__version__`.

        The mock shebang will be treated like text here: ` #!js var test = 0; `.
        ```

When using the colon mock shebang, 3 or more colons can be used.  Mock shebangs must come **immediately** after the
opening backtick(s) and must be followed by at least one space.  If you need to escape a mock shebang, at the start of a
code block, just put a space before it, and it will be treated as part of the code.

The InlineHilite extension can be included in Python Markdown by using the following:

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.inlinehilite'])
```

## Code Highlighting

Assuming Pygments is installed, code highlighting will be handled by [Pygments][pygments]. If Pygments is not installed,
or disabled, code blocks will be output for JavaScript syntax highlighters as:


```html
<code class="highlight language-mylanguage"></code>
```

Highlighting can be further controlled via the [`pymdownx.highlight`](./highlight.md) extension.

## Using JavaScript Highlighters

If using [Pygments][pygments], the elements will be highlighted without issues, but you may need to adjust CSS to get
the general style of the inline block the way you like it.

If you are using a JavaScript highlighter, such as [`highlight.js`][highlightjs], you will most likely need to construct
a JavaScript method to target the inline blocks as these may not be targeted out of the box. You may also find it useful
to tag inline code with a different class than what is used for block code so you can also process and style them
differently. By default, it uses whatever [`pymdownx.highlight`](./highlight.md) uses, but this can be configured
independently for inline code in the [options](#options).

## Custom Inline Blocks

Like [SuperFences](./superfences.md), InlineHilite now provides a support for custom inline blocks.

!!! example "Inline Math"
    For more indepth information on how to reproduce the example above, check out [Arithmatex Documentation
    ](./arithmatex.md#alternative-math-blocks).

    === "Output"
        `#!math p(x|y) = \frac{p(y|x)p(x)}{p(y)}`

    === "Markdown"
        ```
        `#!math p(x|y) = \frac{p(y|x)p(x)}{p(y)}`
        ```

Custom inline code blocks are created via the `custom_inline` option.  `custom_inline` takes an array of dictionaries
where each dictionary defines a custom inline code block. The dictionaries requires the following keys:

Keys        | Description
----------- | -----------
`name`      | The language name that is specified when using the fence in Markdown. If given `*`, it will override the base inline logic, the default for all inline names not handled by other custom inlines.
`class`     | The class name assigned to the HTML element when converting from Markdown to HTML.
`format`    | A function that formats the HTML output. The function should return either an ElementTree object or a string as HTML.

!!! new "New in 7.0"
    Starting in 7.0, you can override the base inline logic (the syntax highlighter) by specifying the custom inline
    with a name of `*`. This means that if an inline does not match any other custom inline, the default, fallback
    inline would be handled by your custom `*` inline. This can be useful for tailoring a inline for a specific,
    favorite JavaScript highlighter.

### Formatters

```py3
def custom_formatter(source, language, css_class, md):
    return el  # Or string
```

In general, formatters take four parameters:

1. The source found between the backticks.
2. The specified language.
3. The class name originally defined via the `class` option in the `custom_inline` entry.
4. The Markdown class object.

It Should return a either an ElementTree element or a string as HTML. When returning a string, InlineHilite will treat
the string as ready for HTML, so escape what needs to be escaped as it is expected to be fully ready HTML and will be
stashed and re-inserted at post processing.

When returning an ElementTree object, remember to wrap string content as `markdown.util.AtomicString` to prevent it from
being processed further, you can also stash raw HTML string content assigned to elements like InlineHilite does by
default above. InlineHilite will not try and guess what you intend, you must manage your content in the ElementTree
objects or the Markdown parser may apply other conversion to your HTML content.

## Options

Option                    | Type         | Default       | Description
------------------------- | ------------ | ------------- | -----------
`css_class`               | string       | `#!py3 ''`    | Class name is applied to the wrapper element of the code. If configured, this setting will override the `css_class` option of Highlight. If nothing is configured here or via or Highlight, the class `highlight` will be used.
`style_plain_text`        | bool         | `#!py3 False` | When `guess_lang` is set to `#!py3 False`, InlineHilite will avoid applying classes to code blocks that do not explicitly set a language. If it is desired to have plain text styled like code, enable this to inject classes so that they can all be styled the same.
`custom_inline`           | [dictionary] | `#!py3 []`    | Custom inline code blocks.

---8<---
links.txt

mathjax.txt
---8<---
