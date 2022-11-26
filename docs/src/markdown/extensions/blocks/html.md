[:octicons-file-code-24:][_html_block]{: .source-link }

# HTML

## Overview

The HTML block allows a user to wrap Markdown in arbitrary HTML elements.

## Usage

Generally, HTML blocks can be defined simply by specifying the `html` generic block type followed by the tag name. As
with all generic blocks, additional attributes can be applied via the `attributes` option.

``` title="Example: HTML"
/// html | div
---
attributes:
  style: 'border: 1px solid red;'
---

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
---
attributes:
  style: 'border: 1px solid red;'
---

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
---
markdown: block
---

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
---
markdown: block
---

some *markdown* content
///
```

</div>

## Per Block Options

Options      | Type       | Descriptions
------------ | ---------- | ------------
`markdown`   | string     | String value to control how Markdown content is processed. Valid options are: `auto`, `block`, `span`, and `raw`.
`attributes` | dictionary | A dictionary containing keys (attributes) and values (attribute values).