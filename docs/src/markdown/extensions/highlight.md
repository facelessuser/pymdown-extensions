# Highlight

## Overview

Highlight is an extension that adds support for code highlighting. Its purpose is to provide a single place to configure syntax highlighting for code blocks. Both [InlineHilite](./inlinehilite.md) and [SuperFences](./superfences.md) can use Highlight to configure their highlight settings, but highlight will also run all non-fence code blocks through the highlighter as well.

The Highlight extension is inspired by [CodeHilite][codehilite], but differs in features. PyMdown Extensions chooses not to implement special language headers for standard Markdown code blocks like CodeHilite does; PyMdown Extensions takes the position that language headers are better suited in fenced code blocks. So standard Markdown code blocks will just be styled as plain text unless `guess_language` is enabled. If you wish to highlight lines and define line numbers per code block, it is advised to use the SuperFences extension. Highlight also provides a feature CodeHilite doesn't, and that is the ability to configure Pygments lexer options by either overriding the language with additional options, or creating an alternate language name with your desired options.

As previously mentioned, both InlineHilite's and SuperFences' highlighting can be controlled by Highlight. Both can use [Pygments][pygments] or JavaScript highlighters to do their code syntax highlighting, but all of the settings here only affect highlighting via Pygments except `use_pygments` and `css_class`.  If you want to use a JavaScript syntax highlighter, set `use_pygments` to `#!py False` or make sure you don't have Pygments installed.

## Syntax Highlighting

If Pygments is installed, it will be the default syntax highlighter, but if it is not, or if `use_pygments` is turned off, code tags will be rendered in the HTML5 format for JavaScript highlighting: `#!html <pre class="highlight"><code class="language-mylanguage"></code></pre>`.

## Extended Pygments Lexer Options

If using Pygments, some lexers have special options.  For instance, the `php` lexer has the option `startinline` which, if enabled, will parse PHP syntax without requiring `#!php <?` at the beginning.  InlineHilite takes the approach of allowing you to create a special Pygments language with options.  So if you wanted to enable `startinline` for `php`, you might create a language name called `php-inline` that maps to `php` with `startinline` enabled.  This is done via the `extend_pygments_lang` option.

`extend_pygments_lang` is an option that takes an array of dictionaries.  Each dictionary contains three keys: `name` which is the new name you are adding, `lang` which is the language the new name maps to, and `options` which is a dictionary of the options you wish to apply.

For example, to create the above mentioned `php-inline` we would feed in the following to `extend_pygments_lang`:

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


## Options

Option                    | Type   | Default                   | Description
------------------------- | ------ | ------------------------- | -----------
`css_class`               | string | `#!py 'highlight'         | Default class to apply to the wrapper element on code blocks. Other extensions can override this.
`guess_lang`              | bool   | `#!py False`              | Guess what syntax language should be used if no language is specified. 
`pygments_style`          | string | `#!python 'default'`      | Set the Pygments' style to use.  This really only has an effect when used with `noclasses`.
`noclasses`               | bool   | `#!py False`              | This will cause the styles to directly be written to the tag's style attribute instead of requiring a stylesheet.
`use_pygments`            | bool   | `#!py True`               | Controls whether Pygments (if available) is used to style the code, or if the code will just be escaped and prepped for a JavaScript syntax highlighter.
`linenums`                | bool   | `#!py False`              | Enable line numbers globally for *block* code.  This will be ignored for *inline* code.
`extend_pygments_lang`    | list   | `#!py []`                 | A list of extended languages to add.  See [Extended Pygments Lexer Options](#extended-pygments-lexer-options) for more info.

--8<-- "refs.md"
