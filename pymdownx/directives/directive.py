"""Directive class."""
from abc import ABCMeta, abstractmethod
import re
import functools

RE_LENGTH_PERCENT = re.compile(
    r"(?:[+\-]?(?:[0-9]*\.)?[0-9]+(?:e[-+]?[0-9]*)?)\s*(ex|p(?:x|c|t)|v(?:w|h|min|vmax)|r?em|(?:c|v)h|(?:c|m)m|in|%)"
)

RE_TAG = re.compile('^[a-z][a-z0-9-]*$', re.I)


def to_tag(value):
    """To tag."""

    value = to_string(value).strip()
    if RE_TAG.match(value) is None:
        raise ValueError('{} is not a valid tag'.format(value))
    return value


def to_flag(value):
    """Convert to flag."""

    if value is True or value is None:
        return value

    if isinstance(value, str):
        value = value.lower()
        if value == 'true':
            return True
        if value == 'false':
            return False

    raise ValueError("Could not convert type {} to a flag".format(type))


def to_ternary(value):
    """Convert to a ternary value."""

    if value is True or value is False or value is None:
        return value

    if isinstance(value, str):
        value = value.lower()
        if value == 'true':
            return True
        if value == 'false':
            return False
        if value in ('null', 'none'):
            return None

    raise ValueError("Could not convert type {} to a flag".format(type))


def to_string(value):
    """Convert to a string value."""

    if isinstance(value, str):
        return value

    if isinstance(value, (int, float, bool)):
        return str(value)

    raise ValueError("Could not convert type {} to a flag".format(type))


def to_html_attribute(value):
    """Convert to HTML attribute."""

    return to_string(value).strip().replace('"', '&quote;')


def to_length_percentages(value):
    """Convert to a string value."""

    if isinstance(value, (int, float)):
        return str(value)

    if isinstance(value, str):
        return value

    if isinstance(value, (int, float, bool)):
        return str(value)

    raise ValueError("Could not convert type {} to a flag".format(type))


def _delimiter(string, split, parser=None):
    """Split the string by the delimiter and then parse with the parser."""

    l = []
    for s in string.split(split):
        s = s.strip()
        if not s:
            continue
        if parser is not None:
            try:
                s = parser(s)
                l.append(s)
            except Exception:
                pass
    return l


def delimiter(split, parser=None):
    """String delimiter function."""

    return functools.partial(_delimiter, split=split, parser=parser)


to_classes = delimiter(' ', to_html_attribute)


class Directive(metaclass=ABCMeta):
    """Directive."""

    # Set to something if argument should be split.
    # Arguments will be split and white space stripped.
    ARG_DELIM = ''
    NAME = ''
    ATOMIC = None

    ARGUMENTS = {}
    OPTIONS = {}

    def __init__(self, length, tracker, md):
        """
        Initialize.

        - `store` allows us to store content until all content is found.
        - `length` specifies the length (number of colons) that the header used
        - `tracker` is a persistent storage for the life of the current Markdown page.
          It is a dictionary where we can keep references until the parent extension is reset.
        - `md` is the Markdown object just in case access is needed to something we
          didn't think about.

        """

        self.atomic = self.ATOMIC
        self.length = length
        self.tracker = tracker
        self.md = md
        self.args = []
        self.options = {}

    def is_atomic(self):
        """Check if this is atomic."""

        return self.atomic

    def parse_config(self, args, **options):
        """Parse configuration."""

        spec = self.ARGUMENTS
        required = spec.get('required', 0)
        optional = spec.get('optional', 0)
        delim = spec.get('delimiter', ' ')
        parsers = spec.get('parsers', [None])
        total = required + optional

        # If we have arguments but allow none,
        # or have no arguments but require at least 1,
        # then quit
        if (args and total == 0) or (not args and required >= 1):
            return False

        # Split arguments if we can have more than 1
        arguments = delimiter(delim)(args) if total > 1 else [args]
        length = len(arguments)

        # If total number of arguments exceed what is allowed, quit
        if length > total or length < required:
            return False

        # Parse each argument with the appropriate parser, if we run out,
        # it is assumed that the last is meant to represent the rest.
        # A `None` for a parser means accept as is.
        total_parsers = len(parsers)
        for e, a in enumerate(arguments):
            parser = parsers[e] if e <= total_parsers else parsers[-1]
            if parser is not None:
                try:
                    a = parser(a)
                except Exception:
                    return False
                arguments[e] = a

        self.args = arguments

        # Fill in defaults options
        spec = self.OPTIONS
        parsed = {}
        for k, v in spec.items():
            if not k:
                continue
            parsed[k] = v[0]

        # Parse provided options
        for k, v in options.items():
            # Parameter not in spec
            if k not in spec:

                # Spec can handle anonymous parameters
                if '' in spec:
                    parser = spec['']
                    if parser is None:
                        try:
                            v = parser(v)
                        except Exception:
                            continue
                else:
                    continue

            # Spec explicitly handles parameter
            else:
                default, parser = spec[k]
                if parser is not None:
                    try:
                        v = parser(v)
                    except Exception:
                        v = default
            parsed[k] = v

        # Add parsed options to options
        self.options = parsed
        return True

    @abstractmethod
    def on_create(self, parent):
        """On create event."""

        return parent

    def on_end(self, el):
        """Perform action on end."""

    def on_add(self, parent):
        """
        Adjust where the content is added.

        Is there a sub-element where this content should go?
        """

        return parent
