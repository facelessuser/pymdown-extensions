[:octicons-file-code-24:][_blocks]{: .source-link }

# Blocks

!!! warning "Alpha Release"
    Blocks is currently only available in the Pymdown Extensions alpha release. It is a work in progress and API and
    syntax are subject to change.

    Please provide feedback here: https://github.com/facelessuser/pymdown-extensions/discussions/1940.

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
[`define`](./definition.md)     | Allows for the creation of definition lists.
[`details`](./details.md)       | The details block allows for the creation of collapsible details/summary constructs.
[`tab`](./tab.md)               | Aims to replace the [Tabbed](../tabbed.md) extension and allows for the creation of tab containers.
[`html`](./html.md)             | HTML is a block that allows for the arbitrary creation of HTML elements of various types.


## Configuring Meta-Plugins

By default, all meta-plugins are included, but you can specify the plugins you desire to use and configure them via the
`blocks` and `block_configs` options.

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

!!! tip "Content and New Lines"
    While there is no hard rule stating that the first content block must have a new line after the header, it should be
    noted that some special content blocks may require an empty line before them, this may simply be due to how they are
    implemented. Simple paragraphs should not require an empty new line before them, but we cannot make a blanket
    statement about all blocks. If in doubt, use an empty line before the first content block.

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

## Options

Option                | Type       |  Default                           | Description
--------------------- | ---------- | ---------------------------------- | -----------
`blocks`              | \[Block\]  | [See here](#included-meta-plugins) | A list of block meta-plugins to register.
`block_configs`       | dictionary | `#!py3 {}`                         | A dictionary used to specify global options for registered meta-plugins.
`colon_syntax`        | bool       | `#!py3 False`                      | Use the colon syntax for block fences (`:::`) instead of the default (`///`). Only available during alpha/beta stage.


## Blocks Plugin API

### Block Structure

The various different block types are created via `Block` plugins. The basic structure of a block is shown below:

```
/// name | argument(s)
    options: per block options

Markdown content.
///
```

In addition, there are sometimes global options for a specific block type are supplied through the `block_configs`
plugin option. Such options would control features for the specific block type they are defined for and would affect all
the blocks of that type globally.

### Creating a Plugin

To create a new Blocks plugin, you must derive a new class from the `Block` class.

```py
from pymdownx.blocks.block import Block

class MyBlock(Block):
    ...
```

You will need to set up related class attributes. At a minimum, `NAME` must be specified with a unique name, and you
must define the `on_create` method which should return the element under which all the content in that block will live.

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
            'blocks': [MyBlock]
        }
    }
))
```

<div class="result" markdown>

```html
<div>
<p>content</p>
</div>
```

</div>

### Arguments

Arguments are used to declare common block specific input for a particular block type. These are often, but not
exclusively, used for things like titles. They are specified on the same line as the initial block deceleration.

Blocks are not required to use arguments and are not included by default and must be declared in the class. Arguments
can be `optional`, `required`, or a combination of both.

The arguments are always parsed as a single string, but if a user declares that multiple arguments are accepted, the
result will be broken by a specified delimiter, the default being a space.

Arguments will be positionally assigned as a list to the instance attribute `self.args` and can be accessed anywhere
after initialization.

```python
class MyBlock(Block):
    # Name used for the block
    NAME = 'my-block'
    ARGUMENTS = {'required': 1, 'optional': 1, 'delimiter': ','}
```

!!! tip "Validating Arguments"
    If you'd like to validate arguments, you can utilize the [`on_parse` event](#on_parse-event). It is also acceptable
    manually parse arguments in the `on_parse` event as well. This may be useful if the arguments cannot be parsed with
    a simple delimiter.

### Options

Options is how a block specifies any per block features via an indented YAML block immediately after the block
declaration. The YAML indented block is considered a part of the header and is great for options that don't make sense
as part of the first line declaration.

An option consists of a keyword to specify the option name, and then a list containing the default value and a validator
callback. The callback function should take the input and validate the type and/or coerce the value to an appropriate
value. If the input, for whatever reason, is deemed invalid, the callback function should raise an error.

After processing, all options will be available as a dictionary via the instance attribute `self.options`. Options
will be accessible via the keyword and will return the resolved value.

!!! tip "Built-in validators"
    A number of Built-in validators are provided. Check out [Built-in Validators](#built-in-validators) to learn more,
    or feel free to write your own.

```py
class MyBlock(Block):
    # Name used for the block
    NAME = 'my-block'
    OPTIONS = {
        'tag_name': ['default', type_tag]
    }
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

### Built-in Validators

A number of validators are provided via for the purpose of validating [YAML option inputs](#options). If what you need
is not present, feel free to write your own.


#### `type_number`

Takes a YAML input value and verifies that it is a `float` or `int`.

Returns the valid number (`float` or `int`) or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': [0.0, type_number]}
```

#### `type_integer`

Takes a YAML input value and verifies that it is an `int`.

Returns the valid `int` or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': [0, type_integer]}
```

#### `type_ranged_number`

Takes a `minimum` and/or `maximum` and returns a type function that accepts an input and validates that it is a number
(`float` or `int`) that is within the specified range. If `#!py None` is provided for either `minimum` or `maximum`,
they will be unbounded.

Returns the valid number (`float` or `int`) or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': [0.0, type_ranged_number(0.0, 100.0)]}
```

#### `type_ranged_integer`

Takes a `minimum` and/or `maximum` and returns a type function that accepts an input and validates that it is an `int`
that is within the specified range. If `#!py None` is provided for either `minimum` or `maximum`, they will be
unbounded.

Returns the valid `int` or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': [0, type_ranged_integer(0, 100)]}
```

#### `type_html_tag`

Takes a YAML input and validates that it is a `str` and that the string is a valid HTML tag.

Returns the valid `str` or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': ['div', type_html_tag]}
```

#### `type_boolean`

Takes a YAML input and validates that it is a boolean value.

Returns the valid boolean or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': [False, type_boolean]}
```

#### `type_ternary`

Takes a YAML input and validates that it is a `bool` value or `#!py None`.

Returns the valid `bool` or `#!py3 None` or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': [None, type_ternary]}
```

#### `type_string`

Takes a YAML input and validates that it is a `str` value.

Returns the valid `str` or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': ['default', type_string]}
```

#### `type_insensitive_string`

Takes a YAML input and validates that it is a `str` value and normalizes it by lower casing it.

Returns the valid, lowercase `str` or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': ['default', type_insensitive_string]}
```

#### `type_string`

Takes a YAML input and validates that it is a `str` value.

Returns the valid `str` or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': ['default', type_string]}
```

#### `type_string_in`

Takes a list of acceptable string inputs and a string type callback and returns a type function that takes an input,
runs it through the string type callback, and then validates that the `str` value is found in the acceptable string
list.

Returns the valid `str` or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': ['this', type_string_in(['this', 'that'], type_insensitive_string)]}
```

#### `type_string_delimiter`

Takes a delimiter and string type callback and returns a function that takes an input, verifies that it is a `str`,
splits it by the delimiter, and ensures that each part validates with the given string type callback.

Returns a list of valid `str` values or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': ['default', type_string_delimiter(',' type_insensitive_string)]}
```

#### `type_html_attribute_name`

Takes a YAML input value and verifies that it is a `str` and formats the name to be a valid HTML attribute.

Returns a `str` that is a valid HTML attribute name or raises `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': ['default', type_html_attribute_name]}
```

#### `type_html_attribute_value`

Takes a YAML input value and verifies that it is a `str` and formats the value to be a suitable, HTML attribute value by
escaping any quotes with `&quot;`.

Returns a `str` that is a valid HTML attribute value or raises `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': ['default', type_html_attribute_value]}
```

#### `type_html_attribute_dict`

Takes a YAML input value and verifies that it is a `dict[str, str]` and formats the keywords to be valid HTML attribute
names and formats the values to valid HTML attribute values.

Returns a `dict[str, str]` that contains valid HTML attribute names and values or raises `ValueError`.

!!! note
    The provided dictionary input will be safely copied such that the default will not be modified.

```py
class Block:
    OPTIONS = {'keyword': [{}, type_html_attribute_dict]}
```

#### `type_html_class`

Essentially an alias for `type_html_attribute_value` that is intended to be used to validate `str` values as HTML
classes.

Returns a `str` that is a valid CSS class or raises `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': ['default', type_html_class]}
```

#### `type_html_classes`

Takes a YAML input value and verifies that it is a `str` and treats it as a space delimited input. The input will
be split by spaces and each part will be run through `type_html_class`.

Returns a list of `str` that are valid CSS classes or raises `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': ['default', type_html_classes]}
```
