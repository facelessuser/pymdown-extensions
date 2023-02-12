[:octicons-file-code-24:][_html_block]{: .source-link }

# HTML

!!! warning "Alpha Release"
    Blocks is currently only available in the Pymdown Extensions alpha release. It is a work in progress and API and
    syntax are subject to change.

    Please provide feedback here: https://github.com/facelessuser/pymdown-extensions/discussions/1940.

## Overview

The HTML block allows a user to wrap Markdown in arbitrary HTML elements.

By default, the meta-plugin is registered when `pymdownx.blocks` is registered, but if you were customizing which
meta-plugins get loaded, you can do so by doing the following:

```py3
import markdown
from pymdownx.blocks.html import HTML
md = markdown.Markdown(
    extensions=['pymdownx.blocks']
    extension_configs={
        'pymdownx.blocks': {
            'blocks': [HTML]
            # Use block_configs to set block specific global settings
        }
    }
)
```

## Usage

Generally, HTML blocks can be defined simply by specifying the `html` generic block type followed by the tag name. As
with all generic blocks, additional attributes can be applied via the `attributes` option.

``` title="Example: HTML"
/// html | div
    attributes:
      style: 'border: 1px solid red;'

some *markdown* content
///
```

<div class="result" markdown>

```md-render
---
extensions:
- pymdownx.blocks
---
/// html | div
    attributes:
      style: 'border: 1px solid red;'

some *markdown* content
///
```

</div>

By default HTML blocks will automatically have the content rendering determined from tag name, so `div` blocks will be
treated as block elements, `span` will be treated as inline elements, and things like `pre` will treat the content as
raw text that should not be processed by Markdown further. With that said, there may be cases where an HTML element
isn't properly recognized yet, or the user simply wants to control how the element processes its content, in these
cases, the `markdown` option can be used to specify how Markdown content is handled.

In the following example we force `pre` to handle content as Markdown block content instead of the usual raw content
default.

``` title="Example: Pre as Block"
/// html | pre
some *markdown* content
///

/// html | pre
    markdown: block

some *markdown* content
///
```

<div class="result" markdown>

```md-render
---
extensions:
- pymdownx.blocks
---
/// html | pre
some *markdown* content
///

/// html | pre
    markdown: block

some *markdown* content
///
```

</div>

## Per Block Options

Options      | Type       | Descriptions
------------ | ---------- | ------------
`markdown`   | string     | String value to control how Markdown content is processed. Valid options are: `auto`, `block`, `span`, and `raw`.
`attributes` | dictionary | A dictionary containing keys (attributes) and values (attribute values).
