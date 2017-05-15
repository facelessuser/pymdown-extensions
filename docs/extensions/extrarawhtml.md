# ExtraRawHTML

## Overview

Python Markdown provides an `extra` extension that has features similar to PHP Markdown Extra.  For reasons covered in [`pymdownx.extra`](./extra.md), PyMdown Extensions implements its own `extra` extension.  In order to accomplish this, Python Markdown's raw HTML parsing functionality, which is used to parse nested Markdown inside HTML blocks, had to be split out of the `extra` implementation.  Afterwards, it was decided expose it to allow people who maybe didn't want to use all of the features found in `extra`, but still wanted to use the parsing of nested Markdown inside of HTML blocks.  This is basically a wrapper around Python Markdown's `extra` extension's raw HTML parsing.  For more info see [Python Markdown's Extra documentation][nested-markdown].

--8<-- "links.md"
