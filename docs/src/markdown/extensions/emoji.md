[:octicons-file-code-24:][_emoji]{: .source-link }

# Emoji

## Overview

The Emoji extension adds support for inserting emoji via simple short names enclosed within colons: `:short_name:`.
This is accomplished by using a short name index to map easy to remember names to associated Unicode data. The Unicode
data is then converted into actual Unicode emoji characters and/or special HTML elements (usually images) that represent
the emoji.

!!! example "Emoji Example"

    === "Output"
        :smile: :heart: :thumbsup:

    === "Markdown"
        ```
        :smile: :heart: :thumbsup:
        ```

The Emoji extension can be included in Python Markdown by using the following:

```py3
import markdown
md = markdown.Markdown(extensions=['pymdownx.emoji'])
```

## Supported Emoji Providers

There are a number of emoji short name conventions that people may be aware of. These conventions are always tied to a
specific emoji set. These conventions differ because there is no official Unicode short name convention. At the present,
Emoji chooses to focus on three specific emoji sets:


=== "EmojiOne"
    [EmojiOne][emojione] (<img align="absmiddle" alt=":smile:" class="emojione" src="https://cdnjs.cloudflare.com/ajax/libs/emojione/2.2.7/assets/png/1f604.png" title=":smile:" /> <img align="absmiddle" alt=":heart:" class="emojione" src="https://cdnjs.cloudflare.com/ajax/libs/emojione/2.2.7/assets/png/2764.png" title=":heart:" /> <img align="absmiddle" alt=":thumbsup:" class="emojione" src="https://cdnjs.cloudflare.com/ajax/libs/emojione/2.2.7/assets/png/1f44d.png" title=":thumbsup:" />):
    EmojiOne is a high quality emoji set with support for gender and skin tone modifiers. Their free emoji set includes
    PNGs in sizes of 32x32, 64x64, and 128x128 which are all available via a CDN.

    The older EmojiOne (version 2.2.7), is what is used by default. It is the last truly free version. EmojiOne has
    rebranded with the name JoyPixels and now has an even more restrictive license for their graphical assets. Their
    latest short name list is still used for Twemoji as that portion is available under the MIT license via their
    toolkit repo @JoyPixels/emoji-toolkit.

=== "Twemoji"
    [Twemoji][twemoji] (<img align="absmiddle" alt=":smile:" class="twemoji" src="https://twemoji.maxcdn.com/v/latest/72x72/1f604.png" title=":smile:" /> <img align="absmiddle" alt=":heart:" class="twemoji" src="https://twemoji.maxcdn.com/v/latest/72x72/2764.png" title=":heart:" /> <img align="absmiddle" alt=":thumbsup:" class="twemoji" src="https://twemoji.maxcdn.com/v/latest/72x72/1f44d.png" title=":thumbsup:" />):
    Twemoji is Twitter's open source emoji set which also covers a great many emoji with skin tones and gender modifiers.
    The hosted CDN provides 72x72 PNG emoji or SVG emoji.

    While Gemoji and EmojiOne have a short name convention, Twemoji does not, and there are very few 3rd party projects
    that provide short names anywhere close to all the provided emoji that Twemoji supports. Since JoyPixels has an MIT
    licensed index of short names closest to what Twemoji supports, we use their short name list for Twemoji. There will
    be a reasonable attempt to patch in emoji not found in JoyPixels' index, but if JoyPixels is ever significantly
    behind, we may wait for JoyPixels to catch up.

=== "Gemoji"

    [Gemoji][gemoji] (<img align="absmiddle" alt=":smile:" class="gemoji" src="https://github.githubassets.com/images/icons/emoji/unicode/1f604.png" title=":smile:"/> <img align="absmiddle" alt=":heart:" class="gemoji"src="https://github.githubassets.com/images/icons/emoji/unicode/2764.png" title=":heart:"/> <img align="absmiddle" alt=":+1:" class="gemoji" src="https://github.githubassets.com/images/icons/emoji/unicode/1f44d.png" title=":+1:" />):
    Gemoji is GitHub's open source emoji solution. It contains a lot of common emoji and a couple special, non Unicode
    emoji (like Gemoji's `:octocat:` <img align="absmiddle" alt=":octocat:" class="gemoji" src="https://github.githubassets.com/images/icons/emoji/octocat.png" title=":octocat:" />).
    If you are a GitHub user, you are probably familiar with some of the short names associated with it. Their
    associated CDN contains the emoji in 75x75 PNG format.

!!! warning "Emoji Image Licensing"
    PyMdown Extensions has no affiliation with EmojiOne, Gemoji, or Twemoji.  The indexes generated from their sources
    are covered under their respective licensing.  When using their images or CSS, please see their licensing terms to
    ensure proper usage and attributions.

    === "EmojiOne"
        - https://github.com/joypixels/emoji-toolkit#joypixels-version-2
        - http://creativecommons.org/licenses/by/4.0/

    === "Twemoji"
        - https://github.com/twitter/twemoji/blob/gh-pages/LICENSE-GRAPHICS

    === "Gemoji"
        - https://github.com/github/gemoji/blob/master/LICENSE

All short name indexes that Emoji uses are generated from EmojiOne's or Gemoji's latest official source tag -- Twemoji
uses JoyPixels' index as the Twemoji repository does not ship with a short name index. The indexes contain the emoji
names, short names, values, etc.; everything needed to insert Unicode emoji characters or specially crafted HTML
elements.

## Emoji Output Formats

Depending on your needs, you may have different requirements for how emoji get displayed in your documents. You may want
to use PNG images, or maybe you really like SVG images. Maybe you just want to convert short names to the actual Unicode
code points.  There are a variety of ways you may want to output emoji, and the Emoji extension has you covered.

Emoji provides various output formats that take the Unicode data associated with a short name (or the short name itself
in the case of a custom emoji) and generates an HTML output. Not all of the provided output formats will work for each
emoji index, but there are a few that should work for all three. Check out
[Default Emoji Generators](#default-emoji-generators) or [Custom Emoji Generators](#custom-emoji-generators) to learn
more.

## Default Emoji Indexes

By default, Emoji provides three indexes: `emojione`, `gemoji`, and `twemoji`.  All indexes are generated from the most
recent official release tag source (in the case of Twemoji, short names are acquired from the generated index in
@JoyPixels/emoji-toolkit). They can be used by passing in one of the three functions below via the `emoji_index`
parameter.  Pass the actual function reference, not a string. If you need to create your own, just check out
[Custom Emoji Indexes](#custom-emoji-generators).

!!! tip
    If you are attempting to configure these options in a YAML based configuration (like in [MkDocs][mkdocs]), please
    see the [FAQ](../faq.md#function-references-in-yaml) to see how to specify function references in YAML.

=== "EmojiOne"

    ```
    pymdownx.emoji.emojione
    ```

    This is the default function that is used. EmojiOne was rebranded as JoyPixels and is no longer permissible
    enough to be used. The release used here is for 2.2.7 which is the last usable, truly free version of EmojiOne.
    Users are still required to comply with acknowledgments. JoyPixels 3.0+ graphical assets will not be supported
    moving forward as the license is too restrictive, tough the latest index of their friendly names is supported
    under the MIT license and is used to generate friendly, short names for Twemoji.

    You can always find out what tag it was built with by doing the following:

    ```pycon3
    >>> import pymdownx.emoji1_db as e1db
    >>> e1db.version
    'v2.2.7'
    ```

    To see the full list of short names for this index, see the index [source][emojione-index].

=== "Twemoji"
    ```
    pymdownx.emoji.twemoji
    ```

    This function provides an index of the latest Twemoji supported emoji (at the time of release).  The associated
    short names are currently borrowed from JoyPixels' index found in their @JoyPixels/emoji-toolkit repo. JoyPixels
    short name index is available under the MIT license and is used as Twemoji does not provide its own list of
    short names.

    There are a few emoji that are currently Twemoji specific, two of which are likely to always be as they are not
    part of the official emoji spec. The short names are listed below.

    ??? info "Twemoji Specific Emoji"
        Twemoji provides some non-standard emoji. We've made them available following the naming patterns that
        EmojiOne follows as we are using their short name index.

        The emoji are either some that only Twemoji supports, rarely supported by others, or emoji that have tone
        and/or gender modifiers that aren't supported in the Unicode specifications. We've also provided appropriate
        aliases for consistency with other like emoji.

        ```
        :pirate_flag:
        :shibuya:

        :skier_tone1:
        :skier_tone2:
        :skier_tone3:
        :skier_tone4:
        :skier_tone5:

        :woman_levitate:
        :woman_levitate_tone1:
        :woman_levitate_tone2:
        :woman_levitate_tone3:
        :woman_levitate_tone4:
        :woman_levitate_tone5:

        :woman_in_business_suit_levitating_tone1:
        :woman_in_business_suit_levitating_tone2:
        :woman_in_business_suit_levitating_tone3:
        :woman_in_business_suit_levitating_tone4:
        :woman_in_business_suit_levitating_tone5:

        :woman_in_tuxedo:
        :woman_in_tuxedo_tone1:
        :woman_in_tuxedo_tone2:
        :woman_in_tuxedo_tone3:
        :woman_in_tuxedo_tone4:
        :woman_in_tuxedo_tone5:

        :transgender_sign:
        :transgender_flag:
        ```

    You can always find out what tag it was built with by doing the following:

    ```pycon3
    >>> import pymdownx.twemoji_db as twdb
    >>> twdb.version
    'v12.1.3'
    >>> twdb.index_version
    '5.0.5'
    ```

    To see the full list of short names for this index, see the index [source][twemoji-index].

=== "Gemoji"
    ```
    pymdownx.emoji.gemoji
    ```

    This function provides an index of the latest Gemoji supported emoji (at the time of release).

    You can always find out what tag it was built with by doing the following:

    ```pycon3
    >>> import pymdownx.gemoji_db as gmdb
    >>> gmdb.version
    'v3.0.1'
    ```

    To see the full list of short names for this index, see the index [source][gemoji-index].

## Default Emoji Generators

Emoji provides six default emoji generators. PNG output and Unicode code point output are supported for all three
indexes. SVG output is only supported for Twemoji and the older 2.2.7 EmojiOne set. PNG sprites and the "Font Awesome"
like format are only supported by EmojiOne.  SVG sprites is only supported by the 2.2.7 EmojiOne.

You can select a generator to use by passing in one of the functions below via the `emoji_generator` parameter.  Pass
the actual function reference, not a string. If you need to create your own, just check out
[Custom Emoji Generators](#custom-emoji-generators).

!!! tip
    If you are attempting to configure these options in a YAML based configuration (like in [MkDocs][mkdocs]), please
    see the [FAQ](../faq.md#function-references-in-yaml) to see how to specify function references in YAML.

=== "PNG"

    ```
    pymdownx.emoji.to_png
    ```

    This is a general purpose generator which provides EmojiOne, GitHub, and Twemoji CDN path(s) out of the box.
    Depending on the index you've chosen, you the appropriate CDN will be provided.  If this ever gets out of date,
    a new CDN can be passed in via `image_path` and/or `non_standard_image_path`. EmojiOne actually has multiple
    PNGs sizes of 32, 64, and 128, but the default CDN path is the one for size 64:
    `https://cdnjs.cloudflare.com/ajax/libs/emojione/2.2.7/assets/png/64/`. You can change it for a larger or
    smaller PNG size by updating the size in the URL and passing the new URL in through `image_path`. The PNG output
    form is as follows:

    ```html
    <img alt="😄" class="emojione" src="https://cdnjs.cloudflare.com/ajax/libs/emojione/2.2.7/assets/png/64/1f604.png" title=":smile:" />
    ```

    **Generator Specific Options**

    Option                    | Type       | Default                        | Description
    ------------------------- | ---------- | ------------------------------ | -----------
    `classes`                 | string     | Name of the index used         | Specifies the class(es) to be used in the image element.
    `image_path`              | string     | CDN for the default index used | This can be either a local path or a CDN containing the assets.  By default, an appropriate CDN is provided for EmojiOne, Gemoji, and Twemoji depending on which index is being used.
    `non_standard_image_path` | string     | CDN for the default index used | This can be either a local path, or a CDN containing the assets. Currently, only Gemoji's non-standard emoji take advantage of this as the GitHub CDN alters the path slightly for its non-Unicode emoji.  By default, an appropriate CDN is provided for Gemoji.
    `attributes`              | dictionary | `#!py3 {}`                      | A dictionary containing tag attributes as key value string pairs. The dictionary keys are the attribute names and dictionary values are the attribute values.

=== "SVG"
    ```
    pymdownx.emoji.to_svg
    ```

    This generator was written to output SVG images and supports EmojiOne and Twemoji. EmojiOne's SVG support is only
    for the free 2.2.7 release, so the default CDN still references the 2.2.7 release. EmojiOne short names added after
    2.2.7 will not find images.  You can of course reference local SVG images as well by pointing `image_path` to them
    as well. The SVG image outputs as:

    ```html
    <img alt="😄" class="emojione" src="https://cdn.jsdelivr.net/emojione/assets/svg/1f604.svg" title=":smile:" />
    ```

    **Generator Specific Options**

    Option       | Type       | Default                   | Description
    ------------ | ---------- | ------------------------- | -----------
    `classes`    | string     | Name of the index used    | Specifies the class(es) to be used in the image element. The default will match the name of the index used.
    `image_path` | string     | A CDN for EmojiOne images | This can be either a local path or a CDN containing the assets.  By default, an appropriate CDN is provided for EmojiOne.
    `attributes` | dictionary | `#!py3 {}`                 | A dictionary containing tag attributes as key value string pairs. The dictionary keys are the attribute names and dictionary values are the attribute values.

=== "PNG Sprite"
    ```
    pymdownx.emoji.to_png_sprite
    ```

    This generator was written to support PNG sprite output for EmojiOne.  It is expected that this will be used in
    conjunction with the the official EmojiOne CSS.  You can include the CSS from the CDN in your document. The CSS
    comes in three sizes: 32, 64, 128. Make sure to set the correct size in the options to generate the appropriate
    classes.

    Example CDN for the 2.2.7 version with 64px PNGs:
    `https://cdnjs.cloudflare.com/ajax/libs/emojione/2.2.7/assets/sprites/emojione.sprites.css`.

    `to_png_sprite` outputs the emoji as a span in the form below.  The CSS will apply the appropriate mapping in the
    sprite PNG to the background image of the span.

    ```html
    <span class="emojione-64-people _1f604" title=":smile:">😄</span>
    ```

    **Generator Specific Options**

    Option       | Type       | Default                | Description
    ------------ | ---------- | ---------------------- | -----------
    `classes`    | string     | Name of the index used | Class(es) used for the span where the classes are inserted as "class" in the following template: `#!py3 '%(class)s-%(size)s-%(category)s _%(unicode)s'`.
    `size`       | int        | `#!py3 64`              | Integer specifying the size for the class above.
    `attributes` | dictionary | `#!py3 {}`              | A dictionary containing tag attributes as key value string pairs. The dictionary keys are the attribute names and dictionary values are the attribute values.

=== "SVG Sprite"
    ```
    pymdownx.emoji.to_svg_sprite
    ```

    This was written to support EmojiOne SVG sprite output.  The output form was taken directly from an example in the
    EmojiOne source.  It is expected that the the user will provide a local version of the official SVG sprite and the
    path to it.  Unfortunately there is no free 3.0 SVG sprite, so you will need to [download][emojione-sprites-svg] the
    old 2.27 one. The output is:

    ```html
    <svg class="emojione"><description>😄</description><use xlink:href="./../assets/sprites/emojione.sprites.svg#emoji-1f604"></use></svg>
    ```

    **Generator Specific Options**

    Option       | Type   | Default                | Description
    ------------ | ------ | ---------------------- | -----------
    `classes`    | string | Name of the index used | Class(es) to apply to the `svg` element where the classes are inserted as "class" in the following template: `#!py3 '%(class)s-%(unicode)s'`.
    `image_path` | string | `#!py3 ''`              | Path to the SVG sprites.

=== "Alt"
    ```
    pymdownx.emoji.to_alt
    ```

    This generator supports all emoji indexes.  The generator outputs the alt value directly to the document.  The
    output can be Unicode characters, HTML entities, or even just the short name depending on what the global setting of
    `alt` is set to.

    ```html
    😃
    ```

    There are no generator specific options.

## Custom Emoji Indexes

```py3
def emoji_index(options, md)
```

In order to provide a custom index, the Emoji extension must be given a function that returns a suitable emoji index.
The function should simply return the custom index. It accepts both on options dictionary and the markdown object. The
options object is the same object that is specified in in the extensions [settings](#options).

The index should be returned in the following format:

```py3
emoji_index = {
    # Name is the name of the index.  This is passed into the emoji
    # generator functions and can be used to differentiate logic
    # for different indexes if required.
    "name": "myindex",

    # The actual index.  A dictionary of all the emoji.
    # Different emoji short names with the same Unicode data
    # can be mentioned under aliases.
    "emoji": {
        # Key is the short name.
        ":zero:": {

            # Name is the long name.
            "name": "keycap digit zero",

            # Category of emoji.
            # Not needed if this is a non-Unicode, custom
            # emoji with no category
            "category": "symbol",

            # Unicode is the representation of the Unicode
            # code points, but it is not necessarily valid Unicode
            # code points. Essentially it is what represents the Unicode
            # and is used as the image name for pngs and svgs. Depending
            # on the index, it may not be code points alt all. It is also
            # sometimes used as part of special class names in the HTML
            # output (depending on the generator).
            #
            # In the case of Gemoji and EmojiOne this is the Unicode code
            # points with variations and joiners striped out. In the case of
            # Twemoji, it is usually full valid code points though leading
            # zeros are stripped from the beginning.
            #
            # Do not include this if the emoji is a custom, non-Unicode emoji.
            "unicode": "0030-20e3",

            # This is the full Unicode code points and is
            # used for the "alt" attributes in the HTML output of images.
            # It is redundant to include this if it is the
            # same as 'unicode', but it won't hurt anything if it is.
            #
            # Do not include this if the emoji is a custom,
            # non-Unicode emoji. This shows a fully qualified emoji code,
            # but it could just as easily be "0030-2033" which is also valid.
            # Some indexes will provide fully qualified, some may not.
            "unicode_alt": "0030-fe0f-20e3"
        },
        # No need to specify 'unicode_alt' as it is the same
        # as 'unicode'.
        ":thumbsup:": {
            "name": "thumbs up sign",
            "unicode": "1f44d",
            "category": "people"
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

!!! new "New 7.1"
    Emoji indexes now accept `options` and `md`. The old sans argument format will still be accepted, but in the future
    the arguments will be expected.

## Custom Emoji Generators

```py3
def emoji_generator(index, shortname, alias, uc, alt, title, category, options, md)
```

Each different kind of output is controlled by a different emoji generator function, but all generator functions have
the same input format. The options object is the same object that is specified in in the extensions [settings](#options)
and is shared with the index as well.

Parameter   | Type       |Description
----------- | ---------- | ----------
`index`     | string     | The name of the selected emoji index.
`shortname` | string     | The current short name.  This may differ from the actual name used in a document as aliases get translated to the main short name.
`alias`     | string     | If the specified short name is an alias, that alias will be set here, and the main short name will be found under `shortname`.  This will be `None` if the name used was not an alias.
`uc`        | string     | This is a string representation of the Unicode, it could technically be anything as this is normally used to reference image files. So while some indexes will have this be code points, it may not contain code points at all or it may strip out code points for simpler image names. So the value here will not always be practical for calculating the actual Unicode points of an emoji.  This will be `None` for non-standard emoji that are not Unicode.
`alt`       | string     | This is the alternative emoji value (or fallback value).  Its format will differ depending on the extension setting `alt` and also the index being used. This will be returned as either the full valid Unicode characters or HTML entities, or it will be the short name used.  See the `alt` setting for more info.
`title`     | string     | This is the title that can be used in image elements.  Depending on the global extension setting `title`, this will either return the full long description, the short name, or `None`.  See the `title` setting for more info.
`category`  | string     | Category of the emoji, or `None` if there is no category for the emoji.
`options`   | dictionary | This is a dictionary to specify generator and index function specific options.  This can be anything, and it is up to the generator function and the index function to parse relevant options and provide defaults.
`md`        | class      | This is the Markdown class object.  This is mainly used to access specific things needed from the Markdown class when formatting your output.  If you needed to stash your output, you would do something like: `#!py3 md.htmlStash.store(alt, safe=True)`.

!!! warning "Non-Unicode emoji"
    Keep in mind that Gemoji ships with some non-standard emoji like `:octocat:` that do not have Unicode code
    points.  `uc` and `alt` are affected by this and will return `None` and the short name respectively instead of
    strings describing the Unicode points.  For example `:octocat:` will just return `None` for `uc` and `:octocat:`
    for `alt`.  If you are parsing an index with custom emoji, like Gemoji has, then you need to be aware of this.

## Using with MkDocs

This project uses these extensions with [MkDocs][mkdocs] to generate the documentation.  It might not be obvious how to
set the index or generator functions in MkDocs' YAML settings file, but it is actually pretty easy.  The functions are
referenced like you would import them in Python except you also append them with a special prefix to let the YAML module
know that the setting value is a Python object.  For instance, to specify the `to_svg` generator, you would simply
reference it like this: `#!yaml !!python/name:pymdownx.emoji.to_svg` (or you could use your own custom module :wink:).

```yaml
markdown_extensions:
  - pymdownx.emoji:
      emoji_generator: !!python/name:pymdownx.emoji.to_svg
```

## Emoji Index Updates

The Emoji extension might at times be behind on having indexes built from the latest repositories. We try to keep the
indexes updated with new releases, but if they fall out of date, you can open an issue on the this project's issue page
to alert the maintainer(s) and they will update them when someone gets a chance.  Pull requests are also welcome.  The
process for updating the indexes is automated, so it is fairly easy to do a pull request.  See
[Generating Emoji Indexes](../about/development.md#generating-emoji-indexes) for more info.

## Options

Option                      | Type       | Default              | Description
--------------------------- | ---------- | -------------------- | -----------
`emoji_index`               | function   | `emojione` index     | A function that returns the index to use when parsing `:short_name:` syntax. See [Default Emoji Indexes](#default-emoji-indexes) to see the provided indexes.
`emoji_generator`           | function   | `to_png` generator   | A function that takes the emoji info and constructs the desired emoji output. See [Default Emoji Generators](#default-emoji-generators) to see the provided generators.
`title`                     | string     | `#!py3thon 'short'`   | Specifies the title format that is fed into the emoji generator function.  Can either be `long` which is the long description of the emoji, `short` which is the short name (`:short:`), or `none` which will simply pass `None`.
`alt`                       | string     | `#!py3thon 'unicode'` | Specifies the format for the alt value that is passed to the emoji generator function. If `alt` is set to `short`, the short name will be passed to the generator.  If `alt` is set to `unicode` the Unicode characters are passed to the generator.  Lastly, if `alt` is set to `html_entity`, the Unicode characters are passed encoded as HTML entities.
`remove_variation_selector` | bool       | `#!py3thon False`     | Specifies whether variation selectors should be removed from Unicode alt. Currently, only `fe0f` is removed as it is the only one presently found in the current emoji sets.
`options`                   | dictionary | `#!py3thon {}`        | Options that are specific to emoji generator functions.  Supported parameters can vary from function to function.

!!! new "New 7.1"
    `options` is now shared between index and generator functions opposed to being passed to the generator function
    only. The generator and/or index function should decide which of the arguments are relevant for its usage and parse
    accordingly.

!!! tip "Legacy GitHubEmoji Emulation"
    The Emoji extension was actually created to replace the now retired GitHubEmoji extension. Emoji was written to be
    much more flexible.  If you have a desire to configure the output to be like the legacy GitHubEmoji extension, you
    can use the settings below. This shows the full setup. To learn more about the settings used, continue reading the
    documentation.

    ```py3
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

--8<-- "refs.txt"
