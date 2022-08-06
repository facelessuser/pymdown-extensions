"""Directives."""
from markdown import Extension
from markdown.blockprocessors import BlockProcessor, HRProcessor
from collections import namedtuple
import xml.etree.ElementTree as etree
import re

YAML = re.compile(r'^((-{3})\n(.*?)(?<=\n)\2(?:\n|$))', re.DOTALL)

RE_REMOVE_DIV = re.compile(r'^\s*<div[^>]+>(.*?)</div>\s*$', re.DOTALL)

RE_KEY_VALUE = re.compile(r'^[ ]{0,3}(?P<key>[A-Za-z0-9_-]+):\s*(?P<value>.*)')

RE_START = re.compile(
    r'(?:^|\n)[ ]{0,3}(:{3,})[ ]*\{[ ]*(\w+)[ ]*\}(.*?)(?:\n|$)'
)

RE_END = re.compile(
    r'(?m)^[ ]{0,3}(:{3,})[ ]*(?:\n|$)'
)

RE_FRONTMATTER_START = re.compile(r'(?m)\s*^[ ]{0,3}(-{3})[ ]*(?:\n|$)')

RE_FRONTMATTER_END = re.compile(
    r'(?m)^[ ]{0,3}(-{3})[ ]*(?:\n|$)'
)

RE_NAME = re.compile(
    r'[^A-Z_a-z\u00c0-\u00d6\u00d8-\u00f6\u00f8-\u02ff'
    r'\u0370-\u037d\u037f-\u1fff\u200c-\u200d'
    r'\u2070-\u218f\u2c00-\u2fef\u3001-\ud7ff'
    r'\uf900-\ufdcf\ufdf0-\ufffd'
    r'\:\-\.0-9\u00b7\u0300-\u036f\u203f-\u2040]+'
)

# Track directive entries
DBlock = namedtuple("DBlock", "directive el parent")


def get_frontmatter(string):
    """
    Get frontmatter from string.

    YAML-ish key value pairs.
    """

    frontmatter = {}
    fail = False

    for line in string.strip().split('\n')[1:-1]:
        pair = RE_KEY_VALUE.match(line)
        if pair:
            key = pair.group('key')
            value = pair.group('value').strip()
            frontmatter[key] = value
        else:
            fail = True
            break
    if fail:
        return None

    return frontmatter


class Directive:
    """Directive."""

    # Set to something if argument should be split.
    # Arguments will be split and white space stripped.
    ARG_DELIM = ''
    NAME = ''
    STORE = False

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

        self.store = []
        self.length = length
        self.tracker = tracker
        self.md = md
        self.args = []
        self.options = {}

    @classmethod
    def on_validate(cls, args):
        """Validate arguments."""

        return True

    def config(self, args, **options):
        """Parse configuration."""

        self.args = []
        if args and self.ARG_DELIM:
            for a in args.split(self.ARG_DELIM):
                a = a.strip()
                if not a:
                    continue
                self.args.append(a)
        elif args:
            self.args = [args]
        self.options = options

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


class Figure(Directive):
    """Figure capture directive."""

    NAME = 'figure'

    @classmethod
    def on_validate(cls, args):
        """Validate arguments."""

        return bool(args)

    def on_add(self, el):
        """Return the `figcaption`."""

        return list(el)[-1]

    def on_create(self, parent):
        """Create the element."""

        height = self.options.get('height', '').replace('"', '&quote;')
        width = self.options.get('width', '').replace('"', '&quote;')
        alt = self.options.get('alt', '').replace('"', '&quote;')

        attributes = {"src": self.args[0].replace('"', '&quote;')}
        if height:
            attributes['height'] = height
        if width:
            attributes['width'] = width
        if alt:
            attributes['alt'] = alt
        fig = etree.SubElement(parent, 'figure')
        etree.SubElement(fig, 'img', attributes)
        etree.SubElement(fig, 'figcaption')

        return fig


class Admonition(Directive):
    """Admonition."""

    NAME = 'admonition'

    def on_create(self, parent):
        """Create the element."""

        # Create the admonition
        el = etree.SubElement(parent, 'div')

        # Create the title
        t = self.options.get('type', '').lower()
        title = self.args[0] if self.args and self.args[0] else t.title()
        if not title:
            title = 'Attention'
        ad_title = etree.SubElement(el, 'p', {'class': 'admonition-title'})
        ad_title.text = title

        # Set classes
        classes = []
        for c in self.options.get('class', '').split(' '):
            c = c.strip()
            if c:
                classes.append(c)
        if t != 'admonition':
            classes.insert(0, t)
        classes.insert(0, 'admonition')
        el.set('class', ' '.join(classes))
        return el


class Note(Admonition):
    """Note."""

    NAME = 'note'

    def config(self, args, **options):
        """Parse configuration."""

        super().config(args, **options)
        self.options['type'] = 'note'


class Attention(Admonition):
    """Attention."""

    NAME = 'attention'

    def config(self, args, **options):
        """Parse configuration."""

        super().config(args, **options)
        self.options['type'] = 'attention'


class Caution(Admonition):
    """Caution."""

    NAME = 'caution'

    def config(self, args, **options):
        """Parse configuration."""

        super().config(args, **options)
        self.options['type'] = 'caution'


class Danger(Admonition):
    """Danger."""

    NAME = 'danger'

    def config(self, args, **options):
        """Parse configuration."""

        super().config(args, **options)
        self.options['type'] = 'danger'


class Error(Admonition):
    """Error."""

    NAME = 'error'

    def config(self, args, **options):
        """Parse configuration."""

        super().config(args, **options)
        self.options['type'] = 'error'


class Tip(Admonition):
    """Tip."""

    NAME = 'tip'

    def config(self, args, **options):
        """Parse configuration."""

        super().config(args, **options)
        self.options['type'] = 'tip'


class Hint(Admonition):
    """Hint."""

    NAME = 'hint'

    def config(self, args, **options):
        """Parse configuration."""

        super().config(args, **options)
        self.options['type'] = 'hint'


class Important(Admonition):
    """Important."""

    NAME = 'danger'

    def config(self, args, **options):
        """Parse configuration."""

        super().config(args, **options)
        self.options['type'] = 'danger'


class Warn(Admonition):
    """Warning."""

    NAME = 'warning'

    def config(self, args, **options):
        """Parse configuration."""

        super().config(args, **options)
        self.options['type'] = 'warning'


class Tab(Directive):
    """Tabbed container."""

    NAME = 'tab'

    def __init__(self, length, tracker, md):
        """Initialize."""

        super().__init__(length, tracker, md)
        if 'tab_group_count' not in tracker:
            tracker['tab_group_count'] = 0

    @classmethod
    def on_validate(cls, args):
        """Validate arguments."""

        return bool(args)

    def last_child(self, parent):
        """Return the last child of an `etree` element."""

        if len(parent):
            return parent[-1]
        else:
            return None

    def on_add(self, parent):
        """Adjust where the content is added."""

        for d in parent.findall('div'):
            c = d.attrib['class']
            if c == 'tabbed-content' or c.startswith('tabbed-content '):
                return list(d)[-1]

        return parent

    def on_create(self, parent):
        """Create the element."""

        new_group = self.options.get('new', 'false').lower() == 'true'
        title = self.args[0] if self.args and self.args[0] else ''
        sibling = self.last_child(parent)
        tabbed_set = 'tabbed-set tabbed-alternate'
        classes = [c for c in self.options.get('classes', '').split(' ') if c]
        tag_id = self.options.get('id', '')

        if (
            sibling and sibling.tag.lower() == 'div' and
            sibling.attrib.get('class', '') == tabbed_set and
            not new_group
        ):
            first = False
            tab_group = sibling
            sibling.set('__directive__', '')

            index = [index for index, _ in enumerate(tab_group.findall('input'), 1)][-1]
            labels = None
            content = None
            for d in tab_group.findall('div'):
                if d.attrib['class'] == 'tabbed-labels':
                    labels = d
                elif d.attrib['class'] == 'tabbed-content':
                    content = d
                if labels is not None and content is not None:
                    break
        else:
            first = True
            self.tracker['tab_group_count'] += 1
            tab_group = etree.SubElement(
                parent,
                'div',
                {'class': tabbed_set, 'data-tabs': '%d:0' % self.tracker['tab_group_count']}
            )

            index = 0
            labels = etree.SubElement(
                tab_group,
                'div',
                {'class': 'tabbed-labels'}
            )
            content = etree.SubElement(
                tab_group,
                'div',
                {'class': 'tabbed-content'}
            )

        data = tab_group.attrib['data-tabs'].split(':')
        tab_set = int(data[0])
        tab_count = int(data[1]) + 1

        attributes = {
            "name": "__tabbed_%d" % tab_set,
            "type": "radio",
            "id": "__tabbed_%d_%d" % (tab_set, tab_count)
        }

        if first:
            attributes['checked'] = 'checked'

        input_el = etree.Element(
            'input',
            attributes
        )
        tab_group.insert(index, input_el)
        lab = etree.SubElement(
            labels,
            "label",
            {
                "for": "__tabbed_%d_%d" % (tab_set, tab_count)
            }
        )
        lab.text = title

        classes.insert(0, 'tabbed-block')
        attrib = {'class': ' '.join(classes)}
        if tag_id:
            attrib['id'] = tag_id
        etree.SubElement(
            content,
            "div",
            attrib
        )

        tab_group.attrib['data-tabs'] = '%d:%d' % (tab_set, tab_count)

        return tab_group


class Details(Directive):
    """Admonition."""

    NAME = 'details'

    def on_create(self, parent):
        """Create the element."""

        # Create Detail element
        el = etree.SubElement(parent, 'details')

        # Get the type
        t = self.options.get('type', '').lower()

        # Is it open?
        args = {}
        if self.options.get('open', 'false').lower() == 'true':
            args['open'] = 'open'

        # Create the summary
        title = self.args[0] if self.args and self.args[0] else t.title()
        if not title:
            title = 'Summary'
        summary = etree.SubElement(el, 'summary')
        summary.text = title

        # Compile and add classes
        classes = [c for c in self.options.get('class', '').split(' ') if c]
        if t:
            classes.insert(0, t)
        if classes:
            el.set('class', ' '.join(classes))

        return el


class HTML(Directive):
    """Admonition."""

    NAME = 'html'
    TAG = re.compile('^[a-z][a-z0-9-]*$', re.I)

    @classmethod
    def on_validate(cls, args):
        """Validate arguments."""

        # Reject HTML names that are not valid
        return args and cls.TAG.match(args.strip()) is not None

    def on_create(self, parent):
        """Create the element."""

        attributes = {}
        for k, v in self.options.items():
            # Sanitize attribute names
            name = RE_NAME.sub('_', k)
            # Quote values
            value = v.replace('"', '&quote;')
            attributes[name] = value

        # Create element
        return etree.SubElement(parent, self.args[0].lower(), attributes)


class DirectiveProcessor(BlockProcessor):
    """Generic block processor."""

    def __init__(self, parser, md, directives):
        """Initialization."""

        super().__init__(parser)

        self.md = md
        # The directives classes indexable by name
        self.directives = {d.NAME: d for d in directives}
        # Persistent storage across a document for directives
        self.trackers = {}
        # Currently queued up directives
        self.stack = []
        # Idle directives that are hungry for more blocks.
        self.hungry = []
        # When set, the assigned directive is actively parsing blocks.
        self.working = None
        # Cached the found parent when testing
        # so we can quickly retrieve it when running
        self.cached_parent = None

    def test(self, parent, block):
        """Test to see if we should process the block."""

        # Are we hungry for more?
        if self.get_parent(parent) is not None:
            return True

        # Is this the start of a new directive?
        m = RE_START.search(block)
        d = self.directives.get(m.group(2).strip()) if m else None
        if d and d.on_validate(m.group(3).strip()):
            return True

        return False

    def _reset(self):
        """Reset."""

        self.stack.clear()
        self.hungry.clear()
        self.working = None
        self.trackers = {d: {} for d in self.directives.keys()}

    def split_end(self, blocks, length):
        """Search for end and split the blocks while removing the end."""

        good = []
        bad = []
        end = False

        # Split on our end notation for the current directive
        for e, block in enumerate(blocks):

            # Find the end of the directive
            m = None
            for match in RE_END.finditer(block):
                if len(match.group(1)) >= length:
                    m = match
                    break

            # Separate everything from before the "end" and after
            if m:
                temp = block[:m.start(1)]
                if temp:
                    good.append(temp)
                end = True

                # Since we found our end, everything after is unwanted
                temp = block[m.end(1):]
                if temp:
                    bad.append(temp)
                bad.extend(blocks[e + 1:])
                break
            else:
                # Gather blocks until we find our end
                good.append(block)

        # Augment the blocks
        blocks.clear()
        blocks.extend(bad)

        # Send back the new list of blocks to parse and note whether we found our end
        return good, end

    def split_header(self, block, blocks):
        """Split, YAML-ish header out."""

        good = []
        bad = []

        # Empty block, nothing to do
        if not block:
            blocks.insert(0, block)
            return {}

        # See if we find a start to the config
        start = RE_FRONTMATTER_START.match(block.strip('\n'))
        if start is None:
            blocks.insert(0, block)
            return {}

        # Look for the end of the config
        begin = start.end(0)
        m = RE_FRONTMATTER_END.search(block, begin)
        if m:
            good.append(block[start.start(0):m.end(1)])

            # Since we found our end, everything after is unwanted
            temp = block[m.end(1):]
            if temp:
                bad.append(temp)
            bad.extend(blocks[:])

        # Attempt to parse the config.
        # If successful, augment the blocks and return the config.
        if good:
            frontmatter = get_frontmatter('\n'.join(good))
            if frontmatter is not None:
                blocks.clear()
                blocks.extend(bad)
                return frontmatter

        # No config
        blocks.insert(0, block)
        return {}

    def get_parent(self, parent):
        """Get parent."""

        # Returned the cached parent from our last attempt
        if self.cached_parent:
            parent = self.cached_parent
            self.cached_parent = None
            return parent

        temp = parent
        while temp:
            for hungry in self.hungry:
                if hungry.parent is temp:
                    self.cached_parent = temp
                    return temp
            if temp is not None:
                temp = self.lastChild(temp)
        return None

    def parse_blocks(self, blocks, entry):
        """Parse the blocks."""

        # Get the target element and parse
        target = entry.directive.on_add(entry.el)
        self.parser.state.set('directives')
        working = self.working
        self.working = entry
        self.parser.parseBlocks(target, blocks)
        self.parser.state.reset()
        self.working = working

    def run(self, parent, blocks):
        """Convert to details/summary block."""

        # Get the appropriate parent for this directive
        temp = self.get_parent(parent)
        if temp is not None:
            parent = temp

        # Is this the start of a directive?
        m = RE_START.search(blocks[0])

        if m:
            # Ensure a "tight" parent list item is converted to "loose".
            if parent and parent.tag in ('li', 'dd'):
                text = parent.text
                if parent.text:
                    parent.text = ''
                    p = etree.SubElement(parent, 'p')
                    p.text = text

            # Create a directive object
            name = m.group(2).lower()
            directive = self.directives[name](len(m.group(1)), self.trackers[name], self.md)

            # Remove first line
            block = blocks.pop(0)
            block = block[m.end():]

            # Get frontmatter and argument(s)
            options = self.split_header(block, blocks)
            arguments = m.group(3).strip()

            # Update the config for the directive
            directive.config(arguments, **options)

            # Create the block element
            el = directive.on_create(parent)

            # Push a directive block entry on the stack.
            self.stack.append(DBlock(directive, el, parent))

            # Split out blocks we care about
            ours, end = self.split_end(blocks, directive.length)

            # Parse the blocks under the directive
            index = len(self.stack) - 1
            self.parse_blocks(ours, self.stack[-1])

            # Clean up directive if we are at the end
            # or add it to the hungry list.
            if end:
                del self.stack[index]
            else:
                self.hungry.append(self.stack[index])

        else:
            for r in range(len(self.hungry)):
                hungry = self.hungry[r]
                if parent is hungry.parent:
                    # Get the current directive
                    directive, el, _ = hungry

                    # Find and remove end from the blocks
                    ours, end = self.split_end(blocks, directive.length)

                    # Get the target element and parse
                    self.parse_blocks(ours, hungry)

                    # Clean up if we completed the directive
                    if end:
                        for r in range(len(self.stack)):
                            if self.stack[r].el is el:
                                del self.stack[r]
                                del self.hungry[r]
                                break

                    break


class HRProcessor1(HRProcessor):
    """Process Horizontal Rules."""

    RE = r'^[ ]{0,3}(?=(?P<atomicgroup>(-+[ ]{1,2}){3,}|(_+[ ]{1,2}){3,}|(\*+[ ]{1,2}){3,}))(?P=atomicgroup)[ ]*$'
    SEARCH_RE = re.compile(RE, re.MULTILINE)


class HRProcessor2(HRProcessor):
    """Process Horizontal Rules."""

    RE = r'^[ ]{0,3}(?=(?P<atomicgroup>(-+){3,}|(_+){3,}|(\*+){3,}))(?P=atomicgroup)[ ]*$'
    SEARCH_RE = re.compile(RE, re.MULTILINE)


class DirectiveExtension(Extension):
    """Add generic Blocks extension."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'directives': [[], "Directives to load, if not defined, the default ones will be loaded."]
        }

        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        """Add Blocks to Markdown instance."""
        md.registerExtension(self)

        config = self.getConfigs()
        directives = config['directives']

        if not directives:
            directives = [
                Admonition,
                Details,
                HTML,
                Note,
                Attention,
                Caution,
                Danger,
                Error,
                Tip,
                Hint,
                Important,
                Warn,
                Tab,
                Figure
            ]

        self.extension = DirectiveProcessor(md.parser, md, directives)
        # We want to be right after list indentations are processed
        md.parser.blockprocessors.register(self.extension, "directives", 89)
        # Monkey patch Markdown so we can use `---` for configuration
        md.parser.blockprocessors.register(HRProcessor1(md.parser), 'hr', 50)
        md.parser.blockprocessors.register(HRProcessor2(md.parser), 'hr2', 29.9999)

    def reset(self):
        """Reset."""

        self.extension._reset()


def makeExtension(*args, **kwargs):
    """Return extension."""

    return DirectiveExtension(*args, **kwargs)
