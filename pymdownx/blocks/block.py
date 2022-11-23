"""Block class."""
from abc import ABCMeta, abstractmethod
import re
import functools
import copy

RE_TAG = re.compile('^[a-z][a-z0-9-]*$', re.I)

RE_NAME = re.compile(
    r'[^A-Z_a-z\u00c0-\u00d6\u00d8-\u00f6\u00f8-\u02ff'
    r'\u0370-\u037d\u037f-\u1fff\u200c-\u200d'
    r'\u2070-\u218f\u2c00-\u2fef\u3001-\ud7ff'
    r'\uf900-\ufdcf\ufdf0-\ufffd'
    r'\:\-\.0-9\u00b7\u0300-\u036f\u203f-\u2040]+'
)


def _ranged_number(value, minimum, maximum, number_type):
    """Check the range of the given number type."""

    value = number_type(value)
    if minimum is not None and value < minimum:
        raise ValueError('{} is not greater than {}'.format(value, minimum))

    if maximum is not None and value > maximum:
        raise ValueError('{} is not greater than {}'.format(value, minimum))

    return value


def type_number(value):
    """Ensure type number or fail."""

    if not isinstance(value, (float, int)):
        raise ValueError("Could not convert type {} to a number".format(type(value)))

    return value


def type_integer(value):
    """Ensure type integer or fail."""

    if not isinstance(value, int):
        if not isinstance(value, float) or not value.is_integer():
            raise ValueError("Could not convert type {} to an integer".format(type(value)))
        value = int(value)

    return value


def type_ranged_number(minimum=None, maximum=None):
    """Ensure typed number is within range."""

    return functools.partial(_ranged_number, minimum=minimum, maximum=maximum, number_type=type_number)


def type_ranged_integer(minimum=None, maximum=None):
    """Ensured type integer is within range."""

    return functools.partial(_ranged_number, minimum=minimum, maximum=maximum, number_type=type_integer)


def type_tag(value):
    """Ensure type tag or fail."""

    value = type_string(value).strip()
    if RE_TAG.match(value) is None:
        raise ValueError('{} is not a valid tag'.format(value))
    return value


def type_boolean(value):
    """Ensure type boolean or fail."""

    if not isinstance(value, bool):
        raise ValueError("Could not convert type {} to a boolean".format(type(value)))
    return value


def type_ternary(value):
    """Ensure type ternary or fail."""

    if value is True or value is False or value is None:
        return value

    raise ValueError("Could not convert type {} to a ternary value".format(type(value)))


def type_string(value):
    """Ensure type string or fail."""

    if isinstance(value, str):
        return value

    raise ValueError("Could not convert type {} to a string".format(type(value)))


def type_string_insensitive(value):
    """Ensure type string and normalize case."""

    return type_string(value).lower()


def type_html_attribute_value(value):
    """Ensure type HTML attribute value or fail."""

    return type_string(value).replace('"', '&quot;')


def type_html_attribute_name(value):
    """Ensure type HTML attribute name or fail."""

    return RE_NAME.sub('_', type_string(value))


def _delimiter(string, split, string_type):
    """Split the string by the delimiter and then parse with the parser."""

    l = []
    # Ensure input is a string
    string = type_string(string)
    for s in string.split(split):
        s = s.strip()
        if not s:
            continue
        # Ensure each part conforms to the desired string type
        s = string_type(s)
        l.append(s)
    return l


def _string_in(value, accepted, string_type):
    """Ensure type string is within the accepted values."""

    value = string_type(value)
    if value not in accepted:
        raise ValueError('{} not found in {}'.format(value, str(accepted)))
    return value


def type_string_in(accepted, string_type=type_string):
    """Ensure type string is within the accepted list."""

    return functools.partial(_string_in, accepted=accepted, string_type=string_type)


def type_string_delimiter(split, string_type=type_string):
    """String delimiter function."""

    return functools.partial(_delimiter, split=split, string_type=string_type)


def type_attribute_dict(value):
    """Attribute dictionary."""

    if not isinstance(value, dict):
        raise ValueError('Attributes should be contained within a dictionary')

    attributes = {}
    for k, v in value.items():
        k = type_html_attribute_name(k)
        if k.lower() == 'class':
            k = 'class'
            v = type_classes(v)
        else:
            v = type_html_attribute_value(v)
        attributes[k] = v

    return attributes


def type_class(value):
    """Ensure type class is valid and adjust HTML escaping as required."""

    value = type_html_attribute_value(value)
    if ' ' in value:
        raise ValueError('A single class should be provided')
    return value


# Ensure class(es) or fail
type_classes = type_string_delimiter(' ', type_html_attribute_value)


class Block(metaclass=ABCMeta):
    """Block."""

    # Set to something if argument should be split.
    # Arguments will be split and white space stripped.
    NAME = ''

    # Instance arguments and options
    ARGUMENTS = {}
    OPTIONS = {}

    # Extension config
    CONFIG = {}

    def __init__(self, length, tracker, md, config):
        """
        Initialize.

        - `store` allows us to store content until all content is found.
        - `length` specifies the length (number of colons) that the header used
        - `tracker` is a persistent storage for the life of the current Markdown page.
          It is a dictionary where we can keep references until the parent extension is reset.
        - `md` is the Markdown object just in case access is needed to something we
          didn't think about.

        """

        # Setup up the argument and options spec
        # Note that `attributes` is handled special and we always override it
        self.arg_spec = copy.deepcopy(self.ARGUMENTS)
        self.option_spec = copy.deepcopy(self.OPTIONS)
        if 'attributes' in self.option_spec:
            raise ValueError("'attributes' is a reserved option name and cannot be overriden")
        self.option_spec['attributes'] = [{}, type_attribute_dict]

        self.length = length
        self.tracker = tracker
        self.md = md
        self.args = []
        self.options = {}
        self.config = config
        self.on_init()

    def on_init(self):
        """On initialize."""

    def on_markdown(self):
        """Check how element should be treated by the Markdown parser."""

        return "auto"

    def parse_config(self, args, **options):
        """Parse configuration."""

        spec = self.arg_spec
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
        if args is not None:
            if total > 1:
                arguments = type_string_delimiter(delim)(args)
            else:
                arguments = [args]
        else:
            arguments = []

        length = len(arguments)

        # If total number of arguments exceed what is allowed, quit
        if length > total or length < required:
            return False

        # Parse each argument with the appropriate parser, if we run out,
        # it is assumed that the last is meant to represent the rest.
        # A `None` for a parser means accept as is.
        total_parsers = len(parsers)
        for e, a in enumerate(arguments):
            parser = parsers[e] if e < total_parsers else parsers[-1]
            if parser is not None:
                try:
                    a = parser(a)
                except Exception:
                    return False
                arguments[e] = a

        self.args = arguments

        # Fill in defaults options
        spec = self.option_spec
        parsed = {}
        for k, v in spec.items():
            parsed[k] = v[0]

        # Parse provided options
        for k, v in options.items():

            # Parameter not in spec
            if k not in spec:
                # Unrecognized parameter name
                return False

            # Spec explicitly handles parameter
            else:
                parser = spec[k][1]
                if parser is not None:
                    try:
                        v = parser(v)
                    except Exception:
                        # Invalid parameter value
                        return False
            parsed[k] = v

        # Add parsed options to options
        self.options = parsed

        return self.on_parse()

    def on_parse(self):
        """
        Handle parsing event.

        Return true if everything is okay.
        """

        return True

    @classmethod
    def on_register(cls, block_processor, md, config):
        """Handle registration events."""

    @abstractmethod
    def on_create(self, parent):
        """Create the needed element and return it."""

    def create(self, parent):
        """Create the element."""

        el = self.on_create(parent)

        # Handle general HTML attributes
        attrib = el.attrib
        for k, v in self.options['attributes'].items():
            if k == 'class':
                if k in attrib:
                    v = type_classes(attrib['class']) + v
                attrib['class'] = ' '.join(v)
            else:
                attrib[k] = v
        return el

    def on_end(self, el):
        """Perform any action on end."""

    def on_add(self, parent):
        """
        Adjust where the content is added and return the desired element.

        Is there a sub-element where this content should go?
        This runs before processing every new block.
        """

        return parent
