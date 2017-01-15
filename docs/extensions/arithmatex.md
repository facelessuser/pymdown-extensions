## Overview

The Arithmatex extension searches for `#!tex $...$` or `#!tex $$...$$` and preserves and formats them so that [MathJax][mathjax] can detect them in the HTML output.

`#!tex $...$` is the inline form and requires the opening token (`#!tex $`) to be followed by a non-whitespace character, and the closing to be preceded by a non-white-space character.  This is to help avoid false positives when using the dollar sign in traditional ways such as: I have $2.00 and Bob has $10.00.  The previous statement requires no escaping of the `#!tex $` character.  But when needed, the `#!tex $` character can be escaped using `#!tex \$`.

`#!tex $$...$$` is the *block* form.  When using `#!tex $$`, the block must start with `#!tex $$` and end with `#!tex $$`; a block contains no empty lines.

The Arithmatex extension actually converts the dollar notation to a more reliable notation in the HTML.  So the conversion is as follows: `#!tex $...$` --> `#!tex \(...\)` and `#!tex $$...$$` --> `#!tex \[...\]`.  Keep this in mind when configuring MathJax for your document.  If a different conversion is desired, see [Options](#options) below to learn how to configure it.

## Options

Option            | Type            | Default                   | Description
----------------- |---------------- | ------------------------- |------------
`tex_inline_wrap` | `#!py [string]` | `#!python ['\\(', '\\)']` | An array containing the opening and closing portion of the wrap.
`tex_block_wrap`  | `#!py [string]` | `#!python ['\\[', '\\]']` | An array containing the opening and closing portion of the wrap.

!!! warning "Wrapping Format"
    The wrapping options are **not** run through an HTML escaper, so make sure you escape whatever requires escaping.  The reason we don't escape the wrap strings is so you can inject an HTML tag wrapper if desired.  Most people don't need to insert HTML, but as an example, when these docs are run through CI and spell checked, math is wrapped with `<nospell></nospell>` tags which are filtered out to avoid spell checking the content. So there are practical applications.

## Loading MathJax

Arithmatex requires you to provide the MathJax library and provide and configure it to your liking.  The recommended way of including MathJax is to use the CDN.  Below in this example, we are selecting the default `TeX-MML-AM_CHTML` configuration. This is what *this* documentation site is currently using.

```html
<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-MML-AM_CHTML"></script>
```

If you need to configure or tweak the settings further, make sure to load your configuration tweaks **before** you load the `MathJax.js` file. Below is an example of the configuration that we use to tweak the MathJax in this page.  We include this snippet **before** we include `MathJax.js`.

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

Please see the [MathJax][mathjax] site for more info on using MathJax.

## Examples

````tex
Some Equations:

$$
E(\mathbf{v}, \mathbf{h}) = -\sum_{i,j}w_{ij}v_i h_j - \sum_i b_i v_i - \sum_j c_j h_j
$$

- Here are some more equations:

    $$
        \begin{align}
            p(v_i=1|\mathbf{h}) & = \sigma\left(\sum_j w_{ij}h_j + b_i\right) \\
            p(h_j=1|\mathbf{v}) & = \sigma\left(\sum_i w_{ij}v_i + c_j\right)
        \end{align}
    $$

- Inline equations: $p(x|y) = \frac{p(y|x)p(x)}{p(y)}$.
````

Some Equations:

$$
E(\mathbf{v}, \mathbf{h}) = -\sum_{i,j}w_{ij}v_i h_j - \sum_i b_i v_i - \sum_j c_j h_j
$$

- Here are some more equations:

    $$
        \begin{align}
            p(v_i=1|\mathbf{h}) & = \sigma\left(\sum_j w_{ij}h_j + b_i\right) \\
            p(h_j=1|\mathbf{v}) & = \sigma\left(\sum_i w_{ij}v_i + c_j\right)
        \end{align}
    $$

- Inline equations: $p(x|y) = \frac{p(y|x)p(x)}{p(y)}$.

---8<--- "links.md"

---8<--- "mathjax.md"
