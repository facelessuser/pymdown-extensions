## Overview

The Arithmatex extension searches for `#!tex $...$` and `#!tex \(...\)` for inline math, and it searches `#!tex $$...$$`, `#!tex \[...\]`, and `#!tex \begin{}...\end{}` for block math, and preserves and formats them so that [MathJax][mathjax] can detect them in the HTML output.

For the `#!tex $...$` inline form variant, it is expected that the opening token (`#!tex $`) is to be followed by a non-whitespace character, and the closing to be preceded by a non-white-space character.  This is to help avoid false positives when using the dollar sign in traditional ways such as: I have $2.00 and Bob has $10.00.  The previous statement requires no escaping of the `#!tex $` character.  But when needed, the `#!tex $` character can be escaped using `#!tex \$`.

For block forms, the block must start with the appropriate opening for the block type: `#!tex $$`, `#!tex \[`, and `#!tex \begin{env}` for the respective search pattern. A block contains no empty lines.

On output, Arithmatex extension normalizes all output to wrapped with `#!tex \(...\)` for inline math and `#!tex \[...\]` for block math.  In the case of `#!tex \begin{}...\end{}`, `#!tex \begin{env}...\end{env}` will still be present, just wrapped in `#!tex \[...\]`. If a different wrapper is desired, see [Options](#options) below to learn how to configure it.

Optionally you can enable `insert_as_script` and the math equations will be wrapped in a special math script tag which MathJax can already find. The tag will be `#!html <script type="math/tex"></script>` for inline and `#!html <script type="math/tex; mode=display"></script>` for block. This is probably the most reliable HTML form, but if MathJax doesn't load, you don't get fallback text.  When `insert_as_script` is enabled, `tex_inline_wrap` and `tex_block_wrap` are ignored.

## Options

Option             | Type            | Default                              | Description
------------------ | --------------- | ------------------------------------ |------------
`inline_syntax`    | `#!py [string]` | `#!py ['dollar', 'round']`           | Syntax to search for: dollar=`#!tex $...$` and round=`#!tex \(...\)`.
`block_syntax`     | `#!py [string]` | `#!py ['dollar', 'square', 'begin']` | Syntax to search for: dollar=`#!tex $...$`, square=`#!tex \[...\]`, and `#!tex \begin{}...\end{}`.
`tex_inline_wrap`  | `#!py [string]` | `#!py ['\\(', '\\)']`                | An array containing the opening and closing portion of the wrap.
`tex_block_wrap`   | `#!py [string]` | `#!py ['\\[', '\\]']`                | An array containing the opening and closing portion of the wrap.
`insert_as_script` | bool            | `#!py False`                         | Instead of using the above wrap options, insert the equations in a `math/tex` script. This form is the most reliable in HTML, but if the MathJax script fails to load, the user won't see any indication of the equations.



!!! warning "Wrapping Format"
    The wrapping options are **not** run through an HTML escaper, only the equation content is escaped (and only when `insert_as_script` is `False`). So make sure you escape whatever requires escaping in your wrap options.  The reason we don't escape the wrap strings is so you can inject an HTML tag wrapper if desired, like a `#!html <div></div>` with a pattern like `#!py ['<div class="my-class">\\[', '\\]</div>']`. It is just to allow some flexibility.

## Loading MathJax

Arithmatex requires you to provide the MathJax library and provide and configure it to your liking.  The recommended way of including MathJax is to use the CDN.  Below in this example, we are selecting the default `TeX-MML-AM_CHTML` configuration. This is what *this* documentation site is currently using.

```html
<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-MML-AM_CHTML"></script>
```

If you need to configure or tweak the settings further, make sure to load your configuration tweaks **before** you load the `MathJax.js` file. Below is an example of the configuration that we use to tweak the MathJax in this page.  We include this snippet **before** we include `MathJax.js`. Note we limit search of in `tex2jax` to what our math is wrapped in.

```js
window.MathJax = {
  jax: ["input/TeX"],
  tex2jax: {
    inlineMath: [ ["\\(","\\)"] ],
    displayMath: [ ["\\[","\\]"] ]
  },
  TeX: {
    TagSide: "right",
    TagIndent: ".8em",
    MultLineWidth: "85%",
    equationNumbers: {
      autoNumber: "AMS",
    },
    unicode: {
      fonts: "STIXGeneral,'Arial Unicode MS'"
    }
  },
  displayAlign: 'left',
  showProcessingMessages: false,
  messageStyle: 'none'
};
```

If using `insert_as_script`, you don't need to configure `tex2jax` inline search patterns as your math is already packaged under script tags that MathJax knows how to find.

Please see the [MathJax][mathjax] site for more info on using MathJax modules and configuring those modules.

## Examples

````tex
Some Block Equations:

$$
E(\mathbf{v}, \mathbf{h}) = -\sum_{i,j}w_{ij}v_i h_j - \sum_i b_i v_i - \sum_j c_j h_j
$$

\[3 < 4\]

\begin{align}
    p(v_i=1|\mathbf{h}) & = \sigma\left(\sum_j w_{ij}h_j + b_i\right) \\
    p(h_j=1|\mathbf{v}) & = \sigma\left(\sum_i w_{ij}v_i + c_j\right)
\end{align}

Inline equations: $p(x|y) = \frac{p(y|x)p(x)}{p(y)}$, \(p(x|y) = \frac{p(y|x)p(x)}{p(y)}\).
````

Some Block Equations:

$$
E(\mathbf{v}, \mathbf{h}) = -\sum_{i,j}w_{ij}v_i h_j - \sum_i b_i v_i - \sum_j c_j h_j
$$

\[3 < 4\]

\begin{align}
    p(v_i=1|\mathbf{h}) & = \sigma\left(\sum_j w_{ij}h_j + b_i\right) \\
    p(h_j=1|\mathbf{v}) & = \sigma\left(\sum_i w_{ij}v_i + c_j\right)
\end{align}

Inline equations: $p(x|y) = \frac{p(y|x)p(x)}{p(y)}$, \(p(x|y) = \frac{p(y|x)p(x)}{p(y)}\).

---8<--- "links.md"

---8<--- "mathjax.md"
