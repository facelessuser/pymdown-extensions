"""
Emoji.

pymdownx.emoji
Emoji extension for emojione or Github's gemoji.

MIT license.

Copyright (c) 2016 - 2017 Isaac Muse <isaacmuse@gmail.com>

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
from markdown import Extension
from markdown.inlinepatterns import Pattern
from markdown import util
import sys

PY3 = sys.version_info >= (3, 0)
IS_NARROW = sys.maxunicode == 0xFFFF

if PY3:
    uchr = chr
else:
    uchr = unichr

RE_EMOJI = r'(:[+\-\w]+:)'
EMOJIONE_SVG_SPRITE_TAG = (
    '<svg class="%(classes)s"><description>%(alt)s</description>'
    '<use xlink:href="%(sprite)s#emoji-%(unicode)s"></use></svg>'
)
SUPPORTED_INDEXES = ('emojione', 'gemoji')
UNICODE_VARIATION_SELECTOR_16 = 'fe0f'
EMOJIONE_SVG_CDN = 'https://cdn.jsdelivr.net/emojione/assets/svg/'
EMOJIONE_PNG_CDN = 'https://cdn.jsdelivr.net/emojione/assets/png/'
GITHUB_UNICODE_CDN = 'https://assets-cdn.github.com/images/icons/emoji/unicode/'
GITHUB_CDN = 'https://assets-cdn.github.com/images/icons/emoji/'
VALID_TITLE = ('long', 'short', 'none')
VALID_ALT = ('short', 'unicode', 'html_entity')

if IS_NARROW:  # pragma: no cover
    # For ease of supporting, just require uniseq for both narrow and wide PY27.

    def get_code_points(s):
        """Get the Unicode code points."""

        pt = []

        def is_full_point(p, point):
            """
            Check if we have a full code point.

            Surrogates are stored in point.
            """
            v = ord(p)
            if 0xD800 <= v <= 0xDBFF:
                del point[:]
                point.append(p)
                return False
            if point and 0xDC00 <= v <= 0xDFFF:
                point.append(p)
                return True
            del point[:]
            return True

        return [(''.join(pt) if pt else c) for c in s if is_full_point(c, pt)]

    def get_ord(c):
        """Get Unicode ord."""

        if len(c) == 2:
            high, low = [ord(p) for p in c]
            ordinal = (high - 0xD800) * 0x400 + low - 0xDC00 + 0x10000
        else:
            ordinal = ord(c)

        return ordinal

else:
    def get_code_points(s):
        """Get the Unicode code points."""

        return [c for c in s]

    def get_ord(c):
        """Get Unicode ord."""

        return ord(c)


def add_attriubtes(options, attributes):
    """Add aditional attributes from options."""

    attr = options.get('attributes', {})
    if attr:
        for k, v in attr.items():
            attributes[k] = v


def emojione():
    """Emojione index."""

    from . import emoji1_db as emoji_map
    return {"name": emoji_map.name, "emoji": emoji_map.emoji, "aliases": emoji_map.aliases}


def gemoji():
    """gemoji_index index."""

    from . import gemoji_db as emoji_map
    return {"name": emoji_map.name, "emoji": emoji_map.emoji, "aliases": emoji_map.aliases}


###################
# Converters
###################
def to_png(index, shortname, alias, uc, alt, title, options, md):
    """Return png element."""

    if index == 'gemoji':
        def_image_path = GITHUB_UNICODE_CDN
        def_non_std_image_path = GITHUB_CDN
    else:
        def_image_path = EMOJIONE_PNG_CDN
        def_non_std_image_path = EMOJIONE_PNG_CDN

    is_unicode = uc is not None
    classes = options.get('classes', index)

    # In genral we can use the alias, but github specific images don't have one for each alias.
    # We can tell we have a github specific if there is no Unicode value.
    if is_unicode:
        image_path = options.get('image_path', def_image_path)
    else:
        image_path = options.get('non_standard_image_path', def_non_std_image_path)

    src = "%s%s.png" % (
        image_path,
        uc if is_unicode else shortname[1:-1]
    )

    attributes = {
        "class": classes,
        "alt": alt,
        "src": src
    }

    if title:
        attributes['title'] = title

    add_attriubtes(options, attributes)

    return util.etree.Element("img", attributes)


def to_svg(index, shortname, alias, uc, alt, title, options, md):
    """Return svg element."""

    attributes = {
        "class": options.get('classes', index),
        "alt": alt,
        "src": "%s%s.svg" % (
            options.get('image_path', EMOJIONE_SVG_CDN),
            uc
        )
    }

    if title:
        attributes['title'] = title

    add_attriubtes(options, attributes)

    return util.etree.Element("img", attributes)


def to_png_sprite(index, shortname, alias, uc, alt, title, options, md):
    """Return png sprite element."""

    attributes = {
        "class": '%(class)s-%(unicode)s' % {
            "class": options.get('classes', '%s %s' % (index, index)),
            "unicode": uc
        }
    }

    if title:
        attributes['title'] = title

    add_attriubtes(options, attributes)

    el = util.etree.Element("span", attributes)
    el.text = alt

    return el


def to_svg_sprite(index, shortname, alias, uc, alt, title, options, md):
    """Return svg sprite element."""

    html = EMOJIONE_SVG_SPRITE_TAG % {
        "classes": options.get('classes', index),
        "alt": alt,
        "sprite": options.get('image_path', './../assets/sprites/emojione.sprites.svg'),
        "unicode": uc
    }

    return md.htmlStash.store(html, safe=True)


def to_awesome(index, shortname, alias, uc, alt, title, options, md):
    """
    Return "awesome style element for "font-awesome" format.

    See: https://github.com/Ranks/emojione/tree/master/lib/emojione-awesome.
    """

    classes = '%s-%s' % (options.get('classes', 'e1a'), shortname[1:-1])
    attributes = {"class": classes}
    add_attriubtes(options, attributes)
    return util.etree.Element("i", attributes)


def to_alt(index, shortname, alias, uc, alt, title, options, md):
    """Return html entities."""

    return md.htmlStash.store(alt, safe=True)


###################
# Classes
###################
class EmojiPattern(Pattern):
    """Return element of type `tag` with a text attribute of group(3) of a Pattern."""

    def __init__(
        self, pattern, index, generator, remove_var_sel,
        alt, title, options, md
    ):
        """Initialize."""

        self._set_index(index)
        self.markdown = md
        self.unicode_alt = alt in ('unicode', 'html_entity')
        self.encoded_alt = alt == 'html_entity'
        self.remove_var_sel = remove_var_sel
        self.title = title
        self.generator = generator
        self.options = options
        Pattern.__init__(self, pattern)

    def _set_index(self, index):
        """Set the index."""

        self.emoji_index = index()

    def _remove_variation_selector(self, value):
        """Remove variation selectors."""

        return value.replace('-' + UNICODE_VARIATION_SELECTOR_16, '')

    def _get_char(self, value):
        """Get the Unicode char."""
        if IS_NARROW:  # pragma: no cover
            if value > 0xFFFF:
                c = ''.join(
                    [
                        uchr(int((value - 0x10000) / (0x400)) + 0xD800),
                        uchr((value - 0x10000) % 0x400 + 0xDC00)
                    ]
                )
            else:
                c = uchr(value)
        else:
            c = uchr(value)
        return c

    def _get_unicode_char(self, value):
        """Get the Unicode char."""

        return ''.join([self._get_char(int(c, 16)) for c in value.split('-')])

    def _get_unicode(self, emoji):
        """
        Get Unicode and Unicode alt.

        Unicode: This is the stripped down form of the Unicode, no joining chars and no variation chars.
            Unicode code points are not always valid.  If this is present and there is no 'unicode_alt',
            Unicode code points can be counted on as valid.  For the most part, the returned `uc` should
            be used to reference image files, or create classes, but for inserting actual Unicode, 'uc_alt'
            should be used.

        Unicode Alt: When present, this will always be valid Unicode points.  This contains not just the
            needed characters to identify the Unicode emoji, but the formatting as well. Joining characters
            and variation characters will be present. If you don't want variation chars, enable the global
            'remove_variation_selector' option.

        If using gemoji, it is possible you will get no Unicode and no Unicode alt.  This occurs with emoji
        like :octocat:.  :octocat: is not a real emoji and has no Unicode code points, but it is provided by
        gememoji as an emoji anyways.
        """

        uc = emoji.get('unicode')
        uc_alt = emoji.get('unicode_alt', uc)
        if uc_alt and self.remove_var_sel:
            uc_alt = self._remove_variation_selector(uc_alt)

        return uc, uc_alt

    def _get_title(self, shortname, emoji):
        """Get the title."""

        if self.title == 'long':
            title = emoji['name']
        elif self.title == 'short':
            title = shortname
        else:
            title = None
        return title

    def _get_alt(self, shortname, uc_alt):
        """Get alt form."""

        if uc_alt is None or not self.unicode_alt:
            alt = shortname
        else:
            alt = self._get_unicode_char(uc_alt)
            if self.encoded_alt:
                alt = ''.join(
                    [util.AMP_SUBSTITUTE + ('#x%04x;' % get_ord(point)) for point in get_code_points(alt)]
                )
        return alt

    def handleMatch(self, m):
        """Hanlde emoji pattern matches."""

        el = m.group(2)

        shortname = self.emoji_index['aliases'].get(el, el)
        alias = None if shortname == el else el
        emoji = self.emoji_index['emoji'].get(shortname, None)
        if emoji:
            uc, uc_alt = self._get_unicode(emoji)
            title = self._get_title(el, emoji)
            alt = self._get_alt(el, uc_alt)
            el = self.generator(
                self.emoji_index['name'],
                shortname,
                alias,
                uc,
                alt,
                title,
                self.options,
                self.markdown
            )

        return el


class EmojiExtension(Extension):
    """Add emoji extension to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'emoji_index': [
                emojione,
                "Function that returns the desired emoji index. - Default: 'pymdownx.emoji.emojione'"
            ],
            'emoji_generator': [
                to_png,
                "Emoji generator method. - Default: pymdownx.emoji.to_png"
            ],
            'title': [
                'short',
                "What title to use on images. You can use 'long' which shows the long name, "
                "'short' which shows the shortname (:short:), or 'none' which shows no title. "
                "- Default: 'short'"
            ],
            'alt': [
                'unicode',
                "Control alt form. 'short' sets alt to the shortname (:short:), 'uniocde' sets "
                "alt to the raw Unicode value, and 'html_entity' sets alt to the HTML entity. "
                "- Default: 'unicode'"
            ],
            'remove_variation_selector': [
                False,
                "Remove variation selector 16 from unicode. - Default: False"
            ],
            'options': [
                {},
                "Emoji options see documentation for options for github and emojione."
            ]
        }
        super(EmojiExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """Add support for emojis."""

        emoji_index = self.getConfigs()["emoji_index"]
        generator = self.getConfigs()['emoji_generator']
        title = self.getConfigs()['title']
        alt = self.getConfigs()['alt']
        options = self.getConfigs()['options']
        remove_var_sel = self.getConfigs()['remove_variation_selector']

        assert title in VALID_TITLE, "Invalid 'title' option!"
        assert alt in VALID_ALT, "Invalid 'alt' option!"

        if ":" not in md.ESCAPED_CHARS:
            md.ESCAPED_CHARS.append(':')

        md.inlinePatterns.add(
            "emoji",
            EmojiPattern(
                RE_EMOJI, emoji_index, generator, remove_var_sel,
                alt, title, options, md
            ),
            "<not_strong"
        )


###################
# Make Available
###################
def makeExtension(*args, **kwargs):
    """Return extension."""

    return EmojiExtension(*args, **kwargs)
