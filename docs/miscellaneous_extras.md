## Alternate Slugify

Python Markdown's default slugify strips out Unicode chars. To better handle Unicode, a couple of optional slugify options have been provided.

### uslugify

In order to handle Unicode characters in slugs better, a slugify has been included at `pymdownx.slugs.uslugify`.  This assumes you are encoding your HTML as UTF-8.  UTF-8 Unicode should be okay in your slugs in modern browsers.  You can use this to override Toc's slugify.

### uslugify_encoded

If you aren't encoding your HTML as UTF-8, or prefer the safer percent encoded Unicode slugs, you can use `pymdownx.slugs.uslugify_encoded` which will percent encode non-ASCII word chars.  You can use this to override Toc's slugify.

--8<-- "abbr.md"
