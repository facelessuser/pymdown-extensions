[:octicons-file-code-24:][_highlight]{: .source-link }

# Highlight

## Overview

Highlight is an extension that adds support for code highlighting. Its purpose is to provide a single place to configure
syntax highlighting for code blocks. Both [InlineHilite](./inlinehilite.md) and [SuperFences](./superfences.md) can use
Highlight to configure their highlight settings, but Highlight will also run all non-fence code blocks through the
highlighter as well.

The Highlight extension is inspired by [CodeHilite][codehilite], but differs in features. PyMdown Extensions chooses not
to implement special language headers for standard Markdown code blocks like CodeHilite does; PyMdown Extensions takes
the position that language headers are better suited in fenced code blocks. So standard Markdown code blocks will just
be styled as plain text unless `guess_language` is enabled. If you wish to highlight lines and define line numbers per
code block, it is advised to use the SuperFences extension.

The Highlight extension can be included in Python Markdown by using the following:

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.highlight'])
```

## Syntax Highlighting

If [Pygments][pygments] is installed, it will be the default syntax highlighter, but if it is not, or if `use_pygments`
is turned off, code tags will be rendered in the HTML5 format for JavaScript highlighting:

```html
<pre class="highlight"><code class="language-mylanguage"></code></pre>
```

`highlight` is the default class name, and will be applied to code blocks, whether Pygments is disabled or not. This
class name can be changed with the `css_class` option.

By default, the prefix `language-` is applied to language classes when Pygments is disabled or when Pygments code blocks
enable language classes via `pygments_lang_class`. This prefix can be changed via the `language_prefix` option.

The language class, and any attributes added via the [`attr_list`][attr-list] extension, are added to the
`#!html <code>` element. The `code_attr_on_pre` option will force them to be attached to the `#!html <pre>` element.

All other options specifically control the Pygments highlighter and will have no affect if Pygments usage is disabled.

## Extended Pygments Lexer Options

If using Pygments, some lexers have special settings. For instance, the `php` lexer has the option `startinline` which,
if enabled, will parse PHP syntax without requiring `#!php <?` at the beginning. Highlight allows you to configure
these settings via the option `extend_pygments_lang`.

`extend_pygments_lang` allows you to create a special Pygments alias language where you can configure the language
settings to your liking.  So if you wanted to enable `startinline` for `php`, you might create a language alias called
`php-inline` that maps to `php` with `startinline` enabled.  This would allow you to use `php` for normal PHP blocks,
but also allow you to do use `php-inline` for code without specifying `#!php <?`. You can also use
`extend_pygments_lang` to completely override the base language's options -- assuming your specified name overrides an
existing name.

`extend_pygments_lang`is an array of dictionaries. Each dictionary contains three keys: `name` which is the new name you
are adding, `lang` which is the language the new name maps to, and `options` which is a dictionary of the options you
wish to apply.

/// example | Highlight Example
To create the above mentioned `php-inline`, this example illustrates the configuration, and Markdown syntax you
would use.

//// tab | Output
`#!php-inline $a = array("foo" => 0, "bar" => 1);`
////

//// tab | Markdown
````
`#!php-inline $a = array("foo" => 0, "bar" => 1);`
````
////

//// tab | Config
```py
extend_pygments_lang = [
    {"name": "php-inline", "lang": "php", "options": {"startinline": True}}
]
```
////
///

/// new | New 9.2
`pygments_lang_class` added in 9.2.
///

## Line Number Styles

Pygments has two available styles when outputting source code with line numbers enabled: `table` and `inline`. `table`
is the default output and creates a table output for lines with numbers.  `inline` places the line numbers directly in
the source code output and can sometimes be undesirable as copy and paste will always copy the line numbers as well.

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

All options below control the Pygments' output. The three exceptions are `use_pygments` which disables Pygments,
`css_class` which sets the name of the class assigned to the generated code blocks, and `code_attr_on_pre` which only
apply when Pygments is disabled. Many of these options are demonstrated in the [SuperFences](./superfences.md) documentation.

Option                    | Type   | Default               | Description
------------------------- | ------ | ----------------------| -----------
`css_class`               | string | `#!py3 'highlight'`   | Default class to apply to the wrapper element on code blocks. Other extensions can override this.
`guess_lang`              | bool   | `#!py3 False`         | Guess what syntax language should be used if no language is specified. `#!py3 True` for always, `#!py3 False` for never, `#!py3 'block'` for block code only, and `#!py3 'inline'` for inline code only.
`pygments_style`          | string | `#!py3 'default'`     | Set the Pygments' style to use.  This really only has an effect when used with `noclasses`.
`noclasses`               | bool   | `#!py3 False`         | This will cause the styles to directly be written to the tag's style attribute instead of requiring a stylesheet.
`use_pygments`            | bool   | `#!py3 True`          | Controls whether Pygments (if available) is used to style the code, or if the code will just be escaped and prepped for a JavaScript syntax highlighter.
`linenums`                | bool   | `#!py3 None`          | Enable line numbers globally for *block* code.  This will be ignored for *inline* code. If set to `#!py3 False` line numbers will be disabled globally and can not be turned on, not even per code block.
`linenums_special`        | int    | `#!py3 1`             | Globally sets the specified nth lines' gutter with the class "special".  This can be overridden in [SuperFences](./superfences.md) per fence if desired.
`linenums_style`          | string | `#!py3 'table'`       | Controls the output style when `linenums` are enabled. Supported styles are Pygments default `table` and `inline`, but also supported is the pymdown-extensions `pymdownx-inline` which provides a special inline mode, see [Line Number Styles](#line-number-styles) for more info.
`linenums_class`          | string | `#!py3 'linenums'`    | Controls the name of the line number class when Pygments is not used.
`extend_pygments_lang`    | list   | `#!py3 []`            | A list of extended languages to add.  See [Extended Pygments Lexer Options](#extended-pygments-lexer-options) for more info.
`language_prefix`         | string | `#!py3 'language-'`   | Controls the prefix applied to the language class when Pygments is not used. By default, uses the HTML5 prefix of `language-`.
`code_attr_on_pre`        | bool   | `#!py3 False`         | By default, the language class and all attributes added via the [`attr_list`][attr-list] extension are attached to the `#!html <code>` element. This forces them to be attached to the `#!html <pre>` element.
`auto_title`              | bool   | `#!py3 False`         | When using Pygments, for all code blocks generate a title header with the name of the lexer being used. The lexer name is pulled directly from Pygments and title cased appropriately.
`auto_title_map`          | dict   | `#!py3 {}`            | A dictionary used to override certain titles returned by `auto_title`. Simply specify the title to override as the key and the desired title as the value.
`line_spans`              | string | `#!py3 ''`            | Controls the Pygments option of a similar name. If set to a nonempty string, e.g. `foo`, the formatter will wrap each output line in a `#!html <span>` tag with an id of `foo-<code_block_number>-<line_number>`.
`anchor_linenums`         | bool   | `#!py3 False`         | Enables the Pygments option of a similar name. If set to `#!py True`, will wrap line numbers in `#!html <a>` tags. Used in combination with `linenums` and `line_anchors`. If `line_anchors` is not configured, `__codelineno` will be assumed as the ID prefix.
`line_anchors`            | bool   | `#!py3 False`         | Controls the Pygments option of a similar name. If set to a nonempty string, e.g. `foo`, the formatter will insert an anchor tag with an id (and name) of `foo-<code_block_number>-<line_number>`.
`pygments_lang_class`     | bool   | `#!py3 False`         | If set to True, the language name used will be included as a class attached to the element with the associated `language_prefix`.

/// new | New 7.1
`linenums_class` was added in `7.1`.
///

/// new | New 7.2
`linenums` now accepts `#!py3 None` as the default for allow line numbers to be enabled per code block.
`#!py3 False` now disables line numbers globally preventing line numbers even if specified per code block. `True`
still enables globally.
///

/// new | New 9.0
`auto_title`, `auto_title_map`, `line_spans`, `anchor_linenums`, and `line_anchors` were all added in `9.0`.
///
