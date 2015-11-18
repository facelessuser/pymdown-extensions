"""Utils."""
import yaml
from collections import OrderedDict
import sys

PY2 = sys.version_info >= (2, 0) and sys.version_info < (3, 0)
PY3 = sys.version_info >= (3, 0) and sys.version_info < (4, 0)

if PY2:
    unicode_type = unicode  # noqa
    string_type = basestring  # noqa
    binary_type = str
else:
    unicode_type = str  # noqa
    string_type = str  # noqa
    binary_type = bytes  # noqa


def yaml_load(stream, loader=yaml.Loader, object_pairs_hook=OrderedDict):
    """
    Custom yaml loader.

    Make all YAML dictionaries load as ordered Dicts.
    http://stackoverflow.com/a/21912744/3609487

    Load all strings as unicode.
    http://stackoverflow.com/a/2967461/3609487
    """

    def construct_mapping(loader, node):
        """Convert to ordered dict."""

        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    def construct_yaml_str(self, node):
        """Override the default string handling function to always return unicode objects."""

        return self.construct_scalar(node)

    class Loader(loader):
        """Custom Loader."""

    Loader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping
    )

    Loader.add_constructor(
        'tag:yaml.org,2002:str',
        construct_yaml_str
    )

    return yaml.load(stream, Loader)
