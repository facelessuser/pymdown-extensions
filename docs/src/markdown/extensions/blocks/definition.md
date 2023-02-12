[:octicons-file-code-24:][_definition_block]{: .source-link }

# Definition

!!! warning "Alpha Release"
    Blocks is currently only available in the Pymdown Extensions alpha release. It is a work in progress and API and
    syntax are subject to change.

    Please provide feedback here: https://github.com/facelessuser/pymdown-extensions/discussions/1940.

## Overview

The definition blocks are an alternative to using Python Markdown's [built-in extension][def-list]. The output is very
similar, but they use the new generic block syntax.

By default, the meta-plugin is registered when `pymdownx.blocks` is registered, but if you were customizing which
meta-plugins get loaded, you can do so by doing the following:

```py3
import markdown
from pymdownx.blocks.definition import Definition
md = markdown.Markdown(
    extensions=['pymdownx.blocks']
    extension_configs={
        'pymdownx.blocks': {
            'blocks': [Definition]
        }
    }
)
```

## Usage

Definitions can be specified using the generic block syntax and the name `define`. Simply create paragraphs for terms
and use a list to provide one or more definitions.

``` title="Example: Definition"
/// define
Apple

- Pomaceous fruit of plants of the genus Malus in
  the family Rosaceae.

///
```

<div class="result" markdown>

```md-render
---
extensions:
- pymdownx.blocks
---
/// define
Apple

- Pomaceous fruit of plants of the genus Malus in
  the family Rosaceae.

///
```

</div>

Multiple terms and definitions can be define in the same block. The terms will all be under the same definition list.

``` title="Example: Multiple Definitions"
/// define
Apple

- Pomaceous fruit of plants of the genus Malus in
  the family Rosaceae.

Orange

- The fruit of an evergreen tree of the genus Citrus.

///
```

<div class="result" markdown>

```md-render
---
extensions:
- pymdownx.blocks
---
/// define
Apple

- Pomaceous fruit of plants of the genus Malus in
  the family Rosaceae.

Orange

- The fruit of an evergreen tree of the genus Citrus.

///
```

</div>

Also, multiple terms can be associated with the same definition.


```
/// define
Term 1

Term 2

- Definition a

Term 3

- Definition b
///
```

<div class="result" markdown>

```md-render
---
extensions:
- pymdownx.blocks
---
/// define
Term 1

Term 2

- Definition a

Term 3

- Definition b
///
```

</div>

## Global Options

Definitions provide no global options.

## Per Block Options

Options      | Type       | Descriptions
------------ | ---------- | ------------
`attributes` | dictionary | A dictionary containing keys (attributes) and values (attribute values).
