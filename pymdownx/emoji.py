"""
Emoji.

pymdownx.emoji
Emoji extension for EmojiOne's, GitHub's, or Twemoji's gemoji.

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
from __future__ import annotations
from markdown import Extension, Markdown
from markdown.inlinepatterns import InlineProcessor
from markdown.postprocessors import Postprocessor
from markdown import util as md_util
import xml.etree.ElementTree as etree
import copy
import re
from typing import Any, Callable, TypedDict
from . import util

RE_EMOJI = r'(:[+\-\w]+:)'
SUPPORTED_INDEXES = ('emojione', 'gemoji', 'twemoji')
UNICODE_VARIATION_SELECTOR_16 = 'fe0f'
EMOJIONE_SVG_CDN = 'https://cdnjs.cloudflare.com/ajax/libs/emojione/2.2.7/assets/svg/'
EMOJIONE_PNG_CDN = 'https://cdnjs.cloudflare.com/ajax/libs/emojione/2.2.7/assets/png/'
TWEMOJI_SVG_CDN = 'https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/svg/'
TWEMOJI_PNG_CDN = 'https://cdn.jsdelivr.net/gh/jdecked/twemoji@16.0.1/assets/72x72/'
GITHUB_UNICODE_CDN = 'https://github.githubassets.com/images/icons/emoji/unicode/'
GITHUB_CDN = 'https://github.githubassets.com/images/icons/emoji/'
NO_TITLE = 'none'
LONG_TITLE = 'long'
SHORT_TITLE = 'short'
VALID_TITLE = (LONG_TITLE, SHORT_TITLE, NO_TITLE)
UNICODE_ENTITY = 'html_entity'
UNICODE_ALT = ('unicode', UNICODE_ENTITY)
LEGACY_ARG_COUNT = 8

MSG_INDEX_WARN = """Using emoji indexes with no arguments is now deprecated.
Emoji indexes now take 2 arguments: 'options' and 'md'.
Please update your custom index accordingly.
"""

MSG_BAD_EMOJI = """
Emoji Extension (strict mode): The following emoji were detected and either had
their name change, were removed, or have never existed.

{}
"""


class EmojiIndex(TypedDict):
    """Structure returned by an emoji index function."""

    name: str
    emoji: dict[str, dict[str, Any]]
    aliases: dict[str, str]


EmojiGenerator = Callable[
    [str, str, str | None, str | None, str, str | None, str | None, dict[str, Any], Markdown],
    etree.Element | str
]


def add_attributes(options: dict[str, Any], attributes: dict[str, str]) -> None:
    """Add additional attributes from options."""

    attr = options.get('attributes', {})
    if attr:
        attributes.update(attr)


# Exists for backwards compatibility as this function
# was initially spelled incorrectly.
add_attriubtes = add_attributes


def emojione(options: dict[str, Any], md: Markdown) -> EmojiIndex:
    """The EmojiOne index."""

    from . import emoji1_db as emoji_map
    return {
        "name": emoji_map.name,
        "emoji": copy.deepcopy(emoji_map.emoji),
        "aliases": copy.deepcopy(emoji_map.aliases)
    }


def gemoji(options: dict[str, Any], md: Markdown) -> EmojiIndex:
    """The Gemoji index."""

    from . import gemoji_db as emoji_map
    return {
        "name": emoji_map.name,
        "emoji": copy.deepcopy(emoji_map.emoji),
        "aliases": copy.deepcopy(emoji_map.aliases)
    }


def twemoji(options: dict[str, Any], md: Markdown) -> EmojiIndex:
    """The Twemoji index."""

    from . import twemoji_db as emoji_map
    return {
        "name": emoji_map.name,
        "emoji": copy.deepcopy(emoji_map.emoji),
        "aliases": copy.deepcopy(emoji_map.aliases)
    }


###################
# Converters
###################
def to_png(
    index: str,
    shortname: str,
    alias: str | None,
    uc: str | None,
    alt: str,
    title: str | None,
    category: str | None,
    options: dict[str, Any],
    md: Markdown
) -> etree.Element:
    """Return PNG element."""

    if index == 'gemoji':
        def_image_path = GITHUB_UNICODE_CDN
        def_non_std_image_path = GITHUB_CDN
    elif index == 'twemoji':
        def_image_path = TWEMOJI_PNG_CDN
        def_non_std_image_path = TWEMOJI_PNG_CDN
    else:
        def_image_path = EMOJIONE_PNG_CDN
        def_non_std_image_path = EMOJIONE_PNG_CDN

    is_unicode = uc is not None
    classes = options.get('classes', index)

    # In general we can use the alias, but github specific images don't have one for each alias.
    # We can tell we have a github specific if there is no Unicode value.
    if is_unicode:
        image_path = options.get('image_path', def_image_path)
    else:  # pragma: no cover
        image_path = options.get('non_standard_image_path', def_non_std_image_path)

    src = "{}{}.png".format(
        image_path,
        uc if is_unicode else shortname[1:-1]
    )

    attributes: dict[str, str] = {
        "class": classes,
        "alt": alt,
        "src": src
    }

    if title:
        attributes['title'] = title

    add_attributes(options, attributes)

    return etree.Element("img", attributes)


def to_svg(
    index: str,
    shortname: str,
    alias: str | None,
    uc: str | None,
    alt: str,
    title: str | None,
    category: str | None,
    options: dict[str, Any],
    md: Markdown
) -> etree.Element:
    """Return SVG element."""

    if index == 'twemoji':
        svg_path = TWEMOJI_SVG_CDN
    else:
        svg_path = EMOJIONE_SVG_CDN

    attributes: dict[str, str] = {
        "class": options.get('classes', index),
        "alt": alt,
        "src": "{}{}.svg".format(
            options.get('image_path', svg_path),
            uc
        )
    }

    if title:
        attributes['title'] = title

    add_attributes(options, attributes)

    return etree.Element("img", attributes)


def to_png_sprite(
    index: str,
    shortname: str,
    alias: str | None,
    uc: str | None,
    alt: str,
    title: str | None,
    category: str | None,
    options: dict[str, Any],
    md: Markdown
) -> etree.Element:
    """Return PNG sprite element."""

    attributes: dict[str, str] = {
        "class": '%(class)s-%(size)s-%(category)s _%(unicode)s' % {
            "class": options.get('classes', index),
            "size": options.get('size', '64'),
            "category": (category if category else ''),
            "unicode": uc
        }
    }

    if title:
        attributes['title'] = title

    add_attributes(options, attributes)

    el = etree.Element("span", attributes)
    el.text = md_util.AtomicString(alt)

    return el


def to_svg_sprite(
    index: str,
    shortname: str,
    alias: str | None,
    uc: str | None,
    alt: str,
    title: str | None,
    category: str | None,
    options: dict[str, Any],
    md: Markdown
) -> etree.Element:
    """
    Return SVG sprite element.

    ```
    <svg class="%(classes)s"><description>%(alt)s</description>
    <use xlink:href="%(sprite)s#emoji-%(unicode)s"></use></svg>
    ```
    """

    xlink_href = '{}#emoji-{}'.format(
        options.get('image_path', './../assets/sprites/emojione.sprites.svg'), uc
    )
    svg = etree.Element("svg", {"class": options.get('classes', index)})
    desc = etree.SubElement(svg, 'description')
    desc.text = md_util.AtomicString(alt)
    etree.SubElement(svg, 'use', {'xlink:href': xlink_href})

    return svg


def to_alt(
    index: str,
    shortname: str,
    alias: str | None,
    uc: str | None,
    alt: str,
    title: str | None,
    category: str | None,
    options: dict[str, Any],
    md: Markdown
) -> str:
    """Return html entities."""

    return md.htmlStash.store(alt)


###################
# Classes
###################
class EmojiPattern(InlineProcessor):
    """Return element of type `tag` with a text attribute of group(2) of an `InlineProcessor`."""

    def __init__(self, pattern: str, config: dict[str, Any], strict_mode: set[str], md: Markdown) -> None:
        """Initialize."""

        InlineProcessor.__init__(self, pattern, md)

        title = config['title']
        alt = config['alt']
        self.options: dict[str, Any] = config['options']
        self._set_index(config["emoji_index"])
        self.unicode_alt = alt in UNICODE_ALT
        self.encoded_alt = alt == UNICODE_ENTITY
        self.remove_var_sel: bool = config['remove_variation_selector']
        self.title: str = title if title in VALID_TITLE else NO_TITLE
        self.generator: EmojiGenerator = config['emoji_generator']
        self.strict: bool = config['strict']
        self.strict_cache = strict_mode

    def _set_index(self, index: Callable[[dict[str, Any], Markdown], EmojiIndex]) -> None:
        """Set the index."""

        self.emoji_index: EmojiIndex = index(self.options, self.md)

    def _remove_variation_selector(self, value: str) -> str:
        """Remove variation selectors."""

        return value.replace('-' + UNICODE_VARIATION_SELECTOR_16, '')

    def _get_unicode_char(self, value: str) -> str:
        """Get the Unicode char."""

        return ''.join([util.get_char(int(c, 16)) for c in value.split('-')])

    def _get_unicode(self, emoji: dict[str, Any]) -> tuple[str | None, str | None]:
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
        """

        uc: str | None = emoji.get('unicode')
        uc_alt: str | None = emoji.get('unicode_alt', uc)
        if uc_alt and self.remove_var_sel:
            uc_alt = self._remove_variation_selector(uc_alt)

        return uc, uc_alt

    def _get_title(self, shortname: str, emoji: dict[str, Any]) -> str | None:
        """Get the title."""

        title: str | None
        if self.title == LONG_TITLE:
            title = emoji['name']
        elif self.title == SHORT_TITLE:
            title = shortname
        else:
            title = None
        return title

    def _get_alt(self, shortname: str, uc_alt: str | None) -> str:
        """Get alt form."""

        if uc_alt is None or not self.unicode_alt:
            alt = shortname
        else:
            alt = self._get_unicode_char(uc_alt)
            if self.encoded_alt:
                alt = ''.join(
                    [md_util.AMP_SUBSTITUTE + ('#x%04x;' % util.get_ord(point)) for point in util.get_code_points(alt)]
                )
        return alt

    def _get_category(self, emoji: dict[str, Any]) -> str | None:
        """Get the category."""

        category: str | None = emoji.get('category')
        return category

    def handleMatch(  # type: ignore[override]
        self, m: re.Match[str], data: str
    ) -> tuple[etree.Element | str | None, int | None, int | None]:
        """Handle emoji pattern matches."""

        text = m.group(1)
        el: etree.Element | str = text

        shortname: str = self.emoji_index['aliases'].get(text, text)
        alias = None if shortname == text else text
        emoji: dict[str, Any] | None = self.emoji_index['emoji'].get(shortname, None)
        if emoji:
            uc, uc_alt = self._get_unicode(emoji)
            title = self._get_title(text, emoji)
            alt = self._get_alt(text, uc_alt)
            category = self._get_category(emoji)
            el = self.generator(
                self.emoji_index['name'],
                shortname,
                alias,
                uc,
                alt,
                title,
                category,
                self.options,
                self.md
            )
        elif self.strict:
            self.strict_cache.add(shortname)

        return el, m.start(0), m.end(0)


class EmojiAlertPostprocessor(Postprocessor):
    """Post processor to strip out unwanted content."""

    def __init__(self, strict_cache: set[str], md: Markdown) -> None:
        """Initialize."""

        self.strict_cache = strict_cache

    def run(self, text: str) -> str:
        """Strip out ids and classes for a simplified HTML output."""

        if len(self.strict_cache):
            raise RuntimeError(
                MSG_BAD_EMOJI.format('\n'.join([f'- {x}' for x in sorted(self.strict_cache)]))
            )
        return text


class EmojiExtension(Extension):
    """Add emoji extension to Markdown class."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
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
            'strict': [
                False,
                "When enabled, if an emoji with a missing name is detected, an exception will be raised."
            ],
            'options': [
                {},
                "Emoji options see documentation for options for github and emojione."
            ]
        }
        super().__init__(*args, **kwargs)

    def reset(self) -> None:
        """Reset."""

        self.strict_cache.clear()

    def extendMarkdown(self, md: Markdown) -> None:
        """Add support for emoji."""

        md.registerExtension(self)

        config = self.getConfigs()

        util.escape_chars(md, [':'])

        self.strict_cache: set[str] = set()
        md.inlinePatterns.register(EmojiPattern(RE_EMOJI, config, self.strict_cache, md), "emoji", 75)
        if config['strict']:
            md.postprocessors.register(EmojiAlertPostprocessor(self.strict_cache, md), "emoji-alert", 50)


###################
# Make Available
###################
def makeExtension(*args: Any, **kwargs: Any) -> EmojiExtension:
    """Return extension."""

    return EmojiExtension(*args, **kwargs)
