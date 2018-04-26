# FAQ

1. > How do I specify function references in YAML if I am using a module like [MkDocs][mkdocs]?

    Pymdown Extensions has a number of extensions that expose customization via options that take function references. If you are using a project like [MkDocs][mkdocs], which allows a user to configure Python Markdown extensions via YAML, specifying function references may not be intuitive.

    Keep in mind that the following examples specifically reference YAML configurations that are implemented via [PyYAML][pyyaml] and are configured to allow Python objects.

    When specifying a function reference in PyYAML, you must prepend the function with `!!python/name:`. For instance, to specify Python Markdown's Toc extension to use one of PyMdown Extensions' slugs in MkDocs:

    ```yaml
    markdown_extensions:
      - markdown.extensions.toc:
          slugify: !!python/name:pymdownx.slugs.uslugify
          permalink: "\ue157"
    ```

    To specify a particular emoji generator in the Emoji extension:

    ```yaml
    markdown_extensions:
      - pymdownx.emoji:
          emoji_generator: !!python/name:pymdownx.emoji.to_png
    ```

--8<-- "refs.md"
