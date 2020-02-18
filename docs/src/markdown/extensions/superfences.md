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
    === "Source"
        ````
        ```{.python .extra-class linenums="1"}
        import hello_world
        ```
        ````

    === "HTML"
        ```html
        <table class="extra-class highlighttable"><tr><td class="linenos"><div class="linenodiv"><pre><span></span>1</pre></div></td><td class="code"><div class="extra-class highlight"><pre><span></span><code><span cv></td><td class="code"><div class="extra-class highlight"><pre><span></span><code><span class="kn">import</span> <spanlass="kn">import</span> <span class="nn">hello_world</span>\n</code></pre></div>\n</td></tr></table>
        ```

When generating additional classes on a JavaScript style code block (non-Pygments code blocks), classes are injected in
the `#!html code` block.

!!! example "Non-Pygments Injecting Classes"
     === "Source"
        ````
        ```{.python .extra-class #id linenums="1"}
        import hello_world
        ```
        ````

    === "HTML"
        ```html
        <pre id="id" class="highlight"><code class="extra-class language-python linenums">import hello_world</code></pre>
        ```

When using a built in [custom formatter](#custom-fences), all classes and IDs are injected on to the first element
`#!html <div>` or `#!html <pre>`. This preserves previous behavior, but you can write your own and inject them in the
way that suites your needs.

## Tabbed Fences

!!! warning "Deprecated 7.0b1"
    The tab option is deprecated in 7.0b1 due to the addition of the general purpose tab extension
    [`pymdownx.tabbed`](./tabbed.md).

    The feature is still usable, but by the class names on the output
    have changed from `superfences-tabs` and `superfences-content` to `tabbed-set` and `tabbed-content` respectively.
    This is to help create unity between the new extension and this feature as we guide people towards the new
    extension.

    To use the legacy class names, you can use the global `legacy_tab_classes` option to get the old style classes. This
    option will be removed, along with the entire `tab=""` feature in 8.0.

SuperFences has the ability to create tabbed code blocks.  Simply add `tab="tab-title"` to the fence's header, and the
code block will will be rendered in a tab with the title `tab-title`.  If you do not provide a title with either `tab=`
or `tab=""`, but you've specified a language, the language will be used as the title. No case transformation is applied
-- what you type is what you get. Consecutive code tabs will be grouped together.

!!! example "Tabbed Code"

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

## Preserve tabs

Python Markdown has an approach where it normalizes whitespace. This means `\r\n` is converted to `\n` and `\t` is
converted to spaces. In 99% of Markdown, this is never really an issue, but with code blocks it can be. Tabs can
sometimes be very useful for aligning certain kinds of data, especially when dealing with characters of varying width.

!!! example "Tabs in Content"

    ```
    ============================================================
    T	Tp	Sp	D	Dp	S	D7	T
    ------------------------------------------------------------
    A	F#m	Bm	E	C#m	D	E7	A
    A#	Gm	Cm	F	Dm	D#	F7	A#
    B♭	Gm	Cm	F	Dm	E♭m	F7	B♭
    ```

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

    === "Source"
        ````
        ```py3
        import foo.bar
        ```
        ````

    === "Output"
        ```py3
        import foo.bar
        ```

## Showing Line Numbers

Line numbers are provided via Pygments and can either be shown per code block or globally for all. To show globally via
[`pymdownx.highlight`](./highlight.md), you must set `linenums` to `#!py3 True` in the respective extension.

To set line numbers per code block, you can specify a special setting directly after the opening tokens (and language if
present). Simply specify the starting line line number with option `linenums="1"`. The setting is followed by the equal
sign and the value must be quoted.  Valid line numbers are n > 0.  If `linenums` is enabled globally, this will just
control the starting line shown in the block.

!!! example "Line Number Example"

    === "Source"
        ````
        ``` linenums="1"
        import foo.bar
        ```
        ````

    === "Output"
        ``` linenums="1"
        import foo.bar
        ```

Pygments also has a few additional options in regards to line numbers. One is "line step" which, if set to a number n >
1, will print only every n^th^ line number. The other option is a setting that can mark line numbers as "special" with a
span and class `special`. If the special parameter is set to a number n > 0, every n^th^ line number is given the CSS
class `special`.

So to set showing only every other line number, we could do the following. Line options are separated by a space, and
"line step" is always the second option, so you must specify line start before line step.

!!! example "Nth Line Example"

    === "Source"
        ````
        ``` linenums="2 2"
        """Some file."""
        import foo.bar
        import boo.baz
        import foo.bar.baz
        ```
        ````

    === "Output"
        ``` linenums="2 2"
        """Some file."""
        import foo.bar
        import boo.baz
        import foo.bar.baz
        ```

To set every other line as special, you must set the third `linenums` option (specify line start and step before it).
Special must be a value of n > 0.

!!! example "Special Line Example"

    === "Source"
        ````
        ``` linenums="1 1 2"
        """Some file."""
        import foo.bar
        import boo.baz
        import foo.bar.baz
        ```
        ````

    === "Output"
        ``` linenums="1 1 2"
        """Some file."""
        import foo.bar
        import boo.baz
        import foo.bar.baz
        ```

For JavaScript libraries, a class of `linenums` is written to the block.  This may or may not be leveraged by your
chosen highlighter.  It is uncertain at this time whether line number support for JavaScript highlighters will be
enhanced beyond this.w what to inject.

## Highlighting Lines

Via Pygments, certain lines can be specified for highlighting.  This is done by specifying a special setting directly
after the opening tokens (and language if present).  The setting is named `hl_lines` and the value should be the
targeted line numbers separated by spaces.

!!! example "Highlight Lines Example"

    === "Source"
        ````
        ``` hl_lines="1 3"
        """Some file."""
        import foo.bar
        import boo.baz
        import foo.bar.baz
        ```
        ````

    === "Output"
        ``` hl_lines="1 3"
        """Some file."""
        import foo.bar
        import boo.baz
        import foo.bar.baz
        ```

Line numbers are always referenced starting at 1 ignoring what the line number is labeled as when showing line numbers.

!!! example "Highlight Lines with Line Numbers Example"

    === "Source"
        ````
        ```hl_lines="1 3" linenums="2"
        """Some file."""
        import foo.bar
        import boo.baz
        import foo.bar.baz
        ```
        ````

    === "Output"
        ``` hl_lines="1 3" linenums="2"
        """Some file."""
        import foo.bar
        import boo.baz
        import foo.bar.baz
        ```

## Custom Fences

SuperFences allows defining custom fences for special purposes, like flow charts and sequence diagrams:

!!! example "Flow Chart Example"

    === "Source"
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

    === "Output"
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

!!! example "Sequence Diagram Example"

    === "Source"
        ````
        ```sequence
        Title: Here is a title
        A->B: Normal line
        B-->C: Dashed line
        C->>D: Open arrow
        D-->>A: Dashed open arrow
        ```
        ````

    === "Output"
        ```sequence
        Title: Here is a title
        A->B: Normal line
        B-->C: Dashed line
        C->>D: Open arrow
        D-->>A: Dashed open arrow
        ```

As shown above, SuperFences defines two default custom fences (which can be removed if desired) called `flow` and
`sequence`, for flowcharts and sequence diagrams respectively. The default custom fences simply preserve the content
between the fences so a JavaScript UML library can convert the content and render the UML. To see *exactly* how to set
up UML like in this documentation, see [UML Diagram Example](#uml-diagram-example).

Custom fences are created via the `custom_fences` option.  `custom_fences` takes an array of dictionaries where each
dictionary defines a custom fence. The dictionaries requires the following keys:

Keys        | Description
----------- | -----------
`name`      | The language name that is specified when using the fence in Markdown. If given `*`, it will override the base fence logic, the default for all fence names not handled by other custom fences.
`class`     | The class name assigned to the HTML element when converting from Markdown to HTML.
`format`    | A function that formats the HTML output. The function should return a string as HTML.
`validator` | An optional parameter that is used to provide a function to validate custom fence parameters.

!!! new "New in 7.0b2"
    Starting in 7.0b2, you can override the base fence logic (the syntax highlighter) by specifying the custom fence
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

!!! new "New 7.0b2"
    The addition of the parameters `classes` and `id_value` is new in 7.0b2. If injecting additional classes or ids via
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

This example illustrates how this document uses the `custom_fences` option to do UML diagrams.  The settings below shows
two new custom languages called `flow` and `sequence` and are the options that must be fed through the `custom_fences`
[option](#options). The `flow` and `sequence` fences will pass the content through the `superfences.fence_code_format`
format function which will wrap the content in `#!html <pre><code` blocks and attach the class `uml-flowchart` or
`uml-sequence-diagram` to the respective `#!html <pre>` block. `superfences.fence_div_format` could just as easily be
used to wrap the content in a `#!html <div>` instead, or a new custom function could have been written and used.

```py3
extension_configs = {
    "pymdownx.superfences": {
        "custom_fences": [
            {
                'name': 'flow',
                'class': 'uml-flowchart',
                'format': pymdownx.superfences.fence_code_format
            },
            {
                'name': 'sequence',
                'class': 'uml-sequence-diagram',
                'format': pymdownx.superfences.fence_code_format
            }
        ]
    }
}
```

As defined above, the custom UML diagrams are recognized when defining a fenced code block with either the language
`flow` or `sequence`.  When they are converted, the HTML element containing this content will have the respective
classes `uml-flowchart` or `uml-sequence-diagram`. The format function we used in this example only escapes the content
to be included in HTML. We will rely on JavaScript libraries to render our flowcharts/diagrams in the browser.

The JavaScript libraries used to render UML in this document are [flowchart.js][flowchart-js] and
[sequence-diagram.js][sequence-diagram-js]. This extension does not provide these JavaScript libraries; you must provide
the necessary JavaScript files for your custom fences yourself. If you wish to follow along with this example to enable
UML, see the requirements below.

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

Simply including the libraries above is not enough as these libraries need to be pointed at the elements they need to
convert.  Also, we need to configure the libraries with the settings we would like.

As mentioned earlier, our flowchart elements have the `uml-flowchart` class assigned to them, and the sequence diagram
elements have the `uml-sequence-diagram` class assigned to them. Below shows an example script to convert the UML
diagrams for both flowcharts and sequence diagrams using the listed libraries above. This script will target the
elements with the classes `uml-flowchart` and `uml-sequence-diagram`. The script will pass the content to the correct
library to render the content.  It will then insert the rendered UML and remove the original source. This is just an
example, and you are not required to use the following script. You are free to modify the example script or write your
own to suite your specific custom fence.

In the below example we create an `onReady` function to execute the conversion when the HTML is loaded.  We create a
`convertUML` function that takes the class name to search for, the converter to use, and a settings object to feed into
the converter.  We then call `onReady` and feed it a callback function that will execute `convertUML` for flowcharts and
for sequence diagrams. Notice that `convertUML` can handle both the `#!html <pre><code>` format or the `#!html <div>`
format we mentioned earlier.

The actual `convertUML` function reads UML instructions from our element and sticks it in a div that gets appended to
our main HTML content (in this case we look for the the `body` tag, but it could be anything). We don't want to do it in
place where our UML instructions are because it might be under an element that is hiding it with `display: none` (like a
`details` tag); it won't render correctly if its parent is not displayed.  After we render the SVG, we insert it back
where it belongs throwing away the original element that had the instructions.

```js linenums="1"
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

  // Change body to whatever element your main Markdown content lives.
  var body = document.querySelectorAll("body");
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

    var text = parentEl.tagName.toLowerCase() === "pre" ? getFromCode(parentEl) : getFromDiv(parentEl);

    // Insert our new div at the end of our content to get general
    // typeset and page sizes as our parent might be `display:none`
    // keeping us from getting the right sizes for our SVG.
    // Our new div will be hidden via "visibility" and take no space
    // via `position: absolute`. When we are all done, use the
    // original node as a reference to insert our SVG back
    // into the proper place, and then make our SVG visible again.
    // Lastly, clean up the old node.
    body[0].appendChild(el);
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

This extension suffers from the same issues that the original fenced block extension suffers from.  Normally Python
Markdown does not parse content inside HTML tags unless they are marked with the attribute `markdown='1'`.  But since
this is run as a preprocessor, it is not aware of the HTML blocks.

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

!!! warning "Deprecated in 7.0b1"
    While `legacy_tab_classes` is a new option, it is also tied to the deprecated code tab feature of SuperFences. It is
    only provided as an option to help with the transition of the code tab feature being deprecated in favor of the
    [Tabbed](./tabbed.md) extension. When the code tabs are removed from SuperFences, so will
    `legacy_tab_classes`.

    `highlight_code` is also disabled and now does nothing. If a non-highlighted variant of fences is preferred, it is
    recommend to use [custom fences](#custom-fences). This option will be removed in a future version.

--8<-- "links.txt"

--8<-- "uml.txt"
