# Spoilers

## Overview

Spoilers is an extension that hides content until clicked. It uses the HTML5 `#!html<details><summary>` tags to accomplish this.  It supports nesting and you can also force the default state to open.

## Syntax

Spoilers must contain a blank line before they start. Use `???` to start the block.  Follow the start of the block with an optional class and the summary contained in quotes. To force the spoiler to be open by default, append a plus sign after the opening tokens `???+`. Content is placed below the header and must be indented.

Simple spoiler:

```
??? "Summary"
    Here's some content.
```

Spoiler with optional class:

```
??? optional-class "Summary"
    Here's some content.
```

Nested spoilers:

```
??? "Summary"
    Here's some content.

    ??? "**Nested**"
        More content
```

Spoiler forced open by default:

```
???+ "open example"
    content
```

## Browser Support

Unfortunately, due how new `#!html<details><summary>` tags are, not all browsers support them.  In order to have them supported most browsers, you will have to provide some fallback styling and JavaScript until all browsers catch up.

This document uses the following style (or something very close to this) to ensure all browsers get style the elements appropriately:

```css
.md-typeset details {
  display: block;
}

.md-typeset details[open] > summary::before {
  content: "\25BC";
}

.md-typeset details summary {
  display: block; cursor: pointer;
}

.md-typeset details summary:focus {
  outline: none;
}

.md-typeset details summary::before {
  content: "\25B6";
  padding-right: 0.5em;
}

.md-typeset details summary::-webkit-details-marker {
  display: none;
}

.md-typeset details.no-details > * {
  display: none;
}

.md-typeset details.no-details summary {
  display: block;
}
```

And it uses this JavaScript that will convert `#!html<details><summary>` tags in browsers that do not support them in to working elements.  You would run the code when on content load.

```js
/**
 * Converts details/summary tags into working elements in browsers that don't yet support them.
 * @return {void}
 */
var spoilers = function () {
  // https://mathiasbynens.be/notes/html5-details-jquery#comment-35
  // Detect if details is supported in the browser
  var isDetailsSupported = function (doc) {
    var el = doc.createElement("details");
    var fake = void 0,
        root = void 0,
        diff = void 0;
    if (!("open" in el)) {
      return false;
    }
    root = doc.body || function () {
      var de = doc.documentElement;
      fake = true;
      return de.insertBefore(doc.createElement("body"), de.firstElementChild || de.firstChild);
    }();
    el.innerHTML = "<summary>a</summary>b";
    el.style.display = "block";
    root.appendChild(el);
    diff = el.offsetHeight;
    el.open = true;
    diff = diff != el.offsetHeight;
    root.removeChild(el);
    if (fake) {
      root.parentNode.removeChild(root);
    }
    return diff;
  }(document);

  if (!isDetailsSupported) {
    var blocks = document.querySelectorAll("details>summary");
    for (var i = 0; i < blocks.length; i++) {
      var summary = blocks[i];
      var details = summary.parentNode;
      if (!details.hasAttribute("open")) {
        if (!!!details.className.match(new RegExp("(\\s|^)no-details(\\s|$)"))) {
          details.className += " no-details";
        }
      }
      summary.addEventListener("click", function (e) {
        var details = e.target.parentNode;
        if (!!details.className.match(new RegExp("(\\s|^)no-details(\\s|$)"))) {
          var reg = new RegExp("(\\s|^)no-details(\\s|$)");
          details.className = details.className.replace(reg, " ");
          details.setAttribute("open", "");
        } else {
          details.className += " no-details";
          details.removeAttribute("open");
        }
      });
    }
  }
};
```

## Examples

???+ "Open example"

    ??? "**Nested** examples 1"
        Some content.

        And some more content.

    ??? "*More* nesting"
        And more content again.
