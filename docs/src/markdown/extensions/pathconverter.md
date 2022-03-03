[:octicons-file-code-24:][_pathconverter]{: .source-link }

# PathConverter

## Overview

PathConverter is an extension that can convert local, relative reference paths to absolute or relative paths for links
and images. It was originally written for a project that wanted to preview the markdown by rendering it in a temporary
location. This extension allowed the paths to be converted to work from the temporary location. This context is
important when trying to understand why this extension was created. It's actual usage is limited to situations like
this, so it isn't something that would get used in most normal scenarios.

PathConverter takes an absolute base path. The base path is the Markdown content's assumed location at time of
conversion.  The path is used as a reference for locating images and referenced files relative to the Markdown content.
Essentially, the references in the Markdown file would currently be relative to this base path at conversion time. The
references existence is not verified, but the it is analyze to determine if it is a relative path, and if so, it is
eligible for conversion. In the case of **absolute** mode, the relative Markdown references would be converted to
absolute paths.

If PathConverter is in **relative** mode, the extension will also need a relative path to convert to.  The relative path
must be an absolute path to the location the HTML is assumed to live after conversion.  If the references paths can be
confirmed to be relative, those references will be converted to relative paths that align to the provided relative path
parameter. The idea is that a Markdown file could be found in a location that is not meant to be its final location.
References within the Markdown source would link relative to the base path, but they would then be converted to be
relative to it's new location -- the relative path parameter.

Currently PathConverter will search desired tags for `href` and `src` attributes. By default, only `a`, `script`, `img`,
and `link` tags are searched.

PathConverter is also intelligent enough to only operate on the file portion of the reference link.  Consider the
following scenario:  `path/to/file.html#header-to-jump-to`.  In the example, `path/to/file.html` will be converted, but
`#header-to-jump-to` will be left unaltered.

As mentioned before, the use cases for something like this are limited, but if you have a situation that lends well to
something like this, PathConverter can help.

The PathConverter extension can be included in Python Markdown by using the following:

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.pathconverter'])
```

## Options

Option          | Type   | Default                     | Description
--------------- | ------ | --------------------------- |------------
`base_path`     | string | `#!py3 ''`                  | A string indicating an absolute base path to be used to find referenced files.
`relative_path` | string | `#!py3 ''`                  | A string indicating an absolute path that the references are to be relative to (not used when `absolute` is set `True`).
`absolute`      | bool   | `#!py3 False`               | Determines whether paths are converted to absolute or relative.
`tags`          | string | `#!py3 'a script img link'` | Tags (separated by spaces) that are searched to find `href` and `src` attributes.
`file_scheme`   | bool   | `#!py3 False`               | Produce file:// URLs instead of raw paths when converting paths to absolute.
