[:octicons-file-code-24:][_slugs]{: .source-link }

# Slugs

## Alternate Slugify

Python Markdown's default slugify used to strip out all Unicode chars. While this is not necessarily true anymore,
PyMdown Extensions offers a configurable slugify to help those with picker preferences. These are very simple slugify
options. There are many slugify options out there, some of which are very sophisticated. Some may prefer using one of
those, but if you just want something simple, this might fill that requirement.

## Using Slugify

`slugify` is a simple Unicode slugify option. It takes various parameters to control how casing is performed in slugs,
what kind of Unicode normalization is preferred, and whether percent encoding of Unicode is preferred.

The available key word options are found below:

Parameter        | Default        | Description
---------------- | -------------- | -----------
`case`           | `#!py3 'none'` | Control case normalization of characters. See case options below.
`percent_encode` | `#!py3 False`  | Percent encode all Unicode characters after case normalization.
`normalize`      | `#!py3 'NFC'`  | Unicode normalization method. For instance, `NFD` will strip diacritics, but `NFC` does not.

Case options are described below:

Option        | Description
------------- | -----------
`none`        | Performs no case normalization preserving whatever case is provided.
`lower`       | Performs simple lower casing on the slug which will operate on Unicode and ASCII alike.
`lower-ascii` | Performs simple lower casing on only ASCII upper case characters.
`fold`        | Applies Python's case folding function on the slug.

Configuration is straight forward. Simply import the slug module and configure how you desire the Toc's extension to
utilize the slugs.

```py
extension = ['markdown.extensions.toc']
extension_configs = {
    'markdown.extensions.toc': {
        "slugify": slugs.slugify(case="lower", percent_encode=True)
    }
}
```

If you are using something like [MkDocs][mkdocs], check out our [FAQ](../faq.md#function-references-in-yaml) which gives
guidance on how to specify configurable functions in the YAML configuration.
