"""
Progress Bar.

pymdownx.progressbar
Simple plugin to add support for progress bars

/* No label */
[==30%]

/* Label */
[==30%  MyLabel]

/* works with attr_list inline style */
[==50/200  MyLabel]{: .additional-class }

~~~
New line is not required before the progress bar but suggested unless in a table.
Can take percentages and divisions.
Floats are okay.  Numbers must be positive.  This is an experimental extension.
Functionality is subject to change.

Minimum Recommended Styling
(but you could add gloss, candy striping, animation, or anything else):

~~~.css
.progress {
  display: block;
  width: 300px;
  margin: 10px 0;
  height: 24px;
  border: 1px solid #ccc;
  -webkit-border-radius: 3px;
  -moz-border-radius: 3px;
  border-radius: 3px;
  background-color: #F8F8F8;
  position: relative;
  box-shadow: inset -1px 1px 3px rgba(0, 0, 0, .1);
}

.progress-label {
  position: absolute;
  text-align: center;
  font-weight: bold;
  width: 100%; margin: 0;
  line-height: 24px;
  color: #333;
  -webkit-font-smoothing: antialiased !important;
  white-space: nowrap;
  overflow: hidden;
}

.progress-bar {
  height: 24px;
  float: left;
  border-right: 1px solid #ccc;
  -webkit-border-radius: 3px;
  -moz-border-radius: 3px;
  border-radius: 3px;
  background-color: #34c2e3;
  box-shadow: inset 0 1px 0px rgba(255, 255, 255, .5);
}

For Level Colors

.progress-100plus .progress-bar {
  background-color: #1ee038;
}

.progress-80plus .progress-bar {
  background-color: #86e01e;
}

.progress-60plus .progress-bar {
  background-color: #f2d31b;
}

.progress-40plus .progress-bar {
  background-color: #f2b01e;
}

.progress-20plus .progress-bar {
  background-color: #f27011;
}

.progress-0plus .progress-bar {
  background-color: #f63a0f;
}
~~~

MIT license.

Copyright (c) 2014 - 2017 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
from __future__ import unicode_literals
from . import util
from markdown import Extension
from markdown import util as md_util
from markdown.extensions.attr_list import AttrListTreeprocessor
from markdown.inlinepatterns import Pattern
from markdown.inlinepatterns import dequote

RE_PROGRESS = r'''(?x)
\[={1,}\s*                                                          # Opening
(?:
  (?P<percent>100(?:.0+)?|[1-9]?[0-9](?:\.\d+)?)% |                 # Percent
  (?:(?P<frac_num>\d+(?:\.\d+)?)\s*/\s*(?P<frac_den>\d+(?:\.\d+)?)) # Fraction
)
(?P<title>\s+(?P<quote>['"]).*?(?P=quote))?\s*                      # Title
\]                                                                  # Closing
(?P<attr_list>\{\:?([^\}]*)\})?                                     # Optional attr list
'''

CLASS_100PLUS = "progress-100plus"
CLASS_90PLUS = "progress-90plus"
CLASS_80PLUS = "progress-80plus"
CLASS_70PLUS = "progress-70plus"
CLASS_60PLUS = "progress-60plus"
CLASS_50PLUS = "progress-50plus"
CLASS_40PLUS = "progress-40plus"
CLASS_30PLUS = "progress-30plus"
CLASS_20PLUS = "progress-20plus"
CLASS_10PLUS = "progress-10plus"
CLASS_0PLUS = "progress-0plus"


class ProgressBarTreeProcessor(AttrListTreeprocessor):
    """Used for AttrList compatibility."""

    def run(self, elem):
        """Inline check for attributes at start of tail."""

        if elem.tail:
            m = self.INLINE_RE.match(elem.tail)
            if m:
                self.assign_attrs(elem, m.group(1))
                elem.tail = elem.tail[m.end():]


class ProgressBarPattern(Pattern):
    """Pattern handler for the progress bars."""

    def __init__(self, pattern):
        """Initialize."""

        Pattern.__init__(self, pattern)

    def create_tag(self, width, label, add_classes, alist):
        """Create the tag."""

        # Create list of all classes and remove duplicates
        classes = sorted(
            set(
                ["progress"] +
                self.config.get('add_classes', '').split() +
                add_classes
            )
        )
        el = md_util.etree.Element("div")
        el.set('class', ' '.join(classes))
        bar = md_util.etree.SubElement(el, 'div')
        bar.set('class', "progress-bar")
        bar.set('style', 'width:%s%%' % width)
        p = md_util.etree.SubElement(bar, 'p')
        p.set('class', 'progress-label')
        p.text = label
        if alist is not None:
            el.tail = alist
            if 'attr_list' in self.markdown.treeprocessors.keys():
                ProgressBarTreeProcessor(self.markdown).run(el)
        return el

    def handleMatch(self, m):
        """Handle the match."""

        label = ""
        level_class = self.config.get('level_class', False)
        add_classes = []
        alist = None
        if m.group(5):
            label = dequote(self.unescape(m.group('title').strip()))
        if m.group('attr_list'):
            alist = m.group('attr_list')
        if m.group('percent'):
            value = float(m.group(2))
        else:
            try:
                num = float(m.group('frac_num'))
            except Exception:  # pragma: no cover
                num = 0.0
            try:
                den = float(m.group('frac_den'))
            except Exception:  # pragma: no cover
                den = 0.0
            if den == 0.0:
                value = 0.0
            else:
                value = (num / den) * 100.0

        # We can never get a value < 0,
        # but we must check for > 100.
        if value > 100.0:
            value = 100.0

        if level_class:
            if value >= 100.0:
                add_classes.append(CLASS_100PLUS)
            elif value >= 90.0:
                add_classes.append(CLASS_90PLUS)
            elif value >= 80.0:
                add_classes.append(CLASS_80PLUS)
            elif value >= 70.0:
                add_classes.append(CLASS_70PLUS)
            elif value >= 60.0:
                add_classes.append(CLASS_60PLUS)
            elif value >= 50.0:
                add_classes.append(CLASS_50PLUS)
            elif value >= 40.0:
                add_classes.append(CLASS_40PLUS)
            elif value >= 30.0:
                add_classes.append(CLASS_30PLUS)
            elif value >= 20.0:
                add_classes.append(CLASS_20PLUS)
            elif value >= 10.0:
                add_classes.append(CLASS_10PLUS)
            else:
                add_classes.append(CLASS_0PLUS)

        return self.create_tag('%.2f' % value, label, add_classes, alist)


class ProgressBarExtension(Extension):
    """Add progress bar extension to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'level_class': [
                True,
                "Include class that defines progress level in increments of 10 - Default: True"
            ],
            'add_classes': [
                '',
                "Add additional classes to the progress tag for styling.  "
                "Classes are separated by spaces. - Default: None"
            ]
        }

        super(ProgressBarExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """Add the progress bar pattern handler."""

        util.escape_chars(md, ['='])
        progress = ProgressBarPattern(RE_PROGRESS)
        progress.config = self.getConfigs()
        progress.markdown = md
        md.inlinePatterns.add("progress-bar", progress, ">escape")


def makeExtension(*args, **kwargs):
    """Return extension."""

    return ProgressBarExtension(*args, **kwargs)
