"""Tabs."""
import xml.etree.ElementTree as etree
from .directive import Directive, to_flag, to_classes, to_html_attribute, to_string


class Tabs(Directive):
    """
    Tabbed container.

    Arguments (1):
    - Title

    Options:
    - `new`: force a new tab group by setting to `true` or `false`
    - `class`: classes to apply to the tab block
    - `id`: id to apply to the tab block.

    Content:

    Tab content
    """

    NAME = 'tab'

    ARGUMENTS = {'required': 1, 'parsers': [to_string]}
    OPTIONS = {
        'new': [False, to_flag],
        'class': [[], to_classes],
        'id': ['', to_html_attribute]
    }

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

        new_group = self.options['new']
        title = self.args[0] if self.args and self.args[0] else ''
        sibling = self.last_child(parent)
        tabbed_set = 'tabbed-set tabbed-alternate'
        classes = self.options['class']
        tag_id = self.options['id']

        if (
            sibling and sibling.tag.lower() == 'div' and
            sibling.attrib.get('class', '') == tabbed_set and
            not new_group
        ):
            first = False
            tab_group = sibling

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
