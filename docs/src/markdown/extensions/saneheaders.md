[:octicons-file-code-24:][_saneheaders]{: .source-link }

# SaneHeaders

## Overview

SaneHeaders is an extension that alters the default hashed headers extension to require headers to have spaces after the
hashes (`#`) in order to be recognized as headers. This allows for other extension syntaxes to use `#` in their syntaxes
as long as no spaces follow the `#` at the beginning of a line. For instance,
[MagicLink's issue syntax](./magiclink.md#issues-and-pull-requests) issue syntax uses hashes followed by numbers
(`#998`) to represent issue links. There may extensions that use names after hashes to provide tags (`#tag`). With
SaneHeaders, these syntaxes can coexist. Those familiar with CommonMark may recognize this behavior.

## Syntax

The syntax when using SaneHeaders is exactly like Python Markdown's default logic with the only exception being that
SaneHeaders will not treat hashes at the beginning of a line as a header if they do not have space after them.

In Python Markdown, both of these are treated as headers:

```
## Header

##Also a Header
```

With SaneHeaders, only the first is a header:

```
## Header

##Not a Header
```

--8<-- "links.txt"
