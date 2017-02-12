## Overview

Highlight is an extension that adds no additional syntax patterns to Python Markdown. Its only purpose is to provide a single place to configure syntax highlighting for code blocks. Both [InlineHilite](./inlinehilite.md) and [SuperFences](./superfences.md) can use Highlight to configure their highlight settings.

Both InlineHilite and SuperFences can use [Pygments][pygments] or JavaScript highlighters to do their code syntax highlighting, but all of the settings here affect Pygments highlighting only except `use_pygments`.  If you want to use a JavaScript syntax highlighter, set `use_pygments` to `#!py False` or make sure you don't have Pygments installed.

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
`guess_lang`              | bool   | `#!py False`              | Guess what syntax language should be used if no language is specified. This can be particularly tricky with 
`pygments_style`          | string | `#!python 'default'`      | Set the Pygments' style to use.  This really only has an effect when used with `noclasses`.
`noclasses`               | bool   | `#!py False`              | This will cause the styles to directly be written to the tag's style attribute instead of requiring a stylesheet.
`use_pygments`            | bool   | `#!py True`               | Controls whether Pygments (if available) is used to style the code, or if the code will just be escaped and prepped for a JavaScript syntax highlighter.
`linenums`                | bool   | `#!py False`              | Enable line numbers globally for *block* code.  This will be ignored for *inline* code.
`extend_pygments_lang`    | list   | `#!py []`                 | A list of extended languages to add.  See [Extended Pygments Lexer Options](#extended-pygments-lexer-options) for more info.

--8<-- "refs.md"
