[:octicons-file-code-24:][_tab_block]{: .source-link }

# Tab

!!! warning "Alpha Release"
    Blocks is currently only available in the Pymdown Extensions alpha release. It is a work in progress and API and
    syntax are subject to change.

    Please provide feedback here: https://github.com/facelessuser/pymdown-extensions/discussions/1940.

## Overview

Tab blocks are aimed at replacing the [Tabbed extension](../tabbed.md). They function identical to Tabbed in every way,
even using the same classes, except they use the new generic block syntax.

By default, the meta-plugin is registered when `pymdownx.blocks` is registered, but if you were customizing which
meta-plugins get loaded, you can do so by doing the following:

```py3
import markdown
from pymdownx.blocks.tab import Tab
md = markdown.Markdown(
    extensions=['pymdownx.blocks']
    extension_configs={
        'pymdownx.blocks': {
            'blocks': [Tab]
            # Use block_configs to set block specific global settings
        }
    }
)
```

## Usage

A tab can be defined using the generic bock syntax and the name `tab`. Tabs should also specify the tab title in the
header. Consecutive tabs will automatically be grouped.

``` title="Example: Tabs"
/// tab | Tab 1 title
Tab 1 content
///

/// tab | Tab 2 title
Tab 2 content
///
```

<div class="result" markdown>

<!-- Rendering with old style as we have not switched over to general blocks globally in the documentation -->

=== "Tab 1 title"
    Tab 1 content

=== "Tab 2 title"
    Tab 2 content

</div>

If you want to have two tab containers right after each other, you specify a hard break that will force the specified
tab to start a brand new tab container.

``` title="Example: New Tab Group"
/// tab | Tab A title
Tab A content
///

/// tab | Tab B title
Tab B content
///

/// tab | Tab C Title
    new: True

Will be part of a separate, new tab group.
///
```

<div class="result" markdown>

<!-- Rendering with old style as we have not switched over to general blocks globally in the documentation -->

=== "Tab A title"
    Tab A content

=== "Tab B title"
    Tab B content

===! "Tab C title"
    Will be part of a separate, new tab group.

</div>

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
    attributes:
      class: class-a class-b

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
