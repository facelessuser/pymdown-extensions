---
icon: lucide/chevrons-up-down
---
[:octicons-file-code-24:][_details_block]{: .source-link }
# Details

/// danger | Using `pymdownx.blocks.details` with `pymdownx.details`
The new `pymdownx.blocks.details` extension is meant to replace `pymdownx.details`, they are not meant to be used
together. Their output is identical making it easy to transition by simply swapping out the syntax, but using them both
together can cause issues as they both generate the same output and confuse each other.

If you are switching from `pymdownx.details` to `pymdownx.blocks.details`, ensure you disable `pymdownx.details` to
avoid issues.
///

## Overview

Details blocks are an alternative to using [`pymdownx.details`](../../details.md) and, in fact, aim to potentially replace
them in the future. The output is identical `pymdownx.details`, but they use the new generic block syntax.

By default, the meta-plugin is registered when `pymdownx.blocks` is registered, but if you were customizing which
meta-plugins get loaded, you can do so by doing the following:

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.blocks.details'])
```

## Usage

Admonitions can be specified using the generic block syntax and the name `details`. A summary can be specified in
the header. Additionally, you can apply a specific class like with admonitions if desired.

```text title="Details"
/// details | Some summary
Some content
///
```

/// html | div.result
//// details | Some summary
Some content
////
///

Like with [Admonitions](./admonition.md), you can specify a special class to define the type via the `type` option. If
`type` is set, a class with that name will be added, and if there is no summary, the type will be used as the summary:
`note` -> `Note`.

```text title="Details"
/// details | Some summary
    type: warning

Some content
///
```

/// html | div.result
//// details | Some summary
    type: warning

Some content
////
///

If you wish to specify a details as open (or not collapsed), simply use the option `open`.

```text title="Details Open"
/// details | Some summary
    open: True

Some content
///
```

/// html | div.result
//// details | Some summary
    open: True

Some content
////
///

Like admonitions, you can specify and register special shortcuts for certain details types, but unlike admonitions,
details does not register any default types by default.

```py3
import markdown
from pymdownx.blocks.details import Details

md = markdown.Markdown(
    extensions=['pymdownx.blocks.details'],
    extension_configs={
        'pymdownx.blocks.details": {
            'types': ['details-note', 'details-warning', 'some-custom-type']
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

If further control is desired, you can optionally configure a custom block with a name that differs from the actual
attached class. You can also configure a default title that is not derived from the attached class.

```py3
import markdown
from pymdownx.blocks.details import Details

md = markdown.Markdown(
    extensions=['pymdownx.blocks.details'],
    extension_configs={
        'pymdownx.blocks.details": {
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
/// details | My Default Title
    type: custom

content
///
```

As with all block plugins, you can always add new classes IDs or other attributes via the `attributes` option.

```
/// details | Some title
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
`open`       | bool       | A boolean that determines if the details block is open or closed.
`type`       | string     | A class name to apply as the admonition type.
`attrs`      | dictionary | A dictionary that defines attributes for the outer, wrapper element.
