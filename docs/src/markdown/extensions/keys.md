# Keys

## Overview

Keys is an extension to make entering and styling keyboard key presses easier. Syntactically, Keys is built around the `+` symbol.  A key or combination of key presses is surrounded by `++` with each key press separated with a single `+`.  For instance, if we wanted to represent `Ctrl + Alt + Delete`, we could just format our keys like this: `++ctrl+alt+delete++` --> ++ctrl+alt+delete++.

## Formatting

By default, Keys outputs keys in the form (separator `span`s will be omitted if a separator is not provided via the [options](#options)):

```html
<span class="keys">
  <kbd class="key-ctrl">Ctrl</kbd>
  <span>+</span>
  <kbd class="key-alt">Alt</kbd>
  <span>+</span>
  <kbd class="key-delete">Delete</kbd>
</span>
```

Notice the wrapper `span` has the class `keys` applied to it.  This is so you can target it or the elements under it with CSS. Each recognized key press has its own special key class assigned to it in the form `key-<key name>`. These individual key classes are great if you want to show special modifier key symbols before the key text (which is done in this documentation). The wrapper `keys` class can be customized with options, and the individual key classes are generated from the [key-map index](#key-map-index).

If you would like to generate a key which isn't in the key index, you can extend the key map via a special [option](#extendingmodifying-key-map-index).  But if you don't need a key with a special class generated, or you need a way to quickly enter a one time special key, you can just insert it directly by quoting the text you want displayed instead of a key name: `++ctrl+alt+"My Special Key"++` --> ++ctrl+alt+"My Special Key"++. You can also enter HTML entities: `++ctrl+alt+"&Uuml;"++` --> ++ctrl+alt+"&Uuml;"++ if desired.

## Strict `KBD` Output

According to HTML5 spec on [`kbd`](https://dev.w3.org/html5/spec-preview/the-kbd-element.html), a literal key input, is represented by a `kbd` wrapped the other `kbd`s:

```html
<kbd class="keys">
  <kbd class="key-ctrl">Ctrl</kbd>
  <span>+</span>
  <kbd class="key-alt">Alt</kbd>
  <span>+</span>
  <kbd class="key-delete">Delete</kbd>
</kbd>
```

This is not how many people traditionally use `kbd`s for key inputs, but if you are a stickler for rules, you can enable the `strict` option to use a more "proper" format.

## Key-Map Index

By default, Keys provides a key-map index for English US keyboards. The key-map index is a dictionary that provides all supported key names (which are used as the class in output class `key-<name>`) with their corresponding display text.  There is also a separate alias dictionary which maps some aliases to entries in the key-map index.

### Alphanumeric and Space Keys

Name    | Display     | Aliases
------- | ----------- | -------
`0`     | ++"0"++     |
`1`     | ++"1"++     |
`2`     | ++"2"++     |
`3`     | ++"3"++     |
`4`     | ++"4"++     |
`5`     | ++"5"++     |
`6`     | ++"6"++     |
`7`     | ++"7"++     |
`8`     | ++"8"++     |
`9`     | ++"9"++     |
`a`     | ++"A"++     |
`b`     | ++"B"++     |
`c`     | ++"C"++     |
`d`     | ++"D"++     |
`e`     | ++"E"++     |
`f`     | ++"F"++     |
`g`     | ++"G"++     |
`h`     | ++"H"++     |
`i`     | ++"I"++     |
`j`     | ++"J"++     |
`k`     | ++"K"++     |
`l`     | ++"L"++     |
`m`     | ++"M"++     |
`n`     | ++"N"++     |
`o`     | ++"O"++     |
`p`     | ++"P"++     |
`q`     | ++"Q"++     |
`r`     | ++"R"++     |
`s`     | ++"S"++     |
`t`     | ++"T"++     |
`u`     | ++"U"++     |
`v`     | ++"V"++     |
`w`     | ++"W"++     |
`x`     | ++"X"++     |
`y`     | ++"Y"++     |
`z`     | ++"Z"++     |
`space` | ++"Space"++ | `spc`

### Punctuation Keys

Name            | Display  | Aliases
--------------- | -------- | -------
`backslash`     | ++"\\"++ |
`bar`           | ++"\|"++ | `pipe`
`brace-left`    | ++"{"++  | `open-brace`
`brace-right`   | ++"}"++  | `close-bracket`
`bracket-left`  | ++"["++  | `open-bracket`
`bracket-right` | ++"]"++  | `close-brace`
`colon`         | ++":"++  |
`comma`         | ++","++  |
`double-quote`  | ++"\""++ | `dblquote`
`equal`         | ++"="++  |
`exclam`        | ++"!"++  | `exclamation`
`grave`         | ++"\`"++ | `grave-accent`
`greater`       | ++">"++  | `greater-than`, `gt`
`less`          | ++"<"++  | `less-than`, `lt`
`minus`         | ++"-"++  | `hyphen`
`period`        | ++"."++  |
`plus`          | ++"\+"++ |
`question`      | ++"?"++  | `question-mark`
`semicolon`     | ++";"++  |
`single-quote`  | ++"'"++  |
`slash`         | ++"/"++  |
`tilde`         | ++"~"++  |
`underscore`    | ++"_"++  |

### Navigation Keys

Name          | Display         | Aliases
------------- | --------------- | -------
`arrow-up`    | ++"Up"++        | `up`
`arrow-down`  | ++"Down"++      | `down`
`arrow-left`  | ++"Left"++      | `left`
`arrow-right` | ++"Right"++     | `right`
`page-up`     | ++"Page Up"++   | `prior`, `page-up`, `pg-up`
`page-down`   | ++"Page Down"++ | `next`, `page-dn`, `pg-dn`
`home`        | ++"Home"++      |
`end`         | ++"End"++       |
`tab`         | ++"Tab"++       | `tabulator`

### Editing Keys

Name        | Display         | Aliases
----------- | --------------- | -------
`backspace` | ++"Backspace"++ | `back`, `bksp`
`delete`    | ++"Del"++       | `del`
`insert`    | ++"Ins"++       | `ins`

### Action Keys
Name           | Display            | Aliases
-------------- | ------------------ | -------
`break`        | ++"Break"++        | `cancel`
`caps-lock`    | ++"Caps Lock"++    | `capital`, `cplk`
`clear`        | ++"Clear"++        | `clr`
`eject`        | ++"Eject"++        |
`enter`        | ++"Enter"++        | `return`
`escape`       | ++"Esc"++          | `esc`
`help`         | ++"Help"++         |
`print-screen` | ++"Print Screen"++ | `prtsc`
`scroll-lock`  | ++"Scroll Lock"++  | `scroll`

### Numeric Keypad Keys

Name            | Display         | Aliases
--------------- | --------------- | -------
`num0`          | ++"Num 0"++     |
`num1`          | ++"Num 1"++     |
`num2`          | ++"Num 2"++     |
`num3`          | ++"Num 3"++     |
`num4`          | ++"Num 4"++     |
`num5`          | ++"Num 5"++     |
`num6`          | ++"Num 6"++     |
`num7`          | ++"Num 7"++     |
`num8`          | ++"Num 8"++     |
`num9`          | ++"Num 9"++     |
`num-asterisk`  | ++"Num *"++     | `multiply`
`num-clear`     | ++"Num Clear"++ |
`num-delete`    | ++"Num Del"++   | `num-del`
`num-equal`     | ++"Num ="++     |
`num-lock`      | ++"Num Lock"++  | `numlk`, `numlock`
`num-minus`     | ++"Num -"++     | `subtract`
`num-plus`      | ++"Num \+"++    | `add`
`num-separator` | ++"Num ."++     | `decimal`, `separator`
`num-slash`     | ++"Num /"++     | `divide`
`num-enter`     | ++"Num Enter"++ |

### Modifier keys

Name            | Display           | Aliases
--------------- | ----------------- | -------
`alt`           | ++"Alt"++         | `menu`
`command`       | ++"Cmd"++         | `cmd`
`control`       | ++"Ctrl"++        | `ctrl`
`function`      | ++"Fn"++          | `fn`
`left-alt`      | ++"Left Alt"++    | `lalt`, `left-menu`, `lmenu`
`left-control`  | ++"Left Ctrl"++   | `lcontrol`, `lctrl`, `left-ctrl`
`left-shift`    | ++"Left Shift"++  | `lshift`
`left-windows`  | ++"Left Win"++    | `left-win`, `lwin`
`meta`          | ++"Meta"++        |
`option`        | ++"Option"++      | `opt`
`right-alt`     | ++"Right Alt"++   | `ralt`, `right-menu`, `rmenu`
`right-control` | ++"Right Ctrl"++  | `rcontrol`, `rctrl`, `right-ctrl`
`right-shift`   | ++"Right Shift"++ | `rshift`
`right-windows` | ++"Right Win"++   | `right-win`, `rwin`
`shift`         | ++"Shift"++       |
`windows`       | ++"Win"++         | `win`

### Function keys

Name  | Display   | Aliases
----- | --------- | -------
`f1`  | ++"F1"++  |
`f2`  | ++"F2"++  |
`f3`  | ++"F3"++  |
`f4`  | ++"F4"++  |
`f5`  | ++"F5"++  |
`f6`  | ++"F6"++  |
`f7`  | ++"F7"++  |
`f8`  | ++"F8"++  |
`f9`  | ++"F9"++  |
`f10` | ++"F10"++ |
`f11` | ++"F11"++ |
`f12` | ++"F12"++ |
`f13` | ++"F13"++ |
`f14` | ++"F14"++ |
`f15` | ++"F15"++ |
`f16` | ++"F16"++ |
`f17` | ++"F17"++ |
`f18` | ++"F18"++ |
`f19` | ++"F19"++ |
`f20` | ++"F20"++ |
`f21` | ++"F21"++ |
`f22` | ++"F22"++ |
`f23` | ++"F23"++ |
`f24` | ++"F24"++ |

### Extra Keys

Name                | Display               | Aliases
------------------- | --------------------- | -------
`backtab`           | ++"Back Tab"++        | `bktab`
`browser-back`      | ++"Browser Back"++    |
`browser-favorites` | ++"Browser Favor"++   | `favorites`
`browser-forward`   | ++"Browser Forward"++ | `forward`
`browser-home`      | ++"Browser Home"++    |
`browser-refresh`   | ++"Browser Refresh"++ | `refresh`
`browser-search`    | ++"Browser Search"++  | `search`
`browser-stop`      | ++"Browser Stop"++    |
`copy`              | ++"Copy"++            |
`context-menu`      | ++"Context Menu"++    | `apps`
`mail`              | ++"Mail"++            | `launch-mail`
`media`             | ++"Media"++           | `launch-media`
`media-next-track`  | ++"Next Track"++      | `next-track`
`media-pause`       | ++"Pause"++           | `pause`
`media-play`        | ++"Play"++            | `play`
`media-play-pause`  | ++"Play/Pause"++      | `play-pause`
`media-prev-track`  | ++"Previous Track"++  | `prev-track`
`media-stop`        | ++"Stop"++            | `stop`
`print`             | ++"Print"++           |
`reset`             | ++"Reset"++           |
`select`            | ++"Select"++          |
`sleep`             | ++"Sleep"++           |
`volume-down`       | ++"Volume Down"++     | `vol-down`
`volume-mute`       | ++"Mute"++            | `mute`
`volume-up`         | ++"Volume Up"++       | `vol-up`
`zoom`              | ++"Zoom"++            |

### Mouse

Name            | Display             | Aliases
--------------- | ------------------- | -------
`left-button`   | ++"Left Button"++   | `lbutton`
`middle-button` | ++"Middle Button"++ | `mbutton`
`right-button`  | ++"Right Button"++  | `rbutton`
`x-button1`     | ++"X Button 1"++    | `xbutton1`
`x-button2`     | ++"X Button 2"++    | `xbutton2`

## Extending/Modifying Key-Map Index

If you want to add additional keys, or override text of existing keys, you can feed in your keys via the `key_map` option. The `key_map` parameter takes a simple dictionary with *key names* that are represented by lowercase alphanumeric characters and hyphens (`-`). The values of the dictionary represent the the text that is displayed for the key in the HTML output.

So if you wanted to add a custom key, you could do this: `#!py {"custom": "Custom Key"}`.  If you wanted to override the output of the `option` key and change it from `Option` to `Opt`, you could do this: `#!py {"option": "Opt"}`.

## Options

Option       | Type       | Default       | Description
------------ | ---------- | ------------- | -----------
`separator`  | string     | `#!py '+'`    | Define a separator.
`strict`     | bool       | `#!py False`  | Use strict HTML5 output for keyboard key input.
`class`      | string     | `#!py 'keys'` | Defines a class(es) to apply to the HTML wrapper element.
`camel_case` | bool       | `#!py False`  | Allow the use of camel case for key names `PgUp` --> `pg-up`.
`key_map`    | dictionary | `#!py {}`     | Add additional keys to the key-map index or override output of existing outputs. See [Extending/Modifying Key-Map Index](#extendingmodifying-key-map-index) for more info.

## Examples

```
To copy, press ++ctrl+alt+c++ for Windows or Linux or ++cmd+alt+c++ for Mac.

You can also use custom key labels: ++ctrl+alt+"&Uuml;"++.
```

To copy, press ++ctrl+alt+c++ for Windows or Linux or ++cmd+alt+c++ for Mac.

You can also use custom key labels: ++ctrl+alt+"&Uuml;"++.
