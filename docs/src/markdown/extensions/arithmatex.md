# Arithmatex

## Overview

Arithmatex is an extension that preserves LaTeX math equations during the Markdown conversion process so that they can be used with [MathJax][mathjax]. It searches for the patterns `#!tex $...$` and `#!tex \(...\)` for inline math, and `#!tex $$...$$`, `#!tex \[...\]`, and `#!tex \begin{}...\end{}` for block math. By default, all formats are enabled, but they each format can individually be disabled if desired.

Keep in mind that some equations can make it through without Arithmatex fine.  Arithmatex is meant to *ensure* they make it through.

## Input Format

For the `#!tex $...$` inline variant, it is expected that the opening token (`#!tex $`) is to be followed by a non-whitespace character, and the closing to be preceded by a non-white-space character.  This is to help avoid false positives when using the dollar sign in traditional ways such as: I have $2.00 and Bob has $10.00.  The previous statement requires no escaping of the `#!tex $` character.  But when needed, the `#!tex $` character can be escaped using `#!tex \$`.

For block forms, the block must start with the appropriate opening for the block type: `#!tex $$`, `#!tex \[`, and `#!tex \begin{}` for the respective search pattern. The block must also end with the proper respective end: `#!tex $$`, `#!tex \]`, and `#!tex \end{}`. A block also must contain no empty lines and should be both preceded and followed by an empty line.

## Output Format

If `insert_as_script` is enabled, the math equations will be wrapped in a special MathJax script tag and embedded into the HTML. MathJax can already find these scripts, so there is no need to configure the `tex2jax` extension when setting up MathJax. The tag will be `#!html <script type="math/tex"></script>` for inline and `#!html <script type="math/tex; mode=display"></script>` for block. This is probably the most reliable HTML form, but if MathJax doesn't load, you don't get fallback text.  When `insert_as_script` is enabled, `tex_inline_wrap` and `tex_block_wrap` are ignored.

On output, if `insert_as_script` is `#!py False`, the extension will escape necessary symbols and normalize all output to be wrapped in the more reliable `#!tex \(...\)` for inline math and `#!tex \[...\]` for block math. Then the wrapped content will be inserted into a `span` and embedded into the HTML.  The span provides a container to keep MathJax from gathering multiple equations into one by mistake.  So, with the default settings, if in your Markdown you used `#!tex $...$`, it would be converted to `#!tex \(...\)` in the HTML. Blocks would respectively be normalized from `#!tex $$...$$` to `#!tex \[...\]`.  In the case of `#!tex \begin{}...\end{}`, begins and ends will not be replaced, only wrapped`#!tex \[\begin{}...\end{}\]`. Normalization is provided as MathJax disables detection of `#!tex $...$` by default due to detection issues with money notation.  Since Arithmatex provides additional logic to curb issues with `#!tex $`, we allow it in the Markdown. If a different wrapper is desired, see [Options](#options) below to learn how to change the wrapper.

## Options

Option             | Type            | Default                              | Description
------------------ | --------------- | ------------------------------------ |------------
`inline_syntax`    | `#!py [string]` | `#!py ['dollar', 'round']`           | Syntax to search for: dollar=`#!tex $...$` and round=`#!tex \(...\)`.
`block_syntax`     | `#!py [string]` | `#!py ['dollar', 'square', 'begin']` | Syntax to search for: dollar=`#!tex $...$`, square=`#!tex \[...\]`, and `#!tex \begin{}...\end{}`.
`tex_inline_wrap`  | `#!py [string]` | `#!py ['\\(', '\\)']`                | An array containing the opening and closing portion of the wrap.
`tex_block_wrap`   | `#!py [string]` | `#!py ['\\[', '\\]']`                | An array containing the opening and closing portion of the wrap.
`insert_as_script` | bool            | `#!py False`                         | Instead of using the above wrap options, insert the equations in a `math/tex` script. This form is the most reliable in HTML, but if the MathJax script fails to load, the user won't see any indication of the equations.

!!! danger "Wrapping Format"
    Version `1.7.0`: Arithmatex, when `insert_as_script` is `#!py False`, now runs the wrap options through an HTML escaper and then everything is wrapped in a `span`. This is to isolate equations and prevent them from bleeding into each other when MathJax parses the HTML. Though this is a more aggressive change, it is to meant to provide more reliable output.

## Loading MathJax

Arithmatex requires you to provide the MathJax library and provide and configure it to your liking.  The recommended way of including MathJax is to use the CDN. Latest version at time of writing this is found below.

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js"></script>
```

If you want to load one of the pre-defined configurations that MathJax offers, you can do as shown below.  Notice we are using the [`TeX-MML-AM_CHTML`](http://docs.mathjax.org/en/latest/config-files.html?highlight=TeX-MML-AM_CHTML#the-tex-mml-am-chtml-configuration-file) configuration file.

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-MML-AM_CHTML"></script>
```

If you don't include a pre-defined configuration, you will need to provide your own.  But you can also provide a configuration to tweak the pre-defined configuration.  Here we show a simple example of a configuration done in JavaScript.

```js
window.MathJax = {
  config: ["MMLorHTML.js"],
  jax: ["input/TeX", "output/HTML-CSS", "output/NativeMML"],
  extensions: ["tex2jax.js", "MathMenu.js", "MathZoom.js"],
  tex2jax: {
    inlineMath: [ ["\\(","\\)"] ],
    displayMath: [ ["\\[","\\]"] ]
  },
};
```

If you have `insert_as_script` enabled, you could omit the extension `tex2jax.js` and the `tex2jax` settings.

```js
window.MathJax = {
  config: ["MMLorHTML.js"],
  jax: ["input/TeX", "output/HTML-CSS", "output/NativeMML"],
  extensions: ["MathMenu.js", "MathZoom.js"]
};
```

Please see the [MathJax][mathjax] site for more info on using MathJax extensions/plugins and configuring those extensions/plugins.

## Examples

```tex
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
```

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
