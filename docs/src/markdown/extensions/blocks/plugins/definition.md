[:octicons-file-code-24:][_definition_block]{: .source-link }

# Definition

--8<-- "blocksbeta.md"

## Overview

The definition blocks are an alternative to using Python Markdown's [built-in extension][def-list]. The output is very
similar, but they use the new generic block syntax.

By default, the meta-plugin is registered when `pymdownx.blocks` is registered, but if you were customizing which
meta-plugins get loaded, you can do so by doing the following:

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.blocks.definition'])
```

## Usage

Definitions can be specified using the generic block syntax and the name `define`. Simply create paragraphs for terms
and use a list to provide one or more definitions.

```text title="Definition"
/// define
Apple

- Pomaceous fruit of plants of the genus Malus in
  the family Rosaceae.

///
```

/// html | div.result
//// define
Apple

- Pomaceous fruit of plants of the genus Malus in
  the family Rosaceae.

////
///

Multiple terms and definitions can be define in the same block. The terms will all be under the same definition list.

```text title="Multiple Definitions"
/// define
Apple

- Pomaceous fruit of plants of the genus Malus in
  the family Rosaceae.

Orange

- The fruit of an evergreen tree of the genus Citrus.

///
```

/// html | div.result
//// define
Apple

- Pomaceous fruit of plants of the genus Malus in
  the family Rosaceae.

Orange

- The fruit of an evergreen tree of the genus Citrus.

////
///

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

/// html | div.result
//// define
Term 1

Term 2

- Definition a

Term 3

- Definition b
////
///

As with all block plugins, you can always add new classes IDs or other attributes via the `attributes` option.

```
/// define
    attrs: {class: class-name: id: id-name}

Term 1

- Definition a
///
```

## Global Options

Definitions provide no global options.

## Per Block Options

Options      | Type       | Descriptions
------------ | ---------- | ------------
`attrs`      | string     | A string that defines attributes for the outer, wrapper element.
