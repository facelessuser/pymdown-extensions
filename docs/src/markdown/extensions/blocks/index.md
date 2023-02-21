[:octicons-file-code-24:][_blocks]{: .source-link }

# Blocks

/// warning | Alpha Release
Blocks is currently only available in the Pymdown Extensions alpha release. It is a work in progress and API and
syntax are subject to change.

Please provide feedback here: https://github.com/facelessuser/pymdown-extensions/discussions/1940.
///

## Overview

Blocks is an extension aimed at providing generic blocks inspired by reStructuredText directives. While inspired by
directives, generic blocks are not meant to behave or mirror directives as a 1:1 solution.

The idea behind blocks is to solve a few issues that have existed within Python Markdown block extensions.

1. Markdown has numerous special syntaxes to define various elements, but as people try to add numerous plugins to
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

While any and all feedback is welcome, there is one undecided options that require feedback to help us finalize the
syntax for generic blocks. During the alpha/beta stage, we provide global options so users can try out the different
options and provide their own feedback. Feedback will be taken into consideration as we move towards an official release
candidate. It will be impossible to make all users happy, but we'd like to give users an opportunity to help shape
the direction.

1. Currently, there is no hard decision as to whether we should use `:::` or `///` for the fence syntax. During the
   alpha/beta stage, we provide a global option called `colon_syntax` to switch from using `///` to `:::`. This will
   only be offered during the alpha/beta stage and is provided to allow users to try out give their opinion as to what
   direction Blocks should take in order to finalize the syntax.

## Included Meta-Plugins

Blocks provides a number of "meta-plugins" out of the box. Not are registered by default. You must select and register
the ones you wish to use.

Plugin                                  |  Description
--------------------------------------- | -----------
[`admonition`](./plugins/admonition.md) | The admonition block allows for the creation of admonitions.
[`define`](./plugins/definition.md)     | Allows for the creation of definition lists.
[`details`](./plugins/details.md)       | The details block allows for the creation of collapsible details/summary constructs.
[`tab`](./plugins/tab.md)               | Aims to replace the [Tabbed](../tabbed.md) extension and allows for the creation of tab containers.
[`html`](./plugins/html.md)             | HTML is a block that allows for the arbitrary creation of HTML elements of various types.


## Configuring Meta-Plugins

By default, all meta-plugins are included, but you can specify the plugins you desire to use and configure them via the
`blocks` and `block_configs` options.

```py
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

You can also use simple strings and the plugin will be located and registered accordingly. The syntax is:

```
path.to.module:PluginClass
```

A full example would be:

```py
import markdown

md = markdown.Markdown(
    extensions=['pymdownx.blocks'],
    extension_configs={
        'pymdownx.blocks': {
            'blocks': ['pymdownx.blocks.admonition:Admonition'],
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

/// tip | Content and New Lines
While there is no hard rule stating that the first content block must have a new line after the header, it should be
noted that some special content blocks may require an empty line before them, this may simply be due to how they are
implemented. Simple paragraphs should not require an empty new line before them, but we cannot make a blanket
statement about all blocks. If in doubt, use an empty line before the first content block.
///

Some blocks may implement a special argument in the header for things such as, but not limited to, titles. These
arguments can be optional or sometimes enforced as a requirement. This is up to the given Blocks plugin to decide.

```
/// note | Did you know?
You can create a note with Blocks!
///
```

Lastly, a given Block plugin may allow for additional options that don't make sense in the first line declaration.
This may be because they are rarely used, more complicated, or just make the first line signature more confusing. These
options are per block specific use a YAML syntax. They must be part of the header, which means no new line between the
block declaration and the options or between individual options. The options also must be indented at least four spaces.

For instance, all plugins have inherit an option `$` which allows you to set HTML attributes to the outer element of a
generic block. You can use [Emmet style syntax](https://docs.emmet.io/abbreviations/syntax/) to set an id, classes, or
other arbitrary attributes.

```
/// html | div
    $: #id.some-class[title="A title" data-columns=3]

Some content.
///
```

## Nesting

Generic blocks can be nested as long as the block fence differs in number of leading tokens. This is similar to how
fenced code blocks work. The minimum requirement is that at least three tokens are used.

```
//// admonition | Some title
    $: .note

/// details | Summary
content
///

Content
////
```

## Options

Option                | Type       |  Default                           | Description
--------------------- | ---------- | ---------------------------------- | -----------
`blocks`              | \[Block\]  | `#!py []`                           | A list of block meta-plugins to register.
`block_configs`       | dictionary | `#!py {}`                         | A dictionary used to specify global options for registered meta-plugins.
`colon_syntax`        | bool       | `#!py False`                      | Use the colon syntax for block fences (`:::`) instead of the default (`///`). Only available during alpha/beta stage.
