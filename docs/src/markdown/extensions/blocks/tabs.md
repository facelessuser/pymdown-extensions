# Tabs

## Overview

Tab blocks are aimed at replacing the [Tabbed extension](../tabbed.md). They function identical to Tabbed in every way
except they use the new generic block syntax.

## Usage

A tab can be defined using the generic bock syntax and the name `tab`. Tabs should also specify the tab title in the
header.

```
/// tab | Tab title

Tab content
///
```

Consecutive tabs will automatically be grouped:

```
/// tab | Tab 1 title

Tab1 content
///

/// tab | Tab 2 title

Tab 2 content
///
```

If you want to have two tab containers right after each other, you specify a hard break that will force the specified
tab to start a brand new tab container.

```
/// tab | Tab 1 title

Tab 1 content
///

/// tab | Tab 2 title

Tab 2 content
///

/// tab | Tab A Title
---
new: True
---

Will be part of a separate, new tab group.
///
```

If desired, you can specify a tab to be selected by default with the `select` option.

```
/// tab | Tab 1 title

Tab 1 content
///

/// tab | Tab 2 title
---
select: True
---

Tab 2 should be selected by default.
///
```

As with all block plugins, you can always add new classes IDs or other attributes via the `attributes` option.

```
/// tab | Some title
---
attributes:
  class: class-a class-b
---

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
`attributes` | dictionary | A dictionary containing keys (attributes) and values (attribute values).
