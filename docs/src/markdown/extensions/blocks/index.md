[:octicons-file-code-24:][_blocks]{: .source-link }

# Blocks

!!! warning "Alpha Release"
    Blocks is currently only available in the Pymdown Extensions alpha release. It is a work in progress and API and
    syntax are subject to change.

    Please provide feedback here: https://github.com/facelessuser/pymdown-extensions/discussions/1868.

## Overview

Blocks is an extension aimed at providing generic blocks inspired by reStructuredText directives. While inspired by
directives, generic blocks are not meant to behave or mirror directives as a 1:1 solution.

The idea behind blocks is to solve a few issues that have existed within Python Markdown block extensions.

1. Markdown as numerous special syntaxes to define various elements, but as people try to add numerous plugins to
   perform specialized translations, it can become difficult to continuously come up with new, sensible syntax that does
   not conflict with some other plugin that is desired by users.

2. Traditionally, Python Markdown has implemented any block processors that behave more as containers for multiple child
   blocks using an indentation format (think Admonitions as an example). While this works, this can be tiring to some
   authors who'd like to not have so many nested indentation levels in the documentation. Additionally, most code
   editors will syntax highlight such nested constructs as indented code blocks which can make reading the source
   difficult.

Blocks is a plugin that essentially allows for the creation of its own meta-plugins that function as fenced containers.
Each meta-plugin can do whatever it wants with the content inside the container and allow for a single generic format
to create as many different block style plugins as desired. As the blocks are fenced, indentation is not required to
determine the start and end of the blocks.

Blocks also allows for per block options giving the extension authors an easy way to extend functionality and users an
easy, predictable way to specify such options.

To use Blocks, simply include the extension as shown below.

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.blocks'])
```

## Feedback Requested

While any and all feedback is welcome, there are two undecided options that require feedback to help us finalize the
syntax for generic blocks. During the alpha/beta stage, we provide global options so users can try out the different
options and provide their own feedback. Feedback will be taken into consideration as we move towards an official release
candidate. It will be impossible to make all users happy, but we'd like to give users an opportunity to help shape
the direction.

1. Currently, there is no hard decision as to whether we should use `:::` or `///` for the fence syntax. During the
   alpha/beta stage, we provide a global option called `colon_syntax` to switch from using `///` to `:::`. This will
   only be offered during the alpha/beta stage and is provided to allow users to try out give their opinion as to what
   direction Blocks should take in order to finalize the syntax.

2. Blocks has not yet decided as to whether the YAML config in headers should require YAML fences (`---`) or not. By
   default, YAML fences are optional, but during the alpha/beta period, we are allowing users to enforce YAML fences via
   the global option `require_yaml_fences`.

    The pro to making YAML fences optional is that a user does not have to specify `---` to denote where a YAML config
    starts and ends. Requiring YAML fences may feel tedious to some authors, but the con is that content must be
    separated from the YAML config using a blank line. As a matter of fact, since it can be difficult to determine if
    there is a YAML config when no fence is used, content always requires a new line to separate the header from the
    content:

    ```
    /// name
    yaml-option: true

    Content must be separated from header by a new line
    ///

    /// name

    Even without YAML options, content must be separated from the header by a new line.
    ///
    ```

    If YAML fences are required, then YAML configs in the header can always be easily identified eliminating the
    hard requirement for new lines between the header and the content.

    ```
    /// name
    ---
    yaml-option: true
    ---
    Content does not require a new line before it, but can optionally use one if desired.
    ///

    /// name
    Content does not need a new line when no YAML options are used.
    ///
    ```

## Included Meta-Plugins

Blocks provides a number of "meta-plugins" out of the box.

Plugin                          |  Description
------------------------------- | -----------
[`admonition`](./admonition.md) | The admonition block allows for the creation of admonitions.
[`details`](./details.md)       | The details block allows for the creation of collapsible details/summary constructs.
[`tab`](./tab.md)               | Aims to replace the [Tabbed](../tabbed.md) extension and allows for the creation of tab containers.
[`html`](./html.md)             | HTML is a block that allows for the arbitrary creation of HTML elements of various types.


## Configuring Meta-Plugins

By default, all meta-plugins are included, but you can add or specify different ones and configure them via the `blocks`
and `block_configs` options.

```py3
import markdown
from pymdownx.blocks.admonition import Admonition

md = markdown.Markdown(
    extensions=['pymdownx.blocks'],
    extension_configs={
        'pymdownx.blocks': {
            'blocks': [Admonition],
            'block_configs': {
                "admonition": {
                    'types': ['note', 'warning', 'some-custom-type']
                }
            }
        }
    }
)
```

## Syntax

Syntax for Blocks requires the desired content to be included between fences. Fences are denoted by using three or
more forward slashes. The opening fence must specify the name of the block to invoke it.

```
/// name-of-block

content
///
```

Some blocks may implement a special argument in the header for things such as, but not limited to, titles. These
arguments can be optional or sometimes enforced as a requirement. This is up to the given Blocks plugin to decide.

```
/// note | Did you know?

You can create a note with Blocks!
///
```

Lastly, a given Blocks plugin may allow for arbitrary options that are per block specific. For instance, if we were
using the HTML plugin, we may want to create a `#!html <div>` element but preserve the content as raw text, avoiding
further Markdown processing. We could do this by specifying the special `markdown` option and giving it the value of
`raw`. This is done using a YAML config as part of the header.

```
/// html | div
---
markdown: raw
---

Here is some content
I'd like to preserve.
///
```

It should be noted that the YAML config must be part of the header having no new lines within it. Python Markdown
must be able to capture the start of the block and the config all at once.

!!! warning "Content and Header Separation"
    By default, Blocks currently requires that content be separated from the opening header by one new line, regardless
    of whether a YAML config is provided or not. This is because YAML fences are currently optional, and it is difficult
    to 100% be sure as to whether a block has a YAML config or not without this requirement.

Lastly, it should be noted that all block meta-plugins support the `attributes` option and allow for specifying
attributes that will be attached to the parent element.

```
/// note | Some title
---
attributes: {class: 'some-class some-other-class'}
---

Content
///
```

## Blocks Plugin API

!!! warning "Under Construction"

## Options

Option                | Type       |  Default                           | Description
--------------------- | ---------- | ---------------------------------- | -----------
`blocks`              | \[Block\]  | [See here](#included-meta-plugins) | A list of block meta-plugins to register.
`block_configs`       | dictionary | `#!py3 {}`                         | A dictionary used to specify global options for registered meta-plugins.
`require_yaml_fences` | bool       | `#!py3 False`                      | Specify whether YAML fences for per block options should be required. Only available during alpha/beta stage.
`colon_syntax`        | bool       | `#!py3 False`                      | Use the colon syntax for block fences (`:::`) instead of the default (`///`). Only available during alpha/beta stage.
