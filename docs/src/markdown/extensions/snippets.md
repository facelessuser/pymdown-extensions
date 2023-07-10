[:octicons-file-code-24:][_snippets]{: .source-link }

# Snippets

## Overview

/// warning | Not Meant for User Facing Sites
Snippets is meant to make including snippets in documentation easier, but it should not be used for user facing sites
that take and parse user content dynamically.
///

Snippets is an extension to insert markdown or HTML snippets into another markdown file.  Snippets is great for
situations where you have content you need to insert into multiple documents.  For instance, this document keeps all its
hyperlinks in a separate file and then includes those hyperlinks at the bottom of a document via Snippets. If a link
needs to be updated, it can be updated in one location instead of updating them in multiple files.

Snippets is run as a preprocessor, so if a snippet is found in a fenced code block etc., it will still get processed.

If a snippet declaration is processed, and the specified file cannot be found, then the markup will be removed.

Snippets can handle recursive file inclusion. And if Snippets encounters the same file in the current stack, it will
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

## Snippets Notation

There are two modes of inserting snippets: single line and block. Single line mode accepts a single file name, and block
accepts multiple files. Snippets does not require a specific extension, and as long as a valid file name is specified,
it will attempt to process it.

Snippets paths are relative to base location, by default the current working directory. You can specify a new base
location by setting the `base_path`. You can even allow downloading snippets from external locations. To learn more,
check out ["Specifying Snippet Locations"](#specifying-snippet-locations) and ["URL Snippets"](#url-snippets).

### Single Line Format

Single line format is done by placing the following markup for the single line notation:

```
;--8<-- "filename.ext"
```

As you can see, the notation is ASCII scissors cutting a line followed by the file name.  In the case of the single line
variant, the file name follows directly after the scissors and is quoted.  In the case of the block format, the file
names follow on separate lines and an additional scissor is added afterwards to signal the end of the block.

The dashes can be as few as 1 (`-8<-`) or longer if desired (`---8<---------`); whatever your preference is.  The
important thing is that the notation must reside on a line(s) by itself, and the path, must be quoted in the case of the
single line notation.  If the file name is indented, the content will be indented to that level as well.

You can temporarily disable the snippet by placing a `;` before the file name:

```
;--8<-- "; skip.md"
```

### Block Format

The second approach is known as the block format. Block format allows you to insert multiple files.

```
;--8<--
filename.md
filename.log
;--8<--
```
The block format differs from the single format by requiring the the content to be fenced between two `--8<--`. The
start and end `--8<--` must be on a line by themselves.

When using the block format empty lines are also preserved within the block. Consider the example below.

```
;--8<--
fileA.md

fileB.md
;--8<--
```

This would yield:

```
Content of file A.

Content of file B.
```

If you have a file you want to temporarily ignore, you can comment it out by placing a `;` at the start of the line.

```
;--8<--
include.md
; skip.md
;--8<--
```

### Snippet Lines

/// new | New 9.6
///

When specifying a snippet, you can specify which lines of the Snippet file that you wish to include. To specify line
numbers, simply append the start and/or end to the end of the file name with each number separated with `:`.

-   To specify extraction of content to start at a specific line number, simply use `file.md:3`.
-   To extract all content up to a specific line, use `file.md::3`. This will extract lines 1 - 3.
-   To extract all content starting at a specific line up to another line, use `file.md:4:6`. This will extract lines
  4 - 6.

```
;--8<-- "file.md:4:6"

;--8<--
include.md::3
;--8<--
```

### Snippet Sections

/// new | New 9.7
///

Specifying snippet lines may not always be ideal. The source could change by moving, adding, and/or removing lines. A way
around this is to partition a snippet into named sections and then targeting a specific section to be included instead
of specific line numbers.

Snippet sections can be specified by surrounding a block of text with `--8<-- [start:name]` and `--8<-- [end:name]`.
Then a file can simply specify the snippet using the name instead of line numbers.

```
;--8<-- "include.md:name"

;--8<--
include.md:name
;--8<--
```

Unlike other snippet syntax, the section start and end syntax do not have to be on a line by themselves. This allows
you to embed them in comments depending on the file type. When a section is included, the line with the start and end
are always omitted.

If we wanted to include a function from a Python source, we could specify the snippet as follows:

```python
# --8<-- [start:func]
def my_function(var):
    pass
# --8<-- [end:func]
```

And then just include it in our document:

```
;--8<-- "example.py:func"
```

### Escaping Snippets Notation

/// new | New 9.6
///

If it is necessary to demonstrate the snippet syntax, an escaping method is required. If you need to escape snippets,
just place a `;` right before `-8<-`. This will work for both single line and block format. An escaped snippet
notation will be passed through the Markdown parser with the first `;` removed.


````text title="Escaped Snippets"
```
;;--8<-- "escaped.md"
;;;--8<-- "escaped.md"
```
````

/// html | div.result
```
;--8<-- "escaped.md"
;;--8<-- "escaped.md"
```
///

/// warning | Legacy Escaping
The legacy escape method required placing a space at the end of the line with `-8<-`, while this should still
work, this behavior will be removed at sometime in the future and is discouraged.
///

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

To pass arbitrary HTTP headers in every HTTP request use `url_request_headers`.

/// warning | Nested Snippets
One thing to note though, if a snippet is included via a URL, all nested snippets within it must also be URLs. URL
snippets are not allowed to reference local snippet files.
///

/// new | New 9.5
URL snippet support was introduced in 9.5.
///

## Dedent Subsections

/// new | New 9.10
///

/// warning | Experimental
///

By default, when a subsection is extracted from a file via the [section notation](#snippet-sections) or the
[lines notation](#snippet-lines), the content is inserted exactly how it is extracted. Unfortunately, sometimes you are
extracting an indented chunk, and you do not intend for that chunk to be indented.

`dedent_subsections` is a recent option that has been added to see if it alleviates the issue. When specifying a
subsection of a file to insert as a snippet, via "sections" or "lines", that content will have all common leading
whitespace removed from every line in text.

Depending on how the feature is received, it may be made the default in the future.

## Auto-Append Snippets

Snippets is designed as a general way to target a file and inject it into a given Markdown file, but some times,
especially when building documentation via a library like [MkDocs][mkdocs], it may make sense to provide a way to append
a given file to *every* Markdown document without having to manually include them via Snippet syntax in each page. This
is especially useful for including a page of reference links or abbreviations on every page.

Snippets provides an `auto_append` option that allows a user to specify a list of files that will be automatically
appended to every to Markdown content. Each entry in the list searched for relative to the `base_path` entries.

## Options

Option                 | Type            | Default          | Description
---------------------- | --------------- | ---------------- |------------
`base_path`            | \[string\]      | `#!py3 ['.']`    | A list of strings indicating base paths to be used resolve snippet locations. For legacy purposes, a single string will also be accepted as well. Base paths will be resolved in the order they are specified. When resolving a file name, the first match wins. If a file name is specified, the base name will be matched.
`encoding`             | string          | `#!py3 'utf-8'`  | Encoding to use when reading in the snippets.
`check_paths`          | bool            | `#!py3 False`    | Make the build fail if a snippet can't be found.
`auto_append`          | \[string\]      | `#!py3 []`       | A list of snippets (relative to the `base_path`) to auto append to the Markdown content.
`url_download`         | bool            | `#!py3 False`    | Allows URLs to be specified as file snippets. URLs will be downloaded and inserted accordingly.
`url_max_size`         | int             | `#!py3 33554432` | Sets an arbitrary max content size. If content length is reported to be larger, and exception will be thrown. Default is ~32 MiB.
`url_timeout`          | float           | `#!py3 10.0`     | Passes an arbitrary timeout in seconds to URL requestor. By default this is set to 10 seconds.
`url_request_headers`  | {string:string} | `#!py3 {}`       | Passes arbitrary headers to URL requestor. By default this is set to empty map.
`dedent_subsections`   | bool            | `#!py3 False`    | Remove any common leading whitespace from every line in text of a subsection that is inserted via "sections" or by "lines".
`restrict_base_path`   | bool            | `#!py True`      | Ensure that the specified snippets are children of the specified base path(s). This prevents a path relative to the base path, but not explicitly a child of the base path.
