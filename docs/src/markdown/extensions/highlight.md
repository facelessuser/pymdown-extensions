# Highlight

## Overview

Highlight is an extension that adds support for code highlighting. Its purpose is to provide a single place to configure
syntax highlighting for code blocks. Both [InlineHilite](./inlinehilite.md) and [SuperFences](./superfences.md) can use
Highlight to configure their highlight settings, but highlight will also run all non-fence code blocks through the
highlighter as well.

The Highlight extension is inspired by [CodeHilite][codehilite], but differs in features. PyMdown Extensions chooses not
to implement special language headers for standard Markdown code blocks like CodeHilite does; PyMdown Extensions takes
the position that language headers are better suited in fenced code blocks. So standard Markdown code blocks will just
be styled as plain text unless `guess_language` is enabled. If you wish to highlight lines and define line numbers per
code block, it is advised to use the SuperFences extension. Highlight also provides a feature CodeHilite doesn't, and
that is the ability to configure Pygments lexer options by either overriding the language with additional options, or
creating an alternate language name with your desired options.

As previously mentioned, both InlineHilite's and SuperFences' highlighting can be controlled by Highlight. Both can use
[Pygments][pygments] or JavaScript highlighters to do their code syntax highlighting, but all of the settings here only
affect highlighting via Pygments except `use_pygments` and `css_class`.  If you want to use a JavaScript syntax
highlighter, set `use_pygments` to `#!py3 False` or make sure you don't have Pygments installed.

The Highlight extension can be included in Python Markdown by using the following:

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.highight'])
```

## Syntax Highlighting

If Pygments is installed, it will be the default syntax highlighter, but if it is not, or if `use_pygments` is turned
off, code tags will be rendered in the HTML5 format for JavaScript highlighting: 

```html
<pre class="highlight"><code class="language-mylanguage"></code></pre>
```

## Extended Pygments Lexer Options

If using Pygments, some lexers have special options.  For instance, the `php` lexer has the option `startinline` which,
if enabled, will parse PHP syntax without requiring `#!php <?` at the beginning.  InlineHilite takes the approach of
allowing you to create a special Pygments language with options.  So if you wanted to enable `startinline` for `php`,
you might create a language name called `php-inline` that maps to `php` with `startinline` enabled.  This is done via
the `extend_pygments_lang` option.

`extend_pygments_lang` is an option that takes an array of dictionaries.  Each dictionary contains three keys: `name`
which is the new name you are adding, `lang` which is the language the new name maps to, and `options` which is a
dictionary of the options you wish to apply.

!!! example "Highlight Example"

    To create the above mentioned `php-inline` we would feed in the following to `extend_pygments_lang`:

    ```py
    extended_pygments_lang = [
        {"name": "php-inline", "lang": "php", "options": {"startinline": True}}
    ]
    ```

    Now we can do this:

    ````
    `#!php-inline $a = array("foo" => 0, "bar" => 1);`
    ````

    To get this:

    `#!php-inline $a = array("foo" => 0, "bar" => 1);`

## Line Number Styles

Pygments has two available styles when outputting source code with line numbers enabled: `table` and `inline`. `table`
is the default output and creates a table output for lines with numbers.  `inline` places the line numbers directly in
the source code output and can sometimes be undesirable as it copy and paste will always copy the line numbers as well.

The Highlight extension provides a third line number style called `pymdownx-inline`.  Instead of writing line numbers
directly in the pre like Pygments' default `inline` style does, it writes the line numbers as
`#!html <span class="lineno" data-linenos="1 "></span>`. This way the line numbers are un-selectable and can be
displayed with CSS:

```css
[data-linenos]:before {
  content: attr(data-linenos);
}
```

Line number styles are set with the option `linenums_style` as described in [Options](#options).

## Options

Option                    | Type   | Default               | Description
------------------------- | ------ | ----------------------| -----------
`css_class`               | string | `#!py3 'highlight`    | Default class to apply to the wrapper element on code blocks. Other extensions can override this.
`guess_lang`              | bool   | `#!py3 False`         | Guess what syntax language should be used if no language is specified. 
`pygments_style`          | string | `#!py3thon 'default'` | Set the Pygments' style to use.  This really only has an effect when used with `noclasses`.
`noclasses`               | bool   | `#!py3 False`         | This will cause the styles to directly be written to the tag's style attribute instead of requiring a stylesheet.
`use_pygments`            | bool   | `#!py3 True`          | Controls whether Pygments (if available) is used to style the code, or if the code will just be escaped and prepped for a JavaScript syntax highlighter.
`linenums`                | bool   | `#!py3 False`         | Enable line numbers globally for *block* code.  This will be ignored for *inline* code.
`linenums_special`        | int    | `#!py3 1`             | Globally sets the specified nth lines' gutter with the class "special".  This can be overridden in [SuperFences](./superfences.md) per fence if desired.
`linenums_style`          | string | `#!py3 'table'`       | Controls the output style when `linenums` are enabled. Supported styles are Pygments default `table` and `inline`, but also supported is the pymdown-extensions `pymdownx-inline` which provides a special inline mode, see [Line Number Styles](#line-number-styles) for more info.
`extend_pygments_lang`    | list   | `#!py3 []`            | A list of extended languages to add.  See [Extended Pygments Lexer Options](#extended-pygments-lexer-options) for more info.

--8<-- "refs.txt"
