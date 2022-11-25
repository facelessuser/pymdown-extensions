# Admonition

## Overview

Admonition blocks are an alternative to using Python Markdown's [built-in extension][admonition]. The output is
identical, but they use the new generic block syntax.

## Usage

Admonitions can be specified using the generic block syntax and the name `admonition`. A title can be specified in
the header.

```
/// admonition | Some title
---
type: note
---

Some content
///
```

Out of the box, Admonitions registers a number of shortcuts for common admonition types: note, attention, caution,
danger, error, tip, hint, warning.

These require you to use their special. When using these, `type` does not need to be set and is not accepted.

```
/// note | Some title

Some content
///
```

These default types can actually be overridden or extended by using the global `types` option. Keep in mind that names
cannot conflict with other registered Block plugin names you are using.

```py3
import markdown
from pymdownx.blocks.admonitions import Admonition

md = markdown.Markdown(
    extensions=['pymdownx.blocks'],
    extension_configs={
        'pymdownx.blocks': {
            'blocks': [Admonition],
            'block_configs': {
                "admonition": {
                    'types': ['note', 'warning', 'some-custom-type']
                }
            }
        }
    }
)
```

And then you can use your defined types:

```
/// some-custom-type | Some title

Some content
///
```

As with all block plugins, you can always add new classes IDs or other attributes via the `attributes` option.

```
/// note | Some title
---
attributes:
  class: class-a class-b
---

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
`attributes` | dictionary | A dictionary containing keys (attributes) and values (attribute values).
