# Blocks Extension API

## Block Structure

The various different block types are created via the `Block` class. The `Block` class can define all the various parts
and handling of the various block parts. The basic structure of a block is shown below:

```
/// name | argument
    options: per block options

Markdown content.
///
```

## Block Extension Anatomy

Normally with Python Markdown, you'd create a processor derived from the various processor types available in the
library. You'd then derive an extension from `markdown.Extension` that would register the the processor. Block
extensions are very similar.

A Block extension is comprised of two parts: the `Block` object and the `BlocksExtension`. It should be noted that we do
not use `markdown.Extension`, but `BlocksExtension` which is derived from it. This is done so we can abstract away the
management of all the various registered `Block` extensions. It is important to note though that when using the
`BlocksExtension` that we do not override the `extendMarkdown` method, but instead override `extendMarkdownBlocks`. In
all other respects, `BlocksExtension` is just like `markdown.Extension` and you can register traditional processors via
the `md` object or register `Block` objects via the `block_mgr` object.

Below we have the very bare minimum required to create an extension.

```py
from pymdownx.blocks import BlocksExtension
from pymdownx.blocks.block import Block
import xml.etree.ElementTree as etree

class MyBlock(Block):
    NAME = 'my-block'

    def on_create(self, parent):

        return etree.SubElement(parent, 'div')


class MyBlockExtension(BlocksExtension):

    def extendMarkdownBlocks(self, md, block_mgr):

        block_mgr.register(MyBlock, self.getConfigs())


def makeExtension(*args, **kwargs):
    """Return extension."""

    return MyBlockExtension(*args, **kwargs)
```

Then we can register and run it:

```py
import markdown

MD = """
/// my-block
content
///
"""

print(markdown.markdown(MD, extensions=[MyBlockExtension()]))
```

/// html | div.result
```html
<div>
<p>content</p>
</div>
```
///

## The Block Object

The block object allows us to define the name of a block, whether an argument and/or options are allowed, and how we
generally handle the content.

## Global Options

Global options are often set in the `BlocksExtension` object like traditional extensions. They are meant to globally
control the behavior of a specific block type:

```python
class AdmonitionExtension(BlocksExtension):
    """Admonition Blocks Extension."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            "types": [
                ['note', 'attention', 'caution', 'danger', 'error', 'tip', 'hint', 'warning'],
                "Generate Admonition block extensions for the given types."
            ]
        }

        super().__init__(*args, **kwargs)
```

These options are available in the instantiated `Block` object via the `self.config` attribute.

## Tracking Data Across Blocks

There are times when it can be useful to store data across multiple blocks. Each block instance has access to a tracker
that is specific to a specific block type and persists across all blocks. It is only cleared when `reset` is called on
the `Markdown` object.

The tracker is accessed by a given `Block` extension via the `self.tracker` attribute. The attribute contains a
dictionary where various keys and values can be stored. This can be used to count blocks on a page or anything else you
can think of.

## Accessing the Markdown Object

Some plugins occasionally need access to the current Markdown object. If this is needed, it can be accessed via the
class attribute `self.md`.

## Argument

The argument is used to declare a common block specific input for a particular block type. This is often, but not
exclusively, used for things like titles. It is specified on the same line as the initial block deceleration.

Blocks are not required to use an argument and it is not required by default and must be declared as either optional or
required in order for the block to accept an argument. An argument is declared by setting `ARGUMENT` to `#!py True` if
it is required, `#!py None` if it is optionally allowed, or `#!py False` if it is not allowed.

The argument is always parsed as a single string, if it is desired to validate the format of the argument or even to
process it as multiple arguments, this can be done in the [`on_validate` event](#on_validate-event).

```python
class MyBlock(Block):
    # Name used for the block
    NAME = 'my-block'
    ARGUMENT = True
```

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

/// warning
`attrs` is a reserved option that is automatically applied to all `Block` extensions. This should not be overridden.
`attrs` takes a dictionary of `str` keys  and `str` values describing the attributes to apply to the outer element of
the block as returned by the [`on_create`](#on_create-event).

The `attrs` input input is sent through [`type_html_attribute_dict`](#type_html_attribute_dict) and is accessible to
developers via `self.options['attrs']`. The result is a dictionary of key/value pairs where the key is a `#!py3 str` and
the value is a `#!py3 str` (or `#!py3 list[str]` in the special case of `class`).
///

## `is_raw`

```py
def is_raw(self, tag: Element) -> bool:
    ...
```

This method, given a tag will determine if the block should be considered a "raw" tag based on the Blocks extension's
internal logic.

## `is_block`

```py
def is_block(self, tag: Element) -> bool:
    ...
```

This method, given a tag will determine if the block should be considered a "block" tag based on the Blocks extension's
internal logic.


## `html_escape`

```py
def html_escape(self, text: str) -> str:
    ...
```

Takes a string intended for an HTML tag's content and returns it after applying HTML escaping on it. Escapes `&`, `<`,
and `>`.

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

## `on_validate` Event

```py
def on_validate(self, parent: Element) -> bool:
    ...
```

Executed right after the per block argument and option parsing occurs. The argument and options are accessible via
`self.argument` and `self.options`. `parent` is the current parent element.

`on_validate` is a hook meant to allow the developer to invalidate a block if the options, argument, or even the parent
element do not meet some arbitrary criteria. This hook can also be used to make adjustments variables and even do some
initialization of class variables based on the results of specific options, arguments, or even the parent element.

If validation fails, `#!py3 False` should be returned and the block will not be parsed as a generic block.

## `on_create` Event

```py
    def on_create(self, parent: Element) -> Element:
        ...
```

Called when a block is initially found and initialized. The `on_create` method should create the container for the block
under the parent element. Other child elements can be created on the root of the container, but outer element of the
created container should be returned.

## `on_add` Event

```py
def on_add(self, block: Element) -> Element:
    ...
```

When any calls occur to process new content, `on_add` is called. This gives the block a chance to return the element
where the content is desired.

This can be useful if the outer element is not the element where the content should go. Keep in mind that content can
also be rearranged if needed in the [`on_end` event](#on_end-event).

## `on_markdown` Event

```py
def on_markdown(self) -> str:
    """Check how element should be treated by the Markdown parser."""
    ...
```

The `on_markdown` event is used to declare how the content of the block should be handled by the Markdown parser. A
string with one of the following values _must_ be returned. All content is treated as HTML content and is stored under
the [etree][etree] element returned via the [`on_add` event](#on_add-event).

Only during the [`on_end` event](#on_end-event) will all the content be fully accumulated and processed by relevant
block processors, and only during the [`on_inline_end` event](#on_inline_end-event) will both block and inline
processing be completed.

Result\ Value | Description
------------- | -----------
`block`       | Parsed block content will be handled by the Markdown parser as content under a block element.
`inline`      | Parsed block content will be handled by the Markdown parser as content under an inline element.
`raw`         | Parsed block content will be preserved as is. No additional Markdown parsing will be applied. Content is expected to be indented and should be documented as such.
`auto`        | Depending on whether the wrapping parent is a block element, inline element, or something like a code element, Blocks will choose the best approach for the content. Decision is made based on the element returned by the [`on_add` event](#on_add-event).

When using `raw` mode, all text will be accumulated under the specified element as an [`AtomicString`][atomic]. If
nothing is done with the content during the [`on_end` event](#on_end-event), all the content will be HTML escaped by the
Python Markdown parser. If desired, the content can be placed into the Python Markdown [HTML stash][stash] which will
protect it from any other rouge Treeprocessors. Keep in mind, if the content is stashed HTML escaping will not be
applied automatically, so HTML escape if it is required.

/// warning | Indent Raw Content
Because Python Markdown implements HTML processing as a preprocessor, content for a `raw` block must be indented 4
spaces to avoid the HTML processing step. The content will not be indented when it reaches the [`on_end` event](#on_end-event).
Failure to indent will still allow the code to be processed, but it may not process as expected. An extension that uses
`raw` should make clear that this is a requirement to avoid unexpected results.
///

## `on_end` Event

```py
def on_end(self, block: Element) -> None:
    ...
```

When a block is parsed to completion, the `on_end` event is executed. This allows an extension to perform any post
processing on the elements. You could save the data as raw text and then parse it special at the end or you could walk
the HTML elements and move content around, add attributes, or whatever else is needed.

## `on_inline_end` Event

```py
def on_inline_end(self, block: Element) -> None:
    ...
```

When a block is parsed to completion and all inline parsing has been applied, the `on_inline_end` event is executed. It
is the very last event for a block. This allows an extension to perform any post processing on an element _after_ inline
processing.

## Built-in Validators

A number of validators are provided via for the purpose of validating [YAML option inputs](#options). If what you need
is not present, feel free to write your own. All validators are imported from `pymdownx.blocks.block`.

### `type_any`

```py
def type_any(value: Any) -> Any:
    ...
```

This takes a YAML input and simply passes it through. If you do not want to validate the input because it does not need
to be checked, or if you just want to do it manually in the [`on_validate` event](#on_validate-event), then this is what
you'd want to use.

```py
class Block:
    OPTIONS = {'name': [{}, type_any]}
```

### `type_none`

```py
def type_none(value: Any) -> None:
    ...
```

This takes a YAML input and ensures it is `None` (or `null`) in YAML. This is most useful paired with other types to
indicate the option is "unset". See [`type_multi`](#type_multi) to learn how to combine multiple existing types.

```py
class Block:
    OPTIONS = {'name': [none, type_multi(type_none, type_string)]}
```

### `type_number`

```py
def type_number(value: Any) -> int | float:
    ...
```

Takes a YAML input value and verifies that it is a `float` or `int`.

Returns the valid number (`float` or `int`) or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': [0.0, type_number]}
```

### `type_integer`

```py
def type_integer(value: Any) -> int:
    ...
```

Takes a YAML input value and verifies that it is an `int`.

Returns the valid `int` or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': [0, type_integer]}
```

### `type_ranged_number`

```py
def type_ranged_number(minimum: int | float = None, maximum: int | float = None) -> Callable[[Any], int | float]:
```

Takes a `minimum` and/or `maximum` and returns a type function that accepts an input and validates that it is a number
(`float` or `int`) that is within the specified range. If `#!py None` is provided for either `minimum` or `maximum`,
they will be unbounded.

Returns the valid number (`float` or `int`) or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': [0.0, type_ranged_number(0.0, 100.0)]}
```

### `type_ranged_integer`

```py
def type_ranged_integer(minimum: int = None, maximum: int = None) -> Callable[[Any], int]:
    ...
```

Takes a `minimum` and/or `maximum` and returns a type function that accepts an input and validates that it is an `int`
that is within the specified range. If `#!py None` is provided for either `minimum` or `maximum`, they will be
unbounded.

Returns the valid `int` or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': [0, type_ranged_integer(0, 100)]}
```

### `type_boolean`

```py
def type_boolean(value: Any) -> bool:
    ...
```

Takes a YAML input and validates that it is a boolean value.

Returns the valid boolean or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': [False, type_boolean]}
```

### `type_ternary`

```py
def type_ternary(value: Any) -> bool | None:
    ...
```

Takes a YAML input and validates that it is a `bool` value or `#!py None`.

Returns the valid `bool` or `#!py3 None` or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': [None, type_ternary]}
```

### `type_string`

```py
def type_string(value: Any) -> str:
    ...
```

Takes a YAML input and validates that it is a `str` value.

Returns the valid `str` or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': ['default', type_string]}
```

### `type_insensitive_string`

```py
def type_insensitive_string(value: Any) -> str:
    ...
```

Takes a YAML input and validates that it is a `str` value and normalizes it by lower casing it.

Returns the valid, lowercase `str` or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': ['default', type_insensitive_string]}
```

### `type_string_in`

```py
def type_string_in(value: list[str], insensitive: bool = True) -> Callable[[Any], str]:
    ...
```

Takes a list of acceptable string inputs and a boolean indicating whether comparison should be case insensitive. Returns
a type function that takes an input and then validates that it is a `str` and that the `str` value is found in the
acceptable string list.

Returns the valid `str` or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': ['this', type_string_in(['this', 'that'], type_insensitive_string)]}
```

### `type_string_delimiter`

```py
def type_string_delimiter(value: str, string_type: Callable[[Any], str] = type_string) -> str:
    ...
```

Takes a delimiter and string type callback and returns a function that takes an input, verifies that it is a `str`,
splits it by the delimiter, and ensures that each part validates with the given string type callback.

Returns a list of valid `str` values or raises a `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': ['default', type_string_delimiter(',' type_insensitive_string)]}
```

### `type_html_identifier`

```py
def type_html_identifier(value: Any) -> str:
    ...
```

Tests that a string is an "identifier" as described in CSS. This would normally match tag names, IDs, classes, and
attribute names. This is useful if you'd like to validate such HTML constructs.

Returns a `str` that is a valid identifier or raises `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': ['default', type_html_indentifier]}
```

### `type_html_classes`

```py
def type_html_classes(value: Any) -> list[str]:
    ...
```

Takes a YAML input value and verifies that it is a `str` and treats it as a space delimited input. The input will
be split by spaces and each part will be run through `type_html_identifier`.

Returns a list of `str` that are valid CSS classes or raises `ValueError`.

```py
class Block:
    OPTIONS = {'keyword': ['default', type_html_classes]}
```

### `type_html_attribute_dict`

```py
def type_html_classes(value: Any) -> dict[str, Any]:
    ...
```

/// note
The returned dictionary will have all values set to string except classes which will be a list of strings. The `class`
attribute is processed with `type_html_classes`.

The `id` attribute is also run through `type_html_identifier` to ensure a good ID that can be targeted with traditional
CSS selectors: `#!py3 #id`.
///

Takes a YAML input value and verifies that it is a `dict`. Keys will be verified to be HTML identifiers and the values
to be strings.

Returns a `dict[str, Any]` where the values will either be `str` or `list[str]` as previously noted or raises
`ValueError`.

```py
class Block:
    OPTIONS = {'attributes': [{}, type_html_attribute_dict]}
```

## `type_multi`

```py
def type_multi(*args: Any) -> Callable[[Any], Any]:
    ...
```

Takes a multiple type functions and returns a single type function that takes a YAML input and validates it with all the
provided type functions. If the input fails all the validation functions, a `ValueError` is raised.
