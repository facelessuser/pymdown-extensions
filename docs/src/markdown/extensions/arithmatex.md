[:octicons-file-code-24:][_arithmatex]{: .source-link }

# Arithmatex

## Overview

Arithmatex is an extension that preserves LaTeX math equations during the Markdown conversion process so that they can
be used with libraries like [MathJax][mathjax]. If you prefer to use something other than MathJax, Arithmatex can output
a more generic format suitable for other libraries like [KaTeX][katex].

Arithmatex searches for the patterns `#!tex $...$` and `#!tex \(...\)` for inline math, and `#!tex $$...$$`,
`#!tex \[...\]`, and `#!tex \begin{}...\end{}` for block math. By default, all formats are enabled, but each format can
individually be disabled if desired.

The Arithmatex extension can be included in Python Markdown by using the following:

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.arithmatex'])
```

## Input Format

By default, [`smart_dollar`](#options) mode is enabled for the `#!tex $...$` inline variant. With `smart_dollar` it is
expected that the opening token (`#!tex $`) is to be followed by a non-whitespace character, and the closing to be
preceded by a non-white-space character.  This is to help avoid false positives when using the dollar sign in
traditional ways such as: *I have $2.00 and Bob has $10.00*.  The previous statement requires no escaping of the
`#!tex $` character.  But when needed, the `#!tex $` character can be escaped using `#!tex \$`. `smart_dollar` can be
disabled and will capture any `#!tex $...$` whose dollar symbols are not escaped (`#!tex \$`).

!!! example "Inline Examples"

    === "Output"
        $p(x|y) = \frac{p(y|x)p(x)}{p(y)}$, \(p(x|y) = \frac{p(y|x)p(x)}{p(y)}\).

    === "Markdown"
        ```tex
        $p(x|y) = \frac{p(y|x)p(x)}{p(y)}$, \(p(x|y) = \frac{p(y|x)p(x)}{p(y)}\).
        ```

!!! tip "Inline Configuration"
    When using MathJax, for best results, it is advised to not use [`generic`](#options) mode, and configure MathJax
    without the `text2jax` extension since MathJax automatically detects Arithmatex's default output.

    If using generic mode (for libraries like KaTeX), Arithmatex will convert dollars to the form `#!tex \(...\)` in the
    HTML output. This is because `#!tex $...$` is extremely problematic to scan for, which is why MathJax and KaTeX
    disable `#!tex $...$` by default in their plain text scanners, and why Arithmatex enables `smart_dollar` by default
    when scanning for `#!tex $...$`.

    It is advised that if you are outputting in in `generic` mode that you do not configure your JavaScript library to
    look for `#!tex $...$` and instead look for `#!tex \(...\)`, and let Arithmatex's handle `#!tex $...$`.

For block forms, the block must start with the appropriate opening for the block type: `#!tex $$`, `#!tex \[`, and
`#!tex \begin{}` for the respective search pattern. The block must also end with the proper respective end: `#!tex $$`,
`#!tex \]`, and `#!tex \end{}`. A block also must contain no empty lines and should be both preceded and followed by an
empty line.

!!! example "Block Examples"

    === "Output"
        $$
        E(\mathbf{v}, \mathbf{h}) = -\sum_{i,j}w_{ij}v_i h_j - \sum_i b_i v_i - \sum_j c_j h_j
        $$

        \[3 < 4\]

        \begin{align}
            p(v_i=1|\mathbf{h}) & = \sigma\left(\sum_j w_{ij}h_j + b_i\right) \\
            p(h_j=1|\mathbf{v}) & = \sigma\left(\sum_i w_{ij}v_i + c_j\right)
        \end{align}

    === "Markdown"
        ```tex
        $$
        E(\mathbf{v}, \mathbf{h}) = -\sum_{i,j}w_{ij}v_i h_j - \sum_i b_i v_i - \sum_j c_j h_j
        $$

        \[3 < 4\]

        \begin{align}
            p(v_i=1|\mathbf{h}) & = \sigma\left(\sum_j w_{ij}h_j + b_i\right) \\
            p(h_j=1|\mathbf{v}) & = \sigma\left(\sum_i w_{ij}v_i + c_j\right)
        \end{align}
        ```

## MathJax Output Format

The math equations will be wrapped in a special MathJax script tag and embedded into the HTML. This format does not
require the `tex2jax.js` extension when setting up MathJax. The tag will be in the form of
`#!html <script type="math/tex"></script>` for inline and `#!html <script type="math/tex; mode=display"></script>` for
block.

By default, Arithmatex will also generate a preview span with the class `MathJax_Preview` that can/should be hidden when
the math content is actually loaded. If you do not want to generate the preview, simply set `preview` to
`#!py3 False`.

## Generic Output Format

If [`generic`](#options) is enabled, the extension will escape necessary symbols and normalize all output to be wrapped
in the more reliable `#!tex \(...\)` for inline math and `#!tex \[...\]` for display math (unless changed via
`tex_inline_wrap` and `tex_block_wrap` in the [options](#options)). Lastly, everything is inserted into a
`#!html <span>` or `#!html <div>` for inline and display math respectively.

With the default settings, if in your Markdown you used `#!tex $...$` for inline math, it would be converted to
`#!html <span class="arithmatex">\(...\)</span>` in the HTML. Blocks would be normalized from `#!tex $$...$$` to
`#!html <div class="arithmatex">\[...\]</div>`.  In the case of `#!tex \begin{}...\end{}`, begins and ends will not be
replaced, only wrapped: `#!html <div class="arithmatex">\[\begin{}...\end{}\]</div>`.

## Loading MathJax

Arithmatex requires you to provide the MathJax library and provide and configure it to your liking.  The recommended way
of including MathJax is to use the CDN. Latest version at time of writing this is found below.

=== "MathJax 3"
    ```html
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
    ```

=== "Legacy: MathJax 2"
    ```html
    <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js"></script>
    ```

Generally, it is best to add your own configuration to get exactly what you want. Here we show some simple examples of
configurations done in JavaScript. We've provided two basic configurations below: one that is configured for
Arithmatex's [MathJax Output Format](#mathjax-output-format), and one that works with the
[Generic Output Format](#generic-output-format) by using `tex2jax`. These are a good starting point, so feel free to
take them and configure them further. Please see the [MathJax][mathjax] site for more info on using MathJax
extensions/plugins and configuring those extensions/plugins.

=== "Default - MathJax 3"
    ```js
    window.MathJax = {
      options: {
        ignoreHtmlClass: 'tex2jax_ignore',
        processHtmlClass: 'tex2jax_process',
        renderActions: {
          find: [10, function (doc) {
            for (const node of document.querySelectorAll('script[type^="math/tex"]')) {
              const display = !!node.type.match(/; *mode=display/);
              const math = new doc.options.MathItem(node.textContent, doc.inputJax[0], display);
              const text = document.createTextNode('');
              const sibling = node.previousElementSibling;
              node.parentNode.replaceChild(text, node);
              math.start = {node: text, delim: '', n: 0};
              math.end = {node: text, delim: '', n: 0};
              doc.math.push(math);
              if (sibling && sibling.matches('.MathJax_Preview')) {
                sibling.parentNode.removeChild(sibling);
              }
            }
          }, '']
        }
      }
    };
    ```

=== "Generic - MathJax 3"
    ```js
    window.MathJax = {
      tex: {
        inlineMath: [ ["\\(","\\)"] ],
        displayMath: [ ["\\[","\\]"] ],
        processEscapes: true,
        processEnvironments: true
      },
      options: {
        ignoreHtmlClass: ".*|",
        processHtmlClass: "arithmatex"
      }
    };
    ```

=== "Legacy: Default - MathJax 2"
    ```js
    MathJax.Hub.Config({
      config: ["MMLorHTML.js"],
      jax: ["input/TeX", "output/HTML-CSS", "output/NativeMML"],
      extensions: ["MathMenu.js", "MathZoom.js"]
    });
    ```

=== "Legacy: Generic - MathJax 2"
    ```js
    MathJax.Hub.Config({
      config: ["MMLorHTML.js"],
      extensions: ["tex2jax.js"],
      jax: ["input/TeX", "output/HTML-CSS", "output/NativeMML"],
      tex2jax: {
        inlineMath: [ ["\\(","\\)"] ],
        displayMath: [ ["\\[","\\]"] ],
        processEscapes: true,
        processEnvironments: true,
        ignoreClass: ".*|",
        processClass: "arithmatex"
      },
    });
    ```

Notice that in our generic configuration, we set up `tex2jax` to only load `arithmatex` classes by excluding all
elements and adding an exception for the `arithmatex` class. We also don't bother adding `#!tex $...$` and
`#!tex $$...$$` to the `inlineMath` and `displayMath` options as Arithmatex converts them respectively to
`#!tex \(...\)` and `#!tex \[...\]` in the HTML output (unless altered in [Options](#options)). But we do have to enable
`processEnvironments` to properly process `#!tex \begin{}...\end{}` blocks.

## Loading KaTeX

In order to use KaTeX, the generic output format is required. You will need to include the KaTeX library:

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.9.0/katex.min.js"></script>
```

And the KaTeX CSS:

```html
<link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.9.0/katex.min.css">
```

Though KaTeX does have its own auto load script, we want to ensure it *only* loads math content from elements with the
`arithmatex` class. Below is a script that would do just that. Notice we check for and strip wrappers `#!tex \(...\)`
and `#!tex \[...\]` off the content of the elements and send it through the renderer. We also don't bother adding
`#!tex $...$` and `#!tex $$...$$` to the `inlineMath` and `displayMath` options as Arithmatex converts them respectively
to `#!tex \(...\)` and `#!tex \[...\]` in the HTML output (unless altered in [Options](#options)).

```js
(function () {
'use strict';

var katexMath = (function () {
    var maths = document.querySelectorAll('.arithmatex'),
        tex;

    for (var i = 0; i < maths.length; i++) {
      tex = maths[i].textContent || maths[i].innerText;
      if (tex.startsWith('\\(') && tex.endsWith('\\)')) {
        katex.render(tex.slice(2, -2), maths[i], {'displayMode': false});
      } else if (tex.startsWith('\\[') && tex.endsWith('\\]')) {
        katex.render(tex.slice(2, -2), maths[i], {'displayMode': true});
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
    if (typeof katex !== "undefined") {
      katexMath();
    }
  });
})();

}());
```

## Alternative Math Blocks

!!! tip "Alternate Math Format"
    The alternate math format functions use the **default** style that embeds math content in scripts, not the
    **generic** format that just escapes the content in plain text.

[InlineHilite](./inlinehilite.md) and [SuperFences](./superfences.md) both have a feature where you can specify your own
custom inline and fence blocks respectively. Arithmatex provides a number of compatible formats that can be used in
conjunction with InlineHilite and SuperFences to create an alternative (and possibly more preferable) syntax for math.

In InlineHilite, by simply providing the following configuration (no need to include `pymdownx.arithmatex` as an
extension), you can create a familiar inline math format:

```py3
import pymdownx.arithmatex as arithmatex

extensions = [
    "pymdownx.inlinehilite"
]

extension_config = {
    "pymdownx.inlinehilite": {
        "custom_inline": [
            {"name": "math", "class": "arithmatex", arithmatex.inline_mathjax_format}
        ]
    }
}
```

!!! example "Inline Math"

    === "Output"
        `#!math p(x|y) = \frac{p(y|x)p(x)}{p(y)}`

    === "Markdown"
        ```
        `#!math p(x|y) = \frac{p(y|x)p(x)}{p(y)}`
        ```


In SuperFences, by providing the following configuration (no need to include `pymdownx.arithmatex` as an extension), you
can create math fences:

```py3
import pymdownx.arithmatex as arithmatex

extensions = [
    "pymdownx.inlinehilite"
]

extension_config = {
    "pymdownx.superfences": {
        "custom_fences": [
            {"name": "math", "class": "arithmatex", arithmatex.inline_mathjax_format}
        ]
    }
}
```

!!! example "Math Fences"

    === "Output"
        ```math
        \begin{align}
            p(v_i=1|\mathbf{h}) & = \sigma\left(\sum_j w_{ij}h_j + b_i\right) \\
            p(h_j=1|\mathbf{v}) & = \sigma\left(\sum_i w_{ij}v_i + c_j\right)
        \end{align}
        ```

    === "Markdown"
        ````
        ```math
        \begin{align}
            p(v_i=1|\mathbf{h}) & = \sigma\left(\sum_j w_{ij}h_j + b_i\right) \\
            p(h_j=1|\mathbf{v}) & = \sigma\left(\sum_i w_{ij}v_i + c_j\right)
        \end{align}
        ```
        ````

Provided formats are found below:

Name                            | Description
------------------------------- | -----------
`inline_mathjax_preview_format` | Inline format suitable for InlineHilite that preserves math in MathJax script format with an appropriate preview.
`inline_mathjax_format`         | Inline format suitable for InlineHilite that preserves math in MathJax script format without a preview.
`inline_generic_format`         | Inline format suitable for InlineHilite that preserves math in generic spans with `arithmatex` class. Content will be wrapped with `\(` and `\)`, so your math library should target those for conversion.
`block_mathjax_preview_format`  | Display/block format suitable for SuperFences that preserves math in MathJax script format with an appropriate preview.
`block_mathjax_format`          | Display/block format suitable for SuperFences that preserves math in MathJax script format without a preview.
`block_generic_format`          | Display/block format suitable for SuperFences that preserves math in generic spans with `arithmatex` class. Content will be wrapped with `\[` and `\]`, so your math library should target those for conversion.

## Options

Option            | Type     | Default                               | Description
----------------- | -------- | ------------------------------------- |------------
`inline_syntax`   | [string] | `#!py3 ['dollar', 'round']`           | Syntax to search for: dollar=`#!tex $...$` and round=`#!tex \(...\)`.
`block_syntax`    | [string] | `#!py3 ['dollar', 'square', 'begin']` | Syntax to search for: dollar=`#!tex $...$`, square=`#!tex \[...\]`, and `#!tex \begin{}...\end{}`.
`generic`         | bool     | `#!py3 False`                         | Output in a generic format suitable for non MathJax libraries.
`tex_inline_wrap` | [string] | `#!py3 ['\\(', '\\)']`                | An array containing the opening and closing portion of the `generic` wrap.
`tex_block_wrap`  | [string] | `#!py3 ['\\[', '\\]']`                | An array containing the opening and closing portion of the `generic` wrap.
`smart_dollar`    | bool     | `#!py3 True`                          | Enable Arithmatex's smart dollar logic to minimize math detection issues with `#!tex $`.
`preview`         | bool     | `#!py3 True`                          | Insert a preview to show until MathJax finishes loading the equations.

---8<---
links.txt

mathjax.txt
---8<---
