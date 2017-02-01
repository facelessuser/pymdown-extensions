## Overview

InlineHilite is an inline version of [CodeHilite][codehilite] which adds inline code highlighting.  Borrowing from CodeHilite's existing syntax, InlineHilite utilizes the following syntax to insert inline highlighted code: `` `:::language mycode` `` or `` `#!language mycode` ``.  We will call these specifiers (` #!language` and ` :::language`) mock shebangs.

When using the colon mock shebang, 3 or more colons can be used.  Mock shebangs must come **immediately** after the opening backtick(s) and must be followed by at least one space.  If you need to escape a mock shebang at the start of a code block, just put a space before it and it will be treated as part of the code.

!!! tip "Tip"
    If using Pygments, the elements should be highlighted just fine, but you may need to adjust CSS to get the general style of the inline block the way you like it.

    If you are using a JavaScript highlighter such as `highlight.js` you will most likely need to construct a JavaScript method to target the inline blocks.  You may also find it useful to tag inline blocks with a different class than the block highlighted code so you can also target and style them with CSS differently.  InlineHilite allows you to have a different `css_class` than what is used by `CodeHilite`.

## Pygments Lexer Options

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

!!! Note "Note"
    When specifying extended languages, they are shared across InlineHilite and SuperFences, so if you specify a language in SuperFences, you don't have to specify it in InlineHilite and vice versa.

## Options

By default, InlineHilite will use CodeHilite's settings if it is being used, but InlineHilite can be run without CodeHilite, and if desired, it can be run along side it and ignore CodeHilite's settings.

Option                    | Type   | Default                   | Description
------------------------- | ------ | ------------------------- | -----------
`style_plain_text`        | bool   | `#!py False`              | By default, InlineHilite will avoid syntax highlighting a code block with no language specified or the `text` language specified.  No classes or style will be applied, but the text will be formatted for a code element.  If this is set true, text blocks will be processed and have classes injected into them even though only the plain text lexer is applied.
`use_codehilite_settings` | bool   | `#!py True`               | Determine whether CodeHilite's settings should be used, or if InlineHilite should use a different set.
`guess_lang`              | bool   | `#!py True`               | If CodeHilite is not used, or if ignoring CodeHilite's settings, determine whether InlineHilite should try to guess a code block's language if not specified.
`css_class`               | string | `#!python 'inlinehilite'` | If ignoring CodeHilite's settings, this is the class name that will be injected into code tags when they are processed.
`pygments_style`          | string | `#!python 'default'`      | If CodeHilite is not used, or if ignoring CodeHilite's settings, this will be the Pygments' style to use.  When using Pygments, this really only has an effect when used with `noclasses`.
`noclasses`               | bool   | `#!py False`              | If CodeHilite is not used, or if ignoring CodeHilite's settings, this will cause the styles to directly be written to the tag's style attribute instead of requiring a stylesheet.
`use_pygments`            | bool   | `#!py True`               | If CodeHilite is not used, or if ignoring CodeHilite's settings, this will control whether Pygments (if available) is used on the code block, or if the block's content will just be escaped and prepped for a JavaScript syntax highlighter.
`extend_pygments_lang`    | list   | `#!py []`                 | A list of extended languages to add.  See [Pygments Lexer Options](#pygments-lexer-options) for more info.

## Example

```
Here is some code: `#!js function pad(v){return ('0'+v).split('').reverse().splice(0,2).reverse().join('')}`.

The mock shebang will be treated like text here: ` #!js var test = 0; `.
```

Here is some code: `#!js function pad(v){return ('0'+v).split('').reverse().splice(0,2).reverse().join('')}`

The mock shebang will be treated like text here: ` #!js var test = 0; `.

--8<-- "links.md"
