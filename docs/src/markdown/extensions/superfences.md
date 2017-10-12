# SuperFences

## Overview

SuperFences provides 4 features:

1. The ability to [nest fences](#nested-fence-format) under blockquotes, lists, or other block elements (see [Limitations](#limitations) for more info).
2. Ability to specify [custom fences](#custom-fences) to provide features like flowcharts, sequence diagrams, or other custom blocks.
4. The ability to disable indented code blocks in favor of only using the fenced variant (off by default).

!!! danger "Reminder"
    Remember to read the [Usage Notes](../usage_notes.md) for information that may be relevant when using this extension!

## Nested Fence Format


1. Start and end fence boundaries are specified with either 3 or more backticks or tildes.

2. Start and end fence boundaries must both use matching symbols (backticks or tildes) and must be of the same number of symbols.  If start is 3 backticks, the fence will end with 3 backticks.

3. Start and end fence boundaries must be aligned to the same indentation level.

4. Content between fences must be indented at least the same amount as the start and end boundaries.  Empty lines are exempted.

5. If you are using a fenced block inside a blockquote, at the very least, the first line of the fenced block needs to have the appropriate number of `>` characters signifying the quote depth.

    ````
    > ```
      a fenced block
      ```
    ````

6. Too many blank lines will cause a blockquote to terminate, so remember to use `>` markers accordingly if not marking every line.

    ````
    > ```
      a fenced block

    > with blank lines
      ```
    ````

7. If using a fenced block as the first line of a list, you will have to leave the first line blank, but remember that the list marker must be followed by a space.

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

## Code Highlighting

Assuming Pygments is installed, code highlighting will be handled by [Pygments][pygments] by default. If Pygments is not installed, or disabled, code blocks will be created using HTML5 style tags for a JavaScript syntax highlighter: `#!html <pre class="highlight"><code class="language-mylanguage"></code></pre>`. If you disable `highlight_code`, specified languages will be ignored, and the content will be wrapped in a simple `pre` and `code` tags with no classes.

Highlighting can be further controlled if either the `pymdownx.highlight` extension is used or if Python Markdown's CodeHilite is used. If CodeHilite is configured, it's settings will be used to configure highlighting, but CodeHilite support is deprecated and will be removed in the next major release. It is recommended to instead use [`pymdownx.highlight`](./highlight.md) extension. If `pymdownx.highlight` is included and configured, CodeHilite will be ignored.

When using fenced code blocks, you can specify a specific syntax language to highlight with by specifying the language name directly after the opening tokens (either ` ``` ` or `~~~`). So if we wanted to specify Python as the syntax to highlight with, we could use the following syntax below. Whether using Pygments or some other JavaScript highlighter, please consult your highlighter's documentation for recognized language syntax specifiers.

````
```python
import foo.bar
```
````

## Showing Line Numbers

Line numbers are provided via Pygments and can either be shown per code block or globally for all. To show globally via CodeHilite or `pymdownx.highlight`, you must set `linenums` to `#!py True` in the respective extension.

To set line numbers per code block, you can specify a special setting directly after the opening tokens (and language if present). Simply specify the starting line line number with option `linenums="1"`. The setting is followed by the equal sign and the value must be quoted.  Valid line numbers are n > 0.  If `linenums` is enabled globally, this will just control the starting line shown in the block.

````
``` linenums="1"
import foo.bar
```
````

Pygments also has a few additional options in regards to line numbers. One is "line step" which, if set to a number n > 1, will print only every n^th^ line number. The other option is a setting that can mark line numbers as "special" with a span and class `special`. If the special parameter is set to a number n > 0, every n^th^ line number is given the CSS class `special`.

So to set showing only every other line number, we could do the following. Line options are separated by a space, and "line step" is always the second option, so you must specify line start before line step.

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

For JavaScript libraries, a class of `linenums` is written to the block.  This may or may not be leveraged by your chosen highlighter.  It is uncertain at this time whether line number support for JavaScript highlighters will be enhanced beyond this.

## Highlighting Lines

Via Pygments, certain lines can be specified for highlighting.  This is done by specifying a special setting directly after the opening tokens (and language if present).  The setting is named `hl_lines` and the value should be the targeted line numbers separated by spaces. Line numbers are always referenced starting at 1 ignoring what the line number is labeled as when showing line numbers.

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

## Custom Fences

SuperFences allows defining custom fences for special purposes. For example, SuperFences defines two default custom fences (which can be removed if desired) called `flow` and `sequence`, for flowcharts and sequence diagrams respectively. The default custom fences simply preserve the content between the fences so a JavaScript UML library can convert the content and render the UML. Custom fences are created via the `custom_fences` option.  `custom_fences` takes an array of dictionaries where each dictionary defines a custom fence. The dictionaries requires the following keys:

Keys     | Description
-------- | -----------
`name`   | The language name that is specified when using the fence in Markdown.
`class`  | The class name assigned to the HTML element when converting from Markdown to HTML.
`format` | A function that formats the HTML output.  Should return a string as HTML.

SuperFences provides two format functions by default, but you can always write your own:

Format\ Function                | Description
------------------------------- | -----------
`superfences.fence_code_format` | Places the HTML escaped content of the fence under a `#!html <pre><code>` block.
`superfences.fence_div_format`  | Places the HTML escaped content of the fence under a `#!html <div>` block.

## UML Diagram Examples

This example illustrates how this document uses the `custom_fences` option to do UML diagrams.  Out of the box, SuperFences use the default settings for `custom_fences` for the purpose of including UML. The settings below show the default settings, which define two new custom languages called `flow` and `sequence`. The `flow` and `sequence` fences will pass the content through the `superfences.fence_code_format` format function which will wrap the content in `#!html <pre><code` blocks and attach the class `uml-flowchart` or `uml-sequence-diagram` to the respective `#!html <pre>` block. `superfences.fence_div_format` could just as easily be used to wrap the content in a `#!html <div>` instead, or a new custom function could have been written and used.

```py
custom_fences = [
    {'name': 'flow', 'class': 'uml-flowchart', 'format': superfences.fence_code_format},
    {'name': 'sequence', 'class': 'uml-sequence-diagram', 'format': superfences.fence_code_format}
]
```

As defined above, the custom UML diagrams are recognized when defining a fenced code block with either the language `flow` or `sequence`.  When they are converted, the HTML element containing this content will have the respective classes `uml-flowchart` or `uml-sequence-diagram`. The format function we used in this example only escapes the content to be included in HTML. We will rely on JavaScript libraries to render our flowcharts/diagrams in the browser. Below is an example of defining a flowchart fence.

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

For this example we will use the [flowchart.js][flowchart-js] and [sequence-diagram.js][sequence-diagram-js] JavaScript libraries to render the flow charts in the browser. This extension does not provide these JavaScript libraries; you must provide the necessary JavaScript files for your custom fences. If you wish to follow along with this example to enable UML, see the requirements below.

flowcharts
: 
    - [raphael.js][raphael-js]
    - [flowchart.js][flowchart-js]

sequence diagrams
: 
    Minimum requirements for the latest version available via CDN (at the time of writing this).

    - [raphael.js][raphael-js]
    - [underscore.js][underscore-js]
    - [sequence-diagram.js][sequence-diagram-js]

All of the above mentioned libraries can be included using CDNs (you can use the version of your choice):

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/raphael/2.2.7/raphael.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/underscore.js/1.8.3/underscore-min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/js-sequence-diagrams/1.0.6/sequence-diagram-min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/flowchart/1.6.5/flowchart.min.js"></script>
```

Simply including the libraries above is not enough as these libraries need to be pointed at the elements they need to convert.  Also, we need to configure the libraries with the settings we would like.

As mentioned earlier, our flowchart elements have the `uml-flowchart` class assigned to them, and the sequence diagram elements have the `uml-sequence-diagram` class assigned to them. Below shows an example script to convert the UML diagrams for both flowcharts and sequence diagrams using the listed libraries above. This script will target the elements with the classes `uml-flowchart` and `uml-sequence-diagram`. The script will pass the content to the correct library to render the content.  It will then insert the rendered UML and remove the original source. This is just an example, and you are not required to use the following script. You are free to modify the example script or write your own to suite your specific custom fence.

In the below example we create an `onReady` function to execute the conversion when the HTML is loaded.  We create a `convertUML` function that takes the class name to search for, the converter to use, and a settings object to feed into the converter.  We then call `onReady` and feed it a callback function that will execute `convertUML` for flowcharts and for sequence diagrams. Notice that `convertUML` can handle both the `#!html <pre><code>` format or the `#!html <div>` format we mentioned earlier.

The actual `convertUML` function reads UML instructions from our element and sticks it in a div that gets appended to our main HTML content (in this case we look for the the `article` tag, but it could be anything, even `body`). We don't want to do it in place our UML instructions are because it might be under an element that is hiding it with `display: none` (like a `details` tag); it won't render correctly if its parent is not displayed.  After we render the SVG, we insert it back where it belongs throwing away the original element that had the instructions.

```js
(function () {
'use strict';

/**
 * Targets special code or div blocks and converts them to UML.
 * @param {object} converter is the object that transforms the text to UML.
 * @param {string} className is the name of the class to target.
 * @param {object} settings is the settings for converter.
 * @return {void}
 */
var uml = (function (converter, className, settings) {

  var getFromCode = function getFromCode(parent) {
    // Handles <pre><code>
    var text = "";
    for (var j = 0; j < parent.childNodes.length; j++) {
      var subEl = parent.childNodes[j];
      if (subEl.tagName.toLowerCase() === "code") {
        for (var k = 0; k < subEl.childNodes.length; k++) {
          var child = subEl.childNodes[k];
          var whitespace = /^\s*$/;
          if (child.nodeName === "#text" && !whitespace.test(child.nodeValue)) {
            text = child.nodeValue;
            break;
          }
        }
      }
    }
    return text;
  };

  var getFromDiv = function getFromDiv(parent) {
    // Handles <div>
    return parent.textContent || parent.innerText;
  };

  // Change article to whatever element your main Markdown content lives.
  var article = document.querySelectorAll("article");
  var blocks = document.querySelectorAll("pre." + className + ",div." + className

  // Is there a settings object?
  );var config = settings === void 0 ? {} : settings;

  // Find the UML source element and get the text
  for (var i = 0; i < blocks.length; i++) {
    var parentEl = blocks[i];
    var el = document.createElement("div");
    el.className = className;
    el.style.visibility = "hidden";
    el.style.position = "absolute";

    var text = parentEl.tagName.toLowerCase() === "pre" ? getFromCode(parentEl) : getFromDiv(parentEl)

    // Insert our new div at the end of our content to get general
    // typset and page sizes as our parent might be `display:none`
    // keeping us from getting the right sizes for our SVG.
    // Our new div will be hidden via "visibility" and take no space
    // via `poistion: absolute`. When we are all done, use the
    // original node as a reference to insert our SVG back
    // into the proper place, and then make our SVG visilbe again.
    // Lastly, clean up the old node.
    );
    article[0].appendChild(el);
    var diagram = converter.parse(text);
    diagram.drawSVG(el, config);
    el.style.visibility = "visible";
    el.style.position = "static";
    parentEl.parentNode.insertBefore(el, parentEl);
    parentEl.parentNode.removeChild(parentEl);
  }
});

(function () {
  var onReady = function onReady(fn) {
    if (document.addEventListener) {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      document.attachEvent("onreadystatechange", function () {
        if (document.readyState === "interactive") {
          fn();
        }
      });
    }
  };

  onReady(function () {
    if (typeof flowchart !== "undefined") {
      uml(flowchart, "uml-flowchart");
    }

    if (typeof Diagram !== "undefined") {
      uml(Diagram, "uml-sequence-diagram", { theme: "simple" });
    }
  });
})();

}());
```

## Limitations

This extension suffers from the same issues that the original fenced block extension suffers from.  Normally Python Markdown does not parse content inside HTML tags unless they are marked with the attribute `markdown='1'`.  But since this is run as a preprocessor, it is not aware of the HTML blocks.

SuperFences is made to work with the default extensions out of the box.  It will probably not work with other extensions such as Grid Tables, since that extension allows for characters to obscure the blocks like the blockquote syntax does (though this has been designed to work with blockquotes).  Ideally fenced blocks need to be handled by a block parser, but there is much work to be done on Python Markdown's internal block handlers before this is possible.

SuperFences works best when following the guidelines.  If the guidelines are not followed, odd results may be encountered.

For the reasons above, the nested fences feature really is just a workaround.  But for a lot of people, this functionality is more than sufficient.

## Options

Option                         | Type   | Default      | Description
------------------------------ | ------ | ------------ | -----------
`css_class`                    | string | `#!py ''`    | Class name is applied to the wrapper element of the code. If configured, this setting will override the `css_class` option of either CodeHilite or Highlight. If nothing is configured here or via CodeHilite or Highlight, the class `highlight` will be used.
`disable_indented_code_blocks` | bool   | `#!py False` | Disables Python Markdown's indented code block parsing.  This is nice if you only ever use fenced blocks.
`custom_fences`                | dict   | ``           | Custom fences.
`highlight_code`               | bool   | `#!py True`  | Enable or disable code highlighting.

!!! warning "Deprecated 3.0.0"
    The setting `use_codehilite_settings` has been deprecated since `3.0.0` and now does nothing. It is still present to avoid breakage, but will be removed in the future.

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
