[:octicons-file-code-24:][_tab_block]{: .source-link }

# Tab

--8<-- "blocksbeta.md"

## Overview

Tab blocks are aimed at replacing the [Tabbed extension](../../tabbed.md). They function identical to Tabbed in every
way, even using the same classes, except they use the new generic block syntax.

By default, the meta-plugin is registered when `pymdownx.blocks` is registered, but if you were customizing which
meta-plugins get loaded, you can do so by doing the following:

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.blocks.tab'])
```

## Usage

A tab can be defined using the generic bock syntax and the name `tab`. Tabs should also specify the tab title in the
header. Consecutive tabs will automatically be grouped.

```text title="Tabs"
/// tab | Tab 1 title
Tab 1 content
///

/// tab | Tab 2 title
Tab 2 content
///
```

/// html | div.result

//// tab | Tab 1 title
Tab 1 content
////

//// tab | Tab 2 title
Tab 2 content
////
///

If you want to have two tab containers right after each other, you specify a hard break that will force the specified
tab to start a brand new tab container.

```text title="New Tab Group"
/// tab | Tab A title
Tab A content
///

/// tab | Tab B title
Tab B content
///

/// tab | Tab C Title
    new: true

Will be part of a separate, new tab group.
///
```

/// html | div.result

//// tab | Tab A title
Tab A content
////

//// tab | Tab B title
Tab B content
////

//// tab | Tab C title
    new: true
Will be part of a separate, new tab group.
////
///

If desired, you can specify a tab to be selected by default with the `select` option.

```
/// tab | Tab 1 title
Tab 1 content
///

/// tab | Tab 2 title
    select: True

Tab 2 should be selected by default.
///
```

As with all block plugins, you can always add new classes IDs or other attributes via the `attributes` option.

```
/// tab | Some title
    attrs: {class: class-name: id: id-name}

Some content
///
```

## Global Options

Options           | Type     | Descriptions
----------------- | -------- | ------------
`alternate_style` | bool     | Use the experimental, alternative style.
`slugify`         | function | A function to generate slugs from tab titles.
`separator`       | string   | Default word separator when generating slugs.

## Per Block Options

Options      | Type       | Descriptions
------------ | ---------- | ------------
`new`        | bool       | Force the current tab to start a new tab container.
`select`     | bool       | Force the given tab to be selected in the parent tab container.
`attrs`          | string     | A string that defines attributes for the outer, wrapper element.
