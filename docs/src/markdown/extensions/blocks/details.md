[:octicons-file-code-24:][_details_block]{: .source-link }
# Details

!!! warning "Alpha Release"
    Blocks is currently only available in the Pymdown Extensions alpha release. It is a work in progress and API and
    syntax are subject to change.

    Please provide feedback here: https://github.com/facelessuser/pymdown-extensions/discussions/1940.

## Overview

Details blocks are an alternative to using [`pymdownx.details`](../details.md) and, in fact, aim to potentially replace
them in the future. The output is identical `pymdownx.details`, but they use the new generic block syntax.

By default, the meta-plugin is registered when `pymdownx.blocks` is registered, but if you were customizing which
meta-plugins get loaded, you can do so by doing the following:

```py3
import markdown
from pymdownx.blocks.details import Details
md = markdown.Markdown(
    extensions=['pymdownx.blocks']
    extension_configs={
        'pymdownx.blocks': {
            'blocks': [Details]
            # Use block_configs to set block specific global settings
        }
    }
)
```

## Usage

Admonitions can be specified using the generic block syntax and the name `details`. A summary can be specified in
the header. Additionally, you can apply a specific type if like with admonitions if desired.

``` title="Example: Details"
/// details | Some summary
    type: note

Some content
///
```

<div class="result" markdown>

```md-render
---
extensions:
- pymdownx.blocks
---
/// details | Some summary
    type: note

Some content
///
```

</div>

If you wish to specify a details as open (or not collapsed), simply use the option `open`.

``` title="Example: Details Open"
/// details | Some summary
    open: True

Some content
///
```

<div class="result" markdown>

```md-render
---
extensions:
- pymdownx.blocks
---
/// details | Some summary
    open: True

Some content
///
```

</div>

Like admonitions, you can specify and register special shortcuts for certain details types, but unlike admonitions,
details does not register any default types by default.

```py3
import markdown
from pymdownx.blocks.details import Details

md = markdown.Markdown(
    extensions=['pymdownx.blocks'],
    extension_configs={
        'pymdownx.blocks': {
            'blocks': [Details],
            'block_configs': {
                "details": {
                    'types': ['details-note', 'details-warning', 'some-custom-type']
                }
            }
        }
    }
)
```

And then you can use your defined types:

```
/// some-custom-type | Some summary
Some content
///
```

As with all block plugins, you can always add new classes IDs or other attributes via the `attributes` option.

```
/// details | Some title
    attributes:
      class: class-a class-b

Some content
///
```

## Global Options

Options | Type       | Descriptions
------- | ---------- | ------------
`types` | \[string\] | Specify new plugin subclasses to register for specific admonition types.

## Per Block Options

Options      | Type       | Descriptions
------------ | ---------- | ------------
`type`       | string     | String containing a class name to attach as a type.
`open`       | bool       | A boolean that determines if the details block is open or closed.
`attributes` | dictionary | A dictionary containing keys (attributes) and values (attribute values).
