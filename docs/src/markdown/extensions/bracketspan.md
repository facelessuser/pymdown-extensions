---
icon: lucide/brackets
---
[:octicons-file-code-24:][_bracketspan]{: .source-link }

# BracketSpan

> [!new]
> BracketSpan is new in 12.0

## Overview

BracketSpan is an extension that allows for the creation of arbitrary spans that can be decorated with the
[`attr_list`][attr-list] list extension. To use `attr_list` must also be enabled.

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.bracketspan', 'attr_list'])
```

Spans can be created by enclosing content within a square bracket and applying some attributes using `attr_list` syntax.
It can be noted that if you place an empty `{}`, a span with no special attributes will be created.

```text title="Whitespace"
[span]{style="color: magenta"}
```

/// html | div.result
[span]{style="color: magenta"}
///

BracketSpan should be compatible with other bracket syntaxes, such as links, images, etc. For instance, if the bracket
object represents a reference link, the reference processor will handle it before BracketSpan, and `attr_list` will
apply attributes as it normally would.

```text title="Whitespace"
[Pymdown Extensions]{style="color: magenta"}

[Pymdown Extensions]: https://github.com/facelessuser/pymdown-extensions 
```

/// html | div.result
[Pymdown Extensions]{style="color: magenta"}

[Pymdown Extensions]: https://github.com/facelessuser/pymdown-extensions 
///

## Options

There are currently no options.
