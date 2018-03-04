# Arithmatex

## Overview

Arithmatex is an extension that preserves LaTeX math equations during the Markdown conversion process so that they can be used with [MathJax][mathjax]. If you prefer to use something other than MathJax, Arithmatex can output a more generic format.

Arithmatex searches for the patterns `#!tex $...$` and `#!tex \(...\)` for inline math, and `#!tex $$...$$`, `#!tex \[...\]`, and `#!tex \begin{}...\end{}` for block math. By default, all formats are enabled, but each format can individually be disabled if desired.

## Input Format

For the `#!tex $...$` inline variant, it is expected that the opening token (`#!tex $`) is to be followed by a non-whitespace character, and the closing to be preceded by a non-white-space character.  This is to help avoid false positives when using the dollar sign in traditional ways such as: I have $2.00 and Bob has $10.00.  The previous statement requires no escaping of the `#!tex $` character.  But when needed, the `#!tex $` character can be escaped using `#!tex \$`.

!!! example "Inline Examples"

    ```tex
    $p(x|y) = \frac{p(y|x)p(x)}{p(y)}$, \(p(x|y) = \frac{p(y|x)p(x)}{p(y)}\).
    ```

    $p(x|y) = \frac{p(y|x)p(x)}{p(y)}$, \(p(x|y) = \frac{p(y|x)p(x)}{p(y)}\).

For block forms, the block must start with the appropriate opening for the block type: `#!tex $$`, `#!tex \[`, and `#!tex \begin{}` for the respective search pattern. The block must also end with the proper respective end: `#!tex $$`, `#!tex \]`, and `#!tex \end{}`. A block also must contain no empty lines and should be both preceded and followed by an empty line.

!!! example "Block Examples"

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

    $$
    E(\mathbf{v}, \mathbf{h}) = -\sum_{i,j}w_{ij}v_i h_j - \sum_i b_i v_i - \sum_j c_j h_j
    $$

    \[3 < 4\]

    \begin{align}
        p(v_i=1|\mathbf{h}) & = \sigma\left(\sum_j w_{ij}h_j + b_i\right) \\
        p(h_j=1|\mathbf{v}) & = \sigma\left(\sum_i w_{ij}v_i + c_j\right)
    \end{align}

## MathJax Output Format

The math equations will be wrapped in a special MathJax script tag and embedded into the HTML. MathJax can already find these scripts, so there is no need to include and configure the `tex2jax.js` extension when setting up MathJax. The tag will be `#!html <script type="math/tex"></script>` for inline and `#!html <script type="math/tex; mode=display"></script>` for block.

By default, Arithmatex will also generate a preview span with the class `MathJax_Preview` that MathJax will hide when the math content is actually loaded. If you do not want to see the preview, simply set `preview` to `#!py3 False`.

## Generic Output Format

If [`generic`](#options) is enabled, the extension will escape necessary symbols and normalize all output to be wrapped in the more reliable `#!tex \(...\)` for inline math and `#!tex \[...\]` for block math. The wrapping convention can be changed via `tex_inline_wrap` and `tex_block_wrap` in the [options](#options). Then the wrapped content will be inserted into a `span` or `div` for inline and display math respectively.

With the default settings, if in your Markdown you used `#!tex $...$`, it would be converted to `#!html <span class="arithmatex">\(...\)</span>` in the HTML. Blocks would be normalized from `#!tex $$...$$` to `#!html <div class="arithmatex">\[...\]</div>`.  In the case of `#!tex \begin{}...\end{}`, begins and ends will not be replaced, only wrapped: `#!html <div class="arithmatex">\[\begin{}...\end{}\]</div>`.  Since Arithmatex provides additional logic to curb issues with `#!tex $`, we allow it in the Markdown. If a different wrapper is desired, see [Options](#options) below to learn how to change the wrapper.

## Loading MathJax

Arithmatex requires you to provide the MathJax library and provide and configure it to your liking.  The recommended way of including MathJax is to use the CDN. Latest version at time of writing this is found below.

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js"></script>
```

If you want to load one of the pre-defined configurations that MathJax offers, you can do as shown below.  Notice we are using the [`TeX-MML-AM_CHTML`](http://docs.mathjax.org/en/latest/config-files.html?highlight=TeX-MML-AM_CHTML#the-tex-mml-am-chtml-configuration-file) configuration file.

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.0/MathJax.js?config=TeX-MML-AM_CHTML"></script>
```

If you don't include a pre-defined configuration, you will need to provide your own.  Here we show a simple example of a configuration done in JavaScript.

```js
window.MathJax = {
  config: ["MMLorHTML.js"],
  jax: ["input/TeX", "output/HTML-CSS", "output/NativeMML"],
  extensions: ["MathMenu.js", "MathZoom.js"]
};
```

Please see the [MathJax][mathjax] site for more info on using MathJax extensions/plugins and configuring those extensions/plugins.

## Other Math Libraries

Arithmatex can be used with other libraries besides MathJax. One such library is [KaTeX][katex]. To configure such libraries, please read their documentation.

## Options

Option            | Type     | Default                               | Description
----------------- | -------- | ------------------------------------- |------------
`inline_syntax`   | [string] | `#!py3 ['dollar', 'round']`           | Syntax to search for: dollar=`#!tex $...$` and round=`#!tex \(...\)`.
`block_syntax`    | [string] | `#!py3 ['dollar', 'square', 'begin']` | Syntax to search for: dollar=`#!tex $...$`, square=`#!tex \[...\]`, and `#!tex \begin{}...\end{}`.
`generic`         | bool     | `#!py3 False`                         | Output in a generic format suitable for non MathJax libraries.
`tex_inline_wrap` | [string] | `#!py ['\\(', '\\)']`                 | An array containing the opening and closing portion of the `generic` wrap.
`tex_block_wrap`  | [string] | `#!py ['\\[', '\\]']`                 | An array containing the opening and closing portion of the `generic` wrap.
`preview`         | bool     | `#!py3 True`                          | Insert a preview to show until MathJax finishes loading the equations.

!!! warning "Deprecation"
    `insert_as_script` have been deprecated in 4.6.0. If you are still setting this, it will do nothing.  This option will be removed in the future so it is strongly advised to stop setting them.

    MathJax is, and has always been the default, and now inserting as script is the default as it is the most reliable insertion format, and with the new way previews are inserted, there is no need for the old text conversion method. To output for other math libraries, like [KaTeX][katex], enable `generic`.

---8<--- "links.md"

---8<--- "mathjax.md"
