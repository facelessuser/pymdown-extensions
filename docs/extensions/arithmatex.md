# Arithmatex {: .doctitle}
Syntax for MathJax support.

---

## Overview
The Arithmatex extension searches for `#!tex $...$` or `#!tex $$...$$` and formats them so that [MathJax](http://www.mathjax.org/) can detect them in the HTML output.

`#!tex $...$` is the inline form and requires the opening token (`#!tex $`) to be followed by a non-whitespace character, and the closing to be preceded by a non-whitespace character.  This is to help avoid false positives when using the dollar sign in traditional ways such as: I have $2.00 and Bob has $10.00.  The previous statement required no escaping of the `#!tex $` character.  But when needed, the `#!tex $` character can be escaped using `#!tex \$`.

`#!tex $$...$$` is the *display* or *block* form.  When using `#!tex $$`, the block must start with `#!tex $$` and end with `#!tex $$`; a block contains no empty lines.

The Arithmatex extension actually converts the dollar notation to a more reliable notation in the HTML.  So the conversion is as follows: `#!tex $...$` --> `#!tex \(...\)` and `#!tex $$...$$` --> `#!tex \[...\]`.  Keep this in mind when configuring MathJax for your document.

Arithmatex requires you to point the HTML at the MathJax library and provide the necessary configuration.  The recommended way of including MathJax is to use the CDN:

```html
<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
```

Here is an example of setting up MathJax configuration:

```js
/* mathjax-loader.js */
(function (win, doc) {
  win.MathJax = {
    config: ["MMLorHTML.js"],
    extensions: ["tex2jax.js"],
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
})(window, document);
```

Please see the [MathJax](http://www.mathjax.org/) site for more info on using MathJax.

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
