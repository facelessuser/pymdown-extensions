[:octicons-file-code-24:][_escapeall]{: .source-link }

# EscapeAll

## Overview

If you ever have to stop and try to remember, *Can I escape this char?* or *Will a backslash escape this?*, you are not
alone.  EscapeAll makes `\` escape everything making such questions moot.  Now instead of questioning or looking up what
can be escaped, you can expect that `\` will escape the character following it.  So if you need a literal `\`, just
escape it: `\\`.  Keep in mind this will not escape things in code blocks of any kind.

```text title="Escaping"
\W\e\ \c\a\n\ \e\s\c\a\p\e
\e\v\e\r\y\t\h\i\n\g\!\ \
\❤\😄
```

/// html | div.result
\W\e\ \c\a\n\ \e\s\c\a\p\e
\e\v\e\r\y\t\h\i\n\g\!\ \
\❤\😄
///

There are two special escapes among all of these escapes though: escaping "space" characters and escaping "newline"
characters. If `nbsp` is enabled, an escaped space will be converted into a non-breaking space: `#!html &nbsp;`. If
`hardbreak` is enabled, an escaped newline will be converted to a hard break `#!html <br>`. The advantage of `hardbreak`
is that you can visually see the hard break opposed to Markdown's default method of two spaces at the end of a line.

So in short, EscapeAll escapes all inline characters.

/// question | Q & A
**So all ASCII characters?**

_It escapes everything._

**What about Unicode?**

_It escapes everything!_

**What about...**

_EVERYTHING! IT ESCAPES EVERYTHING!_
///

The EscapeAll extension can be included in Python Markdown by using the following:

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.escapeall'])
```

## Options

Option      | Type | Default         | Description
----------- | ---- | --------------- | ----------
`hardbreak` | bool | `#!py3 False`   | Escaped newlines will be hard breaks: `#!html <br>`.
`nbsp`      | bool | `#!py3 False`   | Escaped spaces will be non-breaking spaces: `#!html &nbsp;`.
