[:octicons-file-code-24:][_blocks]{: .source-link }

# Blocks

--8<-- "blocksbeta.md"

## Overview

Blocks is an extension aimed at providing generic blocks inspired by reStructuredText directives. While inspired by
directives, generic blocks are not meant to behave or mirror directives as a 1:1 solution.

The idea behind blocks is to solve a few issues that have existed within Python Markdown block extensions.

1. Markdown has numerous special syntaxes to define various elements, but as people try to add numerous extensions to
   perform specialized translations, it can become difficult to continuously come up with new, sensible syntax that does
   not conflict with some other extension that is desired by users.

2. Traditionally, Python Markdown has implemented any block processors that behave more as containers for multiple child
   blocks using an indentation format (think Admonitions as an example). While this works, this can be tiring to some
   authors who'd like to not have so many nested indentation levels in the documentation. Additionally, most code
   editors will syntax highlight such nested constructs as indented code blocks which can make reading the source
   difficult.

Blocks is an extension type that essentially allows for the creation of its own extension type that function as fenced
containers. Each extension can do whatever it wants with the content inside the container and allow for a single generic
format to create as many different block style extensions as desired. As the blocks are fenced, indentation is not
required to determine the start and end of the blocks.

Blocks also allows for per block options giving the extension authors an easy way to extend functionality and users an
easy, predictable way to specify such options.

Blocks itself isn't used directly, but there are a variety of extensions created with it. All of which can be registered
in the traditional way.

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.blocks.<extension>'])
```

Pymdown Extensions provides the following extensions.

Extension                               |  Description
--------------------------------------- | -----------
[`admonition`](./plugins/admonition.md) | The admonition block allows for the creation of admonitions.
[`define`](./plugins/definition.md)     | Allows for the creation of definition lists.
[`details`](./plugins/details.md)       | The details block allows for the creation of collapsible details/summary constructs.
[`tab`](./plugins/tab.md)               | Aims to replace the [Tabbed](../tabbed.md) extension and allows for the creation of tab containers.
[`html`](./plugins/html.md)             | HTML is a block that allows for the arbitrary creation of HTML elements of various types.

## Syntax

Syntax for Blocks requires the desired content to be included between fences. Fences are denoted by using three or
more forward slashes. The opening fence must specify the name of the block to invoke it.

```
/// name-of-block
content
///
```

/// tip | Content and New Lines
While there is no hard rule stating that the first content block must have a new line after the header, it should be
noted that some special content blocks may require an empty line before them, this may simply be due to how they are
implemented. Simple paragraphs should not require an empty new line before them, but we cannot make a blanket
statement about all blocks. If in doubt, use an empty line before the first content block.
///

Some blocks may implement a special argument in the header for things such as, but not limited to, titles. This
argument can be optional or sometimes enforced as a requirement. This is up to the given Blocks extension to decide.

```
/// note | Did you know?
You can create a note with Blocks!
///
```

//// html | div.result
/// note | Did you know?
You can create a note with Blocks!
///
////

Lastly, a given Block extension may allow for additional options that don't make sense in the first line declaration.
This may be because they are rarely used, more complicated, or just make the first line signature more confusing. These
options are per block specific use a YAML syntax. They must be part of the header, which means no new line between the
block declaration and the options or between individual options. The options also must be indented at least four spaces.

For instance, all extensions inherit an option `attrs` which allows you to set HTML attributes to the outer element of a
generic block.

```
/// html | div
    attrs: {style: 'font-size: xx-large'}

Some content.
///
```

//// html | div.result
/// html | div
    attrs: {style: 'font-size: xx-large'}

Some content.
///
////

Some blocks may take raw content (and should note this in their documentation) which will avoid further Markdown
processing on the content.  This is done by requiring the content to be an indented code block. Due to the way Python
Markdown works, these content blocks must be indented to avoid having the HTML processor from altering content. Raw
blocks cannot shield content from all preprocessor transformations, but by requiring the content to be indented code
blocks, the content will survive any alterations that a traditional code block would survive.

```
/// html | pre

    Pre blocks are _raw_.
    Additional Markdown parsing is *avoided*.
    Content should be indented.
///
```

//// html | div.result
/// html | pre

    Pre blocks are _raw_.
    Additional Markdown parsing is *avoided*.
    Content should be indented.
///
////

/// tip | Indented Content
Indented content should always be separated from the block header by one empty line so that it is not confused as a YAML
option block.
///

## Nesting

Generic blocks can be nested as long as the block fence differs in number of leading tokens. This is similar to how
fenced code blocks work. The minimum requirement is that at least three tokens are used.

```
//// note | Some title
/// details | Summary
    type: warning
content
///
Content
////
```

///// html | div.result
//// note | Some title
/// details | Summary
    type: warning
content
///

Content
////
/////
