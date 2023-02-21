"""Block class."""
from abc import ABCMeta, abstractmethod
import re
import functools
import copy

# Sub-patterns parts
# Whitespace
WS = r'(?:[ \t])'
# CSS escapes
CSS_ESCAPES = r'(?:\\(?:[a-f0-9]{{1,6}}{ws}?|[^\r\n\f]|$))'.format(ws=WS)
# CSS Identifier
IDENTIFIER = r'''
(?:(?:-?(?:[^\x00-\x2f\x30-\x40\x5B-\x5E\x60\x7B-\x9f])+|--)
(?:[^\x00-\x2c\x2e\x2f\x3A-\x40\x5B-\x5E\x60\x7B-\x9f])*)
'''
# Value: quoted string or identifier
VALUE = r'''
(?:"(?:\\(?:.)|[^\\"\r\n\f]+)*?"|'(?:\\(?:.)|[^\\'\r\n\f]+)*?'|{ident}+)
'''.format(ident=IDENTIFIER)
# Attribute value comparison.
ATTR = r'''
(?:{ws}*(?P<cmp>=){ws}*(?P<value>{value}))?
'''.format(ws=WS, value=VALUE)
# Selector patterns
# IDs (`#id`)
PAT_ID = r'\#{ident}'.format(ident=IDENTIFIER)
# Classes (`.class`)
PAT_CLASS = r'\.{ident}'.format(ident=IDENTIFIER)
# Attributes (`[attr]`, `[attr=value]`, etc.)
PAT_ATTR = r'''
\[(?:{ws}*(?P<attr_name>{ident}){attr})+{ws}*\]
'''.format(ws=WS, ident=IDENTIFIER, attr=ATTR)

RE_IDENT = re.compile(IDENTIFIER, flags=re.I | re.X)
RE_ID = re.compile(PAT_ID, flags=re.I | re.X)
RE_CLASS = re.compile(PAT_CLASS, flags=re.I | re.X)
RE_ATTRS = re.compile(PAT_ATTR, flags=re.I | re.X)
RE_ATTR = re.compile(r'(?P<attr_name>{ident}){attr}'.format(ident=IDENTIFIER, attr=ATTR), flags=re.I | re.X)

ATTRIBUTES = {'id': RE_ID, 'class': RE_CLASS, 'attr': RE_ATTRS}


def parse_selectors(selector, get_tag=True):
    """Parse the selector."""

    eol = len(selector)
    tag = None
    attrs = {}
    end = 0
    m = None

    if get_tag:
        m = RE_IDENT.match(selector)
        if m is None:
            raise ValueError('No defined tag')
        tag = m.group(0)
        end = m.end()

    while end < eol:
        for atype, pat in ATTRIBUTES.items():
            m = pat.match(selector, end)
            if m is not None:
                if atype == 'id':
                    attrs[atype] = m.group(0)[1:]
                    end = m.end()
                elif atype == 'class':
                    if atype not in attrs:
                        attrs[atype] = [m.group(0)[1:]]
                    else:
                        attrs[atype].append(m.group(0)[1:])
                    end = m.end()
                else:
                    results = m.group(0)
                    m2 = RE_ATTR.search(results)
                    while m2 is not None:
                        pos = m2.end()
                        name = m2.group('attr_name').lower()
                        value = m2.group('value')
                        if value is None:
                            value = name if name != 'class' else ''
                        elif value.startswith(('"', "'")):
                            value = value[1:-1]

                        if name == 'class':
                            value = [v for v in value.split(' ') if v]
                            if value:
                                if name in attrs:
                                    attrs[name].extend(value)
                                else:
                                    attrs[name] = value
                        else:
                            value = value
                            attrs[name] = value
                        m2 = RE_ATTR.search(results, pos)
                    end = m.end()
                break

        if m is None:
            raise ValueError('Invalid selector')

    if 'class' in attrs:
        attrs['class'] = ' '.join(attrs['class'])

    return tag, attrs


def type_html_attributes(value):
    """Ensure a string of HTML attributes."""

    value = type_string(value)
    _, attrs = parse_selectors(value, get_tag=False)

    return attrs


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


def type_html_identifier(value):
    """Ensure type HTML attribute name or fail."""

    value = type_string(value)
    m = RE_IDENT.fullmatch(value)
    if m is None:
        raise ValueError('A valid attribute name must be provided')
    return m.group(0)


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


# Ensure class(es) or fail
type_html_classes = type_string_delimiter(' ', type_html_identifier)


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
        if '$' in self.option_spec:
            raise ValueError("'$' is a reserved option name and cannot be overriden")
        self.option_spec['$'] = [{}, type_html_attributes]

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
        for k, v in self.options['$'].items():
            if k == 'class':
                if k in attrib:
                    v = type_html_classes(attrib['class']) + type_html_classes(v)
                    attrib['class'] = ' '.join(v)
                else:
                    attrib['class'] = v
            else:
                attrib[k] = v
        return el

    def on_end(self, block):
        """Perform any action on end."""

    def on_add(self, block):
        """
        Adjust where the content is added and return the desired element.

        Is there a sub-element where this content should go?
        This runs before processing every new block.
        """

        return block
