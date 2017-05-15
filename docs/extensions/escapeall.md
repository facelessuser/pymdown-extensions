# EscapeAll

## Overview

If you ever have to stop and try to remember, *Can I escape this char?* or *Will backslash escape this?*, you are not alone.  EscapeAll makes `\` escape everything making such questions moot.  Now instead of questioning or looking up what can be escaped, you can expect that `\` will escape the character following it.  So if you need a literal `\`, just escape it: `\\`.  Keep in mind this will not escape things in inline, block, or fenced code.

There are two special escapes among all of these, and it is the escape of the "space" character and the "newline" character. If `nbsp` is enabled, an escaped space will be converted into a non-breaking space: `#!html &nbsp;`. If `hardbreak` is enabled, an escaped newline will be converted to a hard break `#!html <br>`. The advantage of `hardbreak` is that you can visually see the hard break opposed to Markdown's default method of two spaces at the end of a line.

So in short, EscapeAll escapes all inline characters.

> So all ASCII characters?

It escapes everything.

> What about Unicode?

It escapes everything!

> What about...

EVERYTHING! IT ESCAPES EVERYTHING!

## Options

Option      | Type | Default | Description
----------- | ---- | ------- | ----------
`hardbreak` | bool | False   | Escaped newlines will be hard breaks: `#!html <br>`.
`nbsp`      | bool | False   | Escaped spaces will be non-breaking spaces: `#!html &nbsp;`.


## Examples

```
\W\e\ \c\a\n\ \e\s\c\a\p\e
\e\v\e\r\y\t\h\i\n\g\!\ \
\❤\😄
```

\W\e\ \c\a\n\ \e\s\c\a\p\e
\e\v\e\r\y\t\h\i\n\g\!\ \
\❤\😄
