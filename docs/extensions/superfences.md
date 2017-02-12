## Overview

SuperFences provides 4 features:

1. The ability to nest fences under blockquotes, lists, or other block elements (this feature is provided as a workaround until a more official and better implementation is provided by the Python Markdown team; see [Limitations](#limitations) for more info).
2. Special UML flowchart fence via the `flow` language specifier.
3. Special UML sequence diagram via the `sequence` language specifier.
4. The ability to disable indented code blocks in favor of only using the fenced variant (off by default).

!!! danger "Reminder"
    Remember to read the [Usage Notes](../usage_notes.md) for information that may be relevant when using this extension!

## Nested Fenced Blocks

Fenced blocks require all nested fence content to be at least at the indentation levels of the fences (blank lines excluded).  The opening and closing fence markers must be indented at the same level.  If you are using a fenced block inside a blockquote, at the very least, the first line of the fenced block needs to have the appropriate number of `>` characters signifying the quote depth.

````
> ```
  a fenced block
  ```
````

Keep in mind that too many blank lines will cause a blockquote to terminate, so remember to use `>` markers accordingly if not marking every line.

````
> ```
  a fenced block

> with blank lines
  ```
````

If using a fenced block as the first line of a list, you will have to leave the first line blank, but remember that the list marker must be followed by a space.

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

## Code Highlighting

Code highlighting is handled via [Pygments][pygments] by default if Pygments is installed. If Pygments is not installed, code blocks will be wrapped in code and pre elements and given a class of `language-<specified_language>` (if a language specifier was given) so that a JavaScript highlighter can style them.

Highlighting in general is configured via external extensions. You can use [`pymdownx.highlight`](./highlight.md) extension, or the legacy method that uses [CodeHilite][codehilite]'s settings if it is configured. If you have CodeHilite configured, but still want to configure settings via `pymdownx.highlight`, just disable `use_codehilite_settings` in the options. In the future, it is planned to abandon sourcing settings from CodeHilite, so keep this in mind when selecting which option to use.

When using fenced code blocks, you can specify a specific a syntax language to highlight with by specifying the language name directly after the opening tokens (either ` ``` ` or `~~~`). So if we wanted to specify Python as the syntax to highlight with, we could use the following syntax below. Please consult your highlighters documentation for recognized language syntax specifiers.

````
```python
import foo.bar
```
````

## Showing Line Numbers

Line numbers are provided via Pygments and can either be shown per code block or globally for all. To show globally via CodeHilite or `pymdownx.highlight`, you must set `linenums` to `#!py True` in the respective extension.

To set per code block you can specify a special setting directly after the opening tokens (and language if present). Simply specify the starting line line number with option `linenums="1"`. The setting is followed by the equal sign and the value quoted.  Valid line numbers are n > 0.  If `linenums` is enabled globally, this will just control the starting line shown in the block.

````
``` linenums="1"
import foo.bar
```
````

Pygments also has a few additional options in regards to line numbers. One is line step which, if set to a number n > 1, only every n^th^ line number is printed. The other is a setting that can mark line numbers as special with span and class `special`. If special value is set to a number n > 0, every n^th^ line number is given the CSS class `special`.

So to set showing only every other line number, we could do the following. Line options are separated by a space.  Line number is always the second option, so you must specify line start before line step.

````
``` linenums="1 2"
"""Some file."""
import foo.bar
import boo.baz
import foo.bar.baz
```
````

To set every other line as special, you must set the third `linenums` option (specify line start and step before it). Special must be a value of n > 0.

````
``` linenums="1 1 2"
"""Some file."""
import foo.bar
import boo.baz
import foo.bar.baz
```
````

For JavaScript libraries, a class of `linenums` is written to the block.  This may or may not be leveraged by your chosen highlighter.  It is uncertain at this time if this will be made more useful in the future.

## Highlighting Lines

Via Pygments, certain lines can be specified for highlighting.  This is done by specifying a special setting directly after the opening tokens (and language if present).  The setting is named `hl_lines` and the value should be line numbers separated by spaces. Line numbers are always referenced starting at 1 ignoring what the line number is labeled as when showing line numbers.

````
``` hl_lines="1 3"
"""Some file."""
import foo.bar
import boo.baz
import foo.bar.baz
```
````

````
``` hl_lines="1 3" linenums="2"
"""Some file."""
import foo.bar
import boo.baz
import foo.bar.baz
```
````

## UML Diagrams

UML diagrams are recognized when defining a fenced code block with either the language `flow` or `sequence`.  When using the UML diagram features, you must provide the necessary JavaScript files for the HTML output.  The requirements are listed below:

**flowcharts:**

- [raphael.js][raphael-js]
- [flowchart.js][flowchart-js]

**sequence diagrams:**

- [raphael.js][raphael-js]
- [underscore.js][underscore-js]
- [sequence-diagram.js][sequence-diagram-js]

All of these libraries can be included using a CDN (you can use the version of your choice):

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/raphael/2.1.4/raphael-min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.3/underscore-min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/js-sequence-diagrams/1.0.6/sequence-diagram-min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/flowchart/1.4.2/flowchart.min.js"></script>
```

Simply including the libraries above is not enough as these libraries need to be pointed at the elements they need to convert.  We are going to show some examples (`uml-converter.js`, `flow-loader.js`, and `sequence-loader.js`) that can be used to target the HTML elements and execute the appropriate library on their content to create the desired diagrams.  The scripts do not have to be used, and you can modify them or write your own to suite your needs; it is provided for convenience.

```js
/* uml-converter.js */
(function (win, doc) {
  win.convertUML = function(className, converter, settings) {
    var charts = doc.querySelectorAll("pre." + className),
        arr = [],
        i, j, maxItem, diagaram, text, curNode;

    // Is there a settings object?
    if (settings === void 0) {
        settings = {};
    }

    // Make sure we are dealing with an array
    for(i = 0, maxItem = charts.length; i < maxItem; i++) arr.push(charts[i])

    // Find the UML source element and get the text
    for (i = 0, maxItem = arr.length; i < maxItem; i++) {
        childEl = arr[i].firstChild;
        parentEl = childEl.parentNode;
        text = "";
        for (j = 0; j < childEl.childNodes.length; j++) {
            curNode = childEl.childNodes[j];
            whitespace = /^\s*$/;
            if (curNode.nodeName === "#text" && !(whitespace.test(curNode.nodeValue))) {
                text = curNode.nodeValue;
                break;
            }
        }

        // Do UML conversion and replace source
        el = doc.createElement('div');
        el.className = className;
        parentEl.parentNode.insertBefore(el, parentEl);
        parentEl.parentNode.removeChild(parentEl);
        diagram = converter.parse(text);
        diagram.drawSVG(el, settings);
    }
  }
})(window, document)

```

```js
/* flow-loader.js */
(function (doc) {
  function onReady(fn) {
    if (doc.addEventListener) {
      doc.addEventListener('DOMContentLoaded', fn);
    } else {
      doc.attachEvent('onreadystatechange', function() {
        if (doc.readyState === 'interactive')
          fn();
      });
    }
  }

  onReady(function(){convertUML('uml-flowchart', flowchart);});
})(document)
```

```js
/* sequence-loader.js */
(function (doc) {
  function onReady(fn) {
    if (doc.addEventListener) {
      doc.addEventListener('DOMContentLoaded', fn);
    } else {
      doc.attachEvent('onreadystatechange', function() {
        if (doc.readyState === 'interactive')
          fn();
      });
    }
  }

  onReady(function(){convertUML('uml-sequence-diagram', Diagram, {theme: 'simple'});});
})(document)
```

UML flowcharts and sequence diagrams will be rendered as HTML `<pre><code>` tags before the JavaScript libraries are run on them.  They will be assigned the CSS classes `uml-flowchart` and `uml-sequence-diagram` respectively for flowcharts and sequence diagrams.

## Limitations

This extension suffers from the same issues that the original fenced block extension suffers from.  Normally Python Markdown does not parse content inside HTML tags unless they are marked with the attribute `markdown='1'`.  But since this is run as a preprocessor, it is not aware of the HTML blocks.

SuperFences is made to work with the default extensions out of the box.  It will probably not work with other extensions such as Grid Tables, since that extension allows for characters to obscure the blocks like the blockquote syntax does (though this has been designed to work with blockquotes).  Ideally fenced blocks need to be handled by a block parser, but there is much work to be done on Python Markdown's internal block handlers before this is possible.

SuperFences works best when following the guidelines.  If the guidelines are not followed, odd results may be encountered.

For the reasons above, the nested fences feature really is just a workaround.  But for a lot of people, this functionality is more than sufficient.

## Options

By default, syntax highlighting settings will be sourced from [CodeHilite][codehilite] if it is configured and `use_codehilite_settings` is enabled, but SuperFences' highlighting can be configure without and/or independently from CodeHilite. If CodeHilite is not configured, or if `use_codehilite_settings` is disabled, default settings will be used and can be configured via [`pymdownx.highlight`](./highlight.md).  CodeHilite support will most likely be abandoned in the future, so keep that in mind when configuring.

Option                         | Type   | Default              | Description
------------------------------ | ------ | -------------------- | -----------
`disable_indented_code_blocks` | bool   | `#!py False` | Disables Python Markdown's indented code block parsing.  This is nice if you only ever use fenced blocks.
`uml_flow`                     | bool   | `#!py True`  | Enable flowcharts.
`uml_sequence`                 | bool   | `#!py True`  | Enable sequence diagrams.
`use_codehilite_settings`      | bool   | `#!py True`  | Get applicable highlight settings from CodeHilite (if currently configured). CodeHilite's settings will be applied to `css_class` and additional behavioral options will be applied. Otherwise, use `css_class`, and configure settings via `pymdownx.highlight`.
`highlight_code`               | bool   | `#!py True`  | Enable or disable code highlighting.

## Examples

This highlights the special features of this extension except for `disable_indented_code_blocks`.

### Nested Fences

```
- This is a list that contains multiple code blocks.

    - Here is an indented block

            ```
            This will still be parsed
            as a normal indented code block.
            ```

    - Here is a fenced code block:

        ```
        This will still be parsed
        as a fenced code block.
        ```

    - Here is a fenced block in blockquotes:

        > ```
        > Blockquotes?
        > Not a problem!
        > ```

    - Here is a highlighted code block:

        ```python
        """Some file."""
        import foo.bar
        import boo.baz
        import foo.bar.baz
        ```

    - Here is a highlighted code block with line numbers:

        ```python linenums="1"
        """Some file."""
        import foo.bar
        import boo.baz
        import foo.bar.baz
        ```

    - Here is a highlighted code block with line numbers and line highlighting:

        ```python hl_lines="2 3" linenums="1"
        """Some file."""
        import foo.bar
        import boo.baz
        import foo.bar.baz
        ```
```

- This is a list that contains multiple code blocks.

    - Here is an indented block

            ```
            This will still be parsed
            as a normal indented code block.
            ```

    - Here is a fenced code block:

        ```
        This will still be parsed
        as a fenced code block.
        ```

    - Here is a fenced block in blockquotes:

        > ```
        > Blockquotes?
        > Not a problem!
        > ```

    - Here is a highlighted code block:

        ```python
        """Some file."""
        import foo.bar
        import boo.baz
        import foo.bar.baz
        ```

    - Here is a highlighted code block with line numbers:

        ```python linenums="1"
        """Some file."""
        import foo.bar
        import boo.baz
        import foo.bar.baz
        ```

    - Here is a highlighted code block with line numbers and line highlighting:

        ```python hl_lines="2 3" linenums="1"
        """Some file."""
        import foo.bar
        import boo.baz
        import foo.bar.baz
        ```

### UML Flow Charts

````
```flow
st=>start: Start:>http://www.google.com[blank]
e=>end:>http://www.google.com
op1=>operation: My Operation
sub1=>subroutine: My Subroutine
cond=>condition: Yes
or No?:>http://www.google.com
io=>inputoutput: catch something...

st->op1->cond
cond(yes)->io->e
cond(no)->sub1(right)->op1
```
````

```flow
st=>start: Start:>http://www.google.com[blank]
e=>end:>http://www.google.com
op1=>operation: My Operation
sub1=>subroutine: My Subroutine
cond=>condition: Yes
or No?:>http://www.google.com
io=>inputoutput: catch something...

st->op1->cond
cond(yes)->io->e
cond(no)->sub1(right)->op1
```

### UML Sequence Diagrams

````
```sequence
Title: Here is a title
A->B: Normal line
B-->C: Dashed line
C->>D: Open arrow
D-->>A: Dashed open arrow
```
````

```sequence
Title: Here is a title
A->B: Normal line
B-->C: Dashed line
C->>D: Open arrow
D-->>A: Dashed open arrow
```

--8<-- "links.md"

--8<-- "uml.md"
