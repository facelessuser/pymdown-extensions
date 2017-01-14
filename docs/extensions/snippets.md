## Overview

Snippets is an extension to insert markdown or HTML snippets into another markdown file. This is done by placing the following markup: `--8<-- "filename.md"`.  As you can see, the notation is an ASCII scissor cutting a line followed by the file name.  The dashes can be as few as 2 (`--8<--`) or longer if desired (`---8<---------`); whatever your preference is.  The important thing is that it must reside on a line by itself, and the path must be quoted.  If it is indented, the content will be indented to that level as well.  If you need to escape the syntax, just make sure a minimum of a space is after the quoted file name.

Snippets can also handle recursive file inclusion.  And if Snippets encounters the same file in the current stack, it will avoid re-processing it in order to avoid an infinite loop (or crash on hitting max recursion depth).

Snippets is run as a preprocessor, so if a snippet is found in a fenced code block etc., it will still get processed.  If the specified file cannot be found, the the markup will be removed.

Snippets is great for situations where you have content you need to insert into multiple documents.  For instance, this document keeps all its hyperlinks in a separate file.  Then includes it at the bottom of a document that uses one or more of the links. If a link needs to be updated, it can be updated in one location.

## Options

Option      | Type   | Default        | Description
----------- | ------ | -------------- |------------
`base_path` | string | `#!py '.'`     | A string indicating a base path to be used resolve snippet locations.
`encoding`  | string | `#!py 'utf-8'` | Encoding to use when reading in the snippets.

## Examples

Assuming you have a snippet named `my_snippet.md`, and the content of `my_snippet.md` is as follows:

```
A snippet
```

Also assuming a base path that points to a folder where both your markdown and your snippet both reside. We can enter this content to load our snippet.

```
Here we will include a snippet.

--8<-- "my_snippet.md" 

```

The result will be:

```
Here we will include a snippet.

A snippet

```
