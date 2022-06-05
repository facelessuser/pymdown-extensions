[:octicons-file-code-24:][_snippets]{: .source-link }

# Snippets

## Overview

Snippets is an extension to insert markdown or HTML snippets into another markdown file.  Snippets is great for
situations where you have content you need to insert into multiple documents.  For instance, this document keeps all its
hyperlinks in a separate file and then includes those hyperlinks at the bottom of a document via Snippets. If a link
needs to be updated, it can be updated in one location instead of updating them in multiple files.

Snippets is run as a preprocessor, so if a snippet is found in a fenced code block etc., it will still get processed.

If when a snippet declaration is processed, and the specified file cannot be found, then the markup will be removed.
If you need to show a snippet example in fenced code, please escape it as listed in
[Snippets Notation](#snippets-notation).

Snippets can handle recursive file inclusion.  And if Snippets encounters the same file in the current stack, it will
avoid re-processing it in order to avoid an infinite loop (or crash on hitting max recursion depth).

This is meant for simple file inclusion, it has no intention to implement features from complex template systems. If you
need something more complex, you may consider using a template environment to process your files **before** feeding them
through Python Markdown.  If you are using a document generation system, this can likely be performed via a plugin for
that document system (assuming a plugin environment is available).

The Snippets extension can be included in Python Markdown by using the following:

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.snippets'])
```

## Specifying Snippet Locations

All snippets are specified relative to the base path(s) specified in the `base_path` option. `base_path` is a list of
paths (though it will take a single string for legacy purposes).

When evaluating paths, they are done in the order specified. The specified snippet will be evaluated against each base
path and the first base path that yields a valid snippet will be returned.

If a base path is a file, the specified snippet will be compared against the base name of that file. For instance, if
we specified a snippet of `test.md` and we had a `base_path` of `#!py3 ["some/location/test.md"]`, this would match.
A specified snippet of `location/test.md` would not match. This is great if you have a one off file outside of your
base directory, but you'd like to directly include it.

## URL Snippets

URLs, if `url_download` is enabled, can also be used as snippets. Instead of using a file, simply specify a URL in
its place. By default, a max size for content is specified with `url_max_size` and a default timeout via `url_timeout`.
If either of these is set to zero, the limits will be ignored.

!!! warning "Nested Snippets"
    One thing to note though, if a snippet is included via a URL, all nested snippets within it must also be URLs. URL
    snippets are not allowed to reference local snippet files.

!!! new "New 9.5"
    URL snippet support was introduced in 9.5.

## Snippets Notation

There are two modes of inserting snippets: single line and block. Single line mode accepts a single file name, and block
accepts multiple files. Snippets does not require a specific extension, and as long as a valid file name is specified,
it will attempt to process it.

Single line format is done by placing the following markup for the single line notation:

<pre><code>--8&lt;-- "filename.ext"</code></pre>

Or you can insert multiple files with block notation:

<pre><code>--8&lt;--
filename.md
filename.log
--8&lt;--</code></pre>

As you can see, the notation is ASCII scissors cutting a line followed by the file name.  In the case of the single line
variant, the file name follows directly after the scissors and is quoted.  In the case of the block format, the file
names follow on separate lines and an additional scissor is added afterwards to signal the end of the block.

The dashes can be as few as 2 (`--8<--`) or longer if desired (`---8<---------`); whatever your preference is.  The
important thing is that the notation must reside on a line(s) by itself, and the path must be quoted in the case of the
single line notation.  If the file name is indented, the content will be indented to that level as well.  To reduce
confusion in block format, it is advised to ensure the entire block is indented to the same level.  If you need to
escape the syntax, just make sure a minimum of a space is after the quoted file name for single line format, or a space
after the start or end block markers in block format.

<pre><code>--8&lt;-- "escaped notation"&lt;space&gt;

--8&lt;--&lt;space&gt;
escaped notation
--8&lt;--&lt;space&gt;</code></pre>

If you have a file you want to temporarily ignore, you can comment it out by prepending the path with `; ` (notice the
semicolon is followed by a space).  This works for both single line and block format:

<pre><code>--8&lt;-- "; skip.md"

--8&lt;--
include.md
; skip.md
--8&lt;--</code></pre>

## Formatting Snippets

When inserting your snippet, it is important to remember that some snippets may need whitespace around them.

<pre><code>This is the file that is including the snippet.
We want blank lines before and after the insertion:

--8&lt;-- "insert.md"

So we put blank lines around the insertion.</code></pre>

In block format, it is important to note that empty lines are preserved for formatting:

<pre><code>--8&lt;--
file1.md

file2.md
--8&lt;--</code></pre>

## Auto-Append Snippets

Snippets is designed as a general way to target a file and inject it into a given Markdown file, but some times,
especially when building documentation via a library like [MkDocs][mkdocs], it may make sense to provide a way to append
a given file to *every* Markdown document without having to manually include them via Snippet syntax in each page. This
is especially useful for including a page of reference links or abbreviations on every page.

Snippets provides an `auto_append` option that allows a user to specify a list of files that will be automatically
appended to every to Markdown content. Each entry in the list searched for relative to the `base_path` entries.

## Options

Option         | Type        | Default          | Description
-------------- | ----------- | ---------------- |------------
`base_path`    | \[string\]  | `#!py3 ['.']`    | A list of strings indicating base paths to be used resolve snippet locations. For legacy purposes, a single string will also be accepted as well. Base paths will be resolved in the order they are specified. When resolving a file name, the first match wins. If a file name is specified, the base name will be matched.
`encoding`     | string      | `#!py3 'utf-8'`  | Encoding to use when reading in the snippets.
`check_paths`  | bool        | `#!py3 False`    | Make the build fail if a snippet can't be found.
`auto_append`  | \[string]\] | `#!py3 []`       | A list of snippets (relative to the `base_path`) to auto append to the Markdown content.
`url_download` | bool        | `#!py3 False`    | Allows URLs to be specified as file snippets. URLs will be downloaded and inserted accordingly.
`url_max_size` | int         | `#!py3 33554432` | Sets an arbitrary max content size. If content length is reported to be larger, and exception will be thrown. Default is ~32 MiB.
`url_timeout`  | float       | `#!py3 10.0`     | Passes an arbitrary timeout in seconds to URL requestor. By default this is set to 10 seconds.
