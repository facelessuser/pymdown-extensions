# StripHTML

## Overview

StripHTML (formally known as PlainHTML) is a simple extension that is run at the end of post-processing.  It searches the final output stripping out unwanted comments and/or tag attributes. Though it does its best to be loaded at the very end of the process, it helps to include this one last when loading up your extensions.

!!! example "Strip Comment"

    ```
    <!-- We are only allowing strip_comments and strip_js_on_attributes
         in this example. -->

    Here is a <strong onclick="myFunction();">test</strong>.
    ```

    ```html
    <p>Here is a <strong>test</strong>.</p>
    ```

Because comments aren't stripped until the end in a post-processing step, they are present throughout the entire Markdown conversion process and could possibly affect parsing, so be careful how you generally insert comments.

!!! caution "Warning"
    This is not meant to be a sanitizer for HTML.  This is just meant to try and strip out style, script, classes, etc. to provide a plain HTML output for the times this is desired; this is not meant as a security extension.  If you want something to secure the output, you should consider running a sanitizer like [Bleach][bleach].

## Options

By default, StripHTML strips the following attributes: `style`, `id`, `class`, and `on<name>`.  StripHTML also strips HTML comments. If desired, its behavior can be configured to strip less or even more, but it is limited to attributes and comments.

Option                   | Type     | Default      | Description
------------------------ |--------- | ------------ | -----------
`strip_comments`         | bool     | `#!py3 True` | Strip HTML comments during post process.
`strip_js_on_attributes` | bool     | `#!py3 True` | Strip JavaScript script attributes with the pattern on* during post process.
`strip_attributes`       | [string] | `#!py3 []`   | A list of tag attribute names to strip.

!!! warning "Deprecation 4.6.0"
    StripHTML used to be known as `pymdownx.plainhtml`, but has been renamed to `pymdownx.striphtml`. The old `plainhtml` is still available. `plainhtml` treats `strip_attributes` as a string of attributes separated by spaces and has a default of `#!py3 "id style class"`.  It is encouraged to migrate to using `pymdownx.striphtml` as `pymdownx.plainhtml` will be removed in version 5.0.

--8<-- "links.md"
