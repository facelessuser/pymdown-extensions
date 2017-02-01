## Overview

SuperFences provides 4 features:

1. The ability to nest fences under blockquotes, lists, or other block elements (this feature is provided as a workaround until a more official and better implementation is provided by the Python Markdown team; see [Limitations](#limitations) for more info).
2. Special UML flowchart fence via the `flow` language specifier.
3. Special UML sequence diagram via the `sequence` language specifier.
4. The ability to disable indented code blocks in favor of only using the fenced variant (off by default).

All features can be turned on or off.

SuperFences relies on the [CodeHilite][codehilite] extension for syntax highlighting, so CodeHilite is expected to be installed and configured if syntax highlighting is desired.  If CodeHilite is not configured or installed, SuperFences will just escape in such a way that a JavaScript highlighter *could* be used.

!!! danger "Reminder"
    Remember to read the [Usage Notes](../usage_notes.md) for information that may be relevant when using this extension!

### Nested Fenced Blocks

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

### UML Diagrams

When using the UML diagram features, you must provide the necessary JavaScript files for the HTML output.  The requirements are listed below:

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

## Pygments Lexer Options

If using Pygments, some lexers have special options.  For instance, the `php` lexer has the option `startinline` which, if enabled, will parse PHP syntax without requiring `#!php <?` at the beginning.  SuperFences takes the approach of allowing you to create a special Pygments language with options.  So if you wanted to enable `startinline` for `php`, you might create a language name called `php-inline` that maps to `php` with `startinline` enabled.  This is done via the `extend_pygments_lang` option.

`extend_pygments_lang` is an option that takes an array of dictionaries.  Each dictionary contains three keys: `name` which is the new name you are adding, `lang` which is the language the new name maps to, and `options` which is a dictionary of the options you wish to apply.

For example, to create the above mentioned `php-inline` we would feed in the following to `extend_pygments_lang`:

```py
extended_pygments_lang = [
    {"name": "php-inline", "lang": "php", "options": {"startinline": True}}
]
```

Now we can do this:

````
```php-inline
$a = array("foo" => 0, "bar" => 1);
foreach ($a as $key => $value) {
  // comment
  echo "{$key} => {$value}" . PHP_EOL;
}
```
````

To get this:

```php-inline
$a = array("foo" => 0, "bar" => 1);
foreach ($a as $key => $value) {
  // comment
  echo "{$key} => {$value}" . PHP_EOL;
}
```

!!! Note "Note"
    When specifying extended languages, they are shared across InlineHilite and SuperFences, so if you specify a language in SuperFences, you don't have to specify it in InlineHilite and vice versa.

## Options

General syntax highlighting settings are configured via CodeHilite which should installed and enabled in order to get the highlighting.

Option                         | Type | Default      | Description
------------------------------ | ---- | ------------ | -----------
`disable_indented_code_blocks` | bool | `#!py False` | Disables Python Markdown's indented code block parsing.  This is nice if you only ever use fenced blocks.
`nested`                       | bool | `#!py True`  | Use nested fences.
`uml_flow`                     | bool | `#!py True`  | Enable flowcharts.
`uml_sequence`                 | bool | `#!py True`  | Enable sequence diagrams.
`extend_pygments_lang`         | list | `#!py []`    | A list of extended languages to add.  See [Pygments Lexer Options](#pygments-lexer-options) for more info.

## Examples

This highlights the special features of this extension except for `disable_indented_code_blocks`.

### Nested Fences

````
    ```
    This will still be parsed
    as a normal indented code block.
    ```

```
This will still be parsed
as a fenced code block.
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

        > ```
        > Blockquotes?
        > Not a problem!
        > ```
````

    ```
    This will still be parsed
    as a normal indented code block.
    ```

```
This will still be parsed
as a fenced code block.
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

        > ```
        > Blockquotes?
        > Not a problem!
        > ```

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
