# HardBreak {: .doctitle}
Visible hard line breaks.

---

## Overview
The Markdown specs states that if a line ends with two or more spaces a `#!html <br>` tag will be inserted.  But sadly, it is not easy to see two spaces at the end of a sentence.  While this makes the document easy to read, it makes it hard to tell when an explicit new line has been inserted.  HardBreak solves this by creating `#!html <br>` tags by escaping the newline. To avoid the need to escape backslashes at the end of a line, HardBreak requires at least one or more leading spaces.  Some other Markdown parsers that implement a similar syntax do not require leading spaces: Pandoc and CommonMark.  If you would like a style more like Pandoc or CommonMark, you can disable the requirement for leading spaces.

Hardbreak will work along side the default two space syntax as well. Escaped newlines will not be counted if it is the last line in a paragraph, inside a code block, or in a header tag; this is no different that the two space syntax.

HardBreak should also not be used in conjunction with Python Markdown's `nl2br` extension. Though there is no real harm in doing this, it does not make sense to pair these together.

## Options

| Option    | Type | Default | Description |
|-----------|------|---------|-------------|
| leading_space | bool | True | Require 1 or more leading spaces before the escaped newline. |

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

Column1 | Column2
------- | -------
Tables  | don't count \
Tables  | don't count
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
