# HardBreak {: .doctitle}
Visible hard line breaks.

---

## Overview
The Markdown specs states that if a line ends with two or more spaces a `#!html <br>` tag will be inserted.  But sadly, it is not easy to see two spaces at the end of a line.  While this makes the document easy to read, it makes it hard to tell when an explicit new line has been inserted.  HardBreak solves this by creating `#!html <br>` tags when the newline is escaped.

This idea is not new and is used by [Pandoc](http://pandoc.org/README.html#backslash-escapes) and [CommonMark](http://spec.commonmark.org/0.22/#hard-line-breaks). Unfortunately I am not very fond of the situation where you purposefully have a backslash at the end of a line: like when listing a Windows file path.  You can escape the backslash in thes situations, but it is just another thing you have to be thinking about.  To avoid the need to escape backslashes at the end of a line and to allow for a cleaner look, HardBreak requires at least one or more leading spaces.  If you prefer Pandoc and CommonMark's styling, you can disable the requirement for leading spaces.

Hardbreak should work along side the default two space syntax as well, so no need to change existing Markdown files.

Escaped newlines will not be counted if it is the last line in a paragraph, inside a code block, or in a header tag; this is no different that the two space syntax.  HardBreak should also not be used in conjunction with Python Markdown's `nl2br` extension. Though there is no real harm in doing this, it does not make sense to pair these together.

## Options

| Option    | Type | Default | Description |
|-----------|------|---------|-------------|
| leading_space | bool | True | Require one or more leading spaces before the escaped newline. |

## Examples
Example is shown requiring leading spaces.

```
Joh Doe       \
123 Some St   \
City, ST, Zip

`Code blocks \
don't count.`

**Other inline spans \
will work.**

###### Headers are Unaffected \
Last line in paragraph is also unaffected. \

c:\Some\path\
and c:\Some\other\path\

An escaped slash: \\
No forced new line.
```

Joh Doe       \
123 Some St   \
City, ST, Zip

`Code blocks \
don't count.`

**Other inline spans \
will work.**

###### Headers are Unaffected \
Last line in paragraph is also unaffected. \

c:\Some\path\
and c:\Some\other\path\

An escaped slash: \\
No forced new line.
