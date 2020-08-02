[:octicons-file-code-24:][_keys]{: .source-link }

# Keys

## Overview

Keys is an extension to make entering and styling keyboard key presses easier. Syntactically, Keys is built around the
`+` symbol.  A key or combination of key presses is surrounded by `++` with each key press separated with a single `+`.

!!! example "Keys Example"

    === "Output"
        ++ctrl+alt+delete++.

    === "Markdown"
        ```
        ++ctrl+alt+delete++
        ```

The Keys extension can be included in Python Markdown by using the following:

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.keys'])
```

!!! tip "Special Characters Before/After Key"
    You might have noticed that in this page many keys show special Unicode symbols before (and sometimes after) a key's
    text. The Keys extension only provides ASCII labels out of the box. Any special Unicode characters that are seen in
    this document are provided by using additional CSS.

    If desired, you can provide your own symbols by doing one of the following:

    1. You can use CSS styling.  The elements are created with classes that are derived from the main key code name (not
      the aliases) so that you can target them to provide special styling. Check out [Formatting](#formatting) for more
      info.

    2. You can also override the label that is output for the key by provided your own text via the `key_map`
      parameter. This would require no additional CSS. More info is provided [here](#extendingmodifying-key-map-index).

## Formatting

By default, Keys outputs keys in the form:

```html
<span class="keys">
  <kbd class="key-ctrl">Ctrl</kbd>
  <span>+</span>
  <kbd class="key-alt">Alt</kbd>
  <span>+</span>
  <kbd class="key-delete">Delete</kbd>
</span>
```

Separator `span`s will be omitted if a separator is not provided via the [options](#options).

Notice the wrapper `span` has the class `keys` applied to it.  This is so you can target it or the elements under it
with CSS. Each recognized key has its own special key class assigned to it in the form `key-<key name>`. These
individual key classes are great if you want to show a special modifier key symbol before the key text (which is done in
this documentation).

The wrapper `keys` class can be customized with options, and the individual key classes are generated from the
[key-map index](#key-map-index).

separator `span`s will be omitted if a separator is not provided via the [options](#options))


## Custom Keys

If you would like to generate a key which isn't in the key index, you can extend the key map via a special
[option](#extendingmodifying-key-map-index).  But if you don't need a key with a special class generated, or you need a
way to quickly enter a one time, arbitrary  key, you can just insert it directly, instead of specifying the key's name,
by quoting the content displayed instead of a key name. You can also enter HTML entities if desired.

!!! example "Quoted Example"

    === "Output"
        ++ctrl+alt+"My Special Key"++

        ++cmd+alt+"&Uuml;"++

    === "Markdown"
        ```
        ++ctrl+alt+"My Special Key"++

        ++cmd+alt+"&Uuml;"++
        ```

## Strict `KBD` Output

According to HTML5 spec on [`kbd`](https://dev.w3.org/html5/spec-preview/the-kbd-element.html), a literal key input, is
represented by a `kbd` wrapped in another `kbd`:

```html
<kbd class="keys">
  <kbd class="key-ctrl">Ctrl</kbd>
  <span>+</span>
  <kbd class="key-alt">Alt</kbd>
  <span>+</span>
  <kbd class="key-delete">Delete</kbd>
</kbd>
```

This is not how many people traditionally use `kbd`s for key inputs, but if you are a stickler for rules, you can enable
the `strict` option to use a more "proper" format.

## Key-Map Index

By default, Keys provides a key-map index for English US keyboards. The key-map index is a dictionary that provides all
the supported key names along with their corresponding display text. There is also a separate alias dictionary which
maps some aliases to entries in the key-map index.

## Extending/Modifying Key-Map Index

If you want to add additional keys, or override text of existing keys, you can feed in your keys via the `key_map`
option. The `key_map` parameter takes a simple dictionary with *key names* that are represented by lowercase
alphanumeric characters and hyphens (`-`). The values of the dictionary represent the the text that is displayed for the
key in the HTML output.

So if you wanted to add a custom key, you could do this: `#!py3 {"custom": "Custom Key"}`.  If you wanted to override
the output of the `option` key and change it from `Option` to `Opt`, you could do this: `#!py3 {"option": "Opt"}`.

### Alphanumeric and Space Keys

Name    | Display   | Aliases
------- | --------- | -------
`0`     | ++0++     |
`1`     | ++1++     |
`2`     | ++2++     |
`3`     | ++3++     |
`4`     | ++4++     |
`5`     | ++5++     |
`6`     | ++6++     |
`7`     | ++7++     |
`8`     | ++8++     |
`9`     | ++9++     |
`a`     | ++a++     |
`b`     | ++b++     |
`c`     | ++c++     |
`d`     | ++d++     |
`e`     | ++e++     |
`f`     | ++f++     |
`g`     | ++g++     |
`h`     | ++h++     |
`i`     | ++i++     |
`j`     | ++j++     |
`k`     | ++k++     |
`l`     | ++l++     |
`m`     | ++m++     |
`n`     | ++n++     |
`o`     | ++o++     |
`p`     | ++p++     |
`q`     | ++q++     |
`r`     | ++r++     |
`s`     | ++s++     |
`t`     | ++t++     |
`u`     | ++u++     |
`v`     | ++v++     |
`w`     | ++w++     |
`x`     | ++x++     |
`y`     | ++y++     |
`z`     | ++z++     |
`space` | ++space++ | `spc`

### Punctuation Keys

Name            | Display           | Aliases
--------------- | ----------------- | -------
`backslash`     | ++backslash++     |
`bar`           | ++bar++           | `pipe`
`brace-left`    | ++brace-left++    | `open-brace`
`brace-right`   | ++brace-right++   | `close-bracket`
`bracket-left`  | ++bracket-left++  | `open-bracket`
`bracket-right` | ++bracket-right++ | `close-bracket`
`colon`         | ++colon++         |
`comma`         | ++comma++         |
`double-quote`  | ++double-quote++  | `dblquote`
`equal`         | ++equal++         |
`exclam`        | ++exclam++        | `exclamation`
`grave`         | ++grave++         | `grave-accent`
`greater`       | ++greater++       | `greater-than`, `gt`
`less`          | ++less++          | `less-than`, `lt`
`minus`         | ++minus++         | `hyphen`
`period`        | ++period++        |
`plus`          | ++plus++          |
`question`      | ++question++      | `question-mark`
`semicolon`     | ++semicolon++     |
`single-quote`  | ++single-quote++  |
`slash`         | ++slash++         |
`tilde`         | ++tilde++         |
`underscore`    | ++underscore++    |

### Navigation Keys

Name          | Display         | Aliases
------------- | --------------- | -------
`arrow-up`    | ++arrow-up++    | `up`
`arrow-down`  | ++arrow-down++  | `down`
`arrow-left`  | ++arrow-left++  | `left`
`arrow-right` | ++arrow-right++ | `right`
`page-up`     | ++page-up++     | `prior`, `page-up`, `pg-up`
`page-down`   | ++page-down++   | `next`, `page-dn`, `pg-dn`
`home`        | ++home++        |
`end`         | ++end++         |
`tab`         | ++tab++         | `tabulator`

### Editing Keys

Name        | Display       | Aliases
----------- | ------------- | -------
`backspace` | ++backspace++ | `back`, `bksp`
`delete`    | ++delete++    | `del`
`insert`    | ++insert++    | `ins`

### Action Keys
Name           | Display          | Aliases
-------------- | -----------------| -------
`break`        | ++break++        | `cancel`
`caps-lock`    | ++caps-lock++    | `capital`, `cplk`
`clear`        | ++clear++        | `clr`
`eject`        | ++eject++        |
`enter`        | ++enter++        | `return`
`escape`       | ++escape++       | `esc`
`help`         | ++help++         |
`print-screen` | ++print-screen++ | `prtsc`
`scroll-lock`  | ++scroll-lock++  | `scroll`

### Numeric Keypad Keys

Name            | Display           | Aliases
--------------- | ----------------- | -------
`num0`          | ++num0++          |
`num1`          | ++num1++          |
`num2`          | ++num2++          |
`num3`          | ++num3++          |
`num4`          | ++num4++          |
`num5`          | ++num5++          |
`num6`          | ++num6++          |
`num7`          | ++num7++          |
`num8`          | ++num8++          |
`num9`          | ++num9++          |
`num-asterisk`  | ++num-asterisk++  | `multiply`
`num-clear`     | ++num-clear++     |
`num-delete`    | ++num-delete++    | `num-del`
`num-equal`     | ++num-equal++     |
`num-lock`      | ++num-lock++      | `numlk`, `numlock`
`num-minus`     | ++num-minus++     | `subtract`
`num-plus`      | ++num-plus++      | `add`
`num-separator` | ++num-separator++ | `decimal`, `separator`
`num-slash`     | ++num-slash++     | `divide`
`num-enter`     | ++num-enter++     |

### Modifier keys

Name            | Display           | Aliases
--------------- | ----------------- | -------
`alt`           | ++alt++           |
`left-alt`      | ++left-alt++      | `lalt`
`right-alt`     | ++right-alt++     | `ralt`
`alt-graph`     | ++alt-graph++     | `altgr`
`command`       | ++command++       | `cmd`
`left-command`  | ++left-command++  | `lcommand`, `lcmd`, `left-cmd`
`right-command` | ++right-command++ | `rcommand`, `rcmd`, `right-cmd`
`control`       | ++control++       | `ctrl`
`left-control`  | ++left-control++  | `lcontrol`, `lctrl`, `left-ctrl`
`right-control` | ++right-control++ | `rcontrol`, `rctrl`, `right-ctrl`
`function`      | ++function++      | `fn`
`meta`          | ++meta++          |
`left-meta`     | ++left-meta++     | `lmeta`
`right-meta`    | ++right-meta++    | `rmeta`
`option`        | ++option++        | `opt`
`left-option`   | ++left-option++   | `loption`, `lopt`, `left-opt`
`right-option`  | ++right-option++  | `roption`, `ropt`, `right-opt`
`shift`         | ++shift++         |
`left-shift`    | ++left-shift++    | `lshift`
`right-shift`   | ++right-shift++   | `rshift`
`super`         | ++super++         |
`left-super`    | ++left-super++    | `lsuper`
`right-super`   | ++right-super++   | `rsuper`
`windows`       | ++windows++       | `win`
`left-windows`  | ++left-windows++  | `lwindows`, `left-win`, `lwin`
`right-windows` | ++right-windows++ | `rwindows`, `right-win`, `rwin`

### Function keys

Name  | Display | Aliases
----- | ------- | -------
`f1`  | ++f1++  |
`f2`  | ++f2++  |
`f3`  | ++f3++  |
`f4`  | ++f4++  |
`f5`  | ++f5++  |
`f6`  | ++f6++  |
`f7`  | ++f7++  |
`f8`  | ++f8++  |
`f9`  | ++f9++  |
`f10` | ++f10++ |
`f11` | ++f11++ |
`f12` | ++f12++ |
`f13` | ++f13++ |
`f14` | ++f14++ |
`f15` | ++f15++ |
`f16` | ++f16++ |
`f17` | ++f17++ |
`f18` | ++f18++ |
`f19` | ++f19++ |
`f20` | ++f20++ |
`f21` | ++f21++ |
`f22` | ++f22++ |
`f23` | ++f23++ |
`f24` | ++f24++ |

### Extra Keys

Name                | Display               | Aliases
------------------- | --------------------- | -------
`backtab`           | ++backtab++           | `bktab`
`browser-back`      | ++browser-back++      |
`browser-favorites` | ++browser-favorites++ | `favorites`
`browser-forward`   | ++browser-forward++   | `forward`
`browser-home`      | ++browser-home++      |
`browser-refresh`   | ++browser-refresh++   | `refresh`
`browser-search`    | ++browser-search++    | `search`
`browser-stop`      | ++browser-stop++      |
`copy`              | ++copy++              |
`context-menu`      | ++context-menu++      | `apps`, `menu`
`mail`              | ++mail++              | `launch-mail`
`media`             | ++media++             | `launch-media`
`media-next-track`  | ++media-next-track++  | `next-track`
`media-pause`       | ++media-pause++       | `pause`
`media-play`        | ++media-play++        | `play`
`media-play-pause`  | ++media-play-pause++  | `play-pause`
`media-prev-track`  | ++media-prev-track++  | `prev-track`
`media-stop`        | ++media-stop++        | `stop`
`print`             | ++print++             |
`reset`             | ++reset++             |
`select`            | ++select++            |
`sleep`             | ++sleep++             |
`volume-down`       | ++volume-down++       | `vol-down`
`volume-mute`       | ++volume-mute++       | `mute`
`volume-up`         | ++volume-up++         | `vol-up`
`zoom`              | ++zoom++              |

### Mouse

Name            | Display           | Aliases
--------------- | ----------------- | -------
`left-button`   | ++left-button++   | `lbutton`
`middle-button` | ++middle-button++ | `mbutton`
`right-button`  | ++right-button++  | `rbutton`
`x-button1`     | ++x-button1++     | `xbutton1`
`x-button2`     | ++x-button2++     | `xbutton2`

## Options

Option       | Type   | Default        | Description
------------ | ------ | -------------- | -----------
`separator`  | string | `#!py3 '+'`    | Define a separator.
`strict`     | bool   | `#!py3 False`  | Use strict HTML5 output for keyboard key input.
`class`      | string | `#!py3 'keys'` | Defines a class(es) to apply to the HTML wrapper element.
`camel_case` | bool   | `#!py3 False`  | Allow the use of camel case for key names `PgUp` --> `pg-up`.
`key_map`    | dict   | `#!py3 {}`     | Add additional keys to the key-map index or override output of existing outputs. See [Extending/Modifying Key-Map Index](#extendingmodifying-key-map-index) for more info.

--8<-- "links.txt"
