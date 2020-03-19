# Release Notes

## Upgrading to 7.0

### Tabbed Extension
A new extension called Tabbed has been added. With the arrival of this general purpose tabbed content extension, it has
made the old SuperFences tabbed content feature redundant. By default, SuperFences will now change the classes it uses
for it's tabbed feature to match those of the new Tabbed extension. CSS should be updated accordingly.

The classes that have changed are `supferfences-tabs` and `superfences-content`, which have changed to `tabbed-set` and
`tabbed-content` respectively. Example CSS is updated in SuperFences for
[reference](../extensions/superfences.md#tabbed-fences).

To help with the transition though, you can quickly switch back to the old style classes by simply enabling the
SuperFences' global option `legacy_tab_classes`:

```py3
extension_configs = {
    "pymdownx.superfences": {
        "legacy_tab_classes": True
    }
}
```

To learn more about migrating to the Tabbed extension, checkout the [Tabbed documentation](../extensions/tabbed.md).

SuperFences' tab content feature will be removed in 8.0. There is no formal date for when this will occur, but it is
recommended to begin migrating as soon as possible, but `legacy_tab_classes` can be used as a stop gap for the short
term.

### Option Deprecation in SuperFences

SuperFences has deprecated `highlight_code`. This option now does nothing and will be removed in some future release.
If this option was used, you will have to use [custom fences](../extensions/superfences.md#custom-fences) to implement
this behavior with your own custom formatter.

### SuperFences' Attribute List Style

Additional classes and IDs can now be injected into fenced code blocks with the format ` ```{.lang .more-class} `.

The attribute list feature also impacts the the custom formatter. While the default formatters will still inject
classes and IDs to the top level element to preserve backwards compatibility, the formatter now must accept the new
keyword parameters `classes` and `id_value`. If you have a custom formatter that does not adhere to this new
requirement, you will see a user warning.

The new format is:

```py3
def custom_formatter(source, language, css_class, options, md, classes=None, id_value='', **kwargs):
    return string
```

While it is recommended for a user to update their custom formatters to receive the new parameters, at the very
least, users should add `**kwargs` to future proof their formatters.

### CodeHilite Separation

SuperFences and InlineHilite no longer sync settings from CodeHilite. To configure either of the extensions, Pymdown
Extension's Highlight extension must be used. CodeHilite can be run along side Highlight if desired, but CodeHilite
cannot be used to augment SuperFences or InlineHilite's behavior.

### Keys Alias Changes

Previously `alt`, `left-alt`, and `right-alt` had aliases `menu`, `left-menu`, `right-menu`, `lmenu`, and `rmenu`. These
aliases have been removed. `menu` will now be an alias for `context-menu`.

It is known that *Alt* has been referred to as *Menu* in the real world, but so is the actual *Menu*/*Apps* key. This
will hopefully create less confusion in the long term, even if there is a little in the short term.

## Upgrading to 6.0

While there are a number of new features and bug fixes, the only backwards incompatible changes are with SuperFences'
custom fences. In an effort to make custom fences more useful, we wanted to be able to pass the `Markdown` object to the
formatters. This gives custom formats access to things like metadata if required.

The format of custom fence formatters already had two different versions: ones without custom options and one with
custom options. As adding yet another parameter would cause more complexity behind the scenes, we decided to introduce
the breaking change of creating a unified format for formatters with custom options and without. In addition to unifying
the format, we also now pass the `Markdown` object to the formatters as an additional parameter.

While we were breaking custom formats, it seemed like a good time to go ahead and change the defaults for the
`custom_fences` options. Most people who are using SuperFences aren't even using the default, niche `flow` and
`sequence` custom fences. Instead of hijacking fence names that most people aren't even using, it seemed more
appropriate to define no custom fences.

Below are instructions on how to upgrade if you were relying on the either the default settings of `custom_fences` or if
you had written your own custom fence formatters.

1. If you've written your own custom fence formatters, the number of parameters needed has changed, so you must update
  your existing formatters.  The needed parameters are the same regardless of whether you are using an options validator
  or not.

    ```py3
    def custom_formatter(source, language, css_class, options, md):
        return string
    ```

2. `flow` and `sequence` are no longer defined by default. If you were relying on the default custom fences, you will
  have to define them manually now. The needed settings are found below:

    ```py3
    extension_configs = {
        "pymdownx.superfences": {
            "custom_fences": [
                {
                    'name': 'flow',
                    'class': 'uml-flowchart',
                    'format': pymdownx.superfences.fence_code_format
                },
                {
                    'name': 'sequence',
                    'class': 'uml-sequence-diagram',
                    'format': pymdownx.superfences.fence_code_format
                }
            ]
        }
    }
    ```

    If you are attempting to configure these options in a YAML based configuration (like in [MkDocs][mkdocs]), please
    see the [FAQ](../faq.md#function-references-in-yaml) to see how to specify function references in YAML.

--8<-- "refs.txt"
