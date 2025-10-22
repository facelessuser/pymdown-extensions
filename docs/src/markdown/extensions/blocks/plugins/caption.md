[:octicons-file-code-24:][_admonition_block]{: .source-link }

# Caption

/// New | New in 10.12
///

## Overview

The Caption extension allows for wrapping blocks in `#!html <figure>` tags and inserting a `#!html <figcaption>` tag
with specified content.

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.blocks.caption'])
```

## Usage
### Adding Captions

Caption is easy to use and simply requires the user to place a caption directly after a block that they'd like to wrap
in a figure with a caption. Figures can have any content: images, tables, quotes, anything.

```text title="Adding Caption"
Fruit      | Amount
---------- | ------
Apple      | 20
Peach      | 10
Banana     | 3
Watermelon | 1

/// caption
Fruit Count
///
```

//// html | div.result
Fruit      | Amount
---------- | ------
Apple      | 20
Peach      | 10
Banana     | 3
Watermelon | 1

/// caption
Fruit Count
///
////

### Nesting Captions

Captions can be nested, and if multiple captions are used on a single block, the block will be wrapped in multiple
nested figures.

```text title="Nested Captions"
![placeholder](../../../images/placeholder.jpeg)

/// caption
Inner caption
///

/// caption
Outer caption
///
```

//// html | div.result
![placeholder](../../../images/placeholder.jpeg)

/// caption
Inner caption
///

/// caption
Outer caption
///
////

If a caption is provided after a figure element that does not already contain a caption, the caption will be inserted
into that figure. This allows for more complex figures with sub-figures.

```html title="Complex Captions"
//// html | figure
![placeholder](../../../images/placeholder.jpeg)

/// caption
Caption 1
///

![placeholder](../../../images/placeholder.jpeg)

/// caption
Caption 2
///
////

/// caption
    attrs: {class: "general"}
General caption
///

<style>
figure.general > figcaption {
    font-weight: bold;
}
</style>
```

///// html | div.result
//// html | figure
![placeholder](../../../images/placeholder.jpeg)

/// caption
Caption 1
///

![placeholder](../../../images/placeholder.jpeg)

/// caption
Caption 2
///
////

/// caption
    attrs: {class: "general"}
General caption
///

<style>
figure.general > figcaption {
    font-weight: bold;
}
</style>
/////

This can be used with Python Markdown's [`md_in_html` extension][md-in-html] as well, but keep in mind that figures
specified in this way must include the `markdown` attribute or they will be invisible to the Caption extension. Further,
if `#!html <figcaption>` elements do not have the `markdown` attribute, Caption will not know a figure already has a
caption.

```html title="Complex Captions: <code>md_in_html</code>"
<figure markdown>
![placeholder](../../../images/placeholder.jpeg)

/// caption
Caption 1
///

![placeholder](../../../images/placeholder.jpeg)

/// caption
Caption 2
///
</figure>

/// caption
    attrs: {class: "general"}
General caption
///

<style>
figure.general > figcaption {
    font-weight: bold;
}
</style>
```

///// html | div.result
<figure markdown>
![placeholder](../../../images/placeholder.jpeg)

/// caption
Caption 1
///

![placeholder](../../../images/placeholder.jpeg)

/// caption
Caption 2
///
</figure>

/// caption
    attrs: {class: "general"}
General caption
///

<style>
figure.general > figcaption {
    font-weight: bold;
}
</style>
/////

### Prepending Captions

Captions are appended by default, but can be configured to be prepended by default is desired. Simply set the global
[`prepend` option](#global-options) to `#!py True`.

```text title="Prepend Caption"
Fruit      | Amount
---------- | ------
Apple      | 20
Peach      | 10
Banana     | 3
Watermelon | 1

/// caption
Fruit Count
///
```

//// html | div.result
```md-render
---
extensions:
- pymdownx.blocks.caption
- tables
extension_configs:
  pymdownx.blocks.caption:
    prepend: true
---
Fruit      | Amount
---------- | ------
Apple      | 20
Peach      | 10
Banana     | 3
Watermelon | 1

/// caption
Fruit Count
///
```
////

Regardless of whether `prepend` is enabled or disabled globally, you can force prepend or append per block by specifying
`<` or `>` in the header for prepending or appending respectively.

```text title="Manual Prepend/Append"
![placeholder](../../../images/placeholder.jpeg)

/// caption | <
Caption 1
///

![placeholder](../../../images/placeholder.jpeg)

/// caption
Caption 2
///
```

//// html | div.result
![placeholder](../../../images/placeholder.jpeg)

/// caption | <
Caption 1
///

![placeholder](../../../images/placeholder.jpeg)

/// caption
Caption 2
///
////

### Auto Prefix and IDs

Caption defines multiple caption types by default: a generic `caption`, `figure-caption`, and `table-caption`. By
default `figure-caption` and `table-caption` are configured with prefix templates, and when used, the figure will have
special prefixes added to the caption with auto incrementing numbers. Additionally, a corresponding ID will be assigned
to the figure that wraps the content for linking.

````text title="Auto Prefix and IDs"
```diagram
graph TD
    A[Hard] -->|Text| B(Round)
    B --> C{Decision}
    C -->|One| D[Result 1]
    C -->|Two| E[Result 2]
```
/// figure-caption
Decision Diagram
///

Fruit      | Amount
---------- | ------
Apple      | 20
Peach      | 10
Banana     | 3
Watermelon | 1

/// table-caption
Fruit Count
///
````

//// html | div.result
```diagram
graph TD
    A[Hard] -->|Text| B(Round)
    B --> C{Decision}
    C -->|One| D[Result 1]
    C -->|Two| E[Result 2]
```
/// figure-caption
Decision Diagram
///

Fruit      | Amount
---------- | ------
Apple      | 20
Peach      | 10
Banana     | 3
Watermelon | 1

/// table-caption
Fruit Count
///
////

Numbers are tracked separately for each caption type that specifies a prefix template. When a caption is nested under
other figures, captions will have a dotted number corresponding with the nested level, e.g. 1, 1.1, 1.1.1, etc.

If desired, auto prefixing of nested sub-levels can be restricted via `auto_levels`. When specifying a non-zero,
positive number, auto-generated IDs and prefixes will be restricted to the specified nesting level. A nesting level of 1
only applies IDs and prefixes to the outermost figure of a given type where a nesting level of 2 will apply to the
outermost figure plus one level of nested children of the same type.

### Increase Nesting Depth

/// warning
Requires [`auto`](#global-options) to be set to `#!py True` (the default).
///

To accommodate various needs, some more control over numbering is exposed. If a user would like to show sub-figure
numbers but not have the figures directly nested under a parent figure, automatic numbers can be influenced by
specifying a specific nesting depth in the header of the caption block. By specifying a number prefixed with `^`, we can
increase the numbering depth for that specific figure by the specified value relative to its current depth. Figures are
still subject to the `auto_levels` limit.

```text title="Nesting Depth"
![placeholder](../../../images/placeholder.jpeg)
/// figure-caption
Caption
///

![placeholder](../../../images/placeholder.jpeg)
/// figure-caption | ^1
Caption
///

![placeholder](../../../images/placeholder.jpeg)
/// figure-caption | ^1
Caption
///

![placeholder](../../../images/placeholder.jpeg)
/// figure-caption
Caption
///
```

//// html | div.result
![placeholder](../../../images/placeholder.jpeg)
/// figure-caption
Caption
///

![placeholder](../../../images/placeholder.jpeg)
/// figure-caption | ^1
Caption
///

![placeholder](../../../images/placeholder.jpeg)
/// figure-caption | ^1
Caption
///

![placeholder](../../../images/placeholder.jpeg)
/// figure-caption
Caption
///
////

/// tip
Nesting depths can be used with per block prepend notation as long as `<` or `>` comes before the depth notation.
///

### Manual Figure Numbers

/// warning
It is recommended to use [`auto`](#global-options) set to `#!py False`, i.e. "manual mode", but can be used with when it is set
to `#!py True` with some limitations.
///

Captions allows for setting figures numbers for prefixes and IDs on the fly. This is mainly designed for use in "manual
mode" ([`auto`](#global-options) set to `#!py False`). The idea was to provide a mode where the user has complete control of
figure numbers if so desired. When in manual mode, the user will only get prefixes when specifying numbers in the header
of figure types that specify a prefix template. Manual mode does not not check or validate these numbers beyond ensuring
they are in fact numbers that are formatted properly.

```text title="Manual Numbers"
![placeholder](../../../images/placeholder.jpeg)
/// figure-caption | 12
Caption
///
```

//// html | div.result
![placeholder](../../../images/placeholder.jpeg)
/// figure-caption | 12
Caption
///
////

/// tip
Manual numbers can be used with per block prepend notation as long as `<` or `>` comes before the number.
///

In "automatic mode" (the default) the number will be used if, and only if, the specified number is greater than the last
figure number (automatic or otherwise) that was used for the specific figure type at the specific number depth. If, for
any reason, this is not true, an automatic figure number at the specified number depth will be used instead.
Essentially, the internal, automatic counter can be increased at any time, but can never be decreased.

As an example, if `1.1` is specified, but the last number for current figure type was `2`, `2.1` will be used instead.
If the number is much bigger, Caption will not care and accept it readily, but it may create a gap in numbering.

Additionally, manual numbers are subject to the `auto_levels` limit when in "automatic mode".

### Static IDs

While automatic mode will generate IDs for prefixed captions, some may prefer an unchanging, static ID for linking. If
you'd like to link to a figure with a static ID, you can specify one on any figure type (prefixed or non-prefixed) and
the ID will be applied instead of any auto-generated ID. Manually specified IDs will not affect auto-incrementing
numerical prefixes.

```
![placeholder](../../../images/placeholder.jpeg)

/// figure-caption
    attrs: {id: static-id}
caption
///
```

IDs specified in this way will also override IDs generated in [manual mode](#manual-figure-numbers).

If you prefer a more compact syntax, the ID can also be specified inline in the caption header. Use `#id-value` (or
`id=id-value`) after any prepend marker or manual numbering:

```
![placeholder](../../../images/placeholder.jpeg)

/// figure-caption | #static-id
caption
///

![placeholder](../../../images/placeholder.jpeg)
/// figure-caption | < #prepend-id
caption
///
```

The inline shorthand behaves the same as the `attrs` front matter and will override any automatically generated ID. It
is available for all caption types, so the same syntax applies to `table-caption`, custom types, etc.

### Configuring Figure Types

While Caption provides a few default figure types, users are free to define their own with different prefixes.

If a figure type is defined with no prefix, that type will never have IDs or prefixes generated for it. The default
generic `caption` type is an example of a non-prefix caption type.

Users can override the default types with their own via the [`types` option](#global-options). `types` is defined as a list
of types which can either be a single string specifying the name of the caption type (with no prefix), or a dictionary
object that specifies, the `name` and `prefix` template for the caption prefix. An empty string for the `prefix` is the
same as no prefix being specified. `{}` must be specified for non-empty templates and is used to insert the
auto-generated numerical number of the figure.

```py
extenconfigs = {
    "pymdownx.blocks.caption": {
        "types": [
            'caption',
            {
                'name': 'figure-caption',
                'prefix': 'Figure {}.'
            },
            {
                'name': 'table-caption',
                'prefix': 'Table {}.'
            }
        ]
    }
}
```

If desired, you can also specify optional classes to be added to a specific figure type via the `classes` option.

```py
extenconfigs = {
    "pymdownx.blocks.caption": {
        "types": [
            'caption',
            {
                'name': 'figure-caption',
                'prefix': 'Figure {}.'
                'classes': 'one-class two-class'
            },
            {
                'name': 'table-caption',
                'prefix': 'Table {}.'
            }
        ]
    }
}
```

Prefix templates are inserted exactly as specified, that means you can also use raw HTML. That also means you must
HTML escape anything that needs it as well.

```py
extenconfigs = {
    "pymdownx.blocks.caption": {
        "types": [
            'caption',
            {
                'name': 'figure-caption',
                'prefix': 'Figure <span class="prefix-fig-num">{}</span>.'
                'classes': 'one-class two-class'
            },
            {
                'name': 'table-caption',
                'prefix': 'Table <span class="prefix-fig-num">{}</span>.'
            }
        ]
    }
}
```

/// new | New 10.16
Using raw HTML in prefix templates was added in 10.16.
///

## Global Options

Options        | Type       | Descriptions
-------------  | ---------- | ------------
`types`        | list       | A list of figure types. Figure types must specify a name and can specify an optional prefix template where `{}` is where the figure number will be inserted.
`prepend`      | boolean    | Prepend captions opposed appending captions to figures. Disabled by default.
`auto`         | boolean    | Auto add IDs to all figure types that include prefix templates. Enabled by default.
`auto_level`   | integer    | Limit auto prefixing to a certain depth. Default is 0 which disables limiting.

## Per Block Options

Options      | Type       | Descriptions
------------ | ---------- | ------------
`attrs`      | dictionary | A string that defines attributes for the outer, wrapper element.
