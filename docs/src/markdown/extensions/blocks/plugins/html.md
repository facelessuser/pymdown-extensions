[:octicons-file-code-24:][_html_block]{: .source-link }

# HTML

--8<-- "blocksbeta.md"

## Overview

The HTML block allows a user to wrap Markdown in arbitrary HTML elements.

By default, the meta-plugin is registered when `pymdownx.blocks` is registered, but if you were customizing which
meta-plugins get loaded, you can do so by doing the following:

```py3
import markdown
from pymdownx.blocks.html import HTML
md = markdown.Markdown(extensions=['pymdownx.blocks.html'])
```

## Usage

Generally, HTML blocks can be defined simply by specifying the `html` generic block type followed by the tag name.

```text title="HTML"
/// html | div
some *markdown* content
///
```

/// html | div.result
//// html | div
some *markdown* content
////
///

Classes and IDs and arbitrary attributes can be specified by using selector-like notation:

- `#!css div.my-class` will add a class of name `my-class` to a tag of name `div`.
- `#!css div#some-id` will add an ID of name `some-id` to a tag of name `div`.
- `#!css div[attr]` will add an attribute of name `attr` to a tag of name `div`. You can also add values
  (`#!css div[attr=value]`),
  quoted values (`#!css div[attr="quoted value"]`), and even multiple values (`#!css div[attr1=value attr2="quoted value"]`).
- Attributes can also be chained: `#!css div#some-id.class[attr=value]`.

```text title="HTML"
/// html | div[style='border: 1px solid red;']
some *markdown* content
///
```

/// html | div.result
//// html | div[style='border: 1px solid red;']
some *markdown* content
////
///

By default HTML blocks will automatically have the content rendering determined from tag name, so `div` blocks will be
treated as block elements, `span` will be treated as inline elements, and things like `pre` will treat the content as
raw text that should not be processed by Markdown further. With that said, there may be cases where an HTML element
isn't properly recognized yet, or the user simply wants to control how the element processes its content, in these
cases, the `markdown` option can be used to specify how Markdown content is handled.

In the following example we force `pre` to handle content as Markdown block content instead of the usual raw content
default.


```text title="Pre as Block"
/// html | pre

    some *markdown* content
///

/// html | pre
    markdown: block

some *markdown* content
///
```

/// html | div.result
//// html | pre

    some *markdown* content
////

//// html | pre
    markdown: block

some *markdown* content
////
///

/// tip | Raw Mode
When using _raw_ tags or forcing _raw_ mode with `markdown: raw`, it is advised to indent the code. This is because
Python Markdown will look for and process raw HTML in non indented blocks. The only avoid this is to use indented
blocks. Content will automatically be dedented by the expected tab length.

Recognized raw block tags: `canvas`, `math`, `option`, `pre`, `script`, `style`, and `textarea`.

Also, make sure to have a new line before indented content so it is not recognized as an attempt to specify YAML
options.
///

## Per Block Options

Options      | Type       | Descriptions
------------ | ---------- | ------------
`markdown`   | string     | String value to control how Markdown content is processed. Valid options are: `auto`, `block`, `inline`, and `raw`.
`attrs`      | string     | A string that defines attributes for the outer, wrapper element.
