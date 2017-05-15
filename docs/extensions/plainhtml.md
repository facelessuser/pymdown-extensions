# PlainHTML

## Overview

PlainHTML is a simple extension that is run at the end of post-processing.  It searches the final output stripping things like `style`, `id`, `class`, and `on<name>` attributes from HTML tags.  It also removes HTML comments.  If you have no desire to see these, this can strip them out.  Though it does its best to be loaded at the very end of the process, it helps to include this one last when loading up your extensions.  If needed, plain HTML can also be configured to strip out just comments or just attributes etc.

Because comments aren't stripped until the end in a post-processing step, they are present throughout the entire Markdown conversion process and could possibly affect parsing, so be careful how you generally insert comments.

!!! caution "Warning"
    This is not meant to be a sanitizer for HTML.  This is just meant to try and strip out style, script, classes, etc. to provide a plain HTML output for the times this is desired; this is not meant as a security extension.  If you want something to secure the output, you should consider running a sanitizer like [Bleach][bleach].

## Options

By default, PlainHTML strips the following attributes: `style`, `id`, `class`, and `on<name>`.  PlainHTML also strips HTML comments. If desired, its behavior can be configured to strip less or even more, but it is limited to attributes and comments.

Option                   | Type   | Default                 |Description
------------------------ |------- | ----------------------- |-----------
`strip_comments`         | bool   | `#!py True`             | Strip HTML comments during post process.
`strip_js_on_attributes` | bool   | `#!py True`             | Strip JavaScript script attributes with the pattern on* during post process.
`strip_attributes`       | string | `#!py 'id class style'` | A string specifying attribute names separated by spaces.

## Examples

```
<!-- We are only allowing strip_comments and strip_js_on_attributes
     in this example. -->

Here is a test. You can verify the result by inspecting the code in your browser.
```

<!-- We are only allowing strip_comments and strip_js_on_attributes
     in this example. -->

Here is a test. You can verify the result by inspecting the code in your browser.

--8<-- "links.md"
