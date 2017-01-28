## Alternate Slugify

Python Markdown's default slugify strips out all Unicode chars. To better handle Unicode, a couple of optional slugify options have been provided. These are very simple slugify options. There are many slugify options out there, some of which are very sophisticated. Some may prefer using one of those, but if you just want something simple, these might fill that requirement.

### `uslugify`

In order to handle Unicode characters in slugs better, a slugify has been included at `pymdownx.slugs.uslugify`. This assumes you are encoding your HTML as UTF-8.  UTF-8 Unicode should be okay in your slugs in modern browsers, so `uslugify` takes the Unicode string and strips out non-word Unicode characters and leaves in Unicode word chars. Spaces are replaced with the separator provided by Toc.  And the entire string is lower cased. You can override Toc's default slugify by feeding in this function via the `slugify` parameter.

### `uslugify_encoded`

If you aren't encoding your HTML as UTF-8, or prefer the safer percent encoded Unicode slugs, you can use `pymdownx.slugs.uslugify_encoded`. This will take the Unicode string, strip out non-Unicode word characters, replace spaces with the provided separator, percent encode the Unicode word characters, and lastly lower case the string. You can override Toc's default slugify by feeding in this function via the `slugify` parameter.

--8<-- "abbr.md"
