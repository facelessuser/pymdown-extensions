"""
Emoji.

pymdownx.emoji
Emoji extension for emojione or Github's gemoji.

MIT license.

Copyright (c) 2016- Isaac Muse <isaacmuse@gmail.com>

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


def add_attriubtes(options, attributes):
    """Add aditional attributes from options."""

    attr = options.get('attributes', {})
    if attr:
        for k, v in attr.items():
            attributes[k] = v


###################
# Converters
###################
def to_png(self, shortname, alias, uc, alt, title):
    """Return png element."""

    if self.index_name == 'gemoji':
        is_unicode = uc is not None
        classes = self.options.get('classes', 'gemoji')

        # In genral we can use the alias, but github specific images don't have one for each alias.
        # We can tell we have a github specific if there is no Unicode value.
        src = "%s%s.png" % (
            self.options.get('image_path', GITHUB_UNICODE_CDN if is_unicode else GITHUB_CDN),
            uc if is_unicode else shortname[1:-1]
        )
    else:
        classes = self.options.get('classes', 'emojione')
        src = "%s%s.png" % (
            self.options.get('image_path', EMOJIONE_PNG_CDN),
            uc
        )

    attributes = {
        "class": classes,
        "alt": alt,
        "src": src
    }

    if title:
        attributes['title'] = title

    add_attriubtes(self.options, attributes)

    return util.etree.Element("img", attributes)


def to_svg(self, shortname, alias, uc, alt, title):
    """Return svg element."""

    attributes = {
        "class": self.options.get('classes', 'emojione'),
        "alt": alt,
        "src": "%s%s.svg" % (
            self.options.get('image_path', EMOJIONE_SVG_CDN),
            uc
        )
    }

    if title:
        attributes['title'] = title

    add_attriubtes(self.options, attributes)

    return util.etree.Element("img", attributes)


def to_png_sprite(self, shortname, alias, uc, alt, title):
    """Return png sprite element."""

    attributes = {
        "class": '%(class)s-%(unicode)s' % {
            "class": self.options.get('classes', 'emojione emojione'),
            "unicode": uc
        }
    }

    if title:
        attributes['title'] = title

    add_attriubtes(self.options, attributes)

    el = util.etree.Element("span", attributes)
    el.text = alt

    return el


def to_svg_sprite(self, shortname, alias, uc, alt, title):
    """Return svg sprite element."""

    html = EMOJIONE_SVG_SPRITE_TAG % {
        "classes": self.options.get('classes', 'emojione'),
        "alt": alt,
        "sprite": self.options.get('image_path', './../assets/sprites/emojione.sprites.svg'),
        "unicode": uc
    }

    return self.markdown.htmlStash.store(html, safe=True)


def to_awesome(self, shortname, alias, uc, alt, title):
    """
    Return "awesome style element for "font-awesome" format.

    See: https://github.com/Ranks/emojione/tree/master/lib/emojione-awesome.
    """

    classes = '%s-%s' % (self.options.get('classes', 'e1a'), shortname[1:-1])
    attributes = {"class": classes}
    add_attriubtes(self.options, attributes)
    return util.etree.Element("i", attributes)


def to_html_entities(self, shortname, alias, uc, alt, title):
    """Return html entities."""

    return self.markdown.htmlStash.store(alt, safe=True)


###################
# Classes
###################
class EmojiPattern(Pattern):
    """Return element of type `tag` with a text attribute of group(3) of a Pattern."""

    def __init__(self, pattern, index, generator, remove_var_sel, unicode_alt, title, options, md):
        """Initialize."""

        if index == 'gemoji':
            import pymdownx.gemoji_db
            self.emoji_index = pymdownx.gemoji_db
        elif index == 'emojione':
            import pymdownx.emoji1_db
            self.emoji_index = pymdownx.emoji1_db
        self.index_name = index
        self.markdown = md
        self.unicode_alt = unicode_alt
        self.remove_var_sel = remove_var_sel
        self.title = title
        self.generator = generator
        self.options = options
        Pattern.__init__(self, pattern)

    def _remove_variation_selector(self, value):
        """Remove variation selectors."""

        return value.replace('-' + UNICODE_VARIATION_SELECTOR_16, '')

    def _get_entity(self, value):
        """Get the HTML entity."""

        return ''.join(["%s#x%s;" % (util.AMP_SUBSTITUTE, c) for c in value.split('-')])

    def _get_unicode(self, emoji):
        """
        Get Unicode and Unicode alt.

        Unicode: This is the stripped down form of the Unicode, no joining chars and no variation chars.
            Unicode is not always valid.  If there is no alternative form, Unicode can be counted on as
            valid.  For the most part, this should be used to reference files, or create classes, but
            for inserting actual Unicode, you should use alt.

        Unicode Alt: When not blank, this will always be valid.  This is what you would use to insert an
            actual Unicode char. This contains not just the needed characters, but the formatting as well.
            Joining characters and variation characters will be present. If you don't want variation chars,
            enable the global 'remove_variation_selector' option.

        If using gemoji, it is possible you will get no Unicode and no Unicode alt.  This occurs with emoji
        like :octocat:.  It's not a real emoji.  But it is provided by gememoji anyways.
        """

        uc = emoji['unicode'] if emoji['unicode'] != '' else None

        if emoji['unicode_alt'] != '':
            if self.remove_var_sel:
                uc_alt = self._remove_variation_selector(emoji["unicode_alt"])
            else:
                uc_alt = emoji["unicode_alt"]
        else:
            uc_alt = uc
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

        if self.index_name == 'gemoji' and uc_alt is None:
            alt = shortname
        else:
            alt = self._get_entity(uc_alt)
        return alt

    def handleMatch(self, m):
        """Hanlde emoji pattern matches."""

        el = m.group(2)
        shortname = self.emoji_index.aliases.get(el, None)
        if shortname is None:
            shortname = el
            alias = None
        else:
            alias = el

        emoji = self.emoji_index.emoji.get(shortname, None)
        if emoji:
            uc, uc_alt = self._get_unicode(emoji)
            title = self._get_title(el, emoji)
            alt = self._get_alt(el, uc_alt)
            el = self.generator(self, shortname, alias, uc, alt, title)

        return el


class EmojiExtension(Extension):
    """Add emoji extension to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'emoji_index': [
                "emojione",
                "Emoji to use (emojione or gemoji). - Default: 'emojione'"
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
            'unicode_alt': [
                True,
                "Insert Unicode as the alt form (done as HTML entities currently). - Default: True"
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
        unicode_alt = self.getConfigs()['unicode_alt']
        options = self.getConfigs()['options']
        remove_var_sel = self.getConfigs()['remove_variation_selector']

        md.inlinePatterns.add(
            "emoji",
            EmojiPattern(RE_EMOJI, emoji_index, generator, remove_var_sel, unicode_alt, title, options, md),
            "<not_strong"
        )


###################
# Make Available
###################
def makeExtension(*args, **kwargs):
    """Return extension."""

    return EmojiExtension(*args, **kwargs)
