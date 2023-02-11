[:octicons-file-code-24:][_blocks]{: .source-link }

# Blocks

!!! warning "Alpha Release"
    Blocks is currently only available in the Pymdown Extensions alpha release. It is a work in progress and API and
    syntax are subject to change.

    Please provide feedback here: https://github.com/facelessuser/pymdown-extensions/discussions/1883.

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

Lastly, a given Blocks plugin may allow for additional options that don't make sense in the first line declaration.
This may be because they are rarely used, more complicated, or just make the first line signature more confusing. These
options are per block specific use a YAML syntax. They must be part of the header, which means no new line between the
block declaration and the options or between individual options. The options also must be indented at least four spaces.

For instance, if we were using the HTML plugin, we may want to create a `#!html <div>` element but also add some class
attributes. We can do this by specifying the `attributes` option.

```
/// html | div
    attributes: {class: some-class}

Here is some content
I'd like to preserve.
///
```

!!! note "Attributes"
    It should be noted that all block meta-plugins support the `attributes` option and allow for specifying attributes
    that will be attached to the parent element.

While there is no hard rule stating that the first content content block must have a new line after the header, it
should be noted that some special content blocks may require an empty line before them. Simple paragraphs should not
require an empty new line, but the same cannot be said about other blocks. If in doubt, use an empty line before the
first content block.

## Nesting

Generic blocks can be nested as long as the block fence differs in number of leading tokens. This is similar to how
fenced code blocks work. The minimum requirement is that at least three tokens are used.

```
//// admonition | Some title
    type: note

/// details | Summary
content
///

Content
////
```

## Blocks Plugin API

### Block Structure

Different blocks are created via `Block` plugins. The basic structure of a block is shown below:

```
/// name | argument(s)
    options: per block options

Markdown content.
///
```

In addition, there are global options that are supplied through the block config.

### Creating a Plugin

To create a new Blocks plugin, you must drive a new class from the `Block` class.

```py
from pymdownx.blocks.block import Block

class MyBlock(Block):
    ...
```

You will need to set up related class attributes. At a minimum, `NAME` must be specified with a unique name, and you
must define the `on_create` method which should return the element under which all the content will live.

Once created, we can include the `pymdownx.blocks` extension and specify our plugin with any others that we want to
have enabled. Below, we only specify our new block.

```py
import markdown
import xml.etree.ElementTree as etree
from pymdownx.blocks.block import Block

class MyBlock(Block):
    # Name used for the block
    NAME = 'my-block'

    def on_create(self, parent):
        """Create the needed element and return it."""

        return etree.SubElement(parent, 'div')

MD = """
/// my-block
content
///
"""

print(markdown.markdown(
    MD,
    extensions=['pymdownx.blocks'],
    extension_configs={
        'pymdownx.blocks': {
            'blocks': [MyBlock],
            'yaml_indent': True
        }
    }
))
```

```html
<div>
<p>content</p>
</div>
```

### Arguments

Arguments are used to declare common block specific input for a particular block type. These are often, but not
exclusively, used for things like titles. They are specified on the same line as the initial block deceleration.

Blocks are not required to use arguments and are not included by default and must be declared in the class. Arguments
can be `optional`, `required`, or a combination of both.

The arguments are always parsed as a single string, but if a user declares that multiple arguments are accepted, the
result will be broken by a specified delimiter, the default being a space.

Arguments are assigned to the `args` class attribute and can be accessed anywhere after initialization:

```python
class MyBlock(Block):
    # Name used for the block
    NAME = 'my-block'
    ARGUMENTS = {'required': 1, 'optional': 1, 'delimiter': ','}

    def on_create(self, parent):
        """Create the needed element and return it."""

        attributes = {} if len(self.args) == 1 else {'special': 'special'}
        return etree.SubElement(parent, self.args[0], attributes)
```

If needed, you can parse the arguments and validate that they meet certain criteria or alternatively parse it as a
specific type. This can be done by specifying special argument parsers via `parsers`.

`parsers` takes a list of functions. Each function should accept a string argument and then return the argument
formatted in any way that is needed. If the string does not validate as the given type, it should raise an error.

Parsers align with the arguments by position, so a parser in the n^th^ position in the list will align with the n^th^
argument. If there are more arguments than parsers, then the last parser will be used for any additional arguments.

In the following example `type_tag` is a function that ensures the string is a valid HTML tag name, while `type_boolean`
ensures the input is either `true` or `false` and returns a boolean if it is.

```py
class MyBlock(Block):
    # Name used for the block
    NAME = 'my-block'
    ARGUMENTS = {'required': 1, 'optional': 1, 'delimiter': ',', 'parsers': [type_tag, type_boolean]}

    def on_create(self, parent):
        """Create the needed element and return it."""

        attributes = {} if len(self.args) == 1 and self.args[1] else {'special': 'special'}
        return etree.SubElement(parent, self.args[0], attributes)
```

### Options

Options is how a block specifies any per block features via an indented YAML block immediately after the block
declaration. The YAML indented block is considered a part of the header and is great for options that don't make sense
as part of the first line declaration. Here a user can specify any accepted option key words and provide parser function
to validate and/or coerce the input to a suitable format. As options are YAML, parser functions can choose to accept any
type that YAML can return. Once parsed, all options are assigned to the class attribute `options` and will be available
after initialization.

```py
class MyBlock(Block):
    # Name used for the block
    NAME = 'my-block'
    OPTIONS = {
        'tag_name': ['default', type_tag]
    }

    def on_create(self, parent):
        """Create the needed element and return it."""

        attributes = {} if len(self.args) == 1 and self.args[1] else {'special': 'special'}
        return etree.SubElement(parent, self.args[0], attributes)
```

### `on_register` Event

```py
@classmethod
def on_register(
    cls,
    blocks_processor: BlocksProcessor,
    md: Markdown,
    config: dict[str, Any]
) -> None:
    ...
```

When a Block plugin is registered, `on_register` is executed.

Parameter          | Description
------------------ | -----------
`blocks_processor` | The parent block processor of the meta plugin.
`md`               | The Markdown object.
`config`           | Global config for the meta plugin.

This is useful if you need to register support extensions (Treeprocessor, Postprocessor, etc.) through the `md` object
if required.

### `on_init` Event

```py
def on_init(self) -> None:
    ...
```

The `on_init` event is run ever time a new block is discovered. If the specified block name in Markdown matches the name
of a registered block, that block class will be instantiated, triggering `on_init` to execute.

This event is run right after the class does its main initialization, so `args`, `options`, `config`, and even a
reference to the `Markdown` object as `md` are accessible via `self`.

The can be a good way to perform setup based on on global or local options.

### `on_parse` Event

```py
def on_parse(self) -> bool:
    ...
```

Executed right after parsing occurs. Arguments and options are accessible via `self.args` and `self.options`. This gives
the plugin a chance to perform additional validation or adjustments if required. If there are issues `#!py3 False`
should be returned and will cause the block to fail.

### `on_create` Event

```py
    def on_create(self, parent: Element) -> None:
        ...
```

Called when a block is initially found and initialized. The `on_create` method should create the container for the block
under the parent element.

### `on_add` Event

```py
def on_add(self, block: Element) -> Element:
    ...
```

When any calls occur to process new content, `on_add` is called. This gives the block a chance to return the element
where the content is desired.

Some initial containers may be more complex and have nested elements already created. `on_add` helps ensure that the
content goes where it is actually desired in the container.

### `on_markdown` Event

```py
def on_markdown(self) -> str:
    """Check how element should be treated by the Markdown parser."""
    ...
```

The `on_markdown` event is used to declare how the content of the block should be handled by markdown.

Option   | Description
-------- | -----------
`block`  | Parse content as if contained within a block.
`inline` | Parse content as if contained within an inline element.
`raw`    | Preserve content as is.
`auto`   | Depending on whether the wrapping parent is a block element, inline element, or something like a code element, Blocks will choose the best approach for the content. Decision is made based on the element returned by [`on_add`](#on_add-event).

### `on_end` Event

```py
def on_end(self, block: Element) -> None:
    ...
```

When a block is parsed to completion, the `on_end` event is executed. This allows a plugin to perform any post
processing on the elements. You could save the data as raw text and then parse it special at the end or you could walk
the HTML elements and move content around, add attributes, or whatever else is needed.

!!! warning "Under Construction"

## Options

Option                | Type       |  Default                           | Description
--------------------- | ---------- | ---------------------------------- | -----------
`blocks`              | \[Block\]  | [See here](#included-meta-plugins) | A list of block meta-plugins to register.
`block_configs`       | dictionary | `#!py3 {}`                         | A dictionary used to specify global options for registered meta-plugins.
`colon_syntax`        | bool       | `#!py3 False`                      | Use the colon syntax for block fences (`:::`) instead of the default (`///`). Only available during alpha/beta stage.
