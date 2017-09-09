# Details

## Overview

Details is an extension that creates collapsible elements that hide their content. It uses the HTML5 `#!html <details><summary>` tags to accomplish this.  It supports nesting and you can also force the default state to be open. And if you want to style some different than others, you can optionally feed in a custom class.

## Syntax

Details must contain a blank line before they start. Use `???` to start a details block or `???+` if you want to start a details block whose default state is 'open'.  Follow the start of the block with an optional class or classes (separated with spaces) and the summary contained in quotes. Content is placed below the header and must be indented.

```
??? optional-class "Summary"
    Here's some content.
```

```
??? multiple optional-class "Summary"
    Here's some content.
```

It is possible to provide only a class or classes.  If this is done, the title will be derived from the *first* class.

```
??? class
   Content.
```

```html
<details class="class"><summary>Class</summary><p>Content.</p></details>
```

```
??? multiple classes
   Content.
```

```html
<details class="multiple classes"><summary>Multiple</summary><p>Content.</p></details>
```

Details will be output in the format below. The content will always be encapsulated in tags of some kind.

```html
<details class="optional-class"><summary>Text</summary><p>Content</p></details>
```

## Browser Support

Unfortunately, due to how new `#!html <details><summary>` tags are, not all browsers support them yet.  In order to have them supported in all new browsers, you will have to provide some fallback styling and JavaScript until all browsers catch up.

This extension's goal is not to provide you with the perfect polyfill (you can design or find you own), but a basic example is provided to show the basic polyfill that is being used in this document. There are more elaborate polyfills available that support jQuery, add keyboard events, or even support back to IE8. Feel free to modify what is here or find a solution that fits your needs.

??? settings "Polyfill Example"
    Here is the basic CSS that that can be used.  It is meant to provide a consistent CSS in both browsers that support `#!html <details><summary>` tags and those that do not.

    ```css
    details {
      display: block;
    }

    details[open] > summary::before {
      content: "\25BC";
    }

    details summary {
      display: block;
      cursor: pointer;
    }

    details summary:focus {
      outline: none;
    }

    details summary::before {
      content: "\25B6";
      padding-right: 0.5em;
    }

    details summary::-webkit-details-marker {
      display: none;
    }

    /* Attach the "no-details" class to details tags
       in browsers that do not support them to get
       open/show functionality. */
    details.no-details:not([open]) > * {
      display: none;
    }

    details.no-details:not([open]) summary {
      display: block;
    }
    ```

    And below is the JavaScript that will detect browsers that do not support `#!html <details><summary>` tags and apply a `no-details` class to all details in those browsers. It will also attach a click event that will toggle the open state. The CSS above will target the `no-details` class and the `open` attribute to hide/show the content of your `#!html <details>` tag. Just run the code after the HTML content is loaded.

    ```js
    (function () {
    'use strict';
    /**
     * Converts details/summary tags into working elements in browsers that don't yet support them.
     * @return {void}
     */
    var details = (function () {

      var isDetailsSupported = function () {
        // https://mathiasbynens.be/notes/html5-details-jquery#comment-35
        // Detect if details is supported in the browser
        var el = document.createElement("details");
        var fake = false;

        if (!("open" in el)) {
          return false;
        }

        var root = document.body || function () {
          var de = document.documentElement;
          fake = true;
          return de.insertBefore(document.createElement("body"), de.firstElementChild || de.firstChild);
        }();

        el.innerHTML = "<summary>a</summary>b";
        el.style.display = "block";
        root.appendChild(el);
        var diff = el.offsetHeight;
        el.open = true;
        diff = diff !== el.offsetHeight;
        root.removeChild(el);

        if (fake) {
          root.parentNode.removeChild(root);
        }

        return diff;
      }();

      if (!isDetailsSupported) {
        var blocks = document.querySelectorAll("details>summary");
        for (var i = 0; i < blocks.length; i++) {
          var summary = blocks[i];
          var details = summary.parentNode;

          // Apply "no-details" to for unsupported details tags
          if (!details.className.match(new RegExp("(\\s|^)no-details(\\s|$)"))) {
            details.className += " no-details";
          }

          summary.addEventListener("click", function (e) {
            var node = e.target.parentNode;
            if (node.hasAttribute("open")) {
              node.removeAttribute("open");
            } else {
              node.setAttribute("open", "open");
            }
          });
        }
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
        details();
      });
    })();

    }());
    ```

## Examples

### Basic Details

The theme used to style this document also provides special styling when a class is not provided, but your theme may not.

```
???+ "Open details"

    ??? "Nested details"
        Some content.
```

???+ "Open details"

    ??? "Nested details"
        Some content.


### Styled Details

```
???+ note "Open styled details"

    ??? danger "Nested details!"
        And more content again.
```

???+ note "Open styled details"

    ??? danger "Nested details!"
        And more content again.
