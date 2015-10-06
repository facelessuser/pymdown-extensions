# PlainHtml {: .doctitle}
Strip down to plain HTML.

---

## Overview
PlainHtml is a simple extension that is run at the end of post-processing.  It searches the final output stripping things like `style`, `id`, `class`, and `on<name>` attributes from HTML tags.  It also removes HTML comments.  If you have no desire to see these, this can strip them out.  Though it does its best to be loaded at the very end of the process, it helps to include this one last when loading up your extensions.  If needed, plain HTML can also be configured to just strip out just comments or just attributes etc.

!!! Caution "Warning"
    This is not meant to be a sanitizer for HTML.  This is just meant to try and strip out style, script, classes, etc. to provide a plain HTML output for the times this is desired; this is not meant as a security extension.  If you want something to secure the output, you should consider running a sanitizer like [bleach](https://pypi.python.org/pypi/bleach).

## Options
By default, PlainHtml strips the following attributes: `style`, `id`, `class`, and `on<name>`.  PlainHtml also strips HTML comments. If desired, its behavior can be configured to strip less or even more, but it is limited to attributes and comments.  If you are using the [PyMdown app](https://github.com/facelessuser/PyMdown), and you want to control what gets stripped, you may want to forgo using the `--plain-html` option laid out in the [user guide](http://facelessuser.github.io/PyMdown/user-guide/general-usage/#plain-html) and just configure the plugin manually; the `--plain-html` option runs with the defaults only.

| Option    | Type | Default |Description |
|-----------|------|---------|------------|
| strip_comments | bool | True | Strip HTML comments during post process. |
| strip_js_on_attributes | bool | True | Strip JavaScript script attributes with the pattern on* during post process. |
| strip_attributes | string | 'id class style' | A string attribute names separated by spaces. |
