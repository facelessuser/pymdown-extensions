"""
Captions.

Captions should be placed after a block, that block will be wrapped in a `figure`
and captions will be inserted either at the end of the figure or at the beginning.
If the preceding block happens to be a `figure`, if no `figcaption` is detected
within, the caption will be injected into that figure instead of wrapping.
Keep in mind that when `md_in_html` is used and raw HTML is used, if `markdown=1`
is not present on the caption, the caption will be invisible to this extension.

Class, IDs, or other attributes will be attached to the figure, not the caption.

`prepend`:
    Will prepend `figcaption` at the start of a `figure` instead of the end.
`autoid`:
    Will generate IDs for all figures unless they have an ID defined already.
    If a figure manually defines an ID, that figure will be skipped along with
    all descendant figures under it since descendant IDs are all relative to the
    parent.
`prefix`:
    Provide a template that will be used to add a prefix with auto incrementing
    figure count. If `autoid` is enabled, there will be interlock between the
    `prefix` and the `autoid` such that the numbers will correspond with one
    another. If a figure defines its own ID, and `autoid` is enabled, `prefix`
    will not be applied to that figure as IDs will not be populated for that
    figure, nor its descendant figures.
`prefix_level`:
    When set to 0, prefixes are added to all figures, but when a non-zero depth
    is provided, prefixes will only be applied to that depth, 1 meaning only the
    outermost `figure`.

"""
import xml.etree.ElementTree as etree
from .block import Block
from .. blocks import BlocksExtension
from markdown.treeprocessors import Treeprocessor


class CaptionTreeprocessor(Treeprocessor):
    """Caption tree processor."""

    def __init__(self, md, config):
        """Initialize."""

        super().__init__(md)

        self.autoid = config['autoid']
        self.prepend = config['prepend']
        self.prefix = config['prefix']
        self.prefix_level = config['prefix_level']

    def run(self, doc):
        """Update caption IDs and prefixes."""

        parent_map = {c: p for p in doc.iter() for c in p}
        count = [0]
        last = 0
        skip = set()

        # Calculate the depth and iteration at that depth of the given figure.
        for el in doc.iter():
            prefix = self.prefix
            stack = -1
            if el.tag == 'figure' and (not self.autoid or 'id' not in el.attrib):
                stack += 1
                current = el
                while True:
                    parent = parent_map.get(current, None)

                    # No more parents
                    if parent is None:
                        break

                    if parent.tag == 'figure' and parent not in skip:
                        if self.prefix_level and stack >= (self.prefix_level - 1):
                            prefix = False
                        stack += 1

                    elif parent.tag == 'figure':
                        skip.add(el)
                        stack = -1
                        break

                    current = parent
            elif el.tag == 'figure':
                skip.add(el)
                continue

            # Found an appropriate figure at an acceptable depth
            if stack > -1:
                if stack > last:
                    if (stack + 1) > len(count):
                        count.append(1)
                    else:
                        count[stack] = 1
                elif stack == last:
                    count[stack] += 1
                elif stack < last:
                    count = count[:stack + 1]
                    count[-1] += 1
                last = stack

                # Auto add an ID
                if self.autoid:
                    el.attrib['id'] = '__caption_' + '_'.join(str(x) for x in count[:stack + 1])

                # Prefix the caption with a given numbered prefix
                if prefix:
                    for child in list(el) if self.prepend else reversed(el):
                        if child.tag == 'figcaption':
                            children = list(child)
                            value = self.prefix.format('.'.join(str(x) for x in count[:stack + 1]))
                            if not len(children) or children[0].tag != 'p':
                                p = etree.Element('p')
                                p.text = value
                                child.insert(0, p)
                            else:
                                text = children[0].text
                                if text is None:
                                    text = ''
                                children[0].text = value + text


class Caption(Block):
    """Figure captions."""

    NAME = 'caption'

    def on_init(self):
        """Initialize."""

        self.prepend = self.config['prepend']
        self.caption = None

    def on_create(self, parent):
        """Create the element."""

        # Find sibling to add caption to.
        fig = None
        child = None
        children = list(parent)
        if children:
            child = children[-1]
            # Do we have a figure with no caption?
            if child.tag == 'figure':
                fig = child
                for c in list(child):
                    if c.tag == 'figcaption':
                        fig = None
                        break

        # Create a new figure if sibling is not a figure or already has a caption.
        # Add sibling to the new figure.
        if fig is None:
            fig = etree.SubElement(parent, 'figure')
            if child is not None:
                fig.append(child)
                parent.remove(child)

        # Add caption to the target figure.
        if self.prepend:
            self.caption = etree.Element('figcaption')
            fig.insert(0, self.caption)
        else:
            self.caption = etree.SubElement(fig, 'figcaption')

        return fig

    def on_add(self, block):
        """Return caption as the target container for content."""

        return self.caption


class CaptionExtension(BlocksExtension):
    """Caption Extension."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            "prefix": [
                "",
                "Specify a prefix to add to captions `{}` will have an incrementing numerical count - Default: ''"
            ],
            "prefix_level": [
                0,
                "Depth of children to add prefixes to - Default: 0"
            ],
            "autoid": [
                False,
                "Auto add IDs - Default: False"
            ],
            "prepend": [
                False,
                "Prepend captions opposed to appending - Default: False"
            ]
        }

        super().__init__(*args, **kwargs)

    def extendMarkdownBlocks(self, md, block_mgr):
        """Extend Markdown blocks."""

        config = self.getConfigs()
        block_mgr.register(Caption, config)
        if config['autoid'] or config['prefix']:
            md.treeprocessors.register(CaptionTreeprocessor(md, config), 'caption_id', 4)


def makeExtension(*args, **kwargs):
    """Return extension."""

    return CaptionExtension(*args, **kwargs)
