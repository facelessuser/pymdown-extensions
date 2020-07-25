[:octicons-file-code-24:][_snippets]{: .source-link }

# Snippets

## Overview

Snippets is an extension to insert markdown or HTML snippets into another markdown file.  Snippets is great for
situations where you have content you need to insert into multiple documents.  For instance, this document keeps all its
hyperlinks in a separate file.  Then includes those hyperlinks at the bottom of a document via snippets. If a link needs
to be updated, it can be updated in one location instead of updating them in multiple files.

Snippets is run as a preprocessor, so if a snippet is found in a fenced code block etc., it will still get processed.
This is great for including the current version of program code.  If the specified file cannot be found, the the markup
will be removed.  If you need to show a snippet example in fenced code, please escape it as listed in
[Snippets Notation](#snippets-notation).

Snippets can handle recursive file inclusion.  And if Snippets encounters the same file in the current stack, it will
avoid re-processing it in order to avoid an infinite loop (or crash on hitting max recursion depth).  Though it should
be said, you should extreme recursion depth as you will hit Python's recursion limit.

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

Snippets does not care what the extension or the content of the ASCII file is.  There are two modes of inserting snippets:
single line and block.

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

## Options

Option         | Type   | Default         | Description
-------------- | ------ | --------------- |------------
`base_path`    | string | `#!py3 '.'`     | A string indicating a base path to be used resolve snippet locations.
`encoding`     | string | `#!py3 'utf-8'` | Encoding to use when reading in the snippets.
`check_paths`  | bool   | `#!py3 false`   | Make the build fail if a snippet can't be found.

--8<-- "links.txt"
