path: tree/master
source: pymdownx/superfences.py

# SuperFences

## Overview

SuperFences provides a number of features:

1. Allowing the [nesting of fences](#nested-fence-format) under blockquotes, lists, or other block elements (see
  [Limitations](#limitations) for more info).
2. Create [tabbed fenced code blocks](#tabbed-fences).
3. Ability to specify [custom fences](#custom-fences) to provide features like flowcharts, sequence diagrams, or other
  custom blocks.
4. Allow disabling of indented code blocks in favor of only using the fenced variant (off by default).
5. Experimental feature that preserves tabs within a code block instead of converting them to spaces which is Python
  Markdown's default behavior.

!!! danger "Reminder"
    Remember to read the [Usage Notes](../usage_notes.md) for information that may be relevant when using this
    extension!

The SuperFences extension can be included in Python Markdown by using the following:

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.superfences'])
```

## Nested Fence Format

1. Start and end fence boundaries are specified with either 3 or more backticks or tildes.

2. Start and end fence boundaries must both use matching symbols (backticks or tildes) and must be of the same number of
  symbols.  If start is 3 backticks, the fence will end with 3 backticks.

3. Start and end fence boundaries must be aligned to the same indentation level.

4. Content between fences must be indented at least the same amount as the start and end boundaries.  Empty lines are
  exempted.

5. If you are using a fenced block inside a blockquote, at the very least, the first line of the fenced block needs to
  have the appropriate number of `>` characters signifying the quote depth.

    ````
    > ```
      a fenced block
      ```
    ````

6. Too many blank lines will cause a blockquote to terminate, so remember to use `>` markers accordingly if not marking
  every line.

    ````
    > ```
      a fenced block

    > with blank lines
      ```
    ````

7. If using a fenced block as the first line of a list, you will have to leave the first line blank, but remember that
  the list marker must be followed by a space.

    ````
    -<space>
        ```
        a fenced block
        ```

    Definition
    :<space>
        ```
        a fenced block
        ```
    ````

8. Fenced blocks should be separated from other blocks by an empty line.

    ````
    Paragraph.

    ```
    a fenced block
    ```

    Another paragraph.
    ````

## Injecting Classes and IDs

You can use the attribute list format to specify classes and IDs (IDs are only injectable in non-Pygments code blocks).
The first provided class is always used as the language class. Arbitrary attributes in the form `key="value"` cannot
be inserted as those are reserved for options such has `linenums` etc.

!!! example "Injecting Classes"

    === "HTML"
        ```html
        <table class="extra-class highlighttable"><tr><td class="linenos"><div class="linenodiv"><pre><span></span>1</pre></div></td><td class="code"><div class="extra-class highlight"><pre><span></span><code><span cv></td><td class="code"><div class="extra-class highlight"><pre><span></span><code><span class="kn">import</span> <spanlass="kn">import</span> <span class="nn">hello_world</span>\n</code></pre></div>\n</td></tr></table>
        ```

    === "Markdown"
        ````
        ```{.python .extra-class linenums="1"}
        import hello_world
        ```
        ````

When generating additional classes on a JavaScript style code block (non-Pygments code blocks), classes are injected in
the `#!html code` block.

!!! example "Non-Pygments Injecting Classes"

    === "HTML"
        ```html
        <pre id="id" class="highlight"><code class="extra-class language-python linenums">import hello_world</code></pre>
        ```

    === "Markdown"
        ````
        ```{.python .extra-class #id linenums="1"}
        import hello_world
        ```
        ````

When using a built in [custom formatter](#custom-fences), all classes and IDs are injected on to the first element
`#!html <div>` or `#!html <pre>`. This preserves previous behavior, but you can write your own and inject them in the
way that suites your needs.

## Tabbed Fences

!!! warning "Deprecated 7.0"
    The tab option is deprecated in 7.0 due to the addition of the general purpose tab extension
    [`pymdownx.tabbed`](./tabbed.md). This feature will be removed in 8.0, and at that time, users will be required to
    use [`pymdownx.tabbed`](./tabbed.md) if they would like to have tabbed code blocks.

    The feature is still usable, but the class names on the output have changed from `superfences-tabs` and
    `superfences-content` to `tabbed-set` and `tabbed-content` respectively. This is to help create unity between the
    new extension and this feature as we guide people towards the new extension.

    To use the legacy class names, you can use the global `legacy_tab_classes` option to get the old style classes. This
    option will be removed, along with the entire `tab=""` feature in 8.0.

SuperFences has the ability to create tabbed code blocks.  Simply add `tab="tab-title"` to the fence's header, and the
code block will will be rendered in a tab with the title `tab-title`.  If you do not provide a title with either `tab=`
or `tab=""`, but you've specified a language, the language will be used as the title. No case transformation is applied
-- what you type is what you get. Consecutive code tabs will be grouped together.

!!! example "Tabbed Code"

    === "Output"
        ```Bash tab=
        #!/bin/bash
        STR="Hello World!"
        echo $STR
        ```

        ```C tab=
        #include 

        int main(void) {
          printf("hello, world\n");
        }
        ```

        ```C++ tab=
        #include <iostream>

        int main() {
          std::cout << "Hello, world!\n";
          return 0;
        }
        ```

        ```C# tab=
        using System;

        class Program {
          static void Main(string[] args) {
            Console.WriteLine("Hello, world!");
          }
        }
        ```

    === "Markdown"

        ````
        ```Bash tab=
        #!/bin/bash
        STR="Hello World!"
        echo $STR
        ```

        ```C tab=
        #include 

        int main(void) {
          printf("hello, world\n");
        }
        ```

        ```C++ tab=
        #include <iostream>

        int main() {
          std::cout << "Hello, world!\n";
          return 0;
        }
        ```

        ```C# tab=
        using System;

        class Program {
          static void Main(string[] args) {
            Console.WriteLine("Hello, world!");
          }
        }
        ```
        ````

In order to use tabbed code blocks, some additional CSS is needed. You can check out the configuration below which will
show the CSS and the HTML it targets. Keep in mind the CSS is just the minimum to get you started. You can tweak it and
modify it to get it how you like it.

??? settings "Tabbed Code Setup"
    === "HTML"
        ```HTML
        <div class="tabbed-set">
        <input name="__tabbed_1" type="radio" id="__tabbed_1_1" checked="checked">
        <label for="__tabbed_1_1">Tab 0</label>
        <div class="tabbed-content">...</div>
        ...
        <input name="__tabbed_1" type="radio" id="__tabbed_1_X" checked="checked">
        <label for="__tabbed_1_X">Tab X</label>
        <div class="tabbed-content">...</div>
        ...
        </div>
        ```

    === "CSS"
        ```CSS
        .tabbed-set {
          display: flex;
          position: relative;
          flex-wrap: wrap;
        }

        .tabbed-set .highlight {
          background: #ddd;
        }

        .tabbed-set .tabbed-content {
          display: none;
          order: 99;
          width: 100%;
        }

        .tabbed-set label {
          width: auto;
          margin: 0 0.5em;
          padding: 0.25em;
          font-size: 120%;
          cursor: pointer;
        }

        .tabbed-set input {
          position: absolute;
          opacity: 0;
        }

        .tabbed-set input:nth-child(n+1) {
          color: #333333;
        }

        .tabbed-set input:nth-child(n+1):checked + label {
            color: #FF5252;
        }

        .tabbed-set input:nth-child(n+1):checked + label + .tabbed-content {
            display: block;
        }
        ```

## Preserve Tabs

Python Markdown has an approach where it normalizes whitespace. This means `\r\n` is converted to `\n` and `\t` is
converted to spaces. In 99% of Markdown, this is never really an issue, but with code blocks it can be. Tabs can
sometimes be very useful for aligning certain kinds of data, especially when dealing with characters of varying width.

!!! example "Tabs in Content"

    === "Output"
        ```
        ============================================================
        T	Tp	Sp	D	Dp	S	D7	T
        ------------------------------------------------------------
        A	F#m	Bm	E	C#m	D	E7	A
        A#	Gm	Cm	F	Dm	D#	F7	A#
        B♭	Gm	Cm	F	Dm	E♭m	F7	B♭
        ```

    === "Markdown"
        ````
        ```
        ============================================================
        T	Tp	Sp	D	Dp	S	D7	T
        ------------------------------------------------------------
        A	F#m	Bm	E	C#m	D	E7	A
        A#	Gm	Cm	F	Dm	D#	F7	A#
        B♭	Gm	Cm	F	Dm	E♭m	F7	B♭
        ```
        ````

If you have a scenario where preserving tabs is a requirement, you can use SuperFences `preserve_tabs` option to prevent
converting tabs to spaces inside fenced code blocks. This *only* applies to fenced code blocks. Indented code blocks and
inline code blocks will still be treated with Python Markdown's default behavior.

This feature is experimental and actually applies the fences before whitespace normalization and bypasses the
normalization for the code content.

## Code Highlighting

Assuming Pygments is installed, code highlighting will be handled by [Pygments][pygments] by default. If Pygments is not
installed, or disabled, code blocks will be created using HTML5 style tags for a JavaScript syntax highlighter:
`#!html <pre class="highlight"><code class="language-mylanguage"></code></pre>`. If you disable `highlight_code`,
specified languages will be ignored, and the content will be wrapped in a simple `pre` and `code` tags with no classes.

Highlighting can be further controlled via the [`pymdownx.highlight`](./highlight.md) extension.

When using fenced code blocks, you can specify a specific syntax language to highlight with by specifying the language
name directly after the opening tokens (either ` ``` ` or `~~~`). Whether using Pygments or some other JavaScript
highlighter, the syntax is the same, but please consult your highlighter's documentation for recognized language syntax
specifiers.

!!! example "Highlight Example"

    === "Output"
        ```py3
        import foo.bar
        ```

    === "Markdown"
        ````
        ```py3
        import foo.bar
        ```
        ````

## Showing Line Numbers

Line numbers are provided via Pygments and can either be shown per code block or globally for all. To show globally via
[`pymdownx.highlight`](./highlight.md), you must set `linenums` to `#!py3 True` in the respective extension.

To set line numbers per code block, you can specify a special setting directly after the opening tokens (and language if
present). Simply specify the starting line line number with option `linenums="1"`. The setting is followed by the equal
sign and the value must be quoted.  Valid line numbers are n > 0.  If `linenums` is enabled globally, this will just
control the starting line shown in the block.

!!! example "Line Number Example"

    === "Output"
        ``` linenums="1"
        import foo.bar
        ```

    === "Markdown"
        ````
        ``` linenums="1"
        import foo.bar
        ```
        ````

Pygments also has a few additional options in regards to line numbers. One is "line step" which, if set to a number n >
1, will print only every n^th^ line number. The other option is a setting that can mark line numbers as "special" with a
span and class `special`. If the special parameter is set to a number n > 0, every n^th^ line number is given the CSS
class `special`.

So to set showing only every other line number, we could do the following. Line options are separated by a space, and
"line step" is always the second option, so you must specify line start before line step.

!!! example "Nth Line Example"

    === "Output"
        ``` linenums="2 2"
        """Some file."""
        import foo.bar
        import boo.baz
        import foo.bar.baz
        ```

    === "Markdown"
        ````
        ``` linenums="2 2"
        """Some file."""
        import foo.bar
        import boo.baz
        import foo.bar.baz
        ```
        ````

To set every other line as special, you must set the third `linenums` option (specify line start and step before it).
Special must be a value of n > 0.

!!! example "Special Line Example"

    === "Output"
        ``` linenums="1 1 2"
        """Some file."""
        import foo.bar
        import boo.baz
        import foo.bar.baz
        ```

    === "Markdown"
        ````
        ``` linenums="1 1 2"
        """Some file."""
        import foo.bar
        import boo.baz
        import foo.bar.baz
        ```
        ````

For JavaScript libraries, a class of `linenums` is written to the block.  This may or may not be leveraged by your
chosen highlighter.  It is uncertain at this time whether line number support for JavaScript highlighters will be
enhanced beyond this.w what to inject.

## Highlighting Lines

Via Pygments, certain lines can be specified for highlighting.  This is done by specifying a special setting directly
after the opening tokens (and language if present).  The setting is named `hl_lines` and the value should be the
targeted line numbers separated by spaces.

!!! example "Highlight Lines Example"

    === "Output"
        ```py3 hl_lines="1 3"
        """Some file."""
        import foo.bar
        import boo.baz
        import foo.bar.baz
        ```

    === "Markdown"
        ````
        ```py3 hl_lines="1 3"
        """Some file."""
        import foo.bar
        import boo.baz
        import foo.bar.baz
        ```
        ````

Line numbers are always referenced starting at 1 ignoring what the line number is labeled as when showing line numbers.

!!! example "Highlight Lines with Line Numbers Example"

    === "Output"
        ```py3 hl_lines="1 3" linenums="2"
        """Some file."""
        import foo.bar
        import boo.baz
        import foo.bar.baz
        ```

    === "Markdown"
        ````
        ```py3 hl_lines="1 3" linenums="2"
        """Some file."""
        import foo.bar
        import boo.baz
        import foo.bar.baz
        ```
        ````

If you'd like to do a range of lines, you can use the notation `x-y` where `x` is the starting line and `y` is the
ending line. You can do multiple ranges and even mix them with non ranges.

!!! example "Highlight Ranges"

    === "Output"
        ```py3 hl_lines="1-2 5 7-8"
        import foo
        import boo.baz
        import foo.bar.baz

        class Foo:
           def __init__(self):
               self.foo = None
               self.bar = None
               self.baz = None
        ```

    === "Markdown"
        ````
        ```py3 hl_lines="1-2 5 7-8"
        import foo
        import boo.baz
        import foo.bar.baz

        class Foo:
           def __init__(self):
               self.foo = None
               self.bar = None
               self.baz = None
        ```
        ````

## Custom Fences

SuperFences allows defining custom fences for special purposes, like flow charts and sequence diagrams:

!!! example "Flow Chart Example"

    === "Output"
        ```mermaid
        graph TD
            A[Hard] -->|Text| B(Round)
            B --> C{Decision}
            C -->|One| D[Result 1]
            C -->|Two| E[Result 2]
        ```

    === "Markdown"
        ````
        ```mermaid
        graph TD
            A[Hard] -->|Text| B(Round)
            B --> C{Decision}
            C -->|One| D[Result 1]
            C -->|Two| E[Result 2]
        ```
        ````

!!! example "Sequence Diagram Example"

    === "Output"
        ```mermaid
        sequenceDiagram
            participant Alice
            participant Bob
            Alice->>John: Hello John, how are you?
            loop Healthcheck
                John->>John: Fight against hypochondria
            end
            Note right of John: Rational thoughts <br/>prevail!
            John-->>Alice: Great!
            John->>Bob: How about you?
            Bob-->>John: Jolly good!
        ```

    === "Markdown"
        ````
        ```mermaid
        sequenceDiagram
            participant Alice
            participant Bob
            Alice->>John: Hello John, how are you?
            loop Healthcheck
                John->>John: Fight against hypochondria
            end
            Note right of John: Rational thoughts <br/>prevail!
            John-->>Alice: Great!
            John->>Bob: How about you?
            Bob-->>John: Jolly good!
        ```
        ````

In the above example, we have set up a custom fence called `mermaid` which allows us to process special charts with
[Mermaid][mermaid]. In this case, our special fence preserves the content and sends them to a an element so that
[Mermaid][mermaid] can then find them and convert them when the document is loaded. To learn more see [UML Diagram
Example](#uml-diagram-example).

Custom fences are created via the `custom_fences` option.  `custom_fences` takes an array of dictionaries where each
dictionary defines a custom fence. The dictionaries require the following keys:

Keys        | Description
----------- | -----------
`name`      | The language name that is specified when using the fence in Markdown. If given `*`, it will override the base fence logic, the default for all fence names not handled by other custom fences.
`class`     | The class name assigned to the HTML element when converting from Markdown to HTML.
`format`    | A function that formats the HTML output. The function should return a string as HTML.
`validator` | An optional parameter that is used to provide a function to validate custom fence parameters.

!!! new "New in 7.0"
    Starting in 7.0, you can override the base fence logic (the syntax highlighter) by specifying the custom fence
    with a name of `*`. This means that if a fence does not match any other custom fences, the default, fallback fence
    would be handled by your custom `*` fence. This can be useful for tailoring a fence output with custom parameters
    for a specific, favorite JavaScript highlighter.

### Formatters

SuperFences provides two format functions by default, but you can always write your own:

Format\ Function                | Description
------------------------------- | -----------
`superfences.fence_code_format` | Places the HTML escaped content of the fence under a `#!html <pre><code>` block.
`superfences.fence_div_format`  | Places the HTML escaped content of the fence under a `#!html <div>` block.

In general, formatters take five parameters: the source found between the fences, the specified language, the class name
originally defined via the `class` option in the `custom_fence` entry, custom options, and the Markdown object (in case
you want access to meta data etc.).

```py3
def custom_formatter(source, language, css_class, options, md, classes=None, id_value='', **kwargs):
    return string
```

!!! new "New 7.0"
    The addition of the parameters `classes` and `id_value` is new in 7.0. If injecting additional classes or ids via
    the [attribute list style](#injecting-classes-and-ids), only then will `classes` and `id_value` be passed in to
    preserve backwards compatibility with old custom formatters. Users, moving forward, should at the very least update
    their formatters with `**kwargs` to future proof their custom formatters in case additional parameters are added
    in the future.

All formatters should return a string as HTML.

!!! tip
    If you are attempting to configure these options in a YAML based configuration (like in [MkDocs][mkdocs]), please
    see the [FAQ](../faq.md#function-references-in-yaml) to see how to specify function references in YAML.

### Validators

The `validator` is used to provide functions that accept or reject provided fence options. The validator is sent two
parameters: the language defined in the fence, and a dictionary of options to validate.

Custom options can be used as keys with quoted values (`key="value"`), or as keys with no value which are used more as a
boolean (`key=`). SuperFences will parse the options in the fence and then pass them to the validator. If the validator
returns true, the options will be accepted and later passed to the formatter.

This custom fence:

````
```custom_fence custom_option="value" other_custom_option=
content
```
````

Would yield this option dictionary:

```py3
{
    "custom_option": "value",
    "other_custom_option": True
}
```

For a contrived example: if we wanted to define a custom fence named `test` that accepts an option `opt` that can only
be assigned a value of `A`, we would write the following validator:

```py3
def custom_validator(language, options):
    """Custom validator."""

    okay = True
    for k in options.keys():
        if k != 'opt':
            okay = False
            break
    if okay:
        if options['opt'] != "A":
            okay = False
    return okay
```

Then later the formatter would be given the options:

```py3
def custom_format(source, language, class_name, options, md):
    """Custom format."""

    return '<div class_name="%s %s", data-option="%s">%s</div>' % (language, class_name, options['opt'], html_escape(source))
```

This would allow us to use the following custom fence:

````
```test opt="A"
test
```
````

!!! tip
    If you are attempting to configure these options in a YAML based configuration (like in [MkDocs][mkdocs]), please
    see the [FAQ](../faq.md#function-references-in-yaml) to see how to specify function references in YAML.

### UML Diagram Example

This example illustrates how you can use the `custom_fences` option to do UML diagrams with [Mermaid][mermaid]. The
settings below show us creating a new custom fence called `mermaid`. The special fence is set under the `custom_fences`
[option](#options).

The `mermaid` fences will pass the content through the `superfences.fence_div_format` format function which will wrap
the content in `#!html <div>` blocks and attach the class `mermaid` to the `#!html <div>` block.

```py3
extension_configs = {
    "pymdownx.superfences": {
        "custom_fences": [
            {
                'name': 'mermaid',
                'class': 'mermaid',
                'format': pymdownx.superfences.fence_div_format
            }
        ]
    }
}
```

The format function we used in this example only escapes the content to be included in HTML. We will rely on the
[Mermaid][mermaid] JavaScript library to render our flowcharts/diagrams in the browser. [Mermaid][mermaid], on load,
will automatically find the `#!html <div>` elements with the `mermaid` class and render them. We can include
[Mermaid][mermaid] via its CDN.

```html
<script src="https://unpkg.com/mermaid@8.4.8/dist/mermaid.min.js"></script>
```

!!! warning "Support"
    Please reference [Mermaid's][mermaid] documents for more information in configuring features. PyMdown Extensions
    does not offer direct support for issues you may have in using [Mermaid][mermaid], feel free to use their issue
    tracker to report problems with their library.

!!! tip "Custom Loading"

    We've found that Mermaid diagrams that are found in tabbed interfaces or details, where the element may be hidden
    on page load, don't always render at a visible size if using Mermaids default loader. We've opted to create our own.

    We also render ours in `#!html <pre><code>` tags. This allows for the cases were something goes wrong and the
    diagrams don't get rendered, we can still show the source as code blocks.

    Our custom loader also adjusts for quirks and ensuring good typesetting for our document environment. All of this
    can be viewed in the source.

    - [Loader][mermaid-loader].
    - [Mermaid configuration settings][mermaid-config]. Note that we turn off themes so that we can use our own, remove
      the `theme` option, or set your favorite.

    This is just for reference.

## Limitations

This extension suffers from some of the same quirks that the original fenced block extension suffers from.  Normally
Python Markdown does not parse content inside HTML tags unless they are marked with the attribute `markdown='1'`.  But
since this is run as a preprocessor, it is not aware of the HTML blocks.

SuperFences is made to work with the default extensions out of the box.  It will probably not work with other extensions
such as Grid Tables, since that extension allows for characters to obscure the blocks like the blockquote syntax does
(though this has been designed to work with blockquotes).  Ideally fenced blocks need to be handled by a block parser,
but there is much work to be done on Python Markdown's internal block handlers before this is possible.

SuperFences works best when following the guidelines.  If the guidelines are not followed, odd results may be
encountered.

For the reasons above, the nested fences feature really is just a workaround.  But for a lot of people, this
functionality is more than sufficient.

## Options

Option                         | Type         | Default       | Description
------------------------------ | ------------ | ------------- | -----------
`css_class`                    | string       | `#!py3 ''`    | Class name is applied to the wrapper element of the code. If configured, this setting will override the `css_class` option of Highlight. If nothing is configured here or in Highlight, the class `highlight` will be used.
`disable_indented_code_blocks` | bool         | `#!py3 False` | Disables Python Markdown's indented code block parsing.  This is nice if you only ever use fenced blocks.
`custom_fences`                | [dictionary] | `#!py3 []`    | Custom fences.
`highlight_code`               | bool         | `#!py3 True`  | Enable or disable code highlighting.
`preserve_tabs`                | bool         | `#!py3 False` | Experimental feature that preserves tabs in fenced code blocks.
`legacy_tab_classes`           | bool         | `#!py3 False` | Use legacy style classes for the deprecated tabbed code feature via `tab="name"`. This option will be dropped when the code tab interface is fully dropped for the general purpose [tabbed](./tabbed.md) extension.

!!! warning "Deprecated in 7.0"
    While `legacy_tab_classes` is a new option, it is also tied to the deprecated code tab feature of SuperFences. It is
    only provided as an option to help with the transition of the code tab feature being deprecated in favor of the
    [Tabbed](./tabbed.md) extension. When the code tabs are removed from SuperFences, so will
    `legacy_tab_classes`.

    `highlight_code` is also disabled and now does nothing. If a non-highlighted variant of fences is preferred, it is
    recommend to use [custom fences](#custom-fences). This option will be removed in a future version.

--8<-- "links.txt"

--8<-- "uml.txt"
