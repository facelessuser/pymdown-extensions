---
icon: lucide/square-scissors
---
[:octicons-file-code-24:][_snippets]{: .source-link }

# Snippets

## Overview

/// warning | Not Meant for User Facing Sites
Snippets is intended for documentation/static content workflows and **must not** be used to render untrusted/user-supplied
content dynamically (public-facing sites, user comments, wikis, etc.).

**Security note:** enabling features like **URL Snippets** (`url_download`) can cause the renderer to make outbound HTTP
requests to arbitrary URLs (including localhost/internal networks), which can lead to SSRF-style risk in unsafe
deployments.

See [Security Considerations](#security-considerations) for details and concrete examples.
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

/// note
XML parsers are sensitive to dashes, so snippet syntax should use single dashes (`-8<-`) when placed within an XML.
///

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
The block format differs from the single format by requiring the content to be fenced between two `--8<--`. The start
and end `--8<--` must be on a line by themselves.

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
-   If you'd like to specify multiple blocks of extraction, separate each one with a `,`: `file.md:1:3,5:6`.

    Each line selection is evaluated independently of previous selections. Selections will be performed in the order
    they are specified. No additional separators (empty lines or otherwise) are inserted between selections, they are
    inserted exactly as specified.
-   Negative indexes can be used as well and will be converted to positive indexes based on the total number of lines
    in the snippet. If a snippet has 10 lines, then `-1` would correspond with line `10` and `-10` would correspond with
    line `1`.

    Be mindful of snippets with trailing, empty new lines at the end as those will be considered as well.

/// note
Lines are never specified with `0`. If `0` is used it will be clamped to `1`.
///

```
;--8<-- "file.md:4:6"

;--8<--
include.md::3
;--8<--
```

/// new | 10.13
Specifying multiple line selections separated with `,` and negative indexing was added in 10.13.
///

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
# ;--8<-- [start:func]
def my_function(var):
    pass
# ;--8<-- [end:func]
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


> [!warning] Symlinks
> Symlinks can be placed in the Snippets path and will be followed. If you do not want Snippets to follow Symlinks,
> do not place them in the restricted path.

## URL Snippets

URLs, if `url_download` is enabled, can also be used as snippets. Instead of using a file, simply specify a URL in
its place. By default, a max size for content is specified with `url_max_size` and a default timeout via `url_timeout`.
If either of these is set to zero, the limits will be ignored.

To pass arbitrary HTTP headers in every HTTP request use `url_request_headers`.

When a URL returns a 429 (Too Many Requests) status code, the extension will automatically retry the request with linear
backoff. The retry behavior can be configured with:

- `max_retries`: Maximum number of retry attempts (default: 3)
- `backoff_factor`: Backoff factor for retry attempts (default: 2)

For example, with default settings, the retry sequence would be:

- First retry: 2 seconds
- Second retry: 4 seconds
- Third retry: 6 seconds

If the server sends a `Retry-After` header (either a number of seconds or a date), that is used instead of the backoff
for that retry, as retrying sooner would only be rejected again. If the server asks for longer than the longest we would
wait on our own (`backoff_factor` times `max_retries`, 6 seconds with the default settings), there is no retry and the
snippet fails right away instead of waiting. This means that if `backoff_factor` is `0`, which never waits, a
`Retry-After` always fails right away.

Retrying blocks the build while it waits. The longest total time spent waiting on a single URL is
`backoff_factor * max_retries * (max_retries + 1) / 2` (12 seconds with the default settings). A URL that fails is only
requested once while processing a document, no matter how many times it is included, but each different URL that is rate
limited can wait this long. If that is too slow for your use case, lower `backoff_factor` or `max_retries`. Setting
`max_retries` to `0` disables retrying altogether.

/// warning | Nested Snippets
One thing to note though, if a snippet is included via a URL, all nested snippets within it must also be URLs. URL
snippets are not allowed to reference local snippet files.
///

/// new | New 10.16
`max_retries` and `backoff_factor` were introduced in 10.16.
///

/// new | New 13.1
`Retry-After` support was added in 13.1.
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
appended to every Markdown content. Each entry in the list is searched for relative to the `base_path` entries.

## Extending Snippets

/// new | New 13.1
///

Snippets is meant to be simple and predictable, so it does not try to support every way you might want to transform
included content. Instead, the preprocessor is split into steps that a third party extension can override to add its own
notation, or to change content as it is included.

For each snippet, the preprocessor does the following:

1. `parse_snippet_target(path)` splits the text that was specified, such as `file.md:1:5`, `file.md:1:2,8:9`, or
   `file.md:section`, into a target dictionary with the keys `path`, `start`, `end`, and `section`. It returns
   `#!py None` if there is no path. Override this to parse extra notation.
2. The snippet is found and read in. Before this happens, the dictionary is given two more keys, `snippet` (the path of
   the file, or the URL) and `is_url`.
3. `select_snippet_lines(lines, target)` picks out the requested lines or section (using `extract_lines` and
   `extract_section`).
4. `process_snippet_lines(lines, target)` is called with the selected lines. By default, it returns them unchanged.
   Override this to change the content.
5. Any snippets in those lines are then expanded in the same way, each getting its own turn through these steps.

/// warning | Lines Still Contain Snippet Notation
`process_snippet_lines` runs *before* snippets nested in the lines are expanded. This has two consequences:

- The lines contain the notation of any nested snippets. A change that rewrites text, such as a find and replace, can
  rewrite that notation, and the nested snippet will then be lost (or fail if `check_paths` is enabled), often with a
  confusing path. For example, renaming `details` to `summary` would change `--8<-- "details.md"` to
  `--8<-- "summary.md"`.
- Changes are not applied to the content of nested snippets, only to the lines of the snippet that included them. A
  nested snippet is changed only if it is given a change of its own.

`get_syntax_mask(lines, is_section)` returns a list with a boolean for every line, which is `#!py True` if the line is
snippet notation (including section markers, block markers, and the paths in between), so it can be skipped. Pass
`is_section` as `#!py target['section'] is not None`.
///

The following is an extension that adds a `rename` change to a snippet, which is used as
`--8<-- "file.md:section | rename old new"`. It leaves any notation alone.

```py
from pymdownx.snippets import SnippetExtension, SnippetPreprocessor


class RenamePreprocessor(SnippetPreprocessor):
    """Rename a term in included content."""

    def parse_snippet_target(self, path):
        """Parse the target, and the rename if there is one."""

        path, sep, spec = path.partition('|')
        target = super().parse_snippet_target(path.strip())
        if target is not None:
            target['rename'] = spec.split()[1:] if sep else None
        return target

    def process_snippet_lines(self, lines, target):
        """Rename the term, but not in snippet notation."""

        if not target['rename']:
            return lines
        old, new = target['rename']
        mask = self.get_syntax_mask(lines, target['section'] is not None)
        return [line if syntax else line.replace(old, new) for line, syntax in zip(lines, mask, strict=True)]


class RenameExtension(SnippetExtension):
    """Use the preprocessor that renames."""

    def extendMarkdown(self, md):
        """Register the extension."""

        self.md = md
        md.registerExtension(self)
        md.preprocessors.register(RenamePreprocessor(self.getConfigs(), md), 'snippet', 32)


def makeExtension(*args, **kwargs):
    """Return extension."""

    return RenameExtension(*args, **kwargs)
```

Hooks should return new lists, and should not modify the lines they are given in place.

## Security Considerations

Snippets is designed for documentation workflows and static content generation. It is **not** intended for use in
public-facing services that render untrusted/user-supplied Markdown dynamically.

### Why This Matters

When Snippets processes a directive as shown below, it will attempt to include the referenced content into the rendered
output.

```text
;--8<-- "some-target"
```

If **URL Snippets** are enabled via `url_download`, the renderer may download content from arbitrary URLs. In unsafe
deployments, this can cause the rendering environment to make outbound HTTP requests to attacker-chosen locations
(including localhost and internal networks), which can resemble SSRF-style behavior.

### Unsafe Example (Do Not Use With Untrusted Input)

If an attacker can influence Markdown content and `url_download` is enabled, they may be able to trigger requests such
as:

```text
;--8<-- "http://127.0.0.1:9999/"
```

### Safe Usage Guidance

If you use Snippets in public-facing CI, preview builds, or documentation pipelines:

- Treat untrusted contributions with caution (e.g., PRs from external contributors).
- Run builds in a sandbox/container with restrictive network/egress policies.
- Avoid enabling `url_download` unless you fully understand the risk and have appropriate isolation in place.
- Prefer static, trusted snippet sources whenever possible.

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
