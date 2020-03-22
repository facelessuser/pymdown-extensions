path: tree/master
source: pymdownx/slugs.py

# Slugs

## Alternate Slugify

Python Markdown's default slugify strips out all Unicode chars. To better handle Unicode, a couple of optional slugify
options have been provided. These are very simple slugify options. There are many slugify options out there, some of
which are very sophisticated. Some may prefer using one of those, but if you just want something simple, these might
fill that requirement.

### `uslugify`

In order to handle Unicode characters in slugs better, a slugify has been included at `pymdownx.slugs.uslugify`. This
assumes you are encoding your HTML as UTF-8.  UTF-8 Unicode should be okay in your slugs in modern browsers. `uslugify`
and normalizes the Unicode with the [`NFC`][unicode-norm] form, and then strips out non-word Unicode characters (`-` is
allowed to pass through as well). Spaces are replaced with the provided separator.  Lastly, the entire string is
lowercased. You can override Toc's default slugify by feeding in this function via the `slugify` parameter.

### `uslugify_encoded`

If you aren't encoding your HTML as UTF-8, or prefer the safer percent encoded Unicode slugs, you can use
`pymdownx.slugs.uslugify_encoded`. This is just like [`uslugify`](#uslugify) except that it percent encodes Unicode
characters. You can override Toc's default slugify by feeding in this function via the `slugify` parameter.

### `uslugify_cased`

If you prefer to keep the casing of your Unicode slugs, this might be the slug for you. This is just like
[`uslugify`](#uslugify) except that it preserves the case of the original text. You can override Toc's default slugify
by feeding in this function via the `slugify` parameter.

### `uslugify_cased_encoded`

If you aren't encoding your HTML as UTF-8, or prefer the safer percent encoded Unicode slugs *and* you prefer to keep
the casing of your Unicode slugs, you can use `pymdownx.slugs.uslugify_cased_encoded`. This is just like
[`uslugify`](#uslugify) except that it percent encodes Unicode characters *and* it preserves the case of the original
text. You can override Toc's default slugify by feeding in this function via the `slugify` parameter.

### `gfm`

If you are looking for a GitHub like slug, this may be for you. This is just like [`uslugify`](#uslugify) except that
ASCII chars are lowercased while Unicode chars are not.

### `gfm_encoded`

If you are looking for a GitHub like slug, this may be for you. This is just like [`uslugify`](#uslugify) except that it
percent encodes Unicode characters and ASCII chars are lowercased while Unicode chars are not.

--8<-- "refs.txt"
