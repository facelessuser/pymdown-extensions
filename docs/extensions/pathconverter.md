# PathConverter {: .doctitle}
Relative and absolute path conversion.

---

## Overview
PathConverter is an extension that can convert paths to absolute or relative paths for links and images.  PathConverter takes a base path (an absolute path used as a reference for locating images and referenced files) and a relative path (an absolute path that the links will be relative to after conversion if not running in absolute mode) and then converts paths for the `href` and/or `src` attributes in `a`, `script`, `img`, and `link` tags.

PathConverter will only operate on file paths that can be confirmed to exist on the system it is run on.  Relative mode is the more useful mode as it can be used to render HTML for use in an actual website.

PathConverter is also intelligent enough to only operate on the file portion of the a path link.  Consider the following scenario:  `path/to/file.html#header-to-jump-to`.  In the example, `path/to/file.html` will be converted, but `#header-to-jump-to` will be left unaltered.

## Options

| Option    | Type | Default | Description |
|-----------|------|---------|-------------|
| base_path | string | '' | A string indicating an absolute base path to be used to find referenced files. |
| relative_path | string | '' | A string indicating an absolute path that the references are to be relative to (not used when `absolute` is set `True`). |
| absolute | bool | False | Determines whether paths are converted to absolute or relative. |
| tags | string | 'a script img link' | Tags (separated by spaces) that are searched to find `href` and `src` attributes. |
