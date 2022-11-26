"""Generic blocks extension."""
from markdown import Extension
from markdown.blockprocessors import BlockProcessor, HRProcessor
from markdown import util as mutil
import xml.etree.ElementTree as etree
import re
from .admonition import Admonition
from .tab import Tab
from .details import Details
from .html import HTML
import yaml

# Fenced block placeholder for SuperFences
FENCED_BLOCK_RE = re.compile(
    r'^([\> ]*){}({}){}$'.format(
        mutil.HTML_PLACEHOLDER[0],
        mutil.HTML_PLACEHOLDER[1:-1] % r'([0-9]+)',
        mutil.HTML_PLACEHOLDER[-1]
    )
)

# Block start/end
RE_START = re.compile(
    r'(?:^|\n)[ ]{0,3}(/{3,})[ ]*([\w-]+)[ ]*(?:\|[ ]*(.*?)[ ]*)?(?:\n|$)'
)

RE_END = re.compile(
    r'(?m)(?:^|\n)[ ]{0,3}(/{3,})[ ]*(?:\n|$)'
)

RE_COLON_START = re.compile(
    r'(?:^|\n)[ ]{0,3}(:{3,})[ ]*([\w-]+)[ ]*(?:\|[ ]*(.*?)[ ]*)?(?:\n|$)'
)

RE_COLON_END = re.compile(
    r'(?m)(?:^|\n)[ ]{0,3}(:{3,})[ ]*(?:\n|$)'
)

# Frontmatter patterns
RE_YAML_START = re.compile(r'(?m)^[ ]{0,3}(-{3})[ ]*(?:\n|$)')

RE_YAML_END = re.compile(
    r'(?m)^[ ]{0,3}(-{3})[ ]*(?:\n|$)'
)


class BlockEntry:
    """Track Block entries."""

    def __init__(self, block, el, parent):
        """Block entry."""

        self.block = block
        self.el = el
        self.parent = parent
        self.hungry = False


def get_frontmatter(string):
    """
    Get frontmatter from string.

    YAML-ish key value pairs.
    """

    frontmatter = None

    try:
        frontmatter = yaml.safe_load(string)
        if not isinstance(frontmatter, dict):
            frontmatter = None
    except Exception:
        pass

    return frontmatter


def reindent(text, pos, level):
    """Reindent the code to where it is supposed to be."""

    indented = []
    for line in text.split('\n'):
        index = pos - level
        indented.append(line[index:])
    return indented


def revert_fenced_code(md, blocks):
    """Look for SuperFences code placeholders and revert them back to plain text."""

    superfences = None
    try:
        from ..superfences import SuperFencesBlockPreprocessor
        processor = md.preprocessors['fenced_code_block']
        if isinstance(processor, SuperFencesBlockPreprocessor):
            superfences = processor.extension
    except Exception:
        pass

    # We could not find the SuperFences extension, so nothing to do
    if superfences is None:
        return blocks

    new_blocks = []
    for block in blocks:
        new_lines = []
        for line in block.split('\n'):
            m = FENCED_BLOCK_RE.match(line)
            if m:
                key = m.group(2)
                indent_level = len(m.group(1))
                original = None
                original, pos = superfences.stash.get(key, (None, None))
                if original is not None:
                    code = reindent(original, pos, indent_level)
                    new_lines.extend(code)
                    superfences.stash.remove(key)
                if original is None:  # pragma: no cover
                    new_lines.append(line)
            else:
                new_lines.append(line)
        new_blocks.append('\n'.join(new_lines))

    return new_blocks


class BlocksProcessor(BlockProcessor):
    """Generic block processor."""

    def __init__(self, parser, md, config):
        """Initialization."""

        self.md = md

        blocks = config['blocks']

        if not blocks:
            blocks = [
                Admonition,
                Details,
                HTML,
                Tab
            ]

        # The Block classes indexable by name
        self.blocks = {}
        self.config = {}
        for b in blocks:
            self.register(b, config['block_configs'].get(b.NAME, {}))

        self.empty_tags = set(['hr'])
        self.block_level_tags = set(md.block_level_elements.copy())
        self.block_level_tags.add('html')

        # Block-level tags in which the content only gets span level parsing
        self.span_tags = set(
            ['address', 'dd', 'dt', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'legend', 'li', 'p', 'summary', 'td', 'th']
        )
        # Block-level tags which never get their content parsed.
        self.raw_tags = set(['canvas', 'math', 'option', 'pre', 'script', 'style', 'textarea'])
        # Block-level tags in which the content gets parsed as blocks
        self.block_tags = set(self.block_level_tags) - (self.span_tags | self.raw_tags | self.empty_tags)
        self.span_and_blocks_tags = self.block_tags | self.span_tags

        super().__init__(parser)

        # Persistent storage across a document for blocks
        self.trackers = {}
        # Currently queued up blocks
        self.stack = []
        # When set, the assigned block is actively parsing blocks.
        self.working = None
        # Cached the found parent when testing
        # so we can quickly retrieve it when running
        self.cached_parent = None
        self.cached_block = None

        # Used during the alpha/beta stage
        self.require_yaml_fences = config['require_yaml_fences']
        self.start = RE_START if not config['colon_syntax'] else RE_COLON_START
        self.end = RE_END if not config['colon_syntax'] else RE_COLON_END

    def register(self, b, config):
        """Register a block."""

        if b.NAME in self.blocks:
            raise ValueError('The block name {} is already registered!'.format(b.NAME))
        self.blocks[b.NAME] = b
        self.config[b.NAME] = self.set_configs(b.CONFIG, config)
        b.on_register(self, self.md, self.config.get(b.NAME, {}))

    def set_configs(self, default, config):
        """Set config for a block extension."""

        d = {}
        for key in default.keys():
            if key in config:
                d[key] = config[key]
            else:
                d[key] = default[key]
        return d

    def test(self, parent, block):
        """Test to see if we should process the block."""

        # Are we hungry for more?
        if self.get_parent(parent) is not None:
            return True

        # Is this the start of a new block?
        m = self.start.search(block)
        if m:

            pre_text = block[:m.start()] if m.start() > 0 else None

            # Create a block object
            name = m.group(2).lower()
            if name in self.blocks:
                generic_block = self.blocks[name](len(m.group(1)), self.trackers[name], self.md, self.config[name])
                # Remove first line
                block = block[m.end():]

                # Get frontmatter and argument(s)
                the_rest = []
                options = self.split_header(block, the_rest, generic_block.length)
                arguments = m.group(3)

                # Options must be valid
                status = options is not None

                # Update the config for the Block
                if status:
                    status = generic_block.parse_config(arguments, **options)

                # Cache the found Block and any remaining content
                if status:
                    self.cached_block = (generic_block, the_rest[0] if the_rest else '')
                    # Any text before the block should get handled
                    if pre_text is not None:
                        self.parser.parseBlocks(parent, [pre_text])

                return status
        return False

    def _reset(self):
        """Reset."""

        self.stack.clear()
        self.working = None
        self.trackers = {d: {} for d in self.blocks.keys()}

    def split_end(self, blocks, length):
        """Search for end and split the blocks while removing the end."""

        good = []
        bad = []
        end = False

        # Split on our end notation for the current Block
        for e, block in enumerate(blocks):

            # Find the end of the Block
            m = None
            for match in self.end.finditer(block):
                if len(match.group(1)) >= length:
                    m = match
                    break

            # Separate everything from before the "end" and after
            if m:
                temp = block[:m.start(0)]
                if temp:
                    good.append(temp)
                end = True

                # Since we found our end, everything after is unwanted
                temp = block[m.end(0):]
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

    def split_header(self, block, blocks, length):
        """Split, YAML-ish header out."""

        # Search for end in first block
        m = None
        for match in self.end.finditer(block):
            if len(match.group(1)) >= length:
                m = match
                break

        # Move block ending to be parsed later
        if m:
            end = block[m.start(0):]
            blocks.insert(0, end)
            block = block[:m.start(0)]

        # More formal YAML config
        start = RE_YAML_START.match(block.strip('\n'))
        if start is not None:
            # Look for the end of the config
            begin = start.end(0)
            m = RE_YAML_END.search(block, begin)
            if m:
                # There shouldn't be anything after the config
                leftover = block[m.end(0):]
                if leftover.strip():
                    if not self.require_yaml_fences:
                        return None
                    else:
                        blocks.insert(0, leftover)

                block = block[start.end(0):m.start(0)]

            # No YAML end
            else:
                return None
        elif self.require_yaml_fences:
            blocks.insert(0, block)
            return {}

        # Attempt to parse the config.
        # If successful, augment the blocks and return the config.
        if block.strip():
            return get_frontmatter(block)
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
            for entry in self.stack:
                if entry.hungry and entry.parent is temp:
                    self.cached_parent = temp
                    return temp
            if temp is not None:
                temp = self.lastChild(temp)
        return None

    def parse_blocks(self, blocks, entry):
        """Parse the blocks."""

        # Get the target element and parse

        for b in blocks:
            target = entry.block.on_add(entry.el)

            # The Block does not or no longer accepts more content
            if target is None:  # pragma: no cover
                break

            tag = target.tag
            mode = entry.block.on_markdown()
            is_block = mode == 'block' or (mode == 'auto' and tag in self.block_tags)
            is_atomic = mode == 'raw' or (mode == 'auto' and tag in self.raw_tags)

            # We should revert fenced code in spans or atomic tags.
            # Make sure atomic tags have content wrapped as `AtomicString`.
            if is_atomic or not is_block:
                text = target.text
                b = '\n\n'.join(revert_fenced_code(self.md, [b]))
                if text:
                    text += '\n\n' + b
                else:
                    text = b
                target.text = mutil.AtomicString(text) if is_atomic else text

            # Block tags should have content go through the normal block processor
            else:
                self.parser.state.set('blocks')
                working = self.working
                self.working = entry
                self.parser.parseChunk(target, b)
                self.parser.state.reset()
                self.working = working

    def run(self, parent, blocks):
        """Convert to details/summary block."""

        # Get the appropriate parent for this Block
        temp = self.get_parent(parent)
        if temp is not None:
            parent = temp

        # Did we find a new Block?
        if self.cached_block:
            # Get cached Block and reset the cache
            generic_block, block = self.cached_block
            self.cached_block = None

            # Discard first block as we've already processed what we need from it
            blocks.pop(0)
            if block:
                blocks.insert(0, block)

            # Ensure a "tight" parent list item is converted to "loose".
            if parent and parent.tag in ('li', 'dd'):  # pragma: no cover
                text = parent.text
                if parent.text:
                    parent.text = ''
                    p = etree.SubElement(parent, 'p')
                    p.text = text

            # Create the block element
            el = generic_block.create(parent)

            # Push a Block entry on the stack.
            self.stack.append(BlockEntry(generic_block, el, parent))

            # Split out blocks we care about
            ours, end = self.split_end(blocks, generic_block.length)

            # Parse the text blocks under the Block
            index = len(self.stack) - 1
            self.parse_blocks(ours, self.stack[-1])

            # Remove Block from the stack if we are at the end
            # or add it to the hungry list.
            if end:
                # Run the "on end" event
                generic_block.on_end(el)
                del self.stack[index]
            else:
                self.stack[index].hungry = True

        else:
            for r in range(len(self.stack)):
                entry = self.stack[r]
                if entry.hungry and parent is entry.parent:
                    # Find and remove end from the blocks
                    ours, end = self.split_end(blocks, entry.block.length)

                    # Get the target element and parse
                    entry.hungry = False
                    self.parse_blocks(ours, entry)

                    # Clean up if we completed the Block
                    if end:
                        # Run "on end" event
                        entry.block.on_end(entry.el)
                        del self.stack[r]
                    else:
                        entry.hungry = True

                    break


class HRProcessor1(HRProcessor):
    """Process Horizontal Rules."""

    RE = r'^[ ]{0,3}(?=(?P<atomicgroup>(-+[ ]{1,2}){3,}|(_+[ ]{1,2}){3,}|(\*+[ ]{1,2}){3,}))(?P=atomicgroup)[ ]*$'
    SEARCH_RE = re.compile(RE, re.MULTILINE)


class HRProcessor2(HRProcessor):
    """Process Horizontal Rules."""

    RE = r'^[ ]{0,3}(?=(?P<atomicgroup>(-+){3,}|(_+){3,}|(\*+){3,}))(?P=atomicgroup)[ ]*$'
    SEARCH_RE = re.compile(RE, re.MULTILINE)


class BlocksExtension(Extension):
    """Add generic Blocks extension."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'blocks': [[], "Blocks extensions to load, if not defined, the default ones will be loaded."],
            'block_configs': [{}, "Global configuration for a given block."],
            'require_yaml_fences': [False, "Require YAML fences in generic blocks."],
            'colon_syntax': [False, "Use colon syntax."]
        }

        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        """Add Blocks to Markdown instance."""

        md.registerExtension(self)

        config = self.getConfigs()
        self.extension = BlocksProcessor(md.parser, md, config)
        # We want to be right after list indentations are processed
        md.parser.blockprocessors.register(self.extension, "blocks", 89)
        # Monkey patch Markdown so we can use `---` for configuration
        md.parser.blockprocessors.register(HRProcessor1(md.parser), 'hr', 50)
        md.parser.blockprocessors.register(HRProcessor2(md.parser), 'hr2', 29.9999)

    def reset(self):
        """Reset."""

        self.extension._reset()


def makeExtension(*args, **kwargs):
    """Return extension."""

    return BlocksExtension(*args, **kwargs)
