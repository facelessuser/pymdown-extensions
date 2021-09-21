"""Generate Markdown isolated from our current document options."""
import markdown
import yaml
import re
from collections import OrderedDict


def yaml_load(stream, loader=yaml.Loader):
    """
    Custom YAML loader.

    Load all strings as Unicode.
    http://stackoverflow.com/a/2967461/3609487
    """

    def construct_yaml_str(self, node):
        """Override the default string handling function to always return Unicode objects."""

        return self.construct_scalar(node)

    class Loader(loader):
        """Custom Loader."""

    Loader.add_constructor(
        'tag:yaml.org,2002:str',
        construct_yaml_str
    )

    return yaml.load(stream, Loader)


def get_frontmatter(text):
    """Get front matter from string."""

    frontmatter = OrderedDict()

    if text.startswith("---"):
        m = re.search(r'^(-{3}\r?\n(?!\r?\n)(.*?)(?<=\n)(?:-{3}|\.{3})\r?\n)', text, re.DOTALL)
        if m:
            yaml_okay = True
            try:
                frontmatter = yaml_load(m.group(2))
                if frontmatter is None:
                    frontmatter = OrderedDict()
                # If we didn't get a dictionary, we don't want this as it isn't front matter.
                assert isinstance(frontmatter, (dict, OrderedDict)), TypeError
            except Exception:
                # We had a parsing error. This is not the YAML we are looking for.
                yaml_okay = False
                frontmatter = OrderedDict()

            if yaml_okay:
                text = text[m.end(1):]

    return frontmatter, text


def md_sub_render(src="", language="", class_name=None, options=None, md="", **kwargs):
    """Formatter wrapper."""
    try:
        fm, text = get_frontmatter(src)
        md = markdown.markdown(
            text,
            extensions=fm.get('extensions', []),
            extension_configs=fm.get('extension_configs', {})
        )
        return md
    except Exception:
        import traceback
        print(traceback.format_exc())
        raise
