# Blocks Plugin API

## Block Structure

The various different block types are created via `Block` plugins. The basic structure of a block is shown below:

```
/// name | argument(s)
    options: per block options

Markdown content.
///
```

In addition, there are sometimes global options for a specific block type are supplied at registration time. Such
options would control features for the specific block type they are defined for and would affect all the blocks of that
type globally.

## Creating a Plugin

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
            'blocks': {MyBlock: None}
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

## Arguments

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

/// tip | Validating Arguments
If you'd like to validate arguments, you can utilize the [`on_parse` event](#on_parse-event). It is also acceptable
manually parse arguments in the `on_parse` event as well. This may be useful if the arguments cannot be parsed with
a simple delimiter.
///

## Options

Options is how a block specifies any per block features via an indented YAML block immediately after the block
declaration. The YAML indented block is considered a part of the header and is great for options that don't make sense
as part of the first line declaration.

An option consists of a keyword to specify the option name, and then a list containing the default value and a validator
callback. The callback function should take the input and validate the type and/or coerce the value to an appropriate
value. If the input, for whatever reason, is deemed invalid, the callback function should raise an error.

After processing, all options will be available as a dictionary via the instance attribute `self.options`. Options
will be accessible via the keyword and will return the resolved value.

/// tip | Built-in validators
A number of Built-in validators are provided. Check out [Built-in Validators](#built-in-validators) to learn more,
or feel free to write your own.
///

```py
class MyBlock(Block):
    # Name used for the block
    NAME = 'my-block'
    OPTIONS = {
        'tag_name': ['default', type_html_indentifier]
    }
```

## Global Config

It may be desirable to have global options. These kind of options affect all blocks and are not configured per block.

Configs are created using the `CONFIG` attribute and should contain a dictionary with default values. It is up to the
plugin creator to validate options as no mechanism is provided at this time to validate global configs. It is recommend
that global options be processed in the [`on_init` event](#on_init-event).

```py
class MyBlock(Block):
    # Name used for the block
    NAME = 'my-block'
    CONFIG = {
        'enable_feature': False
    }
```

## Tracking Data Across Blocks

There are times when it can be useful to store data across multiple blocks. Each block instance has access to a tracker
that is specific to a specific block type and persists across all blocks. It is only cleared when `reset` is called
on the block manager and will reset trackers of all registered blocks.

The tracker is accessed by a given `Block` plugin via the `self.tracker` attribute. The attribute contains a dictionary
where various keys and values can be stored. This can be used to count blocks on a page or anything else you can think
of.

## `on_register` Event

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

## `on_init` Event

```py
def on_init(self) -> None:
    ...
```

The `on_init` event is run every time a new block class is instantiated. This is usually where a specific block type
would handle global options and initialize class variables that are needed. If the specified block name in Markdown
matches the name of a registered block, that block class will be instantiated, triggering the `on_init` event to
execute. Each block in a document that is encountered generates its own, new instance.

Only the global `config` is available at this time via `self.config`. The `Markdown` object is also available via
`self.md`.

The can be a good way to perform setup based on on global or local options.

## `on_parse` Event

```py
def on_parse(self) -> bool:
    ...
```

Executed right after per block argument and option parsing occurs. Arguments and options are accessible via `self.args`
and `self.options`. This gives the plugin a chance to perform additional validation or adjustments of the arguments and
options. This also gives the opportunity to initialize class variables based on the per block arguments and options.

If validation fails, `#!py3 False` should be returned and the block will not be parsed as a generic block.

## `on_create` Event

```py
    def on_create(self, parent: Element) -> None:
        ...
```

Called when a block is initially found and initialized. The `on_create` method should create the container for the block
under the parent element.

## `on_add` Event

```py
def on_add(self, block: Element) -> Element:
    ...
```

When any calls occur to process new content, `on_add` is called. This gives the block a chance to return the element
where the content is desired.

Some initial containers may be more complex and have nested elements already created. `on_add` helps ensure that the
content goes where it is actually desired in the container.

## `on_markdown` Event

```py
def on_markdown(self) -> str:
    """Check how element should be treated by the Markdown parser."""
    ...
```

The `on_markdown` event is used to declare how the content of the block should be handled by the Markdown parser. A
string with one of the following values _must_ be returned. 

Result\ Value | Description
------------- | -----------
`block`       | Parsed block content will be handled by the Markdown parser as content under a block element.
`inline`      | Parsed block content will be handled by the Markdown parser as content under an inline element.
`raw`         | Parsed block content will be preserved as is. No additional Markdown parsing will be applied.
`auto`        | Depending on whether the wrapping parent is a block element, inline element, or something like a code element, Blocks will choose the best approach for the content. Decision is made based on the element returned by the [`on_add` event](#on_add-event).

## `on_end` Event

```py
def on_end(self, block: Element) -> None:
    ...
```

When a block is parsed to completion, the `on_end` event is executed. This allows a plugin to perform any post
processing on the elements. You could save the data as raw text and then parse it special at the end or you could walk
the HTML elements and move content around, add attributes, or whatever else is needed.

## Built-in Validators

A number of validators are provided via for the purpose of validating [YAML option inputs](#options). If what you need
is not present, feel free to write your own.


### `type_number`

Takes a YAML input value and verifies that it is a `float` or `int`.

Returns the valid number (`float` or `int`) or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': [0.0, type_number]}
```

### `type_integer`

Takes a YAML input value and verifies that it is an `int`.

Returns the valid `int` or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': [0, type_integer]}
```

### `type_ranged_number`

Takes a `minimum` and/or `maximum` and returns a type function that accepts an input and validates that it is a number
(`float` or `int`) that is within the specified range. If `#!py None` is provided for either `minimum` or `maximum`,
they will be unbounded.

Returns the valid number (`float` or `int`) or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': [0.0, type_ranged_number(0.0, 100.0)]}
```

### `type_ranged_integer`

Takes a `minimum` and/or `maximum` and returns a type function that accepts an input and validates that it is an `int`
that is within the specified range. If `#!py None` is provided for either `minimum` or `maximum`, they will be
unbounded.

Returns the valid `int` or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': [0, type_ranged_integer(0, 100)]}
```

### `type_boolean`

Takes a YAML input and validates that it is a boolean value.

Returns the valid boolean or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': [False, type_boolean]}
```

### `type_ternary`

Takes a YAML input and validates that it is a `bool` value or `#!py None`.

Returns the valid `bool` or `#!py3 None` or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': [None, type_ternary]}
```

### `type_string`

Takes a YAML input and validates that it is a `str` value.

Returns the valid `str` or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': ['default', type_string]}
```

### `type_insensitive_string`

Takes a YAML input and validates that it is a `str` value and normalizes it by lower casing it.

Returns the valid, lowercase `str` or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': ['default', type_insensitive_string]}
```

### `type_string_in`

Takes a list of acceptable string inputs and a string type callback and returns a type function that takes an input,
runs it through the string type callback, and then validates that the `str` value is found in the acceptable string
list.

Returns the valid `str` or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': ['this', type_string_in(['this', 'that'], type_insensitive_string)]}
```

### `type_string_delimiter`

Takes a delimiter and string type callback and returns a function that takes an input, verifies that it is a `str`,
splits it by the delimiter, and ensures that each part validates with the given string type callback.

Returns a list of valid `str` values or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': ['default', type_string_delimiter(',' type_insensitive_string)]}
```

### `type_html_identifier`

Tests that a string is an "identifier" as described in CSS. This would normally match tag names, IDs, classes, and
attribute names. This is useful if you'd like to validate such HTML constructs.

Returns a `str` that is a valid identifier or raises `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': ['default', type_html_indentifier]}
```

### `type_html_classes`

Takes a YAML input value and verifies that it is a `str` and treats it as a space delimited input. The input will
be split by spaces and each part will be run through `type_html_identifier`.

Returns a list of `str` that are valid CSS classes or raises `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': ['default', type_html_classes]}
```

### `type_html_attribute_dict`

Takes a YAML input value and verifies that it is a `dict`. Keys will be verified to be HTML identifiers and the values
to be strings.

Returns a `dict[str, str]` or raises `ValueError`.

```py
class Block:
    OPTIONS = {'attributes': [{}, type_html_attribute_dict]}
```
