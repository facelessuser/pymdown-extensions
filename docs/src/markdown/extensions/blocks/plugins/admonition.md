---
icon: lucide/sticky-note
---

[:octicons-file-code-24:][_admonition_block]{: .source-link }

# Admonition

/// danger | Using `pymdownx.blocks.admonition` with `admonition`
The new `pymdownx.blocks.admonition` extension is meant to replace `admonition`, they are not meant to be used together.
Their output is identical making it easy to transition by simply swapping out the syntax, but using them both together
can cause issues as they both generate the same output and confuse each other.

If you are switching from `admonition` to `pymdownx.blocks.admonition`, ensure you disable `admonition` to avoid issues.
///

## Overview

Admonition blocks are an alternative to using Python Markdown's [built-in extension][admonition]. The output is
identical, but they use the new generic block syntax.

By default, the meta-plugin is registered when `pymdownx.blocks` is registered, but if you were customizing which
meta-plugins get loaded, you can do so by doing the following:

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.blocks.admonition'])
```

## Usage

Admonitions can be specified using the generic block syntax and the name `admonition`. A title can be specified in
the header.

```text title="Admonition"
/// admonition | Some title
Some content
///
```

/// html | div.result
//// admonition | Some title
Some content
////
///

If desired, you can attach a class to an admonition using the option `type`. If type is set, a class with that name will
be added, and if there is no title, the class name will be used as the title: `note` -> `Note`.

```text title="Admonition"
/// admonition | Some title
    type: warning

Some content
///
```

/// html | div.result
//// admonition | Some title
    type: warning

Some content
////
///


As a shortcut, Admonitions registers a number of admonition blocks that attach common classes: note, attention, caution,
danger, error, tip, hint, warning.

These require you to use their special name. When using these, you do not need to attach class `note`, `attention`, etc.
as they are already done for you.

```text title="Note"
/// note | Some title
Some content
///
```

/// html | div.result
//// note | Some title
Some content
////
///

These default types can actually be overridden or extended by using the global `types` option. Keep in mind that names
cannot conflict with other registered Block plugin names you are using.

```py3
import markdown
from pymdownx.blocks.admonition import Admonition

md = markdown.Markdown(
    extensions=['pymdownx.blocks.admonition'],
    extension_configs={
        'pymdownx.blocks.admonition': {
            'types': ['note', 'warning', 'some-custom-type']
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

If further control is desired, you can optionally configure a custom block with a name that differs from the actual
attached class. You can also configure a default title that is not derived from the attached class.

```py3
import markdown
from pymdownx.blocks.admonition import Admonition

md = markdown.Markdown(
    extensions=['pymdownx.blocks.admonition'],
    extension_configs={
        'pymdownx.blocks.admonition": {
            'types': [{'name': 'some-custom-type', 'class': 'custom', 'title': 'My Default title'}]
        }
    }
)
```

Now when using:

```
/// some-custom-type
content
///
```

It would be the same as using:

```
/// admonition | My Default Title
    type: custom

content
///
```

As with all block plugins, you can always add new classes IDs or other attributes via the `attributes` option.

```
/// note | Some title
    attrs: {class: class-name: id: id-name}

Some content
///
```

/// new | New 10.5
Specifying custom blocks with specific classes and default titles is new in 10.5.
///

## Global Options

Options | Type       | Descriptions
------- | ---------- | ------------
`types` | \[string\] | Specify new plugin subclasses to register for specific admonition types.

## Per Block Options

Options      | Type       | Descriptions
------------ | ---------- | ------------
`type`       | string     | A class name to apply as the admonition type.
`attrs`      | dictionary | A dictionary that defines attributes for the outer, wrapper element.
