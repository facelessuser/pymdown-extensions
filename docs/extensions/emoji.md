# Emoji {: .doctitle}
Easy emoji insertion.

---

# Overview
The Emoji extension adds support for inserting emojis or special emoji tags linked to images that are either local or on a CDN via the syntax `:emoji:`.  Currently the Emoji extension adds support for two different emoji syntax short names. The first index is from [Gemoji](https://github.com/github/gemoji).  Gemoji is Github's open source solution that provides emojis in GFM.  The second is from [EmojiOne](https://github.com/Ranks/emojione) which is another open source emoji solution.

An emoji index is built for Gemoji and EmojiOne from the respective repository sources.  The index contains the emoji's names, shortnames, values, etc.; everything needed to insert emoji or specially crafted HTML elements to reference emoji images.

!!! warning "EmojiOne and Gemoji licensing"
    Pymdownx-extensions has no affiliation with EmojiOne or Gemoji.  The indexes generated from their sources are covered under their respective licensing.  When using their images or CSS, please see their licensing terms to ensure proper usage and attributions.

    EmojiOne: http://emojione.com/licensing/
    Gemoji: https://github.com/github/gemoji/blob/master/LICENSE

## Options
| Option    | Type | Default |Description |
|-----------|------|---------|------------|
| emoji_index | function | pymdownx.emoji.emojione | A function that returns the index to use when parsing `:emoji:` syntax. See [Default Emoji Indexes](#default-emoji-indexes) to see the provided indexes. |
| emoji_generator | function | pymdownx.emoji.to_png | A function that takes the emoji info and constructs the desired emoji ouput. See [Default Emoji Generators](#default-emoji-generators) to see the provided generators. |
| title | str | 'short' | Specifies the title format that is fed into the emoji generator function.  Can either be `long` which is the long description of the emoji, `short` which is the short name (`:short:`), or `none` which will simply pass `None`. |
| alt | str | 'unicode' | Specifies the format for the alt value that is passed to the emoji generator function. If `alt` is set to `short`, the short name will be passed to the generator.  If `alt` is set to `unicode` the Unicode characters are passed to the generator.  Lastly, if `alt` is set to `html_entity`, the Unicode characters are passed encoded as an HTML entities. |
| remove_variation_selector | bool | False | Specifies whether variation selectors should be removed from Unicode alt. Currently only `fe0f` is searched and removed as it is the only one presently found in the current emojis. |
| options | dict | \{} | Options that are specific to emoji generator functions.  Actually supported parameters can vary from function to function. |

!!! tip "Legacy GithubEmoji Emulation"
    The Emoji extension was actually created to replace the now deprecated [githubemoji](./githubemoji.md) extension. Emoji was written to be much more flexible.  If you have a desire to configure the output to be like the legacy githubemoji extension, you can use the settings below. To learn more about settings, read on through the documentation.

    ```python
    import pymdownx.emoji

    github_emulation_parameters = {
        "emoji_index": pymdownx.emoji.gemoji,
        "emoji_generator": pymdownx.emoji.to_png,
        "alt": "short",
        "options": {
            "attributes": {
                "align": "absmiddle",
                "height": "20px",
                "width": "20px"
            }
        }
    }
    ```

## Default Emoji Indexes
By default, Emoji provides two indexes: `emojione` and `gemoji`.  Both indexes are generated from the most recent official release tag source. They can be used by passing in one of the two functions below via the `emoji_index` parameter.  Pass the actual function reference, not a string. If you need to create your own, just check out [Custom Emoji Indexes](#custom-emoji-generators).

pymdownx.emoji.emojione
: 
    This is the default index used and provides an index using the latest EmojiOne supported emojis (at the time of release).  You can always find out what tag it was built with by doing the following:

    ```python
    >>> import pymdownx.emoji1_db as e1db
    >>> e1db.version
    'v2.2.7'
    ```

pymdownx.emoji.gemoji
: 
    This provides an index of the latest Gemoji supported emoji (at the time of release). You can always find out what tag it was built with by doing the following:

    ```python
    >>> import pymdownx.gemoji_db as gmdb
    >>> gmdb.version
    'v3.0.0'
    ```

## Default Emoji Generators

Emoji provides six default emoji generators.  All the generators can be used with the `emojione` index, but only two will work well with the `gemoji` index: `pymdownx.emoji.to_png` and `pymdownx.emoji.to_alt`. They can be used by passing in one of the functions below via the `emoji_generator` parameter.  Pass the actual function reference, not a string. If you need to create your own, just check out [Custom Emoji Generators](#custom-emoji-generators).

pymdownx.emoji.to_png
: 
    This generator was written to do PNG outputs for both Gemoji and EmojiOne.  This outputs the emoji as a PNG image in the form of:

    ```html
    <img alt="😄" class="emojione" src="https://cdn.jsdelivr.net/emojione/assets/png/1f604.png" title=":smile:" />
    ```

    **Generator Specific Options**

    | Option | Type | Default | Description |
    | ------ | ---- | ------- | ----------- |
    | classes | str| name of the index used | Specifies the class(es) to be used in the img element. |
    | image_path | str | CDN for the default index used | This can be either a local path, or it can be a CDN.  By default, an appropriate CDN is provided for EmojiOne and Gemoji depending on which index is being used. |
    | non_standard_image_path | str | CDN for the default index used | This can be either a local path, or it can be a CDN. Currently, only Gemoji's non-standard emojis take advantage of this as the Github CDN alters the path slightly for its non-Unicode emoji.  By default, an appropriate CDN is provided for Gemoji. |
    | attributes | dict | \{} | A dictionary containing tag attributes as key value string pairs. The dict keys are the attribute names and dict values are the attribute values. |

pymdownx.emoji.to_svg
: 
    This generator was written to output EmojiOne SVG images.  This outputs the emoji as a SVG image in the form of:

    ```html
    <img alt="😄" class="emojione" src="https://cdn.jsdelivr.net/emojione/assets/svg/1f604.svg" title=":smile:" />
    ```

    **Generator Specific Options**

    | Option | Type | Default | Description |
    | ------ | ---- | ------- | ----------- |
    | classes | str| name of the index used | Specifies the class(es) to be used in the img element. The default will match the name of the index used. |
    | image_path | str | A CDN for EmojiOne images | This can be either a local path, or it can be a CDN.  By default, an appropriate CDN is provided for EmojiOne. |
    | attributes | dict | \{} | A dictionary containing tag attributes as key value string pairs. The dict keys are the attribute names and dict values are the attribute values. |

pymdownx.emoji.to_png_sprite
: 
    This generator was written to support PNG sprite output for EmojiOne.  It is expected that this will be used in conjunction with the the official EmojiOne CSS.  You can include the CSS from the CDN in your document (version 2.2.7 at the time of writing this): https://cdnjs.cloudflare.com/ajax/libs/emojione/2.2.7/assets/sprites/emojione.sprites.css.  This outputs the emoji as a span in the form below.  The CSS will apply the appropriate mapping in the sprite PNG for the background image of the span.

    ```html
    <span class="emojione emojione-1f604" title=":smile:">😄</span>
    ```

    **Generator Specific Options**

    | Option | Type | Default | Description |
    | ------ | ---- | ------- | ----------- |
    | classes | str | name of the index used | Class used for the span where the classes are inserted as "class" in the following template: `'%(class)s-%(unicode)s'`. |
    | attributes | dict | \{} | A dictionary containing tag attributes as key value string pairs. The dict keys are the attribute names and dict values are the attribute values. |

pymdownx.emoji.to_svg_sprite
: 
    This was written to support EmojiOne SVG sprite output.  The output form was taken directly from an example in the EmojiOne source.  It is expected that the the user will provide a local version of the official SVG sprite and the path to it.  The output is:

    ```html
    <svg class="emojione"><description>😄</description><use xlink:href="./../assets/sprites/emojione.sprites.svg#emoji-1f604"></use></svg>
    ```

    **Generator Specific Options**

    | Option | Type | Default | Description |
    | ------ | ---- | ------- | ----------- |
    | classes | str | name of the index used | Classes to apply to the svg element where the classes are inserted as "class" in the following template: `'%(class)s-%(unicode)s'`. |
    | image_path | str | './../assets/sprites/emojione.sprites.svg' | Path to the SVG sprites. |

pymdownx.emoji.to_awesome
: 
    This generator is another EmojiOne specific output.  This is an output form mentioned here: https://github.com/Ranks/emojione/tree/master/lib/emojione-awesome.  According to EmojiOne's documentation, it aims to give a font-awesome like interface for EmojiOne.  There isn't currently a CDN link that could be found, but you can provide the CSS in your project locally: https://github.com/Ranks/emojione/blob/master/assets/css/emojione-awesome.css.  The output format is:

    ```html
    <i class="e1a-smile"></i>
    ```

    | Option | Type | Default | Description |
    | ------ | ---- | ------- | ----------- |
    | classes | str | 'e1a' | Classes to apply to the svg element where the classes are inserted as "class" in the following template: `'%(class)s-%(shortname)s'`. |
    | attributes | dict | \{} | A dictionary containing tag attributes as key value string pairs. The dict keys are the attribute names and dict values are the attribute values. |

pymdownx.emoji.to_alt
: 
    This generator supports both Gemoji and EmojiOne.  The generator outputs the alt value directly to the document.  The output can be Unicode characters, HTML entities, or even just the short name depending on what the global setting of 'alt' is set to.

    ```html
    😃
    ```

    There are no generator specific options.

## Custom Emoji Indexes
In order to provide a custom index, the emoji extension must be given a function that returns a suitable emoji index.  No parameters are passed to the function.  The function should simply return the custom index in the following format.

```python
emoji_index = {
    # Name is the name of the index.  This is passed into the emoji
    # generator functions and can be used to differentiate logic
    # for different indexes if required.
    "name": "myindex",

    # The actual index.  An dictionary of all the emoji.
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

def emoji_generator(index, shortname, alias, uc, alt, title, options, md)
: 
    | Parameter | Type |Description |
    |---------- | ---- | ----------- |
    | index  | str | The name of the selected emoji index. |
    | shortname | str | The current short name.  This may differ from the actual name used in a document as aliases get translated to the main short name. |
    | alias | str | If the name specified in the document was an alias, that alias will be set here, and the main short name will be found under `shortname`.  This will be `None` if the name used was not an alias. |
    | uc | str | This is a the the Unicode values for the emoji.  This name is used to reference emoji image names or for specifying class names etc., so it may not contain all the code points.  The string returned consists of each Unicode value represented as a hex value separated with hyphens.  Values such as U+200D ZERO WIDTH JOINER and  U+FE0F VARIATION SELECTOR-16 are stripped out.  So the value here will not always be practical for calculating the actual Unicode points of an emoji.  This will be `None` for non-standard emoji that are not Unicode. |
    | alt | str | This is the alternative emoji value (or fallback value).  Its format will differ depending on the extension setting `alt`.  This will be returned as either the Unicode characters, HTML entities, or the short name used.  See the `alt` setting for more info. |
    | title | str  | This is the title that can be used in img elements.  Depending of the global extension setting `title`, this will either return the long name, the short name, or `None`.  See the `title` setting for more info. |
    | options | dict | This is a dictionary to specify generator function specific options.  This can be anything, and it is up to the generator function to parse and provide defaults. |
    | md | class |  This is the Markdown class object.  This mainly used to access specific things needed from the Markdown class.  If you needed to stash your output, you would do something like: `md.htmlStash.store(alt, safe=True)`. |

    !!! Warning "Non-Unicode emojis"
        Keep in mind that Gemoji ships with some non-standard emojis like `:octocat:` that do not have Unicode code points.  `uc` and `alt` are affected by this and will return `None` and the short name respectively instead of strings describing the Unicode points.  For example `:octocat:` will just return `None` for `uc` and `:octocat:` for `alt`.  If you are parsing an index with custom emojis, just like Gemoji has, then you need to be aware of this.

## Using with MkDocs

This project uses these extensions with [MkDocs](https://github.com/mkdocs/mkdocs) to generate the documentation.  It might not be obvious how to set the index or generator functions in Mkdoc's YAML settings file, but it is actually pretty easy.  The functions are referenced like you would import them in Python except you also append them with a special prefix to let the YAML module know that the setting value is a Python object.  For instance, to specify the `to_svg` generator, you would simply reference it like this: `!!python/name:pymdownx.emoji.to_svg` (or you could use your own custom module).

```yaml
markdown_extensions:
  - pymdownx.emoji:
      emoji_generator: !!python/name:pymdownx.emoji.to_svg
```

## Emoji Index Updates
The Emoji extension might not always have indexes built from the latest repos, we try to keep the indexes updated with new releases, but if they fall out of date, you can open an issue on the repo to alert the maintainer(s) and they will update them when someone gets a chance.  Pull requests are also welcome.  The process for updating the indexes is automated, so it is fairly easy to do for a pull request.

1. Ensure you have requests installed: `pip install requests`.
2. Fork the repo and checkout to your machine.
3. `cd pymdown-extensions/tools`
4. Call the generator script: `python gen_emoji --gemoji` or `python gen_emoji --emojione`.  It will prompt you to select a tag to download.  Please pull the latest **official** tag.  Please don't pull experimental tags.  This should update the indexes.
5. Then you want to update the tests.  Step back out to the root of the project: `cd ..`.
6. Force the tests to update via `python run_tests.py -fu`.

Nothing is fool proof.  If they make a breaking change to the files that the script parses, or the location of the files, the auto-update tool may need to be updated itself (hopefully this would be a rare occurrence).  If such a change does occur, and you are feeling brave, a pull request would be appreciated, but in time, they will be resolved regardless.

#Examples
Current examples are all rendered with EmojiOne.

```
EmojiOne :smile: emojis are very useful :thumbsup:.

You can also escape `:` characters to escape the emoji: \:smile:.
```

EmojiOne :smile: emojis are very useful :thumbsup:.

You can also escape `:` characters to escape the emoji: \:smile:.
