## Overview

The Emoji extension adds support for inserting emojis via simple short names enclosed within colons: `:short_name:`.  This is accomplished by using a short name index to map easy to remember names to the Unicode data. The Unicode data is then converted into actual Unicode emoji characters and/or special HTML elements that represent the emoji.

There are a number of familiar emoji short name conventions that people may be aware of, and they differ slightly.  At the present, Emoji chooses to focus on two specific short name conventions. The first convention is from [Gemoji][gemoji] which is GitHub's open source solution that provides emojis in GFM.  The second is from [EmojiOne][emojione] which is another open source emoji solution.

The short name indexes simply provide easy to remember names mapped to the Unicode data. Custom emojis (like Gemoji's `:octocat:`) wold have no Unicode data associated with them and would only provide a long name.  While it may be thought that an index like Gemoji is only for GitHub emoji images, you could easily map EmojiOne images to the Gemoji short names and vice versa. You could even map [Twemoji][twemoji] images to EmojiOne if desired.

Emoji provides various output formats that take the Unicode data associated with a short name (or the short name itself in the case of a custom emoji) and generates an HTML output. Most hosted emoji images follow the same pattern and are named after their Unicode code points separated by hyphens (minus things like zero width joiners and variation selectors).  This is true with EmojiOne, GitHub, and Twemoji, to name a few.  The default output `to_png` could theoretically be used with the EmojiOne index to output valid PNG images for EmojiOne, GitHub, or Twemoji (assuming appropriate CDN or local source images were provided). With that said, some output formats may lend themselves better to assets that are available from a specific provider. For instance, EmojiOne provides SVG, PNG, and sprite assets, while others provide only PNG images.

As previously mentioned, short name indexes are sourced from EmojiOne's and Gemoji's latest official tags. The index contains the emoji names, shortnames, values, etc.; everything needed to insert Unicode emoji characters or specially crafted HTML elements.

!!! warning "EmojiOne and Gemoji licensing"
    PyMdown Extensions has no affiliation with EmojiOne or Gemoji.  The indexes generated from their sources are covered under their respective licensing.  When using their images or CSS, please see their licensing terms to ensure proper usage and attributions.

    EmojiOne: http://emojione.com/licensing/
    Gemoji: https://github.com/github/gemoji/blob/master/LICENSE

## Options

Option                      | Type       | Default              | Description
--------------------------- | ---------- | -------------------- | -----------
`emoji_index`               | function   | `emojione` index     | A function that returns the index to use when parsing `:short_name:` syntax. See [Default Emoji Indexes](#default-emoji-indexes) to see the provided indexes.
`emoji_generator`           | function   | `to_png` generator   | A function that takes the emoji info and constructs the desired emoji output. See [Default Emoji Generators](#default-emoji-generators) to see the provided generators.
`title`                     | string     | `#!python 'short'`   | Specifies the title format that is fed into the emoji generator function.  Can either be `long` which is the long description of the emoji, `short` which is the short name (`:short:`), or `none` which will simply pass `None`.
`alt`                       | string     | `#!python 'unicode'` | Specifies the format for the alt value that is passed to the emoji generator function. If `alt` is set to `short`, the short name will be passed to the generator.  If `alt` is set to `unicode` the Unicode characters are passed to the generator.  Lastly, if `alt` is set to `html_entity`, the Unicode characters are passed encoded as HTML entities.
`remove_variation_selector` | bool       | `#!python False`     | Specifies whether variation selectors should be removed from Unicode alt. Currently, only `fe0f` is removed as it is the only one presently found in the current emojis.
`options`                   | dictionary | `#!python {}`        | Options that are specific to emoji generator functions.  Supported parameters can vary from function to function.

!!! tip "Legacy GitHubEmoji Emulation"
    The Emoji extension was actually created to replace the now deprecated [GitHubEmoji](./githubemoji.md) extension. Emoji was written to be much more flexible.  If you have a desire to configure the output to be like the legacy GitHubEmoji extension, you can use the settings below. This shows the full setup. To learn more about the settings used, continue reading the documentation.

    ```python
    import pymdownx.emoji

    extension_configs = {
        "pymdownx.emoji": {
            "emoji_index": pymdownx.emoji.gemoji,
            "emoji_generator": pymdownx.emoji.to_png,
            "alt": "short",
            "options": {
                "attributes": {
                    "align": "absmiddle",
                    "height": "20px",
                    "width": "20px"
                },
                "image_path": "https://assets-cdn.github.com/images/icons/emoji/unicode/",
                "non_standard_image_path": "https://assets-cdn.github.com/images/icons/emoji/"
            }
        }
    }
    ```

## Default Emoji Indexes

By default, Emoji provides two indexes: `emojione` and `gemoji`.  Both indexes are generated from the most recent official release tag source. They can be used by passing in one of the two functions below via the `emoji_index` parameter.  Pass the actual function reference, not a string. If you need to create your own, just check out [Custom Emoji Indexes](#custom-emoji-generators).

`pymdownx.emoji.emojione`
: 
    This is the default function that is used and provides an index using the latest EmojiOne supported emojis (at the time of release).  You can always find out what tag it was built with by doing the following:

    ```python
    >>> import pymdownx.emoji1_db as e1db
    >>> e1db.version
    'v2.2.7'
    ```

`pymdownx.emoji.gemoji`
: 
    This function provides an index of the latest Gemoji supported emoji (at the time of release). You can always find out what tag it was built with by doing the following:

    ```python
    >>> import pymdownx.gemoji_db as gmdb
    >>> gmdb.version
    'v3.0.0'
    ```

## Default Emoji Generators

Emoji provides six default emoji generators.  All the generators can be used with the `emojione` index, but only two will work well with the `gemoji` index: `pymdownx.emoji.to_png` and `pymdownx.emoji.to_alt`. You can select a generator to use by passing in one of the functions below via the `emoji_generator` parameter.  Pass the actual function reference, not a string. If you need to create your own, just check out [Custom Emoji Generators](#custom-emoji-generators).

`pymdownx.emoji.to_png`
: 
    This is a general purpose generator and, by default, provides an EmojiOne CDN and GitHub CDN path(s).  The PNG output form is as follows:

    ```html
    <img alt="😄" class="emojione" src="https://cdn.jsdelivr.net/emojione/assets/png/1f604.png" title=":smile:" />
    ```

    **Generator Specific Options**

    Option                    | Type       | Default                        | Description
    ------------------------- | ---------- | ------------------------------ | -----------
    `classes`                 | string     | Name of the index used         | Specifies the class(es) to be used in the image element.
    `image_path`              | string     | CDN for the default index used | This can be either a local path or a CDN containing the assets.  By default, an appropriate CDN is provided for EmojiOne and Gemoji depending on which index is being used.
    `non_standard_image_path` | string     | CDN for the default index used | This can be either a local path, or a CDN containing the assets. Currently, only Gemoji's non-standard emojis take advantage of this as the GitHub CDN alters the path slightly for its non-Unicode emoji.  By default, an appropriate CDN is provided for Gemoji.
    `attributes`              | dictionary | `#!py {}`                      | A dictionary containing tag attributes as key value string pairs. The dictionary keys are the attribute names and dictionary values are the attribute values.

`pymdownx.emoji.to_svg`
: 
    This generator was written to output EmojiOne SVG images. The SVG image outputs as:

    ```html
    <img alt="😄" class="emojione" src="https://cdn.jsdelivr.net/emojione/assets/svg/1f604.svg" title=":smile:" />
    ```

    **Generator Specific Options**

    Option       | Type       | Default                   | Description
    ------------ | ---------- | ------------------------- | -----------
    `classes`    | string     | Name of the index used    | Specifies the class(es) to be used in the image element. The default will match the name of the index used.
    `image_path` | string     | A CDN for EmojiOne images | This can be either a local path or a CDN containing the assets.  By default, an appropriate CDN is provided for EmojiOne.
    `attributes` | dictionary | `#!py {}`                 | A dictionary containing tag attributes as key value string pairs. The dictionary keys are the attribute names and dictionary values are the attribute values.

`pymdownx.emoji.to_png_sprite`
: 
    This generator was written to support PNG sprite output for EmojiOne.  It is expected that this will be used in conjunction with the the official EmojiOne CSS.  You can include the CSS from the CDN in your document.  Example CDN for version 2.2.7: `https://cdnjs.cloudflare.com/ajax/libs/emojione/2.2.7/assets/sprites/emojione.sprites.css`. This outputs the emoji as a span in the form below.  The CSS will apply the appropriate mapping in the sprite PNG for the background image of the span.

    ```html
    <span class="emojione emojione-1f604" title=":smile:">😄</span>
    ```

    **Generator Specific Options**

    Option       | Type       | Default                | Description
    ------------ | ---------- | ---------------------- | -----------
    `classes`    | string     | Name of the index used | Class(es) used for the span where the classes are inserted as "class" in the following template: `#!py '%(class)s-%(unicode)s'`.
    `attributes` | dictionary | `#!py {}`              | A dictionary containing tag attributes as key value string pairs. The dictionary keys are the attribute names and dictionary values are the attribute values.

`pymdownx.emoji.to_svg_sprite`
: 
    This was written to support EmojiOne SVG sprite output.  The output form was taken directly from an example in the EmojiOne source.  It is expected that the the user will provide a local version of the official SVG sprite and the path to it.  The output is:

    ```html
    <svg class="emojione"><description>😄</description><use xlink:href="./../assets/sprites/emojione.sprites.svg#emoji-1f604"></use></svg>
    ```

    **Generator Specific Options**

    Option       | Type   | Default                | Description
    ------------ | ------ | ---------------------- | -----------
    `classes`    | string | Name of the index used | Class(es) to apply to the `svg` element where the classes are inserted as "class" in the following template: `#!py '%(class)s-%(unicode)s'`.
    `image_path` | string | `#!py ''`              | Path to the SVG sprites.

`pymdownx.emoji.to_awesome`
: 
    This generator is another EmojiOne specific output called [EmojiOne Awesome][emojione-awesome].  According to EmojiOne's documentation, it aims to give a font-awesome like interface for EmojiOne.  There isn't currently a CDN link that could be found, but you can provide the CSS in your project locally by [downloading it](emojione-awesome-css) from their repository.  The output format is:

    ```html
    <i class="e1a-smile"></i>
    ```

    **Generator Specific Options**

    Option       | Type       | Default      | Description
    ------------ | ---------- | ------------ | -----------
    `classes`    | string     | `#!py 'e1a'` | Class(es) to apply to the element where the classes are inserted as "class" in the following template: `#!py '%(class)s-%(shortname)s'`.
    `attributes` | dictionary | `#!py {}`    | A dictionary containing tag attributes as key value string pairs. The dictionary keys are the attribute names and dictionary values are the attribute values.

`pymdownx.emoji.to_alt`
: 
    This generator supports both Gemoji and EmojiOne.  The generator outputs the alt value directly to the document.  The output can be Unicode characters, HTML entities, or even just the short name depending on what the global setting of 'alt' is set to.

    ```html
    😃
    ```

    There are no generator specific options.

## Custom Emoji Indexes

In order to provide a custom index, the Emoji extension must be given a function that returns a suitable emoji index.  No parameters are passed to the function.  The function should simply return the custom index in the following format.

```python
emoji_index = {
    # Name is the name of the index.  This is passed into the emoji
    # generator functions and can be used to differentiate logic
    # for different indexes if required.
    "name": "myindex",

    # The actual index.  A dictionary of all the emoji.
    # Different emoji shortnames with the same Unicode data
    # can be mentioned under aliases.
    "emoji": {
        # Key is the short name.
        ":zero:": {

            # Name is the long name.
            "name": "keycap digit zero",

            # Unicode is the representation of the Unicode
            # code points with variations and joiners striped out.
            # This is used to reference pngs or svgs associated
            # with the emoji and can also sometimes be used as
            # part of special class names in the HTML output.
            #
            # Do not include this if the emoji is a custom,
            # non-Unicode emoji.
            "unicode": "0030-20e3",

            # This is the full Unicode code points and is
            # used for the "alt" attributes in the HTML output of images.
            # It is redundant to include this if it is the
            # same as 'unicode', but it won't hurt anything if it is.
            #
            # Do not include this if the emoji is a custom,
            # non-Unicode emoji.
            "unicode_alt": "0030-fe0f-20e3"
        },
        # No need to specify 'unicode_alt' as it is the same
        # as 'unicode'.
        ":thumbsup:": {
            "name": "thumbs up sign",
            "unicode": "1f44d"
        },
        # Should not specify any unicode fields
        # as this is not a real unicode emoji.
        ":octocat:": {
            "name": "octocat"
        },
    },
    # Short names that share previously defined Unicode data
    # like '+1' and 'thumbsup' etc.
    "aliases": {
        # Key is the alias.
        # Value is the short name it maps to in the
        # previously defined 'emoji' key.
        ":+1:": ":thumbsup:"
    }
}
```

## Custom Emoji Generators

Each different kind of output is controlled by a different emoji generator function, but all generator functions have the same format. The format is shown below in case you need to create your own custom output generator.

`#!py def emoji_generator(index, shortname, alias, uc, alt, title, options, md)`
: 

    Parameter   | Type       |Description
    ----------- | ---------- | ----------
    `index`     | string     | The name of the selected emoji index.
    `shortname` | string     | The current short name.  This may differ from the actual name used in a document as aliases get translated to the main short name.
    `alias`     | string     | If the name specified in the document was an alias, that alias will be set here, and the main short name will be found under `shortname`.  This will be `None` if the name used was not an alias.
    `uc`        | string     | This is a string of the Unicode values for the emoji.  This is used to reference emoji image names or for specifying class names etc., so it may not contain all the code points.  The string returned consists of each Unicode value represented as a hex value separated with hyphens.  Values such as U+200D ZERO WIDTH JOINER and  U+FE0F VARIATION SELECTOR-16 are stripped out.  So the value here will not always be practical for calculating the actual Unicode points of an emoji.  This will be `None` for non-standard emoji that are not Unicode.
    `alt`       | string     | This is the alternative emoji value (or fallback value).  Its format will differ depending on the extension setting `alt`.  This will be returned as either the Unicode characters, HTML entities, or the short name used.  See the `alt` setting for more info.
    `title`     | string     | This is the title that can be used in image elements.  Depending on the global extension setting `title`, this will either return the long name, the short name, or `None`.  See the `title` setting for more info.
    `options`   | dictionary | This is a dictionary to specify generator function specific options.  This can be anything, and it is up to the generator function to parse and provide defaults.
    `md`        | class      | This is the Markdown class object.  This is mainly used to access specific things needed from the Markdown class.  If you needed to stash your output, you would do something like: `md.htmlStash.store(alt, safe=True)`.

    !!! Warning "Non-Unicode emojis"
        Keep in mind that Gemoji ships with some non-standard emojis like `:octocat:` that do not have Unicode code points.  `uc` and `alt` are affected by this and will return `None` and the short name respectively instead of strings describing the Unicode points.  For example `:octocat:` will just return `None` for `uc` and `:octocat:` for `alt`.  If you are parsing an index with custom emojis, like Gemoji has, then you need to be aware of this.

## Using with MkDocs

This project uses these extensions with [MkDocs][mkdocs] to generate the documentation.  It might not be obvious how to set the index or generator functions in Mkdoc's YAML settings file, but it is actually pretty easy.  The functions are referenced like you would import them in Python except you also append them with a special prefix to let the YAML module know that the setting value is a Python object.  For instance, to specify the `to_svg` generator, you would simply reference it like this: `!!python/name:pymdownx.emoji.to_svg` (or you could use your own custom module).

```yaml
markdown_extensions:
  - pymdownx.emoji:
      emoji_generator: !!python/name:pymdownx.emoji.to_svg
```

## Emoji Index Updates

The Emoji extension might at times be behind on having indexes built from the latest repositories. We try to keep the indexes updated with new releases, but if they fall out of date, you can open an issue on the this project's issue page to alert the maintainer(s) and they will update them when someone gets a chance.  Pull requests are also welcome.  The process for updating the indexes is automated, so it is fairly easy to do for a pull request.  See [Generating Emoji Indexes](../development.md#generating-emoji-indexes) for more info.

## Examples

Current examples are all rendered with EmojiOne.

```
EmojiOne :smile: emojis are very useful :thumbsup:.

You can also escape `:` characters to escape the emoji: \:smile:.
```

EmojiOne :smile: emojis are very useful :thumbsup:.

You can also escape `:` characters to escape the emoji: \:smile:.

--8<-- "refs.md"
