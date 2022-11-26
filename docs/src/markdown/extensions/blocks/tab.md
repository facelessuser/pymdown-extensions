[:octicons-file-code-24:][_tab_block]{: .source-link }

# Tab

## Overview

Tab blocks are aimed at replacing the [Tabbed extension](../tabbed.md). They function identical to Tabbed in every way
except they use the new generic block syntax.

## Usage

A tab can be defined using the generic bock syntax and the name `tab`. Tabs should also specify the tab title in the
header. Consecutive tabs will automatically be grouped.

``` title="Example: Tabs"
/// tab | Tab 1 title

Tab1 content
///

/// tab | Tab 2 title

Tab 2 content
///
```

<div class="result" markdown>

```md-render
---
extensions:
- pymdownx.blocks
extension_configs:
  pymdownx.blocks:
    block_configs:
      tab:
        alternate_style: true
---
/// tab | Tab 1 title

Tab1 content
///

/// tab | Tab 2 title

Tab 2 content
///
```

</div>

If you want to have two tab containers right after each other, you specify a hard break that will force the specified
tab to start a brand new tab container.

``` title="Example: New Tab Group"
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

<div class="result" markdown>

```md-render
---
extensions:
- pymdownx.blocks
extension_configs:
  pymdownx.blocks:
    block_configs:
      tab:
        alternate_style: true
---
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

</div>

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
